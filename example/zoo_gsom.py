import os
import numpy as np
import pandas as pd
import boto3
from gsom import GSOM  # Ensure the correct import

# AWS S3 Configuration
INPUT_BUCKET_NAME = "gsom-input-bucket"
OUTPUT_BUCKET_NAME = "gsom-output-bucket"
FILE_KEY = "zoo.txt"

# Define paths
LOCAL_FILE_PATH = os.path.join(os.getcwd(), "tmp", "zoo.txt")  # Local temp path
OUTPUT_DIR = os.path.join(os.getcwd(), "output")              # Output directory
PLOT_FILE_PATH = os.path.join(OUTPUT_DIR, "gsom_plot.pdf")     # Path to the PDF plot
CSV_FILE_PATH = os.path.join(OUTPUT_DIR, "gsom.csv")           # Path to the CSV output

# Ensure directories exist
os.makedirs(os.path.dirname(LOCAL_FILE_PATH), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Local file path for zoo.txt: {LOCAL_FILE_PATH}")
print(f"Output directory: {OUTPUT_DIR}")

def download_from_s3():
    """
    Download the zoo.txt file from the S3 bucket to a local path.
    """
    s3 = boto3.client("s3")
    try:
        print(f"Attempting to download from bucket: {INPUT_BUCKET_NAME}, file key: {FILE_KEY}")
        s3.download_file(INPUT_BUCKET_NAME, FILE_KEY, LOCAL_FILE_PATH)
        print(f"Downloaded {FILE_KEY} from S3 to {LOCAL_FILE_PATH}")
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        raise

def upload_to_s3(local_file_path, bucket_name, s3_key):
    """
    Uploads a file to S3.
    """
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

    # Step 1: Download the file from S3
    download_from_s3()

    # Step 2: Read the dataset
    try:
        df = pd.read_csv(LOCAL_FILE_PATH)
        print(f"Dataset loaded successfully. Shape: {df.shape}")
    except Exception as e:
        print(f"Error reading dataset: {e}")
        raise

    # Step 3: Train the GSOM map
    try:
        data_training = df.iloc[:, 1:17]
        gsom_map = GSOM(.83, 16, max_radius=4)
        gsom_map.fit(data_training.to_numpy(), 100, 50)
        print("GSOM map training completed successfully.")
    except Exception as e:
        print(f"Error during GSOM training: {e}")
        raise

    # Step 4: Process the data and make predictions
    try:
        df = df.drop(columns=["label"])
        map_points = gsom_map.predict(df, "Name")
        print("Predictions completed successfully.")
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise

    # Step 5: Save outputs to the output directory
    try:
        # Save the GSOM plot
        print(f"Attempting to save GSOM plot to: {PLOT_FILE_PATH}")
        gsom_map.plot(map_points, "Name", output_dir=OUTPUT_DIR)  # Fixed call
        if os.path.exists(PLOT_FILE_PATH):
            print(f"GSOM plot successfully saved to: {PLOT_FILE_PATH}")
        else:
            print(f"Error: GSOM plot not found at: {PLOT_FILE_PATH}")

        # Save the GSOM results as a CSV file
        map_points.to_csv(CSV_FILE_PATH, index=False)
        print(f"CSV file saved to: {CSV_FILE_PATH}")

        # Upload outputs to S3
        if os.path.exists(PLOT_FILE_PATH):
            upload_to_s3(PLOT_FILE_PATH, OUTPUT_BUCKET_NAME, "output/gsom_plot.pdf")
        if os.path.exists(CSV_FILE_PATH):
            upload_to_s3(CSV_FILE_PATH, OUTPUT_BUCKET_NAME, "output/gsom.csv")

    except Exception as e:
        print(f"Error saving outputs: {e}")
        raise

    print("Complete")
