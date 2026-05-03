import yfinance as yf
import pandas as pd
import numpy as np

def main():
    data = yf.download(tickers="CL=F", period='5y')

    # cleaning the columns
    price_series = data['Close']
    price_series = price_series['CL=F']

    # resets date index to be row number and breaks date out as column in df
    # priceSeries = priceSeries.reset_index(0)

    # confirms we are working with a series
    print(isinstance(price_series, pd.Series))

    price_series.name = "Price"

    s_returns = simple_returns(price_series).rename("Simple Returns")
    print(s_returns)

    l_returns = log_returns(price_series).rename("Log Returns")
    print(l_returns)

    return 0


def simple_returns(prices: pd.Series) -> pd.Series:
    """ 
    Calculates simple returns of a pandas price series.
    Appropriate for traders looking to calculate daily PnL.
    """ 
    returns = (prices - prices.shift(1))/prices.shift(1) 
    # similar to returns.pct_change() but without fill_method
    # to forward fill NaNs
    returns = returns.dropna()
    returns.name = "Simple Returns"

    return returns


def log_returns(prices: pd.Series) -> pd.Series:
    """ 
    Calculates log returns of a pandas price series.
    Appropriate for quants looking to do stats modeling.
    """
    returns = np.log(prices/prices.shift(1)) 
    returns = returns.dropna()
    returns.name = "Log Returns"

    return returns

if __name__ == "__main__":
    main()