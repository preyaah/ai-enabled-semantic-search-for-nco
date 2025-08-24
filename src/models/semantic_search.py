from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class NCOSemanticSearch:
    def __init__(self, embeddings_file="data/processed/nco_embeddings.pkl"):
        # Load pre-trained model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load saved embeddings
        print("Loading NCO embeddings...")
        with open(embeddings_file, "rb") as f:
            data = pickle.load(f)
            self.files = data["files"]
            self.embeddings = data["embeddings"]
        print(f"Loaded {len(self.files)} NCO documents")
    
    def search(self, query, top_k=5):
        """
        Search for most similar NCO occupations to the query
        
        Args:
            query (str): User's job description/title
            top_k (int): Number of top matches to return
            
        Returns:
            list: Top matches with filenames and similarity scores
        """
        print(f"Searching for: '{query}'")
        
        # Convert query to embedding
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]  # Descending order
        
        results = []
        for idx in top_indices:
            results.append({
                'file': self.files[idx],
                'confidence': float(similarities[idx]),
                'confidence_percent': round(similarities[idx] * 100, 2)
            })
        
        return results

# Test function
def test_search():
    # Initialize search engine
    search_engine = NCOSemanticSearch()
    
    # Test queries
    test_queries = [
        "sewing machine operator",
        "computer programmer", 
        "school teacher",
        "nurse",
        "accountant"
    ]
    
    print("\n" + "="*50)
    print("TESTING SEMANTIC SEARCH")
    print("="*50)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)
        results = search_engine.search(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            filename = result['file'].split('\\')[-1]  # Get just filename
            confidence = result['confidence_percent']
            print(f"{i}. {filename} ({confidence}% match)")

if __name__ == "__main__":
    test_search()
