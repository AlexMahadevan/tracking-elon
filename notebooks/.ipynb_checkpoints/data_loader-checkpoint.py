import os
import requests
from zipfile import ZipFile

BASE_URL = "https://ton.twimg.com/birdwatch-public-data"

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

def download_and_extract(date_str='2025/03/26', ratings_count=16):
    zip_dir = 'data'
    unzip_dir = os.path.join(zip_dir, 'unzipped')
    os.makedirs(unzip_dir, exist_ok=True)

    # Download the main files
    download_file(f"{BASE_URL}/{date_str}/noteStatusHistory/noteStatusHistory-00000.zip", f"{zip_dir}/noteStatusHistory-00000.zip")
    download_file(f"{BASE_URL}/{date_str}/notes/notes-00000.zip", f"{zip_dir}/notes-00000.zip")

    # Download ratings
    for i in range(ratings_count):
        padded = str(i).zfill(5)
        download_file(f"{BASE_URL}/{date_str}/noteRatings/ratings-{padded}.zip", f"{zip_dir}/ratings-{padded}.zip")

    # Extract
    for file in os.listdir(zip_dir):
        if file.endswith(".zip"):
            with ZipFile(os.path.join(zip_dir, file), 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
            print(f"✅ Unzipped: {file}")
