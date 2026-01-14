import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Load CSV
df_client = pd.read_csv("mediaplan/client_list.csv")
df_mt = pd.read_csv("mediaplan/MediaType_list.csv")
df_vendor = pd.read_csv("mediaplan/vendor_list.csv")

# SQLite Init
conn = sqlite3.connect("mediaplan.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS mediaplan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pod TEXT,
    client TEXT,
    media_type TEXT,
    media_subtype TEXT,
    vendor TEXT,
    budget REAL,
    start_date TEXT,
    end_date TEXT,
    notes TEXT
)
""")
conn.commit()

st.title("📋 Mediapan – Data Driven Mock-Up")

tabs = st.tabs(["➕ Input", "📁 Dataset"])

with tabs[0]:
    # Row 1
    col1, col2, col3 = st.columns(3)
    pod = col1.selectbox("Pod", sorted(df_client["pod"].unique()))

    client = col2.selectbox(
        "Client",
        sorted(df_client[df_client["pod"] == pod]["client"].unique())
    )

    media_type = col3.selectbox(
        "Media Type",
        sorted(df_mt["media_type"].unique())
    )

    # Row 2
    col4, col5, col6 = st.columns(3)
    media_subtype = col4.selectbox(
        "Media Subtype",
        sorted(df_mt[df_mt["media_type"] == media_type]["media_subtype"].unique())
    )

    vendor = col5.selectbox(
        "Vendor",
        sorted(df_vendor[df_vendor["media_subtype"] == media_subtype]["vendor"].unique())
    )

    notes = col6.text_input("Notes")

    # Row 3
    col7, col8, col9, col10 = st.columns(4)
    budget = col7.number_input("Budget", min_value=0.0)
    start_date = col8.date_input("Start Date", value=date.today())
    end_date = col9.date_input("End Date", value=date.today())

    submit = col10.button("Submit", type="primary")

    if submit:
        c.execute("""
            INSERT INTO mediaplan (pod, client, media_type, media_subtype, vendor, budget, start_date, end_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pod, client, media_type, media_subtype, vendor, budget, start_date, end_date, notes))
        conn.commit()
        st.success("Submitted!")

with tabs[1]:
    df = pd.read_sql_query("SELECT * FROM mediaplan", conn)
    edited_df = st.data_editor(df, num_rows="dynamic")

    if st.button("Save Changes"):
        c.execute("DELETE FROM mediaplan")
        conn.commit()
        edited_df.to_sql("mediaplan", conn, if_exists='append', index=False)
        st.success("Saved!")
