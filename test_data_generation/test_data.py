import random
import os

def generate_test_data(file_size_mb, output_file):
    """
    Generate a test data file of a given size.

    Args:
        file_size_mb (int): Target file size in megabytes.
        output_file (str): Output file name (without extension).
    """
    # File size target in bytes
    target_size = file_size_mb * 1024 * 1024
    temp_file = f'{output_file}.txt'

    with open(temp_file, 'w') as f:
        # Write headers
        f.write('Name,' + ','.join([f'w{i}' for i in range(1, 16)]) + ',label\n')

    current_size = os.path.getsize(temp_file)
    while current_size < target_size:
        # Append rows dynamically
        batch_size = 1000  # Adjust batch size for performance
        data = []
        for _ in range(batch_size):
            name = random.choice(['aardvark', 'antelope', 'bass', 'bear', 'boar', 'buffalo'])
            weights = [random.randint(0, 4) for _ in range(15)]
            label = random.randint(0, 1)
            # Format row with commas
            row = f"{name}," + ','.join(map(str, weights)) + f",{label}\n"
            data.append(row)

        # Append to file
        with open(temp_file, 'a') as f:
            f.writelines(data)

        # Check current file size
        current_size = os.path.getsize(temp_file)

    print(f"File generated: {temp_file} with approximate size {file_size_mb} MB")

# List of dataset sizes to generate
data_file_sizes = [20]

# Generate datasets for each size
for size in data_file_sizes:
    generate_test_data(size, f'test_data_{size}MB')
