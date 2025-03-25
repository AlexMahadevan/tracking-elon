import streamlit as st
import sys
sys.path.append('notebooks')
from main_analysis import get_weekly_data

# Load data
@st.cache_data
def load_data():
    data = get_weekly_data()
    return data

data = load_data()

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
st.dataframe(data)
