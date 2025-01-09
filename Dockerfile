FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for SageMaker
EXPOSE 8080

# Add a default entrypoint for SageMaker "serve" command
ENTRYPOINT ["python", "gsom/serve.py"]
