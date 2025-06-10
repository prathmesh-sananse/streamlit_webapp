import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards

# --- PAGE CONFIG ---
st.set_page_config(page_title="💼 Employee Info Dashboard", layout="wide")
st.title("👨‍💼 Employee Information Dashboard")

# --- API FETCH ---
@st.cache_data(ttl=600)
def fetch_employees():
    try:
        response = requests.get("https://mi7-poc.onrender.com/all_employees_info/")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

with st.spinner("🚀 Fetching the employee data"):
    df = fetch_employees()

if not df.empty:
    # --- CLEANUP / ENHANCE ---
    df['HireDate'] = pd.to_datetime(df['HireDate']).dt.strftime('%d %b %Y')
    df['FullName'] = df['EmpFName'] + " " + df['EmpLName']

    # --- FILTER SECTION ---
    with st.sidebar:
        st.header("🔍 Filters")
        depts = sorted(df['DEPTCODE'].unique())
        dept_filter = st.multiselect("Department Code", depts, default=depts)
        job_filter = st.multiselect("Job Title", df['Job'].unique(), default=df['Job'].unique())

    filtered_df = df[(df['DEPTCODE'].isin(dept_filter)) & (df['Job'].isin(job_filter))]

    # --- STATS ---
    st.markdown("## 📊 Summary Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(filtered_df))
    col2.metric("Avg Salary", f"${filtered_df['Salary'].mean():,.2f}")
    col3.metric("Avg Commission", f"${filtered_df['Commission'].mean():,.2f}")
    style_metric_cards(background_color="#2e3c58")

    st.markdown("---")

    # --- EMPLOYEE CARDS ---
    st.markdown("## 🧾 Employee List")

    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image("https://ui-avatars.com/api/?name=" + row['FullName'], width=60)
            with col2:
                st.markdown(f"### {row['FullName']}")
                st.markdown(f"**Role:** {row['Job']}")
                st.markdown(f"**Dept Code:** {row['DEPTCODE']}")
                st.markdown(f"**Manager:** {row['Manager']}")
                st.markdown(f"**Hire Date:** {row['HireDate']}")
                st.markdown(f"**Salary:** 💰 ${row['Salary']:,}")
                if row['Commission'] > 0:
                    st.markdown(f"**Commission:** ${row['Commission']:,}")
        st.markdown("---")

else:
    st.warning("No employee data available.")
