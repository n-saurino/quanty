"""
Phase 1 Mock Interview — Day 10
Quant Trading Sprint

Instructions:
- Implement all code questions directly in this file
- Answer conceptual/comment questions as comments where indicated
- Write answers the way you'd explain them live in a desk interview
- No looking at core/ — implement from scratch
- For SQL questions, write the query as a string variable

Grading standard: desk interview, not classroom.
A weak answer passes the question. A strong answer closes the door on follow-ups.
"""

import pandas as pd
import numpy as np

# ===========================================================================
# SECTION 1 — Returns & Volatility
# ===========================================================================

# Q1. You have a Series of daily log returns with mean 0.0003 and std 0.014.
#     A trader asks: "What's my annualized vol and what does that imply about
#     the likely daily move range?"
#     (a) Compute annualized vol from the std.
#     (b) Give the ±1σ daily dollar range on a $10M position.
#     Answer in comments. Show your arithmetic.

# (a)
# (b)


# Q2. Implement ewma_vol(returns, lam=0.94) from scratch.
#     - Pre-allocate a numpy array
#     - Seed with returns.var()
#     - Recurse: sigma2[t] = lam * sigma2[t-1] + (1 - lam) * r[t-1]^2
#     - Return a pd.Series with the original index
def ewma_vol(returns: pd.Series, lam: float = 0.94) -> pd.Series:
    pass


# Q3 (comment). Your EWMA model (λ=0.94) and your GARCH(1,1) model (α=0.06, β=0.91)
#     both estimate vol at 1.5% today. A large shock hits: today's return is -3.2%.
#     (a) Compute tomorrow's EWMA variance estimate. What is tomorrow's EWMA vol?
#     (b) Compute tomorrow's GARCH variance estimate (ω=0.000003). What is tomorrow's GARCH vol?
#     (c) Three days from now, which model's vol estimate will be higher, and why?

# (a)
# (b)
# (c)


# ===========================================================================
# SECTION 2 — Risk: VaR & ES
# ===========================================================================

# Q4. Implement parametric_var(annual_vol, confidence, position_size, horizon_days=1).
#     - Convert annual vol to daily vol
#     - Apply the correct z-score for the given confidence level
#     - Scale to the given horizon
#     - Return dollar VaR
#     Hint: use scipy.stats.norm.ppf or hardcode z-scores for 95% and 99%.
def parametric_var(annual_vol: float, confidence: float,
                   position_size: float, horizon_days: int = 1) -> float:
    pass


# Q5 (comment). You run parametric VaR and historical VaR on the same WTI position.
#     Parametric gives $180K. Historical gives $310K.
#     (a) Why might they diverge this much?
#     (b) Which would you report to your risk manager and why?
#     (c) What does a historical ES/VaR ratio of 1.8x tell you?

# (a)
# (b)
# (c)


# Q6 (comment). Your desk has three traders. Individual 1-day VaRs at 99%:
#     Trader A: $500K, Trader B: $300K, Trader C: $200K.
#     The desk's combined VaR is $750K.
#     (a) What property of VaR does this illustrate — and is it good or bad?
#     (b) Would ES show the same behavior? Why?
#     (c) What does the diversification benefit imply about the correlation
#         between the three books?

# (a)
# (b)
# (c)


# ===========================================================================
# SECTION 3 — Pandas: Multi-Ticker Operations
# ===========================================================================

# Assume df with columns: ['ticker', 'date', 'close', 'volume']
# DatetimeIndex is set on 'date'. Three tickers, 2 years of daily data.

# Q7. For each ticker, compute:
#     - 20-day rolling Sharpe ratio (annualized mean return / annualized vol)
#     - Assume 0 risk-free rate for simplicity
#     Result should be same shape as input, aligned to original index.
def rolling_sharpe(df: pd.DataFrame, window: int = 20) -> pd.Series:
    pass


# Q8. For each ticker, flag days where volume is more than 2 std devs above
#     that ticker's rolling 20-day average volume.
#     Return a boolean Series aligned to the original index.
def flag_high_volume_days(df: pd.DataFrame, window: int = 20) -> pd.Series:
    pass


# Q9. Compute the 30-day rolling correlation between each pair of tickers'
#     daily log returns. Return a DataFrame with columns like 'TICKER1_TICKER2'
#     and a DatetimeIndex.
#     (Assume exactly 3 tickers for simplicity.)
def rolling_pairwise_correlation(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    pass


# ===========================================================================
# SECTION 4 — SQL Window Functions
# ===========================================================================

# Table schema: prices(date DATE, ticker VARCHAR, close FLOAT, volume BIGINT)

# Q10. For each ticker, return the date and close price for the day with the
#      single largest daily return (close vs prior close) over the last 6 months.
#      Use a window function. Show: date, ticker, close, daily_return, rank.
Q10 = """

"""


# Q11. For each ticker, compute a 5-day moving average of close price.
#      Then return only the rows where today's close is MORE than 2% above
#      the 5-day moving average. Show: date, ticker, close, moving_avg, pct_above.
Q11 = """

"""


# Q12. Write a query that returns, for each ticker, the 3 highest-volume days
#      in the past year. Include date, ticker, volume, and a rank column.
#      Ties in volume should share a rank.
Q12 = """

"""


# ===========================================================================
# SECTION 5 — Futures, Forward Curves & Roll Yield
# ===========================================================================

# Q13 (comment). WTI spot = $89.40. 1-month futures = $87.20. 3-month futures = $84.50.
#      (a) Is the curve in contango or backwardation?
#      (b) Compute the annualized roll yield rolling from spot to the 1-month contract.
#          You hold 30 CL contracts. Give the dollar roll yield per year.
#      (c) A junior analyst says: "Backwardation means oil prices will fall."
#          Is he right? Correct him precisely.

# (a)
# (b)
# (c)


# Q14 (comment). You are long 20 CL contracts at $89.40. Overnight, a large
#      inventory drawdown report causes spot to gap up $3.80.
#      (a) What is your P&L?
#      (b) The 3-month forward price moves from $84.50 to $86.10.
#          Does the curve steepen or flatten? What does this imply about
#          the market's expectation of near-term supply tightness?

# (a)
# (b)


# ===========================================================================
# SECTION 6 — Options Greeks
# ===========================================================================

# Q15 (comment). You are long 100 at-the-money call options on WTI crude.
#      Delta = 0.50, Gamma = 0.08, Vega = 0.12, Theta = -0.03 (per day).
#      Spot = $89.40.
#      (a) WTI moves up $2 overnight. Estimate your new delta.
#      (b) You are long gamma. What does that mean for your hedging P&L if
#          WTI makes large moves repeatedly over the next week?
#      (c) Implied vol spikes from 32% to 40%. What happens to your position value?
#      (d) One week passes with no movement. Estimate the theta decay cost.

# (a)
# (b)
# (c)
# (d)


# Q16 (comment). A trader says: "I'm short a straddle on natural gas going into
#      the EIA storage report."
#      (a) What is a straddle and what is his position's P&L profile?
#      (b) What is his greek exposure — specifically delta, gamma, and vega?
#      (c) The report comes in with a massive inventory surprise and nat gas
#          moves 8% in 20 minutes. Walk through what happens to his P&L.

# (a)
# (b)
# (c)


# ===========================================================================
# SECTION 7 — Probability
# ===========================================================================

# Q17 (comment). You flip a fair coin repeatedly until you get heads.
#      (a) What is the expected number of flips?
#      (b) What is the probability you need more than 4 flips?
#      Show your work.

# (a)
# (b)


# Q18 (comment). A desk has 5 traders. Each independently has a 40% chance of
#      having a losing day on any given day. What is the probability that on a
#      given day, at least 3 traders have a losing day? Show your work.

#


# Q19 (comment). Bayes problem:
#      A commodity trading firm screens resumes. 70% of applicants who pass
#      the technical screen get offers. 15% of applicants who fail the technical
#      screen somehow get offers anyway (referrals, etc.).
#      30% of all applicants pass the technical screen.
#      You receive an offer. What is the probability you passed the technical screen?
#      Show full setup and arithmetic.

#


# ===========================================================================
# SECTION 8 — Market Reasoning (desk interview style)
# ===========================================================================

# Q20 (comment). The Fed just hiked rates 50bps unexpectedly.
#      Walk through the immediate impact on:
#      (a) A pay-fixed interest rate swap (you pay fixed, receive SOFR)
#      (b) A long WTI crude position
#      (c) A long call option on a 10-year Treasury bond
#      For each: direction of P&L and the key mechanism.

# (a)
# (b)
# (c)


# Q21 (comment). You are a junior trader on a commodities desk. Your senior
#      trader asks: "EIA just reported a 6 million barrel crude inventory draw —
#      much larger than the 2 million barrel consensus. Walk me through
#      what happens in the market over the next 30 minutes."
#      Answer as if you are talking to the senior trader live.

#
