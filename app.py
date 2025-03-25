import streamlit as st
import pandas as pd
import os

# Inject global font styles to match your website
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Source Sans Pro', sans-serif !important;
            color: #333;
            background-color: #f9f9f9;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif !important;
            color: #000;
        }

        a {
            color: #0072ff !important;
            text-decoration: none;
        }

        a:hover {
            color: #0056b3 !important;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# Load data directly from the saved weekly data file
@st.cache_data  # Caches data for improved performance
def load_data():
    file_path = 'notebooks/weekly_data/weekly_data_2025-03-09_to_2025-03-15.csv'
    if not os.path.exists(file_path):
        file_path = './weekly_data/weekly_data_2025-03-09_to_2025-03-15.csv'
    return pd.read_csv(file_path)

data = load_data()

# App layout
st.title("Community Notes Analysis")
st.markdown("Explore insights from our weekly Community Notes data analysis.")

# Key Metrics
average_helpfulness_ratio = data['helpfulness_ratio'].mean()
percent_helpful_notes = (data['currentStatus'] == 'CURRENTLY_RATED_HELPFUL').mean() * 100

st.metric("Average Helpfulness Ratio", round(average_helpfulness_ratio, 2))
st.metric("Percentage of Helpful Notes", f"{percent_helpful_notes:.2f}%")

# Prepare data
data['tweet_url'] = data['tweetId'].apply(lambda tid: f"https://twitter.com/anyuser/status/{tid}" if pd.notnull(tid) else "")
columns_to_show = ['tweet_url', 'summary', 'total_helpful', 'total_unhelpful', 'helpfulness_ratio',  'noteId']
existing_columns = [col for col in columns_to_show if col in data.columns]

# Tracked Tweets Analysis
tracked_tweet_ids = [1899636898533867969]
tracked_notes = data[data['tweetId'].isin(tracked_tweet_ids)]

tracked_helpfulness_ratio = tracked_notes['helpfulness_ratio'].mean()
percent_helpful_tracked_notes = (tracked_notes['currentStatus'] == 'CURRENTLY_RATED_HELPFUL').mean() * 100

st.subheader("Tracked Tweet Analysis")
st.metric("Helpfulness Ratio for Tracked Tweets", round(tracked_helpfulness_ratio, 2))
st.metric("% of Helpful Notes on Tracked Tweets", f"{percent_helpful_tracked_notes:.2f}%")

# Helpful Notes Table
helpful_notes = data[data['currentStatus'] == 'CURRENTLY_RATED_HELPFUL']
st.subheader("Helpful Notes")
st.dataframe(helpful_notes[existing_columns].reset_index(drop=True), use_container_width=True)

# Tracked Tweets Notes Table
st.subheader("Notes on Tracked Tweets")
st.dataframe(tracked_notes[existing_columns].reset_index(drop=True), use_container_width=True)

# Full Dataset Table
st.subheader("All of the Week's Data")
st.dataframe(data[existing_columns].sample(min(1000, len(data))).reset_index(drop=True), use_container_width=True)
