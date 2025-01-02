import os
import numpy as np
import pandas as pd
import boto3
import gsom

# AWS S3 Configuration
BUCKET_NAME = "gsom-input-bucket"  # Replace with your bucket name
FILE_KEY = "zoo.txt"               # Path to the file in the bucket
LOCAL_FILE_PATH = "/tmp/zoo.txt"   # Temporary local path for downloaded file

# Define the output directory
OUTPUT_DIR = "/app/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_from_s3():
    """
    Download the zoo.txt file from the S3 bucket to a local path.
    """
    s3 = boto3.client("s3")
    try:
        print(f"Attempting to download from bucket: {BUCKET_NAME}, file key: {FILE_KEY}")
        s3.download_file(BUCKET_NAME, FILE_KEY, LOCAL_FILE_PATH)
        print(f"Downloaded {FILE_KEY} from S3 to {LOCAL_FILE_PATH}")
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        raise

if __name__ == "__main__":
    np.random.seed(1)

    # Step 1: Download the file from S3
    download_from_s3()

    # Step 2: Read the dataset
    df = pd.read_csv(LOCAL_FILE_PATH)
    print(df.shape)
    data_training = df.iloc[:, 1:17]

    # Step 3: Train the GSOM map
    gsom_map = gsom.GSOM(.83, 16, max_radius=4)
    gsom_map.fit(data_training.to_numpy(), 100, 50)

    # Step 4: Process the data and make predictions
    df = df.drop(columns=["label"])
    map_points = gsom_map.predict(df, "Name")

    # Step 5: Save outputs to the output directory
    # Save the GSOM plot
    gsom_map.plot(map_points, "Name", gsom_map=gsom_map, output_dir=OUTPUT_DIR)

    # Save the GSOM results as a CSV file
    csv_output_path = os.path.join(OUTPUT_DIR, "gsom.csv")
    map_points.to_csv(csv_output_path, index=False)

    print(f"CSV file saved to {csv_output_path}")
    print(f"GSOM plot saved to {OUTPUT_DIR}")
    print("Complete")
