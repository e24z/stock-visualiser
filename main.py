import yfinance as yf

aapl = yf.Ticker("AAPL")

hist = aapl.history(period="1y", interval="1d")

print(hist.head)
