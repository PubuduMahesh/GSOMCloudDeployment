# Base image for Python
FROM python:3.9-slim

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=TRUE

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose port 8080 for SageMaker
EXPOSE 8080

# Command to run the Flask server
CMD ["python", "gsom/serve.py"]
