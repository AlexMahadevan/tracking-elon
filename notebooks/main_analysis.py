import pandas as pd
import glob

def get_weekly_data():
    ratings_files = glob.glob('notebooks/data/unzipped/ratings-*.tsv')
    
    ratings_chunks = []
    chunk_size = 200000  # Smaller chunks for efficiency
    start_date = pd.to_datetime('2025-03-09')
    end_date = pd.to_datetime('2025-03-16')

    for idx, file in enumerate(ratings_files):
        print(f"Loading file {idx + 1} of {len(ratings_files)}: {file}")
        for chunk in pd.read_csv(file, sep='\t', chunksize=chunk_size):
            chunk['createdAt'] = pd.to_datetime(chunk['createdAtMillis'], unit='ms')
            filtered_chunk = chunk[(chunk['createdAt'] >= start_date) & (chunk['createdAt'] < end_date)]
            ratings_chunks.append(filtered_chunk[['noteId', 'helpfulnessLevel']])

    if len(ratings_chunks) == 0:
        print("⚠️ No valid data loaded. Check file paths or content.")
        return pd.DataFrame()  # Return empty DataFrame to prevent app crash

    all_ratings = pd.concat(ratings_chunks, ignore_index=True)

    # Group by noteId and summarize
    ratings_summary = all_ratings.groupby('noteId')['helpfulnessLevel'].value_counts().unstack(fill_value=0).reset_index()
    ratings_summary['total_helpful'] = ratings_summary.get('HELPFUL', 0)
    ratings_summary['total_unhelpful'] = ratings_summary.get('NOT_HELPFUL', 0)
    ratings_summary['helpfulness_ratio'] = ratings_summary['total_helpful'] / (
        ratings_summary['total_helpful'] + ratings_summary['total_unhelpful']
    )
    ratings_summary['helpfulness_ratio'] = ratings_summary['helpfulness_ratio'].fillna(0)

    # Load notes and status
    notes = pd.read_csv('notebooks/data/unzipped/notes-00000.tsv', sep='\t', low_memory=False)
    note_status = pd.read_csv('notebooks/data/unzipped/noteStatusHistory-00000.tsv', sep='\t', low_memory=False)

    # Merge datasets
    merged_data = pd.merge(ratings_summary, notes, on='noteId', how='inner')
    merged_data = pd.merge(merged_data, note_status, on='noteId', how='inner')

    return merged_data
