import boto3

# AWS S3 Configuration
BUCKET_NAME = "gsom-output-bucket"  # Replace with your S3 bucket name
S3_KEY = "output/gsom_plot.pdf"     # Replace with the key of the file in the bucket
LOCAL_FILE_PATH = "./gsom_plot.pdf" # Path where the file will be saved locally

def download_file_from_s3(bucket_name, s3_key, local_file_path):
    """
    Download a file from S3 to the local machine.
    """
    s3 = boto3.client('s3')
    try:
        print(f"Downloading s3://{bucket_name}/{s3_key} to {local_file_path}...")
        s3.download_file(bucket_name, s3_key, local_file_path)
        print(f"File successfully downloaded to {local_file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

if __name__ == "__main__":
    download_file_from_s3(BUCKET_NAME, S3_KEY, LOCAL_FILE_PATH)
