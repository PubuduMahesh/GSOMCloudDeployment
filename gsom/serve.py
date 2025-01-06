import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Health Check
@app.route('/ping', methods=['GET'])
def health_check():
    return '', 200

# Prediction Endpoint
@app.route('/invocations', methods=['POST'])
def predict():
    data = request.json
    # Add your model inference logic here
    return jsonify({"result": "Prediction successful"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
