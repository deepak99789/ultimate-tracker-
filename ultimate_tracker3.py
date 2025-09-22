import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from tvDatafeed import TvDatafeed, Interval

# TradingView se data fetch
@st.cache_data
def fetch_data(symbol, exchange, interval, n_bars=500):
    tv = TvDatafeed()
    df = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars)
    return df

# Simple demand/supply zone logic (demo purpose)
def find_zones(df):
    df['rolling_min'] = df['low'].rolling(10).min()
    df['rolling_max'] = df['high'].rolling(10).max()
    zones = df[['rolling_min', 'rolling_max']].dropna()
    return zones

# Streamlit UI
st.set_page_config(page_title="📊 Ultimate Supply-Demand Tracker", layout="wide")

st.title("📊 Ultimate Supply-Demand Zone Screener")

col1, col2, col3 = st.columns(3)
with col1:
    symbol = st.text_input("Symbol", value="RELIANCE")
with col2:
    exchange = st.text_input("Exchange", value="NSE")
with col3:
    interval = st.selectbox("Interval", ["15m", "75m", "125m", "1h", "2h", "1d", "1w", "1M"])

if st.button("Fetch Data"):
    df = fetch_data(symbol, exchange, interval, n_bars=365)
    st.success(f"Data fetched: {df.shape[0]} candles")

    zones = find_zones(df)

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])

    for i, row in zones.iterrows():
        fig.add_hline(y=row['rolling_min'], line_color="green", opacity=0.3)
        fig.add_hline(y=row['rolling_max'], line_color="red", opacity=0.3)

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.tail(20))
