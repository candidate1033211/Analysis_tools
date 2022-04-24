import pandas as pd
import numpy as np

def remove_outliers(df, on=None, dist=1.5):
    """remove outliers from a dataframe based on the mean of a given numeric column"""

    if not on:
        raise ValueError("Please specify which column")
    
    upper_quantile = df[on].quantile(0.75)
    lower_quantile = df[on].quantile(0.25)
    iqr = upper_quantile - lower_quantile
    
    df = df[(df[on] >= lower_quantile - dist * iqr) & (df[on] <= upper_quantile + 1.5 * iqr)]
    
    return df



def find_best_quote(df_slice, price_col="price", side_col="side"):
    """Takes a snapshot of the orderbook in the form of a data frame and returns the best bid ask quote, if present"""
    
    bids = df_slice[df_slice[side_col] == 1] 
    asks = df_slice[df_slice[side_col] == -1]
    bids = bids[price_col].nlargest().to_numpy()
    asks = asks[price_col].nsmallest().to_numpy()
    
    diff = asks[None,:] - bids[:,None]
    indicies = np.where(diff > 0)
    if (not indicies[0].size) and (not indicies[1].size):
        return None, None
    best_bid_idx = indicies[0][0]
    best_ask_idx = indicies[1][0]
    
    best_bid = bids[best_bid_idx]
    best_ask = asks[best_ask_idx]
    return best_bid, best_ask



def random_price(series):
    """returns a random element sampled from a pandas series"""
    if series.empty:
        return np.nan
    else:
        return series.sample(1).values[0]


def bernouli(p):
    result = np.random.choice([1,-1], p=[p, 1-p])
    return result