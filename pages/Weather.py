import streamlit as st
import requests

# Page Configuration
st.set_page_config("Hackathon Demo", layout="centered")
API_KEY = "fbec813b31624fd389d172140250706"

# Title
st.title("🌦️ Live Weather App")
st.markdown("Enter a city name to get the current weather details visually.")

# Initialize session state on first load
if 'city' not in st.session_state:
    st.session_state.city = "Hyderabad"
if 'data' not in st.session_state:
    st.session_state.data = None

# Input
user_input = st.text_input("Enter a City", st.session_state.city)

# Button logic to update city and fetch new data
if st.button("Get Weather"):
    st.session_state.city = user_input
    st.session_state.data = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={st.session_state.city}"
    ).json()

# Initial fetch for default city if not done yet
if st.session_state.data is None:
    with st.spinner("🌍 Loading weather data for default city..."):
        st.session_state.data = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={st.session_state.city}"
        ).json()

# Weather display logic
data = st.session_state.data
if data and 'current' in data:
    location = data['location']
    current = data['current']
    condition = current['condition']

    # Weather Icon & Main Info
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https:" + condition['icon'], width=100)
    with col2:
        st.markdown(f"### {location['name']}, {location['region']}, {location['country']}")
        st.markdown(f"**Condition:** {condition['text']}")
        st.markdown(f"**Local Time:** {location['localtime']}")

    # Temperature Stats
    st.subheader("🌡️ Temperature")
    col1, col2, col3 = st.columns(3)
    col1.metric("Actual (°C)", f"{current['temp_c']}°C")
    col2.metric("Feels Like", f"{current['feelslike_c']}°C")
    col3.metric("Heat Index", f"{current['heatindex_c']}°C")

    # Wind & Pressure
    st.subheader("💨 Wind & Pressure")
    col1, col2, col3 = st.columns(3)
    col1.metric("Wind Speed", f"{current['wind_kph']} kph")
    col2.metric("Wind Direction", current['wind_dir'])
    col3.metric("Pressure", f"{current['pressure_mb']} mb")

    # Humidity & Visibility
    st.subheader("💧 Other Info")
    col1, col2, col3 = st.columns(3)
    col1.metric("Humidity", f"{current['humidity']}%")
    col2.metric("Cloud Cover", f"{current['cloud']}%")
    col3.metric("Visibility", f"{current['vis_km']} km")

    # UV and Gust
    st.subheader("🌞 UV & Gust")
    col1, col2 = st.columns(2)
    col1.metric("UV Index", current['uv'])
    col2.metric("Wind Gust", f"{current['gust_kph']} kph")

    # Optional: Debug output
    with st.expander("📦 Raw JSON Data"):
        st.json(data)

elif data and 'error' in data:
    st.error("❌ " + data['error'].get('message', 'Failed to fetch weather data'))
