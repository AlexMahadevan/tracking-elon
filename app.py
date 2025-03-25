import streamlit as st
import pandas as pd
import os  # <-- Add this line

st.write("Current Working Directory:", os.getcwd())
st.write("Files in notebooks/weekly_data/:", os.listdir('notebooks/weekly_data/'))

@st.cache_data
def load_data():
    print("Files in 'notebooks/weekly_data/':", os.listdir('notebooks/weekly_data/'))  # Debugging step
    return pd.read_csv('notebooks/weekly_data/weekly_data_2025-03-09_to_2025-03-15.csv')

data = load_data()

st.write("Data Columns:", data.columns)
st.write("Sample Data:", data.head())

# App layout
st.title("Community Notes Analysis")
st.markdown("Explore insights from our weekly Community Notes data analysis.")

# Key Metrics
average_helpfulness_ratio = data['helpfulness_ratio'].mean()
percent_helpful_notes = (data['currentStatus'] == 'CURRENTLY_RATED_HELPFUL').mean() * 100

st.metric("Average Helpfulness Ratio", round(average_helpfulness_ratio, 2))
st.metric("Percentage of Helpful Notes", f"{percent_helpful_notes:.2f}%")

# Tracked Tweets Analysis
tracked_tweet_ids = [1899636898533867969]
tracked_notes = data[data['tweetId'].isin(tracked_tweet_ids)]

tracked_helpfulness_ratio = tracked_notes['helpfulness_ratio'].mean()
percent_helpful_tracked_notes = (tracked_notes['currentStatus'] == 'CURRENTLY_RATED_HELPFUL').mean() * 100

st.subheader("Tracked Tweet Analysis")
st.metric("Helpfulness Ratio for Tracked Tweets", round(tracked_helpfulness_ratio, 2))
st.metric("% of Helpful Notes on Tracked Tweets", f"{percent_helpful_tracked_notes:.2f}%")

# Data Table Display
st.subheader("Full Dataset View")
st.dataframe(data.sample(100), use_container_width=True)