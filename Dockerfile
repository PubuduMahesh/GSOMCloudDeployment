# Base image for Python
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH so Python can locate the 'gsom' module
ENV PYTHONPATH=/app

# Copy the rest of the application code into the container
COPY . .

# Set the default command to run the script
CMD ["python", "example/zoo_gsom.py"]
