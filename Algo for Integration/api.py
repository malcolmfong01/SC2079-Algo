import json
import subprocess
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

INPUT_FILE = "input.json"
OUTPUT_FILE = "output.json"

@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({"status": "running"}), 200

@app.route('/path', methods=['POST'])
def path_finding():
    """API Endpoint to update input.json, run main.py, and return only commands"""
    try:
        # Get JSON request data
        content = request.get_json()
        if not content:
            return jsonify({"error": "Invalid JSON input"}), 400

        # Step 1: Update input.json
        with open(INPUT_FILE, "w") as f:
            json.dump(content, f, indent=2)

        # Step 2: Run main.py (pathfinding)
        start_time = time.time()
        result = subprocess.run(
            ["python3", "main.py", INPUT_FILE, OUTPUT_FILE],
            capture_output=True,
            text=True
        )
        execution_time = round(time.time() - start_time, 4)

        # Step 3: Check if main.py ran successfully
        if result.returncode != 0:
            return jsonify({"error": "Failed to run pathfinding", "details": result.stderr}), 500

        # Step 4: Read and return only commands from output.json
        with open(OUTPUT_FILE, "r") as f:
            output_data = json.load(f)

        commands = output_data.get("commands", [])  # Extract only the commands list

        return jsonify(commands)  # Return only commands as a JSON array

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)