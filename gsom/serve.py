import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def health_check():
    # Health check required by SageMaker
    return '', 200

@app.route('/invocations', methods=['POST'])
def predict():
    # Example prediction logic
    data = request.json
    print(f"Received data: {data}")
    return jsonify({"result": "Prediction successful"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # SageMaker expects the container to listen on port 8080
    app.run(host='0.0.0.0', port=port)
