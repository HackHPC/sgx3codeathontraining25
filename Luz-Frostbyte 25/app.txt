from flask import Flask, jsonify, request
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
    """Retrieve the science gateways data with optional search filters."""
    data = load_dataset()

    if isinstance(data, dict) and "error" in data:
        return jsonify(data)

    # Get query parameters from the URL
    name = request.args.get('name')
    abstract = request.args.get('abstract')
    published_on = request.args.get('published_on')
    category = request.args.get('category')
    tag = request.args.get('tag')  # Search by a single tag

    # Filter results based on query parameters
    filtered_data = []
    for item in data:
        if name and name.lower() not in item['name'].lower():
            continue
        if abstract and abstract.lower() not in item['abstract'].lower():
            continue
        if published_on and published_on.lower() not in item['published_on'].lower():
            continue
        if category and category.lower() not in item['category'].lower():
            continue
        if tag and tag.lower() not in [t.lower() for t in item.get('tags', [])]:
            continue
        filtered_data.append(item)

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
