from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# UPDATED: Import the new occupation search engine
from src.models.enhanced_search import EnhancedNCOSearch

app = Flask(__name__)
CORS(app)

# UPDATED: Initialize the new occupation search engine
print("Initializing NCO Occupation Search Engine...")
search_engine = EnhancedNCOSearch()
print("Search engine ready!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        print(f"Received search query: {query}")
        
        # Perform search
        results = search_engine.search(query, top_k=5)
        
        # UPDATED: Format results for individual occupations
        formatted_results = []
        for result in results:
            formatted_results.append({
                'name': result['occupation'],  # Show the occupation description
                'confidence': float(result['confidence_percent']),
                'full_description': result['full_occupation']
            })
        
        print(f"Returning {len(formatted_results)} results")
        
        return jsonify({
            'query': query,
            'results': formatted_results
        })
    
    except Exception as e:
        print(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
