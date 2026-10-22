from flask import Flask, render_template, request
from model import predict_stock, get_close_prices
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

app = Flask(__name__)

stocks = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Meta": "META",
    "Netflix": "NFLX"
}

def save_dark_chart(close_prices, ticker):
    """Save a dark-themed chart matching the website aesthetic."""
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    prices = list(close_prices)
    x = range(len(prices))

    # Gold line
    ax.plot(x, prices, color='#F5C518', linewidth=2.5, zorder=3)
    ax.fill_between(x, prices, alpha=0.08, color='#F5C518')

    # Trend line
    if len(prices) > 1:
        z = np.polyfit(x, prices, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), '--', color='#00e676', linewidth=1.5, alpha=0.6, label='Trend')

    # Styling
    ax.tick_params(colors='#6e7681', labelsize=9)
    ax.spines['bottom'].set_color('#21262d')
    ax.spines['left'].set_color('#21262d')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(f'{ticker} — Last 30 Days', color='#e8e8e8', fontsize=13, pad=15)
    ax.set_ylabel('Price (USD)', color='#6e7681', fontsize=10)
    ax.yaxis.label.set_color('#6e7681')
    ax.xaxis.label.set_color('#6e7681')
    ax.grid(True, color='#21262d', linewidth=0.5, alpha=0.5)

    plt.tight_layout()
    graph_path = os.path.join("static", "graph.png")
    plt.savefig(graph_path, facecolor='#0d1117', dpi=150)
    plt.close()

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    ticker = None
    error = None
    graph_exists = False

    if request.method == "POST":
        ticker = request.form.get("ticker", "").strip()

        try:
            if ticker == "":
                error = "Please select a company."
            else:
                prediction = predict_stock(ticker)
                close_prices = get_close_prices(ticker, period="1mo")
                save_dark_chart(close_prices, ticker)
                graph_exists = True

        except Exception as e:
            error = f"Something went wrong: {str(e)}"

    return render_template(
        "index.html",
        prediction=prediction,
        stocks=stocks,
        ticker=ticker,
        error=error,
        graph_exists=graph_exists
    )

if __name__ == "__main__":
    app.run(debug=True)
