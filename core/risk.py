import pandas as pd
import numpy as np
import yfinance as yf
from core.returns import log_returns

def main():
    confidence = .95
    num_contracts = 50
    contract_size = 1000
    horizon_days_scaling = 10

    cl_df = yf.download(tickers='CL=F', period='5y')

    prices = cl_df['Close']
    prices = prices['CL=F']
    spot = float(prices.iloc[-1])
    notional = num_contracts * contract_size * spot
    returns = log_returns(prices=prices)

    var = var_historical(returns=returns, confidence=confidence, position_size=notional)
    print(f"1-day VaR ({confidence:.0%}, ${notional:,.0f} notional): ${var:,.2f}")
    es = es_historical(returns=returns, confidence=confidence, position_size=notional)
    print(f"Expected Shortfall ({confidence:.0%}): ${es:,.2f}")
    scaled = var_scale(var_1day=var, horizon_days=horizon_days_scaling)
    print(f"{horizon_days_scaling:.0f}-day VaR: ${scaled:,.2f}")

    return 0

def var_historical(
        returns: pd.Series, 
        confidence: float, 
        position_size: float) -> float:
    """
    Calculates the non-parametric VaR from our historical returns. Provides
    the loss amount (1-confidence)% of the trading days but not the size of 
    the loss once that threshold is breached. Gives us where the door is but not
    what is on the other side of it (the size of the loss on this day). Helps
    us understand our max expected loss on confidence% of our trading days.
    Non-parametric var using the historical returns and the actual quantile
    instead of a distribution like in the parametric case

    position_size: dollar notional of the position (e.g. num_contracts * 
    contract_size * spot_price)
    """
    if returns.size == 0:
        raise ValueError("Returns must not be empty")

    alpha = 1 - confidence
    alpha_quantile = np.quantile(returns, alpha)
    var = -alpha_quantile * position_size

    return var

def es_historical(
    returns: pd.Series,
    confidence: float,
    position_size: float) -> float:
    """
    Calculates Expected Shortfall. The expected loss for the trading days
    that we exceed VaR based on our confidence interval. This is a 
    subadditive metric and helpful for understanding the scale of our 
    downside risk on losing days

    position_size: dollar notional of the position (e.g. num_contracts * 
    contract_size * spot_price)
    """
    if returns.size == 0:
        raise ValueError("Returns must not be empty")    
    
    var = var_historical(returns, confidence, position_size)
    var_days = (returns * position_size) <= -var
    returns = returns[var_days]
    es = -returns.mean() * position_size

    return es

def var_scale(var_1day: float, horizon_days: float) -> float:
    """
    Scales VaR for a different sized window. mean drops out because it's 
    close to 0. Leaving just the scaling for the std dev which is 
    sqrt(horizon_days) since variance scales linearly with time and vol scales
    at sqrt(time)
    """

    return var_1day * np.sqrt(horizon_days)

if __name__ == "__main__":
    main()