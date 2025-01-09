from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def health_check():
    # Health check endpoint for SageMaker
    return '', 200

@app.route('/invocations', methods=['POST'])
def predict():
    # Trigger the zoo_gsom.py script
    try:
        # Example prediction logic
        data = request.json
        print(f"Received data: {data}")

        # Execute the zoo_gsom.py script
        result = subprocess.run(
            ["python", "example/zoo_gsom.py"],  # Adjust the path to zoo_gsom.py if needed
            capture_output=True,
            text=True
        )

        # Log the output and errors from the script execution
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
