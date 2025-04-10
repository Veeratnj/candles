import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import numpy as np

# Function to get candlestick chart with buy/sell signals
def get_candlestick_signal(ticker_symbol, n_candles=9, period=10, bullish_percentage=50, bearish_percentage=50):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=f"{str(int(period))}d")

    available_candles = len(data)
    if available_candles < n_candles:
        n_candles = available_candles

    last_n_candles = data.iloc[-n_candles:]

    bullish_signal_series = pd.Series(np.nan, index=last_n_candles.index)
    bearish_signal_series = pd.Series(np.nan, index=last_n_candles.index)

    for index, row in last_n_candles.iterrows():
        open_price, close_price, high, low = row["Open"], row["Close"], row["High"], row["Low"]
        total_range = high - low

        bullish_body_percentage = ((close_price - low) / total_range) * 100 if close_price > open_price else 0
        bearish_body_percentage = ((high - close_price) / total_range) * 100 if open_price > close_price else 0

        if close_price > open_price and bullish_body_percentage >= bullish_percentage:
            bullish_signal_series.loc[index] = close_price

        elif open_price > close_price and bearish_body_percentage >= bearish_percentage:
            bearish_signal_series.loc[index] = close_price

    ap_bullish = mpf.make_addplot(bullish_signal_series, scatter=True, markersize=120, marker="^", color="#1f77b4", label="Buy Signal")
    ap_bearish = mpf.make_addplot(bearish_signal_series, scatter=True, markersize=120, marker="v", color="#ff7f0e", label="Sell Signal")

    fig, ax = mpf.plot(last_n_candles, type="candle", style="charles",
                        title=f"{ticker_symbol} Candlestick Chart",
                        ylabel="Price (INR)", volume=True,
                        addplot=[ap_bullish, ap_bearish],
                        figscale=1.2, figratio=(12,6), returnfig=True)
    return fig

# ----- Streamlit UI -----
st.set_page_config(page_title="Stock Analysis", page_icon="📈")

# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Home", "About Us"])

if page == "Home":
    st.title("📊 Candlestick Chart with Buy/Sell Signals")

    stock_options = {
        "Reliance Industries": "RELIANCE.NS",
        "Tata Consultancy Services": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "Hindustan Unilever": "HINDUNILVR.NS",
        "State Bank of India": "SBIN.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "Adani Enterprises": "ADANIENT.NS",
        "Larsen & Toubro": "LT.NS",
    }

    ticker_symbol = st.selectbox("Select a Stock", options=list(stock_options.keys()))
    ticker_symbol = stock_options[ticker_symbol] 

    n_candles = st.slider("Number of Candles", min_value=5, max_value=50, value=10, step=1)
    period = st.slider("Historical Data Period (Days)", min_value=10, max_value=365, value=100, step=10)
    bullish_percentage = st.slider("Bullish Signal Threshold (%)", min_value=10, max_value=90, value=50, step=5)
    bearish_percentage = st.slider("Bearish Signal Threshold (%)", min_value=10, max_value=90, value=50, step=5)

    if st.button("Generate Chart"):
        fig = get_candlestick_signal(ticker_symbol, n_candles, period, bullish_percentage, bearish_percentage)
        st.pyplot(fig)

elif page == "About Us":
    st.title("ℹ️ About Us")
    st.write("""
    Welcome to the Stock Analysis App! 📈

    This application allows users to analyze stock market trends using **candlestick charts** with **buy/sell signals**.
    
    ### Features:
    - 📊 **Real-time stock data(past data)** from Yahoo Finance
    - 📈 **Candlestick patterns** with buy/sell signal indicators
    - ⚙️ **Adjustable parameters** (candles, period, threshold)
    
    **Developed by: Veerakumar Murugesan**  
    💡 Inspired by professional trading strategies  
    """)

