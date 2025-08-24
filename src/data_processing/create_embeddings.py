from sentence_transformers import SentenceTransformer
from pathlib import Path
import pickle

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small, fast, very good

def read_documents(folder):
    docs = []
    files = sorted(Path(folder).glob("*_tokens.txt"))
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(text)
    return docs, files

def create_and_save_embeddings():
    docs, files = read_documents("data/processed")
    print(f"Encoding {len(docs)} documents...")
    embeddings = model.encode(docs, show_progress_bar=True, batch_size=16)
    # Save embeddings and file order
    with open("data/processed/nco_embeddings.pkl", "wb") as f:
        pickle.dump({"files": [str(f) for f in files], "embeddings": embeddings}, f)
    print("Saved nco_embeddings.pkl with all semantic vectors!")

if __name__ == "__main__":
    create_and_save_embeddings()
