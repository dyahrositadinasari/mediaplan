import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mediaplan Input", layout="wide")

# Dummy mapping
mapping = {
    "Digital": {
        "Meta": {
            "Video": ["View", "ThruPlay", "CPV"],
            "Static": ["CTR", "CPC", "CPM"]
        },
        "Google": {
            "Search": ["CPC", "Conversion", "CPA"],
            "YouTube": ["View", "ThruPlay", "CPV"]
        },
        "TikTok": {
            "Video": ["CPV", "View", "Conversion"]
        }
    },
    "Offline": {
        "TV": {
            "30s Spot": ["GRP", "Reach"]
        },
        "OOH": {
            "Static": ["Reach", "OTS"]
        }
    },
    "KOL": {
        "Influencer": {
            "Post": ["Engagement", "CTR"],
            "Video": ["View", "Engagement"]
        }
    },
    "eCommerce": {
        "Tokopedia": {
            "Banner": ["CTR", "CPC"],
            "Search Ads": ["Conversion", "CPA"]
        },
        "Shopee": {
            "Banner": ["CTR", "CPC"],
            "Search Ads": ["Conversion", "CPA"]
        }
    }
}

# Initialize session storage
if "mediaplan" not in st.session_state:
    st.session_state.mediaplan = pd.DataFrame(columns=[
        "Channel", "Platform", "Format", "KPI", "Budget", "Start Date", "End Date"
    ])

st.title("🗂 Mediaplan Input Dummy App")

st.subheader("Step 1 — Input Planning")

col1, col2, col3, col4 = st.columns(4)

channel = col1.selectbox("Channel", list(mapping.keys()))

platform = col2.selectbox("Platform", list(mapping[channel].keys()))

format = col3.selectbox("Format", list(mapping[channel][platform].keys()))

kpi = col4.selectbox("KPI", mapping[channel][platform][format])

col5, col6, col7 = st.columns(3)
budget = col5.number_input("Budget", min_value=0, step=1000)
start_date = col6.date_input("Start Date", value=datetime.today())
end_date = col7.date_input("End Date", value=datetime.today())

if st.button("Add to Mediapan"):
    new_row = {
        "Channel": channel,
        "Platform": platform,
        "Format": format,
        "KPI": kpi,
        "Budget": budget,
        "Start Date": start_date,
        "End Date": end_date
    }
    st.session_state.mediaplan = pd.concat(
        [st.session_state.mediaplan, pd.DataFrame([new_row])],
        ignore_index=True
    )
    st.success("Row added!")

st.subheader("Step 2 — Review")

st.dataframe(st.session_state.mediaplan, use_container_width=True)

# Export button
if not st.session_state.mediaplan.empty:
    csv = st.session_state.mediaplan.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📤 Export to CSV",
        data=csv,
        file_name="mediaplan.csv",
        mime="text/csv"
    )
