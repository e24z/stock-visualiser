import yfinance as yf
import streamlit as st
import pandas as pd

# User input
ticker = st.text_input("Enter a stock ticker (e.g., AAPL):")

# Checkboxes
show_sma_20 = st.checkbox("Show 20-day SMA")
show_sma_50 = st.checkbox("Show 50-day SMA")
show_returns = st.checkbox("Show Daily Returns")
show_volatility = st.checkbox("Show Rolling Volatility (20-day)")

# Validate input
if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y", interval="1d")

        if hist.empty:
            st.error("No data found for the given ticker. Please try another.")
        else:
            # SMAs
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()

            # Returns and Volatility
            hist['Returns'] = hist['Close'].pct_change()
            hist['Volatility'] = hist['Returns'].rolling(window=20).std()

            # Price chart
            columns_to_plot = ["Close"]
            if show_sma_20:
                columns_to_plot.append("SMA_20")
            if show_sma_50:
                columns_to_plot.append("SMA_50")
            st.subheader("Price & Moving Averages")
            st.line_chart(hist[columns_to_plot])

            # Returns and volatility chart
            if show_returns or show_volatility:
                st.subheader("Returns & Volatility")
                data = pd.DataFrame()
                if show_returns:
                    data["Returns"] = hist["Returns"]
                if show_volatility:
                    data["Volatility"] = hist["Volatility"]
                st.line_chart(data)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter a valid ticker symbol.")
