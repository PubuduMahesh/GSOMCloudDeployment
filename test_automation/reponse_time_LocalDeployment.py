import requests
import time

# Define the endpoint and datasets
endpoint = "http://localhost:8080/invocations"
data_files = [f'test_data_{size}MB.txt' for size in [1, 5, 10, 15, 20]]

response_times = {}

for data_file in data_files:
    # Read dataset content
    with open(data_file, 'r') as f:
        payload = f.read()

    # Send request and measure response time
    start_time = time.time()
    response = requests.post(endpoint, data=payload, headers={"Content-Type": "text/plain"})
    end_time = time.time()

    elapsed_time = end_time - start_time
    response_times[data_file] = elapsed_time
    print(f"Response Time for {data_file}: {elapsed_time:.2f} seconds")

# Print all response times
print("Response Times:", response_times)
