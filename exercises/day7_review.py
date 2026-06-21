"""
Phase 1 Review — Day 7
Quant Trading Sprint

Instructions:
- Implement all code questions directly in this file
- Answer comment/text questions as comments where indicated
- Write answers the way you'd explain them in a desk interview
- No looking at core/ — implement from scratch where asked
"""

import pandas as pd
import numpy as np

# ===========================================================================
# SECTION 1 — Returns & Volatility
# ===========================================================================

# Q1. Implement log_returns(prices) from scratch. No importing from core.
def log_returns(prices: pd.Series) -> pd.Series:
    l_returns = np.log(prices) - np.log(prices.shift(1))
    l_returns = pd.Series(l_returns) 
    l_returns.name = "Log Returns"
    l_returns = l_returns.rename_axis('log_returns')
    return l_returns 


# Q2. Implement annualized_vol(returns, periods_per_year=252) from scratch.
def annualized_vol(returns: pd.Series, periods_per_year: int = 252) -> float:
    vol = returns.std()
    # scales at sqrt(time) because variance scales linearly with time
    annual_vol = vol * np.sqrt(periods_per_year)
    return annual_vol 


# Q3 (comment). You have 60 days of WTI prices. The daily std dev of log returns
#     is 1.4%. What is annualized vol? Is this high or low for crude oil, and why?
#   annualized vol = std dev of log returns * sqrt(# of trading days) 
#   annualized vol = 1.4% * sqrt(252)

# Q4 (comment). Why does vol scale with sqrt(T) and not T? Derive it in one
#     sentence from the i.i.d. assumption.
#   If returns are i.i.d. then variance is the sum of the squared means for 
#   each day of the data. vol is the std dev of the returns which is the 
#   square root of the variance so vol scales with sqrt(T) and variance scales
#   with T.

# ===========================================================================
# SECTION 2 — Distributions & QQ Plots
# ===========================================================================

# Q5 (comment). A return distribution has negative skewness and excess kurtosis
#     of 4. Describe the QQ plot shape vs a normal distribution.
#   The standard normal distribution has kurtosis of 3. Excess kurtosis of 4
#   means that the kurtosis of the distribution is 7 meaning it has extremely
#   fat tails. Negative skewness means the tail on the left of the distribution
#   is long so there are more outcomes in the left of the plot than the standard
#   normal distribution. I think the QQ plot has fat tails on both sides (top and 
#   bottom of the chart bend away from the linear diagonal of the plot). I think
#   the bottom of the QQ plot bends more heavily to the left of the plot due to
#   the skew


# Q6 (comment). Name two reasons the normal distribution fails to model
#     daily equity or commodity returns accurately.
#   The assumption that returns are i.i.d breaks down because returns are not 
#   actually independent when you consider volatility clustering. Volatility 
#   clustering is when volatility of returns persists, defining regimes and 
#   patterns of volatility across a time series.


# Q7 (comment). What is the ES/VaR ratio for a normally distributed loss at 95%
#     confidence? What does a ratio of 1.7x tell you?
#   The ES/VaR ration for a normally distributed loss at 95% is 1.25x. A ratio
#   of 1.7x tells me that the size of a losing days are significantly larger 
#   than the VaR threshold. So the average loss on a losing day that exceeds
#   the threshold is about 70% larger than that threshold value. This means
#   the tails are very fat on the negative return side.

# ===========================================================================
# SECTION 3 — Pandas
# ===========================================================================

# Assume you have a DataFrame `df` with columns: ['date', 'ticker', 'close', 'volume']
# It contains 3 tickers and 2 years of daily data. DatetimeIndex is set.

# Q8. Compute 20-day rolling annualized vol of log returns per ticker.
#     Result should be same shape as input, aligned to original index.
def rolling_vol_per_ticker(df: pd.DataFrame, window: int = 20) -> pd.Series:
    result = df['close']
    result = result.groupby('ticker')['close'].apply(lambda g: log_returns(g)\
                 .rolling(window=window).std()*np.sqrt(252))

    return result 


# Q9. Find all rows where a ticker's daily log return is more than 2 std devs
#     from its own historical mean. Return as a filtered DataFrame.
def find_outlier_returns(df: pd.DataFrame) -> pd.DataFrame:
    # need to iterate through each ticker in the dataframe and calculate a 
    # return column using log_returns(). Then append it to the appropriate 
    # ticker group in the dataframe. Then need to add a filter "outlier" to 
    # check that the return for the ticker > mean + 2 std_devs
    df = df.copy()
    df['return'] = df.groupby('ticker')['close'].apply(log_returns)\
                    .reset_index(level=0, drop=True) 
    mean = df.groupby('ticker')['return'].transform('mean')
    std = df.groupby('ticker')['return'].transform('std')
    outlier = (df['return'] > mean + 2*std) \
                | (df['return'] < mean - 2*std)  
    df = df[outlier]

    return df


# Q10. Resample to weekly. For each ticker compute: last closing price of the
#      week and total log return for the week.
def weekly_summary(df: pd.DataFrame) -> pd.DataFrame:
    df['return'] = df.groupby('ticker')['close'].apply(log_returns)\
                    .reset_index(level=0, drop=True)
    df = df.groupby('ticker').resample('W').agg(
        weekly_return=('return', 'sum'),
        close=('close', 'last')
    )
    return df


# ===========================================================================
# SECTION 4 — SQL
# ===========================================================================

# Table schema: prices(date, ticker, close, volume)

# Q11. Write a SQL query that returns, for each ticker, the single day with
#      the highest volume in the last 90 days.
Q11 = """
    With ranked As(
    Select date,
      ticker,
      close,
      volume,
      ROW_NUMBER() Over (Partition By ticker Order By volume Desc) As rnk
    From prices 
    Where date >= CURRENT_DATE - Interval '90 days'
    )

    Select date, ticker, close, volume
    From ranked
    Where rnk = 1
"""

# Q12. Write a SQL query showing each row's close price alongside the previous
#      trading day's close for the same ticker. Use a window function.
Q12 = """
    Select date,
    ticker,
    close,
    volume,
    Lag(close, 1) Over (Partition By ticker Order By date) As prev_close
    From prices
"""

# Q13. Write a query that ranks tickers by their average daily return over
#      the past 30 days, highest first.
Q13 = """
    With returns As(
        Select date,
        ticker,
        close,
        volume,
        Lag(close, 1) Over (Partition By ticker Order By date) As prev_close
        (close - Lad(close,1) Over (Partition By ticker Order By date)
        /Lag(close, 1) Over (Partition By ticker Order By date) As daily_return
        From prices
        Where date >= CURRENT_DATE - Interval '30 days'
    )

    Select ticker, Avg(daily_return) as avg_daily_return
    From returns
    Group By ticker
    Order By avg_daily_return Desc 
"""

# ===========================================================================
# SECTION 5 — Futures & Forward Curves
# ===========================================================================

# Q14. Implement forward_price(spot, rate, storage_cost, T) from scratch.
def forward_price(spot: float, rate: float, storage_cost: float, T: float) -> float:
    f_price = spot + (rate + storage_cost) * spot * T
    return f_price 


# Q15 (comment). Spot WTI = $85, risk-free = 5%, storage = 2%, T = 0.5 years.
#      What is the no-arbitrage forward price?
#   forward_price = 85 + (.05 + .02) * 85 * 0.5 

# Q16 (comment). Spot = $85, 6-month futures = $82. Contango or backwardation?
#      Compute the annualized roll yield on 25 CL contracts. Give a dollar figure.
#   Backwardation. 
#   annualized roll yield = (spot - future) * num_contracts * contract_size * annualize_ratio      
#   annualized roll yield = (85 - 82) * 25 * 1000 * (365 / 180)

# Q17 (comment). You are long 10 CL contracts. Spot rises $4. What is your P&L?
#   PnL = 10 * 1000 * 4

# ===========================================================================
# SECTION 6 — VaR & ES
# ===========================================================================

# Q18. Implement var_historical(returns, confidence, position_size) from scratch.
def var_historical(returns: pd.Series, confidence: float, position_size: float) -> float:
    # non-parametric: using the actual historical results rather than
    # a distribution
    result = 0.0
    alpha = 1 - confidence
    alpha_quantile = np.quantile(returns, q=alpha)
    result = -alpha_quantile * position_size

    return result 


# Q19. Implement es_historical(returns, confidence, position_size) from scratch.
def es_historical(returns: pd.Series, confidence: float, position_size: float) -> float:
    result = 0
    alpha = 1 - confidence
    alpha_quantile = np.quantile(returns, q=alpha)
    outlier = (returns < alpha_quantile)
    outliers = returns[outlier]
    result = -outliers.mean() * position_size

    return result


# Q20 (comment). Your 1-day VaR at 99% confidence is $95,000.
#      What is your 10-day VaR? What assumption are you making?
#   scaled_VaR = VaR * sqrt(T)
#   scaled_VaR = 95_000 * sqrt(10) ~= 95_000 * 3.1


# Q21 (comment). Why is ES a better risk measure than VaR for setting desk-level
#      risk limits across multiple traders? Name the specific property.
#   Due to the property of subadditivity. This means that ES still gives the 
#   proper incentive for diversification because the total expected risk of 
#   a portfolio of multiple traders must be less than or equal to their 
#   individual risk profiles

# ===========================================================================
# SECTION 7 — GARCH & EWMA
# ===========================================================================

# Q22 (comment). Your GARCH(1,1) parameters: ω=0.000002, α=0.08, β=0.90.
#      Today's vol estimate: 1.5% daily. Today's return: -2.8%.
#      What is tomorrow's variance estimate? What is tomorrow's vol?
#   Alpha is the shock factor (the effect from today's vol on tomorrow's vol)
#   and Beta is the persistence factor (the effect of the long-run vol on 
#   tomorrow's vol). 
#   tomorrow's var estimate = .000002 + (.08 * (-0.028)**2) + (.015**2 * .9)

# Q23 (comment). What is the long-run variance of this GARCH model?
#   the long run variance of the GARCH model is  
#   long_run_variance = w/(1 - alpha - Beta)


# Q24 (comment). When would you use EWMA instead of GARCH, and vice versa?
#   They both seem similar because they weight the past less than the present.
#   EWMA for daily risk monitoring, GARCH for vol forecasting and options work.
#   EWMA has no memory of where vol "should" be, it only tracks recent moves.
#   GARCH knows vol will eventually revert to w/(1-a-B). This mean reversion
#   is key for anything beyond a 1-day horizon.


# ===========================================================================
# SECTION 8 — Probability
# ===========================================================================

# Q25 (comment). Bayes problem:
#      60% of traders on a desk are "good" (40% monthly win rate).
#      40% are "average" (25% monthly win rate).
#      Trader A just had a winning month. What is P(Trader A is good)?
#   Bayes theorem: P(A | B) = (P(A) * P(B | A)) / P(B)
#   P(A | B) = Trader is good given he has a winning month 
#   P(B) = Trader has a winning month = (.6*.4) + (.4*.25)
#   P(A) = Trader is good = .6
#   P(B | A) = trader has a winning month given the trader is good = .4
#   P(A | B) = (.6 * .4) / ((.6*.4) + (.4*.25)) = .24/.34 = .7059 = 70.59%


# Q26 (comment). You roll a fair six-sided die. If the result is >= 4,
#      you collect that dollar amount. If < 4, you collect $1.
#      What is the expected value of this game?


# Q27 (comment). Your GARCH model has alpha=0.05, beta=0.92.
#      A large shock hits today (return = -4%, current vol was 1.2%).
#      Qualitatively describe what happens to your vol estimate over the
#      next 10 days. Which parameter drives the spike? Which drives the decay?
