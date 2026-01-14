import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- DB init ---
conn = sqlite3.connect("mediaplan.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS mediaplan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client TEXT,
    media TEXT,
    channel TEXT,
    format TEXT,
    budget REAL,
    start_date TEXT,
    end_date TEXT,
    notes TEXT
)
""")
conn.commit()

# --- Mapping ---
MEDIA_MAP = {
    "Digital": {
        "Facebook": ["Feed", "Video", "Stories"],
        "Instagram": ["Feed", "Reels", "Stories"],
        "TikTok": ["In-Feed", "TopView"],
        "YouTube": ["TrueView", "In-Stream"],
        "Google Display": ["Display Banner"],
    },
    "TV": {
        "Free-to-Air": ["15s", "30s"],
        "Cable": ["30s"],
        "OTT": ["15s", "30s"],
    },
    "Radio": {
        "Local FM": ["30s Spot", "60s Spot"],
        "National FM": ["30s Spot"],
    },
    "Print": {
        "Newspaper": ["Full Page", "Half Page", "Quarter Page"],
        "Magazine": ["Full Page", "Half Page"],
    },
    "OOH": {
        "Billboard": ["Static", "Digital"],
        "Transit": ["Static"],
        "Mall": ["Static", "Digital"],
    },
    "Cinema": {
        "Cinema Screen": ["15s", "30s"],
    },
}

st.title("📋 Mediapan Mock-Up App")

tabs = st.tabs(["➕ Input", "📁 Dataset"])

# --- TAB INPUT ---
with tabs[0]:
    st.subheader("Add Mediapan Entry")

    client = st.text_input("Client Name")
    media = st.selectbox("Media", list(MEDIA_MAP.keys()))

    channel = st.selectbox("Channel", list(MEDIA_MAP[media].keys()))
    format_ = st.selectbox("Format", MEDIA_MAP[media][channel])

    budget = st.number_input("Budget", min_value=0.0)
    start_date = st.date_input("Start Date", date.today())
    end_date = st.date_input("End Date", date.today())
    notes = st.text_area("Notes (optional)")

    if st.button("Submit"):
        c.execute("""
            INSERT INTO mediaplan (client, media, channel, format, budget, start_date, end_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (client, media, channel, format_, budget, start_date, end_date, notes))
        conn.commit()
        st.success("Data submitted!")

# --- TAB DATASET ---
with tabs[1]:
    st.subheader("Editable Dataset")

    df = pd.read_sql_query("SELECT * FROM mediaplan", conn)

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        key="editor"
    )

    if st.button("Save Changes"):
        c.execute("DELETE FROM mediaplan")
        conn.commit()

        edited_df.to_sql("mediaplan", conn, if_exists='append', index=False)
        st.success("Database updated!")
