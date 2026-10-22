import yfinance as yf
from sklearn.linear_model import LinearRegression
import pandas as pd

def get_close_prices(ticker, period="1y"):
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError("No stock data available.")

    close_data = data["Close"]

    # If Close is a DataFrame (for some yfinance outputs), take first column
    if isinstance(close_data, pd.DataFrame):
        close_series = close_data.iloc[:, 0]
    else:
        close_series = close_data

    close_series = close_series.dropna()

    close_prices = [float(x) for x in close_series.tolist()]

    if len(close_prices) == 0:
        raise ValueError("No valid closing prices found.")

    return close_prices

def predict_stock(ticker):
    close_prices = get_close_prices(ticker, period="1y")

    X = [[i] for i in range(len(close_prices))]

    model = LinearRegression()
    model.fit(X, close_prices)

    future_days = [7, 14, 21, 30]
    predictions = {}

    for d in future_days:
        future_index = [[len(close_prices) + d]]
        pred = model.predict(future_index)[0]
        predictions[d] = round(float(pred), 2)

    return predictions