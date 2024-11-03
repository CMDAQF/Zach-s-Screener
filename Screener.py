import tkinter as tk
import yfinance as yf
from tkinter import ttk

# Define a function to fetch stock data
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="2d")  # Fetch the last 2 days of data for price change
        price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        price_change = price - prev_close
        percent_change = (price_change / prev_close) * 100
        return price, price_change, percent_change
    except Exception as e:
        return None, None, None

# Define a function to update the stock data in the GUI
def update_stock_data(tickers):
    for ticker, tile in tiles.items():
        price, price_change, percent_change = fetch_stock_data(ticker)
        if price is not None:
            # Update the tile text with current price, price change, and percent change
            tile['text'] = (f"{ticker}\n"
                            f"Price: ${price:.2f}\n"
                            f"Change: ${price_change:.2f}\n"
                            f"% Change: {percent_change:.2f}%")
            # Change the tile background color based on price change
            if price_change > 0:
                tile.config(background="green")  # Stock price is up
            elif price_change < 0:
                tile.config(background="red")    # Stock price is down
            else:
                tile.config(background="gray")   # No change in stock price
        else:
            tile['text'] = f"{ticker}\nData not available"
            tile.config(background="black")  # Default to black if data is unavailable
    root.after(5000, lambda: update_stock_data(tickers))  # Refresh data every 5 seconds

# Define a function to create stock tiles
def create_stock_tiles(root, tickers):
    global tiles
    tiles = {}
    row = 0
    col = 0

    for ticker in tickers:
        frame = ttk.Frame(root, borderwidth=2, relief="groove", padding=(10, 10))
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        tile = ttk.Label(frame, text=f"{ticker}\nLoading...", font=("Arial", 12), justify="center")
        tile.pack(fill=tk.BOTH, expand=True)

        tiles[ticker] = tile

        # Arrange tiles in a grid (e.g., 4 tiles per row)
        col += 1
        if col > 3:
            col = 0
            row += 1

    # Configure grid rows and columns to expand proportionally
    for i in range(row + 1):
        root.grid_rowconfigure(i, weight=1)
    for j in range(4):  # Assuming 4 columns
        root.grid_columnconfigure(j, weight=1)

# Define the list of stock tickers
tickers = ["TQQQ", "SQQQ", "FNGU", "QUBT"]

# Create the GUI window
root = tk.Tk()
root.title("Stock Screener")
root.configure(bg="black")  # Set the background of the window to black
root.geometry("600x400")

# Create tiles for each stock
create_stock_tiles(root, tickers)

# Start updating stock data
update_stock_data(tickers)

# Run the GUI main loop
root.mainloop()
