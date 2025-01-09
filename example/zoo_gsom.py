import os
import numpy as np
import pandas as pd
import boto3
from gsom import GSOM  # Ensure the correct import

# AWS S3 Configuration
BUCKET_NAME = "gsom-input-bucket"
FILE_KEY = "zoo.txt"

# Define a cross-platform temporary local file path
LOCAL_FILE_PATH = os.path.join(os.getcwd(), "tmp", "zoo.txt")  # Local temp path
OUTPUT_DIR = os.path.join(os.getcwd(), "output")              # Output directory

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
        plot_path = os.path.join(OUTPUT_DIR, "gsom_plot.pdf")
        print(f"Attempting to save GSOM plot to: {plot_path}")
        gsom_map.plot(map_points, "Name", output_dir=OUTPUT_DIR)  # Fixed call
        if os.path.exists(plot_path):
            print(f"GSOM plot successfully saved to: {plot_path}")
        else:
            print(f"Error: GSOM plot not found at: {plot_path}")

        # Save the GSOM results as a CSV file
        csv_output_path = os.path.join(OUTPUT_DIR, "gsom.csv")
        map_points.to_csv(csv_output_path, index=False)
        print(f"CSV file saved to: {csv_output_path}")

    except Exception as e:
        print(f"Error saving outputs: {e}")
        raise

    print("Complete")
