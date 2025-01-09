# Use a slim Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Install the `gsom` module
RUN pip install .

# Expose the Flask app's port
EXPOSE 8080

# Set the default command to run the server
CMD ["python", "gsom/serve.py"]
