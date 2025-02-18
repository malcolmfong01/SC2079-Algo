from flask import Flask, request, jsonify
import json
import subprocess
from consts import Direction

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    print("Received data:", data)  # Debugging information

    input_file_path = '/Users/mal/Documents/codes/SC2079-Algo/Algo for Integration/input.json'
    output_file_path = '/Users/mal/Documents/codes/SC2079-Algo/Algo for Integration/output.json'
    
    # Update the input.json file with the received data
    save_input(data, input_file_path)
    
    # Run the command to execute the algorithm
    result = subprocess.run(['python3', 'main.py', 'input.json', 'output.json'], cwd='/Users/mal/Documents/codes/SC2079-Algo/Algo for Integration', capture_output=True, text=True)
    print("Subprocess result:", result)  # Debugging information
    
    if result.returncode != 0:
        print("Error:", result.stderr)  # Debugging information
        return jsonify({"status": "error", "message": result.stderr}), 500
    
    # Load the output.json file to include in the response
    output_data = load_input(output_file_path)
    print("Output data:", output_data)  # Debugging information
    
    return jsonify(output_data), 200

def load_input(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_input(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)