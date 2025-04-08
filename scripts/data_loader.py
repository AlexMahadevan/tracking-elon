import os
import requests
from zipfile import ZipFile

BASE_URL = "https://ton.twimg.com/birdwatch-public-data"
SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
UNZIP_DIR = os.path.join(SAVE_DIR, "unzipped")

def download_file(url, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"✅ Downloaded: {file_path}")
    else:
        print(f"❌ Failed to download: {url}")

def download_and_extract(date_str='2025/04/08', ratings_count=16):
    os.makedirs(UNZIP_DIR, exist_ok=True)

    # Download noteStatusHistory and notes
    download_file(f"{BASE_URL}/{date_str}/noteStatusHistory/noteStatusHistory-00000.zip",
                  f"{SAVE_DIR}/noteStatusHistory-00000.zip")
    download_file(f"{BASE_URL}/{date_str}/notes/notes-00000.zip",
                  f"{SAVE_DIR}/notes-00000.zip")

    # Download ratings
    for i in range(ratings_count):
        padded = str(i).zfill(5)
        download_file(f"{BASE_URL}/{date_str}/noteRatings/ratings-{padded}.zip",
                      f"{SAVE_DIR}/ratings-{padded}.zip")

    # Extract all ZIP files
    for file in os.listdir(SAVE_DIR):
        if file.endswith(".zip"):
            zip_path = os.path.join(SAVE_DIR, file)
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(UNZIP_DIR)
            print(f"✅ Unzipped: {file}")

if __name__ == '__main__':
    download_and_extract(date_str='2025/04/08')
