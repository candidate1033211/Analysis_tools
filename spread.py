import pandas as pd 
import numpy as np
from auxilary import find_best_quote


def intraday_spread_bq(df, window="2Min", price_col="price", side_col="side", timestamp_col="timestamp", tick=0.1):
    """Takes an order book as a pandas dataframe and returns the bid ask spread at the best quote in a snapshot of the order book at a rate specified by the variable window"""
    
    spreads = []
    timestamps = []
    
    for sample in df.resample(window, on=timestamp_col):
        timestamp = sample[0].time()
        interval = sample[1]
        best_bid, best_ask = find_best_quote(interval, price_col, side_col)
        if best_bid:
            spread = best_ask - best_bid
            spreads.append(spread)
            timestamps.append(timestamp)
            
    result = pd.DataFrame()
    result["spread"] = spreads
    result["time"] = timestamps
    result = result.groupby("time").apply(lambda x: x["spread"].mean())
    result = result.reset_index()
    result = result.rename({0:"spread"}, axis=1)
    return result