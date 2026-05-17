import pandas as pd
import numpy as np
import yfinance as yf
from core.returns import log_returns

def main():
    data = yf.download(tickers="CL=F", period='5y')

    # cleaning the columns
    price_series = data['Close']
    price_series = price_series['CL=F']

    # resets date index to be row number and breaks date out as column in df
    # priceSeries = priceSeries.reset_index(0)

    price_series.name = "Price"

    # calculate log returns
    l_returns = log_returns(price_series)

    # calculate historical vol
    h_vol = historical_vol(l_returns)
    print(f"Historical volatility: {h_vol:.2%}")

    # calculate annualized vol
    a_vol = annualized_vol(l_returns)
    print(f"Annualized volatility: {a_vol:.2%}")

    #calculate rolling vol
    r_vol = rolling_vol(l_returns, 23)
    r_vol.name = "Rolling Vol"
    print(r_vol)

    return 0
    
def historical_vol(returns: pd.Series, window=None) -> float | pd.Series: 
    """
    Calculates historical volatility (std dev of log returns) for either
    the entire sample or a rolling window set as a parameter
    """
    if window is None:
        return returns.std()
    else:
        return returns.rolling(window).std().rename("Rolling Volatility")


def annualized_vol(returns: pd.Series, periods_per_year=252) -> float:
    """
    Annualizes daily volatility by scaling by sqrt(periods_per_year).
    Use when reporting risk to a trader. Vol is always quoted annualized
    on a desk. 
    """
    a_vol = historical_vol(returns) * np.sqrt(periods_per_year)

    return a_vol

def rolling_vol(returns: pd.Series, window, periods_per_year=252) -> pd.Series:
    """
    Annualizes daily volatility by scaling by sqrt(periods_per_year) for a given
    window size. Returns a series of the annualized vol for different windows
    in the returns series. Helpful for identifying risk and trade sizing for 
    different volatility regimes in the series.
    """
    r_vol = historical_vol(returns, window=window) * np.sqrt(periods_per_year) 
    r_vol.name = "Rolling Annualized Volatility"

    return r_vol 

def ewma_vol(returns: pd.Series, lam: float=0.94) -> pd.Series:
    """
    Calculates the exponentially weighted daily volatility to account for 
    vol regime changes by weighting recent return and vol more heavily than 
    older data in the window
    """
    # preallocate list of variances
    variance = np.zeros(len(returns))

    # seed the first variance value
    variance[0] = returns.var()

    # prev_variance needs to be updated with the variance that we calculate 
    # in this formula for each succeeding calculation
    for i in range(1, len(returns)):
        variance[i] = lam*variance[i-1] + (1-lam)*returns.iloc[i-1]**2

    result = pd.Series(np.sqrt(variance), index=returns.index)

    return result

if __name__ == "__main__":
    main()