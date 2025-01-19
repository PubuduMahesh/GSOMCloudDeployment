import boto3
import json

# Initialize SageMaker runtime client
sm_runtime = boto3.client("sagemaker-runtime", region_name="eu-north-1")

# Invoke the endpoint
response = sm_runtime.invoke_endpoint(
    EndpointName="gsom-cloud-endpoint",
    Body=json.dumps({"key": "value"}),  # Replace with your input
    ContentType="application/json"
)

# Parse the response
result = json.loads(response["Body"].read().decode("utf-8"))
print("Response from endpoint:", result)
