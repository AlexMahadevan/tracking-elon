import streamlit as st
import pandas as pd
import os
import altair as alt

# === Styling ===
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

pd.set_option('display.float_format', lambda x: '%.2f' % x)

# === Load data ===
@st.cache_data
def load_data(filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename, dtype={'tweetId': str})
        return df
    else:
        st.warning(f"File not found: {filename}")
        return pd.DataFrame()

# === Paths ===
recent_path = 'notebooks/weekly_data/recent_period_2025-03-11_to_2025-03-25.csv'
earlier_path = 'notebooks/weekly_data/earlier_period_2025-02-03_to_2025-02-14.csv'

recent_df = load_data(recent_path)
earlier_df = load_data(earlier_path)

# === Tracked tweet IDs ===
tracked_tweet_ids = [
    "1904618817986474240", "1904222280655286776", "1904160507952529616", "1902411743428514085",
    "1902361782255063090", "1902131566521795054", "1902003410255176021", "1901964313511731387",
    "1901631931298525519", "1901441626116870156", "1901317322041597987", "1900608417515081812",
    "1899905798593274270", "1900670438260257276", "1899980394604175778", "1899561031996985814",
    "1901406082800459809", "1901011700343861315", "1900741103424286723", "1904362652987429338",
    "1903215026682380513", "1902818394946277485", "1899637674241048800", "1899636898533867969"
]

# === Metric calculator ===
def calc_metrics(df, label):
    all_notes_ratio = df['helpfulness_ratio'].mean()
    notes_per_tweet = df.groupby('tweetId').size().mean()

    helpful_notes = df[df['currentStatus'] == 'CURRENTLY_RATED_HELPFUL']
    helpful_notes_ratio = helpful_notes['helpfulness_ratio'].mean()

    tracked = df[df['tweetId'].isin(tracked_tweet_ids)]
    tracked_notes_ratio = tracked['helpfulness_ratio'].mean() if not tracked.empty else 0
    tracked_notes_per_tweet = tracked.groupby('tweetId').size().mean() if not tracked.empty else 0

    tracked_helpful = tracked[tracked['currentStatus'] == 'CURRENTLY_RATED_HELPFUL']
    tracked_helpful_ratio = tracked_helpful['helpfulness_ratio'].mean() if not tracked_helpful.empty else 0

    return pd.DataFrame({
        'Period': [label],
        'Helpfulness Ratio (All Notes)': [round(all_notes_ratio, 2)],
        'Helpfulness Ratio (Helpful Notes Only)': [round(helpful_notes_ratio, 2)],
        'Notes per Tweet (All)': [round(notes_per_tweet, 2)],
        'Tracked Helpfulness Ratio (All Notes)': [round(tracked_notes_ratio, 2)],
        'Tracked Helpfulness Ratio (Helpful Only)': [round(tracked_helpful_ratio, 2)],
        'Notes per Tweet (Tracked)': [round(tracked_notes_per_tweet, 2)]
    })

# === Header ===
st.title("Community Notes Timeframe Comparison")
st.markdown("We compare the helpfulness of notes and number of proposed notes per tweet across two periods.")


# === Table ===
recent_metrics = calc_metrics(recent_df, "Recent (Mar 11–25)")
earlier_metrics = calc_metrics(earlier_df, "Earlier (Feb 3–14)")
comparison_df = pd.concat([earlier_metrics, recent_metrics], ignore_index=True)

# Melt the dataframe for plotting
melted = comparison_df.melt(id_vars='Period', var_name='Metric', value_name='Value')

# Create bar chart
chart = alt.Chart(melted).mark_bar().encode(
    x=alt.X('Period:N', title=None),
    y=alt.Y('Value:Q'),
    color='Period:N',
    column=alt.Column('Metric:N', title='Metric')
).properties(
    title='📊 Key Metrics Comparison',
    width=150,
    height=300
)

st.altair_chart(chart, use_container_width=True)

st.subheader("📊 Comparison of Key Metrics")
st.dataframe(comparison_df.style.set_properties(**{'white-space': 'nowrap'}), use_container_width=True)

# === Sample Notes ===
st.subheader("🔍 Sample of Recent Notes")
if not recent_df.empty:
    st.dataframe(recent_df[['noteId', 'tweetId', 'helpfulness_ratio', 'summary', 'total_helpful', 'total_unhelpful']].sample(10), use_container_width=True)

st.subheader("🔍 Sample of Earlier Notes")
if not earlier_df.empty:
    st.dataframe(earlier_df[['noteId', 'tweetId', 'helpfulness_ratio', 'summary', 'total_helpful', 'total_unhelpful']].sample(10), use_container_width=True)

# === Tracked Notes Tables ===
st.subheader("🧵 Tracked Tweet Notes — Recent")
tracked_recent = recent_df[recent_df['tweetId'].isin(tracked_tweet_ids)]
if not tracked_recent.empty:
    st.dataframe(tracked_recent[['noteId', 'tweetId', 'helpfulness_ratio', 'summary', 'total_helpful', 'total_unhelpful']], use_container_width=True)
else:
    st.write("No tracked tweet notes found for recent period.")

st.subheader("🧵 Tracked Tweet Notes — Earlier")
tracked_earlier = earlier_df[earlier_df['tweetId'].isin(tracked_tweet_ids)]
if not tracked_earlier.empty:
    st.dataframe(tracked_earlier[['noteId', 'tweetId', 'helpfulness_ratio', 'summary', 'total_helpful', 'total_unhelpful']], use_container_width=True)
else:
    st.write("No tracked tweet notes found for earlier period.")
