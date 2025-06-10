import streamlit as st
import requests
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="🏢 Department Overview", layout="wide")
st.title("🏢 Department Overview")

# --- API FETCH ---
@st.cache_data(ttl=600)
def fetch_departments():
    try:
        response = requests.get("https://mi7-poc.onrender.com/all_departments_info/")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Failed to fetch department data: {e}")
        return pd.DataFrame()

with st.spinner("🚀 Fetching the departments data"):
    df = fetch_departments()

if not df.empty:
    # --- STATS ---
    st.markdown("## 🧾 Summary")

    col1, col2 = st.columns(2)
    col1.metric("Total Departments", len(df))
    col2.metric("Unique Locations", df['LOCATION'].nunique())
    style_metric_cards(background_color="#2e3c58")

    st.markdown("---")

    # --- LOCATION MAP (SIMULATED USING BAR) ---
    st.markdown("### 🌍 Department Locations")
    loc_count = df['LOCATION'].value_counts().reset_index()
    loc_count.columns = ['Location', 'Department Count']

    fig = px.bar(loc_count, x='Location', y='Department Count',
                 color='Location', text='Department Count',
                 title="Departments by Location",
                 template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- DEPARTMENT DETAILS ---
    st.markdown("### 🗂️ Departments")

    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"#### 📌 {row['DeptName']} Department")
            st.markdown(f"- **Dept Code**: `{row['DEPTCODE']}`")
            st.markdown(f"- **Location**: 🏙️ {row['LOCATION']}")
        st.markdown("---")

else:
    st.warning("No department data available.")
