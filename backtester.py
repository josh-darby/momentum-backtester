import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'UNH']
raw = yf.download(tickers, start='2018-01-01', end='2024-01-01', auto_adjust=True)
prices = raw['Close']

# Convert daily prices to month-end prices
monthly_prices = prices.resample('ME').last()

# Monthly percentage returns
monthly_returns = monthly_prices.pct_change()

# 12-1 momentum signal (exclude most recent month)
momentum = monthly_returns.shift(1).rolling(11).sum()

# Rank stocks by momentum each month
ranks = momentum.rank(axis = 1, ascending = False)
n = len(tickers)
# Long top 3, short bottom 3
longs = (ranks <= 3).astype(int)
shorts = (ranks > n - 3).astype(int)
portfolio = longs - shorts

#Shift positions forward one month to avoid lookahead bias
portfolio_returns = (portfolio.shift(1) * monthly_returns).sum(axis = 1) 

cumulative = (1 + portfolio_returns).cumprod()

sharpe = (portfolio_returns.mean() / portfolio_returns.std()) * (12 ** 0.5)
print(f"Sharpe Ratio : {sharpe:.2f}")


spy = yf.download('SPY', start='2018-01-01', end='2024-01-01', auto_adjust=True)
spy_monthly = spy['Close'].resample('ME').last()
spy_returns = spy_monthly.pct_change()
spy_cumulative = (1 + spy_returns).cumprod().squeeze()

combined_plot = pd.DataFrame({
    'Momentum Strategy' : cumulative,
    'S&P 500' :spy_cumulative
})

combined_plot.plot(color = ['r', 'g'])

plt.ylabel("Growth of $1")
plt.xlabel("Date")
plt.legend()
plt.title("Momentum Factor Backtest (12-1), 2018-2024")
plt.show()