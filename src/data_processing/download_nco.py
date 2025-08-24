import requests
from pathlib import Path
import time

def download_file(url, destination):
    print(f"Downloading {url} ...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    chunk_size = 8192

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                done = int(50 * downloaded / total_size)
                print('\r[{}{}]'.format('=' * done, ' ' * (50-done)), end='')

    print(f"\nSaved to: {destination}")

def download_nco_datasets():
    urls = {
        "nco_vol1_abstract.pdf": "https://labour.gov.in/sites/default/files/National%20Classification%20of%20Occupations%20_Vol%20I-%202015.pdf",
        "nco_vol2a_detailed.pdf": "https://www.ncs.gov.in/Documents/National%20Classification%20of%20Occupations%20_Vol%20II-A-%202015.pdf",
        "nco_vol2b_detailed.pdf": "https://labour.gov.in/sites/default/files/National%20Classification%20of%20Occupations_Vol%20II-B-%202015.pdf"
    }
    data_folder = Path("data/raw")
    data_folder.mkdir(exist_ok=True)
    
    for filename, url in urls.items():
        destination = data_folder / filename
        if destination.exists():
            print(f"{filename} already downloaded.")
        else:
            download_file(url, destination)
            time.sleep(1)  # polite delay

if __name__ == "__main__":
    download_nco_datasets()
