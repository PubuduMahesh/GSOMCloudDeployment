import os
import numpy as np
import pandas as pd
import boto3
import sys
import json
from gsom import GSOM

def upload_to_s3(local_file_path, bucket_name, s3_key):
    s3_client = boto3.client('s3')
    try:
        print(f"Uploading {local_file_path} to s3://{bucket_name}/{s3_key}")
        s3_client.upload_file(local_file_path, bucket_name, s3_key)
        print(f"File successfully uploaded to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise

if __name__ == "__main__":
    np.random.seed(1)

    if len(sys.argv) < 2:
        raise ValueError("Missing path to JSON input")

    with open(sys.argv[1], "r") as f:
        payload = json.load(f)

    input_bucket = payload["input_bucket"]
    input_key = payload["input_key"]
    output_bucket = payload["output_bucket"]
    gsom_params = payload["gsom_params"]

    file_name = input_key.split("/")[-1]
    local_path = f"/tmp/{file_name}"
    output_dir = "/tmp"
    output_csv = os.path.join(output_dir, "gsom.csv")
    output_plot = os.path.join(output_dir, "gsom_plot.pdf")

    os.makedirs(output_dir, exist_ok=True)

    print(f"Downloading s3://{input_bucket}/{input_key} to {local_path}")
    boto3.client("s3").download_file(input_bucket, input_key, local_path)

    df = pd.read_csv(local_path)
    training_data = df.iloc[:, 1:gsom_params["dimensions"] + 1]

    gsom = GSOM(**gsom_params)
    gsom.fit(training_data.to_numpy(), training_iterations=100, smooth_iterations=50)

    df = df.drop(columns=["label"]) if "label" in df.columns else df
    map_points = gsom.predict(df, "Name")

    print(f"Saving plot to {output_plot}")
    gsom.plot(map_points, "Name", output_dir=output_dir)

    print(f"Saving CSV to {output_csv}")
    map_points.to_csv(output_csv, index=False)

    upload_to_s3(output_plot, output_bucket, "output/gsom_plot.pdf")
    upload_to_s3(output_csv, output_bucket, "output/gsom.csv")

    print("✅ GSOM execution completed and results uploaded.")
