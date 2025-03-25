import streamlit as st
import pandas as pd
import os  # <-- Add this line

#st.write("Current Working Directory:", os.getcwd())
# st.write("Files in notebooks/weekly_data/:", os.listdir('notebooks/weekly_data/'))

@st.cache_data
def load_data():
    print("Files in 'notebooks/weekly_data/':", os.listdir('notebooks/weekly_data/'))  # Debugging step
    return pd.read_csv('notebooks/weekly_data/weekly_data_2025-03-09_to_2025-03-15.csv')

data = load_data()

# App layout
st.title("Tracking Elon and Trump on Community Notes")
st.markdown("Community Notes posts from Donald Trump and Elon Musk rarely go public. Here's a look at data showing this from March 9 - March 15.")

st.subheader("Overall data")
# Key Metrics
average_helpfulness_ratio = data['helpfulness_ratio'].mean()
percent_helpful_notes = (data['currentStatus'] == 'CURRENTLY_RATED_HELPFUL').mean() * 100

st.metric("Helpfulness ratio for all helpful notes", round(average_helpfulness_ratio, 2))
st.metric("Overall percentage of helpful notes", f"{percent_helpful_notes:.2f}%")

# Tracked Tweets Analysis
tracked_tweet_ids = [1899636898533867969]
tracked_notes = data[data['tweetId'].isin(tracked_tweet_ids)]

tracked_helpfulness_ratio = tracked_notes['helpfulness_ratio'].mean()
percent_helpful_tracked_notes = (tracked_notes['currentStatus'] == 'CURRENTLY_RATED_HELPFUL').mean() * 100

st.subheader("Trump and Musk data")
st.metric("Helpfulness ratio for Trump and Musk posts", round(tracked_helpfulness_ratio, 2))
st.metric("% of Helpful notes on Trump and Musk posts", f"{percent_helpful_tracked_notes:.2f}%")

# Data Table Display
st.subheader("Full Dataset View")
st.dataframe(data.sample(100), use_container_width=True)