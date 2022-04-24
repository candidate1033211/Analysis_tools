import pandas as pd
import numpy as np
from auxilary import find_best_quote



def intraday_distance_from_bq(df, window="2Min", price_col="price", side_col="side", timestamp_col="timestamp"):
    "Returns distance of arriving orders from the most recent available best quote in a snapshot. the window argument determines the frequency of the snapshots"
    
    distances = []
    best_bid = np.nan
    best_ask = np.nan
    for sample in df.resample(window, on=timestamp_col):
        time = sample[0].time()
        sample = sample[1]
        dist_from_best_bid = sample[sample[side_col] == 1][price_col] - best_bid
        dist_from_best_ask = sample[sample[side_col] == -1][price_col] - best_ask
        dist_from_best_quote = dist_from_best_bid.values.tolist() + dist_from_best_ask.values.tolist()
        dist_from_best_quote = pd.DataFrame({"dist": dist_from_best_quote, "time":time})
        distances.append(dist_from_best_quote)
        best_bid_, best_ask_ = find_best_quote(sample)
        if best_bid_ and best_ask_:
            best_bid = best_bid_
            best_ask = best_ask_
    result = pd.concat(distances, ignore_index=True)
    return result