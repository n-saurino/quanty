import pandas as pd
import numpy as np


def main():
    """
    Used day4_cleaning.ipynb in the week1 notebook to test these methods
    """
    return 0

def detect_missing_dates(df, freq='B'):
    """
    Identify dates that are missing from the expected calendar
    """
    full_range = pd.date_range(start=df.index.min(), end=df.index.max(),
                               freq=freq)
    missing_dates = full_range.difference(df.index)

    return missing_dates 

def detect_stale_prices(df: pd.DataFrame, ticker_col='ticker', 
                        price_col='close', window=2) -> pd.Series:
    """
    Flag rows where the price is identical to the previous day's price for the
    same ticker
    """
    valid_window = df.groupby(ticker_col)[price_col]\
                     .transform(lambda x: x.rolling(window=window).std()) == 0
    result = valid_window.fillna(False)

    return result 

def detect_outliers(df: pd.DataFrame, ticker_col='ticker', price_col='close', 
                    threshold=3.0) -> pd.Series:
    """
    Flag rows where the price deviates more than threshold standard deviations 
    from the rolling mean for that ticker
    """
    df_mean = df.groupby(ticker_col)[price_col]\
                .transform(lambda x: x.mean())
    
    df_std = df.groupby(ticker_col)[price_col]\
               .transform(lambda x: x.std())

    result = abs((df[price_col] - df_mean) / df_std) > threshold 

    return result

if __name__ == "__main__":
    main()