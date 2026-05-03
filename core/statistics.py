import pandas as pd
import numpy as np
import yfinance as yf
from scipy.stats import chi2 
from core.returns import log_returns

def main():
    data = yf.download(tickers="CL=F", period='5y')

    # cleaning the columns
    price_series = data['Close']
    price_series = price_series['CL=F']

    # resets date index to be row number and breaks date out as column in df
    # priceSeries = priceSeries.reset_index(0)

    price_series.name = "Price"
    l_returns = log_returns(price_series)
    skew = skewness(l_returns)
    k = kurtosis(l_returns)
    excess_k = excess_kurtosis(l_returns)
    jb = jarque_bera(l_returns)

    print(f"Skewness: {skew:.4f}")
    print(f"Kurtosis: {k:.4f}")
    print(f"Excess Kurtosis: {excess_k:.4f}")
    print(f"Jarque Bera: {jb[0]:.4f}, P: {jb[1]:.4f}")
    return 0

def skewness(returns: pd.Series) -> float:
    """
    Calculates the asymmetry of a distribution. Helping a trader identify the 
    ways a returns series may differ from the normal distribution. 

    0 is symmetrical, negative (left) skew, positive (right) skew.

    Larger skew value indicates a heavier tail (returns in this tail are more
    common and larger than the normal distribution)

    Skewness indicates tail risk to for the trader's position.
    """
    n = returns.size
    mean_returns = returns.mean()
    std_returns = returns.std()
    adj_factor = np.sqrt(n*(n-1))/(n-2)
    skew_term = (1/n)*np.sum(((returns - mean_returns)/std_returns)**3)
    fp_skew = adj_factor * skew_term
    return fp_skew

def kurtosis(returns: pd.Series) -> float:
    """
    Calculates a shape descriptor of the distribution (4th standardized moment)
    that indicates fatter/thinner tails.

    Fatter tails will be reflected in QQ plots as convex-concave.

    This method returns the raw kurtosis. Normal distribution has Kurtosis = 3,
    with fatter tails > 3 and thinner tails < 3.

    A VaR model calibrated to normal returns at 99% CI will be breached far more
    often than 1% of the time when kurtosis > 3.

    High kurtosis with negative skewness means fat tails AND the left tail is 
    heavier (larger and more frequent losses often seen in equity returns)
    """
    n = returns.size
    mean_returns = returns.mean()
    std_returns = returns.std()
    k = (1/n)*np.sum(((returns - mean_returns)/std_returns)**4)    

    return k

def excess_kurtosis(returns: pd.Series) -> float:
    """
    Calculates the kurtosis of the distribution relative to the normal 
    distribution (kurtosis = 3). Important for a trader to understand the tail-
    risk of their distribution vs the normal distribution.
    """
    excess_k = kurtosis(returns) - 3

    return excess_k

def jarque_bera(returns: pd.Series) -> tuple[float,float]:
    """
    Tests whether a return series is normally distributed using the Jarque-Bera 
    test.

    Combines skewness and excess kurtosis into a single test statistic to 
    evaluate whether a return distribution departs significantly from normality.
    Use this as the first diagnostic when evaluating whether a normal 
    distribution model is appropriate for a return series.

    The null hypothesis is that the data is normally distributed (skewness = 0 
    and excess kurtosis = 0). A small p-value (< 0.05) means you reject 
    normality and should consider a heavier-tailed model such as a 
    t-distribution. Use excess_kurtosis() and skewness() to diagnose the nature 
    of the departure. JB signals that something is wrong; the other functions 
    tell you what.

    Under the null hypothesis the test statistic follows a chi-squared 
    distribution with 2 degrees of freedom.

    Returns:
        tuple[float, float]: (statistic, p_value)
            - statistic: JB test statistic. Values near 0 indicate normality.
              Large values indicate significant departure from normality.
            - p_value: probability of observing this statistic under the null
              hypothesis of normality. p < 0.05 is the conventional threshold
              for rejecting normality.
    """
    n = returns.size
    constant = n/6
    skew = skewness(returns)
    excess_k = excess_kurtosis(returns)
    jb_stat = constant*(skew**2 + (excess_k**2)/4)
    degrees_of_freedom = 2
    p = chi2.sf(jb_stat, degrees_of_freedom)
    jb = (jb_stat, p)

    return jb 

def estimate_t_dof(returns: pd.Series) -> float | None:
    """
    Calculates the appropriate t-distribution degree of freedom for a non-
    normal distribution
    """
    excess_k = excess_kurtosis(returns) 
    if excess_k <= 0:
        return None

    # v is undefined when excess_kurtosis <= 0
    v = (6/excess_k) + 4

    return v

if __name__ == "__main__":
    main()