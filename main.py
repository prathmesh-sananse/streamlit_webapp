import streamlit as st
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Hackathon Prototype",
    page_icon="🚀",
    layout="wide"
)

# --------- Hero Section ---------
st.markdown("""
    <style>
        .hero {
            text-align: center;
            padding: 3rem 1rem;
        }
        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            color: white;
        }
        .hero p {
            font-size: 1.3rem;
            color: #6c757d;
        }
    </style>
    <div class="hero">
        <h1>🌐 Welcome to Hackathon Hub</h1>
        <p>Your all-in-one prototype for real-time weather and data analytics.</p>
    </div>
""", unsafe_allow_html=True)

# --------- Feature Cards ---------
st.markdown("### 🔍 Explore Features")

col1, col2, col3, col4 = st.columns(4)

card_style = """
    <style>
        .card {
            border: 1px solid #f0f2f6;
            border-radius: 16px;
            padding: 25px;
            background-color: #ffffff;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }

        .card h3 {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 1.5rem;
        }

        .card p {
            color: #444;
            font-size: 1rem;
            line-height: 1.5;
        }

        .card a button {
            margin-top: 10px;
            font-size: 1rem;
            cursor: pointer;
        }
    </style>
"""

st.markdown(card_style, unsafe_allow_html=True)

# ---- Weather Card ----
with col1:
    st.markdown("""
        <div class="card">
            <h3 style='color:#1f77b4;'>☀️ Live Weather App</h3> 
            <p>Fetch real-time weather using city.</p>
            <a href="http://localhost:8501/Weather" target="_self">
                <button style='background-color:#1f77b4; color:white; border:none; padding:10px 20px; border-radius:6px;'>Go to Weather</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# ---- Analytics Card ----
with col2:
    st.markdown("""
        <div class="card">
            <h3 style='color:#ff7f0e;'>📊 Data Analytics</h3>
            <p>Analyze and visualize prices data using interactive charts.</p>
            <a href="http://localhost:8501/Stocks" target="_self">
                <button style='background-color:#ff7f0e; color:white; border:none; padding:10px 20px; border-radius:6px;'>Go to Analytics</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card">
            <h3 style='color:#2ca02c;'>👥 Employee API</h3>
            <p>View employee data in a structured format.</p>
            <a href="http://localhost:8501/Employee" target="_self">
                <button style='background-color:#2ca02c; color:white; border:none; padding:10px 20px; border-radius:6px;'>View Employees</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="card">
            <h3 style='color:#d62728;'>🏢 Departments API</h3>
            <p>Explore all department information.</p>
            <a href="http://localhost:8501/Department" target="_self">
                <button style='background-color:#d62728; color:white; border:none; padding:10px 20px; border-radius:6px;'>View Departments</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# --------- Footer ---------
st.markdown("""---""")
st.markdown(
    f"<p style='text-align:center; color:gray;'>Made with ❤️ for the Hackathon • {datetime.now().year}</p>",
    unsafe_allow_html=True
)
