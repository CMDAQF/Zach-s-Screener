import pandas as pd
import yfinance  as yf #pip install yfinance

###########################################   CAN BE CHANGED  #############################################
start= '2021-01-01'
end = '2023-05-31'
###########################################   CAN BE CHANGED  #############################################
# Define the backtest function
def stock_backtester(ticker, start_date, end_date, initial_cash, shares_per_trade):
    # Fetch historical data
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Initialize backtester variables
    cash = initial_cash
    shares_owned = 30
    ticker = []
    trade_log = []
    

    # Loop over each trading day
    for date, row in stock_data.iterrows():
        close_price = row['Close']

        # Example strategy: Buy when the price is low (e.g., less than $200), sell when high (e.g., greater than $300)
        if close_price < 200 and cash >= close_price * shares_per_trade:
            # Buy shares
            shares_bought = shares_per_trade
            cash -= close_price * shares_bought
            shares_owned += shares_bought
            trade_log.append((date, 'Buy', shares_bought, close_price))

        elif close_price > 300 and shares_owned >= shares_per_trade:
            # Sell shares
            shares_sold = shares_per_trade
            cash += close_price * shares_sold
            shares_owned -= shares_sold
            trade_log.append((date, 'Sell', shares_sold, close_price))

    # After the loop, calculate the portfolio value
    portfolio_value = cash + shares_owned * stock_data.iloc[-1]['Close']

    # Create a report
    #trade_log_df
