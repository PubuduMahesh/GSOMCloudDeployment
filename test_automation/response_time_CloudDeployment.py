import boto3
import time

# Initialize SageMaker runtime client
sm_client = boto3.client('sagemaker-runtime', region_name='<region>')

# Endpoint name
endpoint_name = "<endpoint-name>"

# List of datasets in S3
data_files = [f'datasets/test_data_{size}MB.txt' for size in [1, 5, 10, 15, 20]]
bucket_name = "<S3 bucket-name>"

# Measure response times
response_times = {}

for file_key in data_files:
    # Download the dataset from S3 (if needed locally for analysis)
    local_file = file_key.split('/')[-1]
    boto3.client('s3').download_file(bucket_name, file_key, local_file)

    # Read dataset content
    with open(local_file, 'r') as f:
        payload = f.read()

    # Measure response time
    start_time = time.time()
    response = sm_client.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=payload,
        ContentType='text/plain'  # Adjust content type as per your setup
    )
    end_time = time.time()

    # Log response time
    elapsed_time = end_time - start_time
    response_times[file_key] = elapsed_time
    print(f"Response Time for {file_key}: {elapsed_time:.2f} seconds")

# Print all response times
print("Response Times:", response_times)
