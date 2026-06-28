# Momentum Factor Backtest (12-1 Strategy)

A long-short momentum strategy that ranks stocks by past performance 
and tests whether recent winners continue to outperform recent losers.

## What is Momentum Investing?

Momentum investing is based on the idea that stocks that have performed 
well recently tend to continue outperforming, while stocks that have 
performed poorly tend to continue underperforming.

Rather than identifying undervalued companies, momentum investors focus 
on the persistence of market trends — buying recent winners and shorting 
recent losers. This strategy is based on the academic momentum factor 
first documented by Jegadeesh and Titman (1993).

## Methodology

### Data
Historical adjusted price data was downloaded via Yahoo Finance using 
the `yfinance` library. The universe consisted of ten large-cap US stocks:
AAPL, MSFT, GOOG, AMZN, META, TSLA, NVDA, JPM, V, UNH.

Daily prices were resampled to monthly frequency by taking the final 
closing price of each month.

### The 12-1 Momentum Signal
For each stock, the momentum score was calculated as the cumulative 
return over the previous 11 months, skipping the most recent month. 
This gives a signal based on returns from months t-12 to t-2.

The most recent month is excluded because short-term price movements 
tend to exhibit mean reversion, which weakens the signal.

### Portfolio Construction
At the end of each month:
- Stocks were ranked by momentum score
- The top 3 stocks were held long (+1)
- The bottom 3 stocks were held short (-1)
- All other stocks were excluded (0)

### Avoiding Lookahead Bias
Portfolio positions were shifted forward by one month before calculating 
returns. This ensures that momentum signals calculated at the end of 
month t are only applied to returns in month t+1 — reflecting what would 
have been knowable in real time.

## Results

The equity curve tracks the growth of $1 invested in the strategy from 
2018 to 2024. The strategy performed strongly during the post-pandemic 
technology rally, peaking in early 2022 as momentum trends were 
concentrated among a small number of high-growth stocks. Performance 
deteriorated in 2023 as the market rotated and previous winners 
reversed — a well-known weakness of momentum strategies during 
mean-reverting markets.

## Libraries

- `pandas` — data manipulation and time series resampling
- `numpy` — numerical operations
- `matplotlib` — plotting the equity curve
- `yfinance` — downloading historical price data