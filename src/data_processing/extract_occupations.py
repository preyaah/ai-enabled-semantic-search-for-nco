import re
from pathlib import Path

def extract_individual_occupations(text_file):
    """Extract individual occupation entries from NCO text"""
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Processing {text_file.name}, content length: {len(content)} characters")
    
    # Try multiple patterns to extract occupations
    occupations = []
    
    # Pattern 1: NCO codes like "1234 - Job Title" or "1234. Job Title"
    pattern1 = r'(\d{4})\s*[-–.]\s*([^0-9\n]+?)(?=\d{4}\s*[-–.]|\n\n|\Z)'
    matches1 = re.findall(pattern1, content, re.DOTALL)
    
    for code, desc in matches1:
        cleaned_desc = re.sub(r'\s+', ' ', desc.strip())
        if len(cleaned_desc) > 20:  # Keep substantial entries
            occupations.append(f"NCO-{code}: {cleaned_desc}")
    
    # Pattern 2: Look for job titles in structured format
    # Split by common separators and look for job-like entries
    lines = content.split('\n')
    current_entry = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_entry and len(current_entry) > 50:
                occupations.append(current_entry)
            current_entry = ""
            continue
        
        # Check if line looks like a job title or description
        if any(keyword in line.lower() for keyword in ['work', 'job', 'occupation', 'duties', 'responsibilities', 'tasks']):
            current_entry += " " + line
        elif re.match(r'^[A-Z][a-z]', line):  # Starts with capital letter
            if current_entry:
                if len(current_entry) > 50:
                    occupations.append(current_entry.strip())
                current_entry = line
            else:
                current_entry = line
        else:
            current_entry += " " + line
    
    # Add the last entry
    if current_entry and len(current_entry) > 50:
        occupations.append(current_entry.strip())
    
    # Remove duplicates and clean up
    unique_occupations = []
    seen = set()
    
    for occ in occupations:
        cleaned = re.sub(r'\s+', ' ', occ.strip())
        # Create a simple hash to check for near-duplicates
        occ_hash = cleaned.lower()[:100]
        if occ_hash not in seen and len(cleaned) > 30:
            unique_occupations.append(cleaned)
            seen.add(occ_hash)
    
    return unique_occupations[:200]  # Limit to 200 per file to avoid overwhelming

def process_all_files():
    """Process all extracted text files to get individual occupations"""
    input_folder = Path("data/raw")
    output_folder = Path("data/interim") 
    output_folder.mkdir(exist_ok=True)
    
    all_occupations = []
    
    for txt_file in input_folder.glob("*_extracted.txt"):
        print(f"\nProcessing {txt_file.name}")
        occupations = extract_individual_occupations(txt_file)
        
        if occupations:
            # Save individual occupations from this file
            output_file = output_folder / f"{txt_file.stem}_occupations.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                for i, occ in enumerate(occupations):
                    f.write(f"Entry_{i+1}: {occ}\n\n")
            
            print(f"Extracted {len(occupations)} occupation entries")
            all_occupations.extend(occupations)
        else:
            print(f"No occupations found in {txt_file.name}")
    
    # Save all occupations in one file
    all_occupations_file = output_folder / "all_occupations.txt"
    with open(all_occupations_file, 'w', encoding='utf-8') as f:
        for i, occ in enumerate(all_occupations):
            f.write(f"Occupation_{i+1}: {occ}\n\n")
    
    print(f"\nTotal occupations extracted: {len(all_occupations)}")
    print(f"All occupations saved to: {all_occupations_file}")
    
    return all_occupations

if __name__ == "__main__":
    process_all_files()
