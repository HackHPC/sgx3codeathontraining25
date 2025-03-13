from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Set the path to your JSON file
JSON_FILE_PATH = r"C:\Users\luzva\Downloads\science_gateways_extended.json"

# Function to load dataset
def load_dataset():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"error": "Dataset file not found"}

@app.route('/science_gateways', methods=['GET'])
def get_science_gateways():
    data = load_dataset()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
