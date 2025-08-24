import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.stem.porter import PorterStemmer
from pathlib import Path

# Load spaCy English model and increase max_length limit
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2000000  # Set above your largest file size
stemmer = PorterStemmer()

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace/newlines/tabs
    text = re.sub(r'\s+', ' ', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize using spaCy
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.is_alpha and token.text not in STOP_WORDS:
            stem = stemmer.stem(token.text)
            tokens.append(stem)
    return tokens

def preprocess_nco_files():
    data_folder = Path("data/raw")
    output_folder = Path("data/processed")
    output_folder.mkdir(exist_ok=True)
    for txt_file in data_folder.glob("*_extracted.txt"):
        print(f"Processing {txt_file}")
        with open(txt_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
        tokens = []
        chunk_size = 50000  # Process text in 50,000 character chunks
        for i in range(0, len(raw_text), chunk_size):
            chunk = raw_text[i:i+chunk_size]
            tokens.extend(preprocess_text(chunk))
        # Save tokens as a space-separated file
        out_file = output_folder / (txt_file.stem + "_tokens.txt")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(" ".join(tokens))
        print(f"Saved processed tokens to {out_file}")

if __name__ == "__main__":
    preprocess_nco_files()
