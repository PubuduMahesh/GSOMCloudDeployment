from flask import Flask, request, jsonify
import os
import subprocess
import json

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def health_check():
    return '', 200

@app.route('/invocations', methods=['POST'])
def predict():
    try:
        data = request.json
        print(f"Received data: {json.dumps(data, indent=2)}")

        # Write JSON input to a temp file
        input_path = "/tmp/payload.json"
        with open(input_path, "w") as f:
            json.dump(data, f)

        # Execute the script with path to JSON as argument
        result = subprocess.run(
            ["python", "example/zoo_gsom.py", input_path],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"zoo_gsom.py executed successfully:\n{result.stdout}")
            return jsonify({"result": "Prediction successful", "log": result.stdout})
        else:
            print(f"zoo_gsom.py execution failed:\n{result.stderr}")
            return jsonify({"error": "Prediction failed", "log": result.stderr}), 500

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
