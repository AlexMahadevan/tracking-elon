import pandas as pd
import glob
import requests
from zipfile import ZipFile
import os

# Download Data
BASE_URL = "https://ton.twimg.com/birdwatch-public-data/2025/03/23"

def download_file(url, file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"✅ Downloaded: {file_path}")
    else:
        print(f"❌ Failed to download: {url}")

def download_all_data():
    download_file(f"{BASE_URL}/noteStatusHistory/noteStatusHistory-00000.zip", 'data/noteStatusHistory-00000.zip')
    download_file(f"{BASE_URL}/notes/notes-00000.zip", 'data/notes-00000.zip')
    for i in range(16):
        download_file(f"{BASE_URL}/noteRatings/ratings-{str(i).zfill(5)}.zip", f'data/ratings-{str(i).zfill(5)}.zip')

# Unzip Data
def unzip_data():
    for file in os.listdir('data/'):
        if file.endswith(".zip"):
            with ZipFile(f'data/{file}', 'r') as zip_ref:
                zip_ref.extractall('data/unzipped')

# Load and Filter Data
def get_weekly_data():
    ratings_files = glob.glob('data/unzipped/ratings-*.tsv')

    ratings_chunks = []
    chunk_size = 500000
    start_date = pd.to_datetime('2025-03-09')
    end_date = pd.to_datetime('2025-03-16')

    for idx, file in enumerate(ratings_files):
        print(f"Loading file {idx + 1} of {len(ratings_files)}: {file}")
        for chunk in pd.read_csv(file, sep='\t', chunksize=chunk_size):
            chunk['createdAt'] = pd.to_datetime(chunk['createdAtMillis'], unit='ms')
            filtered_chunk = chunk[(chunk['createdAt'] >= start_date) & (chunk['createdAt'] < end_date)]
            ratings_chunks.append(filtered_chunk[['noteId', 'helpfulnessLevel', 'createdAt']])

    all_ratings = pd.concat(ratings_chunks, ignore_index=True)

    # Group and Aggregate Data
    ratings_summary = all_ratings.groupby('noteId')['helpfulnessLevel'].value_counts().unstack(fill_value=0).reset_index()
    ratings_summary['total_helpful'] = ratings_summary.get('HELPFUL', 0)
    ratings_summary['total_unhelpful'] = ratings_summary.get('NOT_HELPFUL', 0)
    ratings_summary['helpfulness_ratio'] = ratings_summary['total_helpful'] / (
        ratings_summary['total_helpful'] + ratings_summary['total_unhelpful']
    )
    ratings_summary['helpfulness_ratio'] = ratings_summary['helpfulness_ratio'].fillna(0)

    # Load Notes and NoteStatus
    notes = pd.read_csv('data/unzipped/notes-00000.tsv', sep='\t', low_memory=False)
    notes_status = pd.read_csv('data/unzipped/noteStatusHistory-00000.tsv', sep='\t', low_memory=False)

    # Add Time Filters
    notes['createdAt'] = pd.to_datetime(notes['createdAtMillis'], unit='ms')
    filtered_notes = notes[(notes['createdAt'] >= start_date) & (notes['createdAt'] < end_date)]

    notes_status['currentStatusDate'] = pd.to_datetime(notes_status['timestampMillisOfCurrentStatus'], unit='ms')
    filtered_note_status = notes_status[
        (notes_status['currentStatusDate'] >= start_date) &
        (notes_status['currentStatusDate'] < end_date)
    ]

    # Merge Data
    merged_data = pd.merge(ratings_summary, filtered_notes, on='noteId', how='inner')
    merged_data = pd.merge(merged_data, filtered_note_status, on='noteId', how='inner')

    return merged_data
