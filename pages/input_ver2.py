import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime

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

st.title("📋 Mediapan Mock-Up")

tabs = st.tabs(["➕ Input", "📁 Dataset"])


# --- TAB INPUT ---
with tabs[0]:
    client = st.text_input("Client")

    row1 = st.columns([1,1,1,1])
    media = row1[0].selectbox("Media", list(MEDIA_MAP.keys()))
    channel = row1[1].selectbox("Channel", list(MEDIA_MAP[media].keys()))
    format_ = row1[2].selectbox("Format", MEDIA_MAP[media][channel])
    notes = row1[3].text_input("Notes")

    row2 = st.columns([1,1,1,1])
    budget = row2[0].number_input("Budget", min_value=0.0)
    start_date = row2[1].date_input("Start Date", value=date.today())
    end_date = row2[2].date_input("End Date", value=date.today())
    submit = row2[3].button("Submit", type="primary")

    if submit:
        c.execute("""
            INSERT INTO mediaplan (client, media, channel, format, budget, start_date, end_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (client, media, channel, format_, budget, start_date, end_date, notes))
        conn.commit()
        st.success("Data submitted!")


# --- TAB DATASET (Editable) ---
with tabs[1]:
    df = pd.read_sql_query("SELECT * FROM mediaplan", conn)

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        key="editor"
    )

    if st.button("Save Changes"):
        c.execute("DELETE FROM mediaplan")
        conn.commit()
        edited_df.to_sql("mediaplan", conn, if_exists="append", index=False)
        st.success("Saved!")
