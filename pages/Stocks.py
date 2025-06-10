import streamlit as st
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import date

st.set_page_config(page_title="📊 Trending Stock Visualizer", layout="wide")
st.title("📈 Trending Stocks Dashboard (Live from Yahoo Finance)")

# -- STEP 1: Scrape Yahoo Trending Tickers --
@st.cache_data(show_spinner=False)
def get_trending_stocks():
    url = "https://finance.yahoo.com/trending-tickers"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    tickers = []
    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        if cols:
            tickers.append(cols[0].text.strip())

    tickers = tickers[:20]

    data = []
    for symbol in tickers:
        try:
            stock = yf.Ticker(symbol).info
            data.append({
                "Label": f"{symbol} - {stock.get('shortName', 'N/A')}",
                "Symbol": symbol
            })
        except:
            continue

    return pd.DataFrame(data)

with st.spinner("🚀 Fetching trending stocks from Yahoo Finance..."):
    trending_df = get_trending_stocks()

if trending_df.empty:
    st.error("⚠️ Couldn't fetch trending tickers.")
    st.stop()

# -- STEP 2: Stock Selector --
selected_label = st.selectbox("Select from trending stock", trending_df["Label"])
selected_symbol = trending_df.loc[trending_df["Label"] == selected_label, "Symbol"].values[0]

# -- STEP 3: Date Range Input --
start_date = st.date_input("Start Date", date(2023, 1, 1))
end_date = st.date_input("End Date", date.today())

# -- STEP 4: Fetch Stock Data --
@st.cache_data
def load_stock_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end, interval="1d")
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Fetch historical stock data with spinner
with st.spinner(f"📈 Loading {selected_symbol} historical data..."):
    stock_data = load_stock_data(selected_symbol, start_date, end_date)

if stock_data.empty:
    st.warning("No data found for the selected stock.")
    st.stop()

# Pagination parameters
rows_per_page = 5
total_rows = len(stock_data)
total_pages = (total_rows + rows_per_page - 1) // rows_per_page  # Ceiling division

# Initialize page number in session state if not set
if "page_num" not in st.session_state:
    st.session_state.page_num = 1

# Pagination parameters
rows_per_page = 5
total_rows = len(stock_data)
total_pages = (total_rows + rows_per_page - 1) // rows_per_page  # Ceiling division

# Initialize session state variable if not present
if "page_num" not in st.session_state:
    st.session_state.page_num = 1

# Handle page bounds
if st.session_state.page_num < 1:
    st.session_state.page_num = 1
elif st.session_state.page_num > total_pages:
    st.session_state.page_num = total_pages

# Button Layout aligned with DataFrame corners
btn_col1, spacer, btn_col2 = st.columns([1, 8, 1])

with btn_col1:
    if st.button("⬅️ Prev", key="prev_page") and st.session_state.page_num > 1:
        st.session_state.page_num -= 1

with btn_col2:
    if st.button("Next ➡️", key="next_page") and st.session_state.page_num < total_pages:
        st.session_state.page_num += 1

# Calculate start and end indices
start_idx = (st.session_state.page_num - 1) * rows_per_page
end_idx = start_idx + rows_per_page

# Display paginated data
st.dataframe(stock_data.iloc[start_idx:end_idx], use_container_width=True)


# -- STEP 5: Visualizations --

st.subheader("📊 Line Chart")
st.line_chart(stock_data.set_index("Date")["Close"])

st.subheader("📉 Bar Chart (Volume)")
st.bar_chart(stock_data.set_index("Date")["Volume"])

st.subheader("🌊 Area Chart (Cumulative Return)")
stock_data['Return'] = stock_data['Close'].pct_change()
stock_data['Cumulative'] = (1 + stock_data['Return']).cumprod()
st.area_chart(stock_data.set_index("Date")["Cumulative"])
