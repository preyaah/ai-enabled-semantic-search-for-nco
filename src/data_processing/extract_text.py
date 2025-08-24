import pdfplumber
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    all_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    all_text.append(text)
                else:
                    print(f"Warning: Page {i+1} in {pdf_path.name} has no extractable text.")
    except Exception as e:
        print(f"Error extracting text from {pdf_path.name}: {e}")
        return None
    return "\n".join(all_text)

def extract_text_from_all_pdfs():
    data_folder = Path("data/raw")
    for pdf_file in data_folder.glob("*.pdf"):
        print(f"\nExtracting text from: {pdf_file.name}")
        text = extract_text_from_pdf(pdf_file)
        if text:
            output_file = data_folder / (pdf_file.stem + "_extracted.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved extracted text to: {output_file}")
        else:
            print(f"Skipped saving for {pdf_file.name} due to extraction error.")

if __name__ == "__main__":
    extract_text_from_all_pdfs()
