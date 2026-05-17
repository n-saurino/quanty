import pandas as pd
from numpy.polynomial import Polynomial
from core.CurveShape import CurveShape


def main():
    return 0

def forward_price(spot: float, rate: float, storage_cost: float, T: float):
    """
    No-arbitrage formula: F = S + (r + c) * S * T
    """
    f_price = spot + (rate + storage_cost) * spot * T

    return f_price

def roll_yield(near_price: float, far_price: float, days_to_roll: float=30) -> float:
    annualize_factor = 365/days_to_roll
    r_yield =  (near_price - far_price) / near_price
    annualized_r_yield = r_yield * annualize_factor

    return annualized_r_yield

def curve_shape(prices: pd.Series, threshold: float = 0.001) -> CurveShape:
    x = range(len(prices))
    coefs = Polynomial.fit(x, prices.values, 1).convert().coef
    # coefs[0] = intercept, coefs[1] = slope
    slope = coefs[1]
    normalized_slope = slope/prices.mean()

    if normalized_slope > threshold:
        return CurveShape.CONTANGO 
    elif normalized_slope < -threshold:
        return CurveShape.BACKWARDATION
    else:
        return CurveShape.FLAT

if __name__ == "__main__":
    main()