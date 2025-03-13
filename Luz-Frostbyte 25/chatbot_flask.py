from flask import Flask, request, jsonify, render_template
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

# Load the dataset
science_gateways = [
    {"name": "Custos Admin Gateway", "abstract": "Custos provides security services...",
     "site_url": "https://portal.usecustos.org/"},
    {"name": "EDGE-Bioinformatics-Gateway", "abstract": "The EDGE Bioinformatics Science Gateway...",
     "site_url": "https://edgebioinformatics.org/"},
    {"name": "CyberWater", "abstract": "To tackle fundamental scientific questions...",
     "site_url": "https://cyberwater.scigap.org/"},
    {"name": "Biolearns", "abstract": "A python-based co-expression network analysis web tool.",
     "site_url": "https://biolearns.medicine.iu.edu/"},
    {"name": "Future Water Indiana", "abstract": "Building a computer-based watershed model...",
     "site_url": "https://gateway.futurewater.indiana.edu/"}
    {"name": "Plant Biosecurity", "category": "09 May 2024|Science Gateways",
     "site": "https://sciencegateways.org/resources/9842",
     "abstract": "Plant Biosecurity is a set of measures designed to protect a crop, crops or a sub-group of crops from emergency plant pests at national, regional and individual farm levels.",
     "published_on": "N/A", "site_url": "http://www.pbcrc.com.au/",
     "cite": "(2024), \"Plant Biosecurity,\" https://sciencegateways.org/resources/plantbiosecurity.",
     "tags": ["biosecurity", "leaflet", "plant"]},
    {"name": "Crowdmap", "category": "09 May 2024|Science Gateways",
     "site": "https://sciencegateways.org/resources/9843",
     "abstract": "Crowdmap is a tool that allows you to crowdsource information and see it on a map and timeline.",
     "published_on": "N/A", "site_url": "https://crowdmap.com/welcome",
     "cite": "(204), \"Crowdmap,\" https://sciencegateways.org/resources/crowdmap.",
     "tags": ["crowdmap", "crowdsource", "open source"]},
    # (Add all the newly added datasets here...)2
]

# Prepare text corpus for similarity matching
corpus = [f"{g['name']} {g['abstract']}" for g in science_gateways]
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(corpus)


def find_best_match(user_query, top_n=3):




:wq
"""Finds the most relevant science gateway based on user query."""
    query_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    return [science_gateways[i] for i in top_indices if similarities[i] > 0.1]

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get("message", "")
    results = find_best_match(user_input)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
