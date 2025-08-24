from sentence_transformers import SentenceTransformer
from pathlib import Path
import pickle

def create_occupation_embeddings():
    # Load model
    model = SentenceTransformer('all-mpnet-base-v2')
    
    # Read all individual occupations
    occupations_file = Path("data/interim/all_occupations.txt")
    
    if not occupations_file.exists():
        print("Error: all_occupations.txt not found. Run extract_occupations.py first.")
        return
    
    with open(occupations_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into individual occupations
    occupation_entries = content.split('\n\n')
    occupations = []
    
    for entry in occupation_entries:
        if entry.strip() and 'Occupation_' in entry:
            # Remove the "Occupation_X:" prefix
            clean_entry = entry.split(':', 1)[-1].strip()
            if len(clean_entry) > 20:
                occupations.append(clean_entry)
    
    print(f"Creating embeddings for {len(occupations)} occupations...")
    
    if occupations:
        # Create embeddings
        embeddings = model.encode(occupations, show_progress_bar=True, batch_size=16)
        
        # Save embeddings
        output_file = Path("data/processed/occupation_embeddings.pkl")
        with open(output_file, "wb") as f:
            pickle.dump({
                "occupations": occupations,
                "embeddings": embeddings
            }, f)
        
        print(f"Saved {len(occupations)} occupation embeddings to {output_file}")
    else:
        print("No occupations found to process!")

if __name__ == "__main__":
    create_occupation_embeddings()
