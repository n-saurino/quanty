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
        return returns.rolling(window).std()


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
    TODO - Add docstring for rolling window 
    """
    r_vol = historical_vol(returns, window=window) * np.sqrt(periods_per_year) 
    return r_vol 

if __name__ == "__main__":
    main()