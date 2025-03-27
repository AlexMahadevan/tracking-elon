import pandas as pd
import glob
import os

# === Paths ===
base_dir = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(base_dir, 'data/unzipped')
weekly_path = os.path.join(base_dir, 'notebooks/weekly_data')
os.makedirs(weekly_path, exist_ok=True)

# === Load notes and status history ===
notes = pd.read_csv(os.path.join(data_path, 'notes-00000.tsv'), sep='\t', dtype={'tweetId': str}, low_memory=False)
note_status = pd.read_csv(os.path.join(data_path, 'noteStatusHistory-00000.tsv'), sep='\t', low_memory=False)

notes['createdAt'] = pd.to_datetime(notes['createdAtMillis'], unit='ms')
note_status['currentStatusDate'] = pd.to_datetime(note_status['timestampMillisOfCurrentStatus'], unit='ms')

# === Helper function to filter ratings ===
def load_filtered_ratings(start_date, end_date):
    ratings_files = glob.glob(os.path.join(data_path, 'ratings-*.tsv'))
    chunk_size = 500000
    chunks = []
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    for file in ratings_files:
        for chunk in pd.read_csv(file, sep='\t', chunksize=chunk_size):
            chunk['createdAt'] = pd.to_datetime(chunk['createdAtMillis'], unit='ms')
            filtered = chunk[(chunk['createdAt'] >= start) & (chunk['createdAt'] < end)]
            chunks.append(filtered[['noteId', 'helpfulnessLevel', 'createdAt']])

    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()

# === Define periods ===
periods = {
    'recent': ('2025-03-11', '2025-03-25'),
    'earlier': ('2025-02-03', '2025-02-14')
}

# === Main processor ===
def process_period(label, start_date, end_date):
    print(f"Processing {label} period: {start_date} to {end_date}")
    ratings = load_filtered_ratings(start_date, end_date)
    print(f"➡️  Ratings count: {len(ratings)}")

    summary = ratings.groupby('noteId')['helpfulnessLevel'].value_counts().unstack(fill_value=0).reset_index()
    summary['total_helpful'] = summary.get('HELPFUL', 0)
    summary['total_unhelpful'] = summary.get('NOT_HELPFUL', 0)
    summary['helpfulness_ratio'] = summary['total_helpful'] / (
        summary['total_helpful'] + summary['total_unhelpful']
    )
    summary['helpfulness_ratio'] = summary['helpfulness_ratio'].fillna(0)

    merged = pd.merge(summary, notes, on='noteId', how='left')
    merged = pd.merge(merged, note_status, on='noteId', how='left')

    out_path = os.path.join(weekly_path, f"{label}_period_{start_date}_to_{end_date}.csv")
    merged.to_csv(out_path, index=False)
    print(f"✅ Saved: {out_path}")

    return merged

# === Run for both periods ===
recent_df = process_period('recent', *periods['recent'])
earlier_df = process_period('earlier', *periods['earlier'])
