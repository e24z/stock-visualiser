import yfinance as yf
import streamlit as st
import pandas as pd

# Add a text input for the user to enter a ticker symbol
ticker = st.text_input("Enter a stock ticker (e.g., AAPL):")

# Add checkboxes for SMA display
show_sma_20 = st.checkbox("Show 20-day SMA")
show_sma_50 = st.checkbox("Show 50-day SMA")

# Validate the input
if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y", interval="1d")

        if hist.empty:
            st.error("No data found for the given ticker. Please try another.")
        else:
            # Calculate SMAs regardless of checkbox state
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()

            columns_to_plot = ["Close"]
            if show_sma_20:
                columns_to_plot.append("SMA_20")
            if show_sma_50:
                columns_to_plot.append("SMA_50")

            st.line_chart(hist[columns_to_plot])

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter a valid ticker symbol.")