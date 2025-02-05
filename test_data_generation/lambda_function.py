import random
import io
import boto3

def generate_test_data(file_size_mb, bucket_name, file_key):
    """
    Generate a test data file of a given size and upload it directly to S3.

    Args:
        file_size_mb (int): Target file size in megabytes.
        bucket_name (str): S3 bucket name.
        file_key (str): S3 object key (file name).
    """
    target_size = file_size_mb * 1024 * 1024  # Convert MB to bytes
    buffer = io.StringIO()  # In-memory buffer

    # Write headers
    buffer.write('Name,' + ','.join([f'w{i}' for i in range(1, 16)]) + ',label\n')

    current_size = len(buffer.getvalue().encode('utf-8'))  # Current buffer size
    while current_size < target_size:
        # Append rows dynamically
        batch_size = 1000  # Adjust batch size for performance
        data = []
        for _ in range(batch_size):
            name = random.choice(['aardvark', 'antelope', 'bass', 'bear', 'boar', 'buffalo'])
            weights = [random.randint(0, 4) for _ in range(15)]
            label = random.randint(0, 1)
            row = f"{name}," + ','.join(map(str, weights)) + f",{label}\n"
            data.append(row)

        # Write to the buffer
        buffer.writelines(data)

        # Update current size
        current_size = len(buffer.getvalue().encode('utf-8'))

    # Upload buffer content directly to S3
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=buffer.getvalue())
    print(f"File uploaded to s3://{bucket_name}/{file_key} with size {file_size_mb} MB")

def lambda_handler(event, context):
    """
    Lambda handler function to generate and upload test data file to S3.

    Args:
        event (dict): Event data (not used in this function).
        context (object): Lambda context (not used in this function).
    """
    bucket_name = "gsom-input-bucket"  # Replace with your S3 bucket name
    file_key = "zoo.txt"      # Replace with your desired file name in S3
    file_size_mb = 20                   # File size in MB

    generate_test_data(file_size_mb, bucket_name, file_key)
    return {
        "statusCode": 200,
        "body": f"File uploaded to s3://{bucket_name}/{file_key}"
    }
