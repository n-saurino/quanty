import numpy as np
import pandas as pd
from core.CurveShape import CurveShape as cs 
from numpy.polynomial import Polynomial

def main():
    return

class ForwardCurve:
    def __init__(self, curve_dict: dict):
        self.raw_curve = curve_dict 
        self.curve = {}
        for (t, p) in curve_dict.items():
            tenor = self._parse_tenor(t)
            self.curve[tenor] = p

    def _parse_tenor(self, label: str) -> int:
        time_descriptor = label[-1]

        if label == 'spot':
                return 0
        elif time_descriptor == 'M':
            return int(label[:-1])
        elif time_descriptor == 'Y':
            # times 12 because 12 months in a year
            return int(label[:-1])*12
        else:
            raise Exception("Tenor label is not in Months or Years as M or Y")

    def spread(self, tenor1: str, tenor2: str) -> float:
        tenor1 = self._parse_tenor(tenor1)
        tenor2 = self._parse_tenor(tenor2)
        return self.curve[tenor1] - self.curve[tenor2] 

    def curve_shape(self, threshold: float=0.001) -> cs:
        """
        similar logic to core.curve_shape
        """
        x = self.curve.keys() 
        curve_prices = pd.Series(self.curve.values())
        coefs = Polynomial.fit(x, curve_prices, 1).convert().coef
        # coefs[0] = intercept, coefs[1] = slope
        slope = coefs[1]
        normalized_slope = slope/curve_prices.mean()

        if normalized_slope > threshold:
            return cs.CONTANGO
        elif normalized_slope < -threshold:
            return cs.BACKWARDATION
        else:
            return cs.FLAT


def theoretical_futures_price(spot: float, r: float, storage: float, 
                            convenience_yield: float, T: float) -> float:
    """
    returns the theoretical futures price approximation factoring in
    risk-free rate, storage costs, convenience yield and time horizon for 
    futures contract (as a float: 3-month = 3/12 = .25)
    """
    price = spot*np.exp((r+storage-convenience_yield)*T)
    return price

def roll_yield(near_price, far_price, contract_size) -> float:
    """
    returns the dollar yield per contract for contract rolls.
    should return positive dollar-yield for backwardation and negative for
    contango
    """
    dollar_yield = (far_price - near_price)*contract_size
    return -dollar_yield
   
if __name__ == "__main__":
    main()