import streamlit as st
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Hackathon Prototype",
    page_icon="🚀",
    layout="wide"
)

# --------- Hero Section ---------
st.title("🌐 Welcome to Hackathon Hub")
st.markdown("#### Your all-in-one prototype for real-time weather, analytics & data visualization")
st.markdown("---")

# --------- Feature Navigation Header ---------
st.header("🔍 Explore Features")

# --------- Layout: 2 Columns x 2 Rows ---------
col1, col2 = st.columns(2)

# Row 1 - Left
with col1:
    with st.container():
        st.subheader("☀️ Live Weather App")
        st.write("Get real-time weather data by entering a city name.")
        if st.button("🌤️ Go to Weather App", key="weather"):
            st.switch_page("pages/Weather.py")

# Row 1 - Right
with col2:
    with st.container():
        st.subheader("📊 Stock Analytics")
        st.write("Visualize and analyze stock prices using interactive charts.")
        if st.button("📈 Go to Analytics Dashboard", key="stocks"):
            st.switch_page("pages/Stocks.py")

# Row 2 - Left
with col1:
    with st.container():
        st.subheader("👥 Employee Data Viewer")
        st.write("View employee details fetched from an API.")
        if st.button("🧑‍💼 View Employees", key="employees"):
            st.switch_page("pages/Employee.py")

# Row 2 - Right
with col2:
    with st.container():
        st.subheader("🏢 Departments Info")
        st.write("Explore all departments and their locations.")
        if st.button("🏬 View Departments", key="departments"):
            st.switch_page("pages/Department.py")

# --------- Footer ---------
st.markdown("---")
st.markdown(
    f"<p style='text-align:center;'>Made with ❤️ for the Hackathon • {datetime.now().year}</p>",
    unsafe_allow_html=True
)
