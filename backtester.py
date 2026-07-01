import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

tickers = [
    'AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'NVDA',       # Tech
    'JPM', 'BAC', 'GS', 'V', 'MA',                        # Financials
    'UNH', 'JNJ', 'PFE', 'ABBV',                          # Healthcare
    'XOM', 'CVX',                                         # Energy
    'PG', 'KO', 'WMT', 'HD',                              # Consumer
    'CAT', 'HON', 'UPS',                                  # Industrials
    'DIS', 'NFLX', 'CMCSA',                               # Media
    'LIN', 'NEE'                                          # Utilities
]



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
n_assets = momentum.notna().sum(axis = 1)
n_positions = (n_assets // 10).clip(lower = 1)

longs = ranks.le(n_positions, axis = 0).astype(int)
shorts = ranks.gt(n_assets - n_positions, axis = 0).astype(int)
portfolio = longs - shorts


# Equal weight each side of the portfolio
weighted_portfolio = portfolio.div(n_positions, axis = 0)

# Shift positions forward one month to avoid lookahead bias
portfolio_returns = (weighted_portfolio.shift(1) * monthly_returns).sum(axis = 1) 

cumulative = (1 + portfolio_returns).cumprod()

# Risk metrics
ann_return = (1 + portfolio_returns).prod() ** (12/len(portfolio_returns)) - 1
ann_vol = portfolio_returns.std() * np.sqrt(12)
sharpe = ann_return / ann_vol

running_max = cumulative.cummax()
drawdown = (cumulative - running_max) / running_max
max_drawdown = drawdown.min()

hit_rate = (portfolio_returns > 0).mean() 
turnover = weighted_portfolio.diff().abs().sum(axis = 1).mean() / 2 # one-sided

print(f"Annualised Return:     {ann_return:.2%}")
print(f"Annualised Volatility: {ann_vol:.2%}")
print(f"Sharpe Ratio:          {sharpe:.2f}")
print(f"Max Drawdown:          {max_drawdown:.2%}")
print(f"Hit Rate:              {hit_rate:.2%}")
print(f"Avg Monthly Turnover:  {turnover:.2%}")


# Benchmark comparison
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