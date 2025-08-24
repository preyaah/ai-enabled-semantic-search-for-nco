from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class NCOOccupationSearch:
    def __init__(self, embeddings_file="data/processed/occupation_embeddings.pkl"):
        # Load pre-trained model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load saved occupation embeddings
        print("Loading NCO occupation embeddings...")
        with open(embeddings_file, "rb") as f:
            data = pickle.load(f)
            self.occupations = data["occupations"]
            self.embeddings = data["embeddings"]
        print(f"Loaded {len(self.occupations)} individual occupations")
    
    def search(self, query, top_k=5):
        """
        Search for most similar NCO occupations to the query
        
        Args:
            query (str): User's job description/title
            top_k (int): Number of top matches to return
            
        Returns:
            list: Top matches with occupation descriptions and similarity scores
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
            occupation = self.occupations[idx]
            # Truncate long descriptions for display
            display_text = occupation[:150] + "..." if len(occupation) > 150 else occupation
            
            results.append({
                'occupation': display_text,
                'full_occupation': occupation,
                'confidence': float(similarities[idx]),
                'confidence_percent': float(round(similarities[idx] * 100, 2))
            })
        
        return results

# Test function
def test_occupation_search():
    # Initialize search engine
    search_engine = NCOOccupationSearch()
    
    # Test queries
    test_queries = [
        "software engineer",
        "computer programmer", 
        "school teacher",
        "nurse",
        "accountant",
        "sewing machine operator",
        "chef",
        "electrician"
    ]
    
    print("\n" + "="*60)
    print("TESTING INDIVIDUAL OCCUPATION SEARCH")
    print("="*60)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 40)
        results = search_engine.search(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            confidence = result['confidence_percent']
            occupation = result['occupation']
            print(f"{i}. {occupation}")
            print(f"   Confidence: {confidence}%")
            print()

if __name__ == "__main__":
    test_occupation_search()
