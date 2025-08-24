from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EnhancedNCOSearch:
    def __init__(self, embeddings_file="data/processed/occupation_embeddings.pkl"):
        self.model = SentenceTransformer('all-mpnet-base-v2')
        
        with open(embeddings_file, "rb") as f:
            data = pickle.load(f)
            self.occupations = data["occupations"]
            self.embeddings = data["embeddings"]
        
        # Synonym dictionary for query expansion
        self.synonyms = {
            "software engineer": ["programmer", "developer", "software developer", "coder", "software architect"],
            "nurse": ["nursing", "healthcare worker", "medical nurse", "registered nurse", "healthcare professional"],
            "teacher": ["educator", "instructor", "professor", "academic", "tutor", "lecturer"],
            "accountant": ["accounting", "bookkeeper", "financial analyst", "auditor", "tax professional"],
            "chef": ["cook", "culinary professional", "kitchen staff", "food preparation"],
            "electrician": ["electrical technician", "electrical worker", "electrical installer"],
            "mechanic": ["automotive technician", "repair technician", "maintenance worker"],
            "doctor": ["physician", "medical doctor", "healthcare provider", "medical professional"],
            "lawyer": ["attorney", "legal professional", "advocate", "counsel"],
            "manager": ["supervisor", "administrator", "executive", "team leader"]
        }
    
    def expand_query(self, query):
        """Expand query with synonyms"""
        expanded_queries = [query]
        
        query_lower = query.lower()
        for key, synonyms in self.synonyms.items():
            if key in query_lower:
                expanded_queries.extend(synonyms)
                break
        
        # Also add individual words for broader matching
        words = query.lower().split()
        if len(words) > 1:
            expanded_queries.extend(words)
        
        return expanded_queries
    
    def search(self, query, top_k=5):
        """Enhanced search with query expansion"""
        print(f"Searching for: '{query}'")
        
        # Expand the query
        expanded_queries = self.expand_query(query)
        print(f"Expanded to: {expanded_queries}")
        
        # Get embeddings for all expanded queries
        query_embeddings = self.model.encode(expanded_queries)
        
        # Calculate similarities for each expanded query
        all_similarities = []
        for qemb in query_embeddings:
            similarities = cosine_similarity([qemb], self.embeddings)[0]
            all_similarities.append(similarities)
        
        # Take the MAXIMUM similarity across all expanded queries
        max_similarities = np.maximum.reduce(all_similarities)
        
        # Boost scores by 1.2x (20% boost) for multi-query matching
        max_similarities = np.minimum(max_similarities * 1.2, 1.0)
        
        # Get top k results
        top_indices = np.argsort(max_similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            occupation = self.occupations[idx]
            display_text = occupation[:150] + "..." if len(occupation) > 150 else occupation
            
            results.append({
                'occupation': display_text,
                'full_occupation': occupation,
                'confidence': float(max_similarities[idx]),
                'confidence_percent': float(round(max_similarities[idx] * 100, 2))
            })
        
        return results

# Test the enhanced search
def test_enhanced_search():
    search_engine = EnhancedNCOSearch()
    
    test_queries = [
        "software engineer",
        "nurse", 
        "teacher",
        "chef",
        "electrician"
    ]
    
    print("TESTING ENHANCED SEARCH")
    print("="*50)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 30)
        results = search_engine.search(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            confidence = result['confidence_percent']
            occupation = result['occupation']
            print(f"{i}. {confidence}% - {occupation}")

if __name__ == "__main__":
    test_enhanced_search()
