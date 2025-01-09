import boto3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# S3 Configuration
s3_client = boto3.client('s3')
S3_BUCKET = "gsom-output-bucket"

@app.route('/ping', methods=['GET'])
def health_check():
    return '', 200

@app.route('/invocations', methods=['POST'])
def predict():
    # Your model logic here
    data = request.json
    # Assuming output.pdf is generated in /tmp/output.pdf
    output_file_path = "/tmp/output.pdf"

    # Upload to S3
    s3_key = "output/output.pdf"
    s3_client.upload_file(output_file_path, S3_BUCKET, s3_key)

    return jsonify({"result": "Prediction successful", "s3_path": f"s3://{S3_BUCKET}/{s3_key}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
