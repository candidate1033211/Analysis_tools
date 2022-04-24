import pandas as pd
from auxilary import remove_outliers, find_best_quote



def intraday_total_volume(df, window="2Min", size_col="size", price_col="price", timestamp_col="timestamp", price_adjusted=True, **kwargs):
    """returns total volume (size) of orders within a snapshot of the orderbook at frequency specified by window"""
    df = df.copy()
    
    if price_adjusted:
        df[size_col] = df[size_col] * df[price_col]
        
    cols = [size_col, timestamp_col]
    df = df[cols]
    
    result = df.resample(window, on=timestamp_col).apply(
             lambda y: y[size_col].sum())
    result = result.reset_index()
    result = result.rename({timestamp_col:"time", 0:"size"}, axis=1)
    result["time"] = result["time"].apply(lambda x: x.time())
    result = remove_outliers(result, on="size", **kwargs)
    result = result.groupby("time", sort=False).apply(lambda x: x["size"].mean())
    result = result.reset_index().rename({0:"size"}, axis=1)
    return result



def intraday_volume_at_bq(df, window="2Min", size_col="size", price_col="price", timestamp_col="timestamp", side_col="side", price_adjusted=True, **kwargs):
    """"Returns intraday volume at the best quote within a snapshot of the orderbook. The frequency of the snapshots is determined by the window variable"""
    df = df.copy()
    
    if price_adjusted:
        df[size_col] = df[size_col] * df[price_col]
    
    volumes = []
    timestamps = []
    for interval in df.resample(window, on=timestamp_col):
        
        timestamp = interval[0].time()
        interval = interval[1]
        best_bid, best_ask = find_best_quote(interval, price_col, side_col)
        
        if best_bid and best_ask:
            best_bid_volume = interval[(interval[side_col] == 1) & (interval[price_col] == best_bid)][size_col].sum()
            best_ask_volume = interval[(interval[side_col] == -1) & (interval[price_col] == best_ask)][size_col].sum()
            volume_at_best_quote = best_bid_volume + best_ask_volume
            volumes.append(volume_at_best_quote)
            timestamps.append(timestamp)
            
    result = pd.DataFrame()
    result["time"] = timestamps
    result["volume"] = volumes
    result = remove_outliers(result, on="volume", **kwargs)
    result = result.groupby("time").apply(lambda x: x["volume"].mean())
    result = result.reset_index()
    result = result.rename({0:"volume"}, axis=1)
    return result