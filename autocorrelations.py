import numpy as np
import pandas as pd

def autocorrelation(series, num_lags=50):
    
    n = len(series)
    n = int(np.log10(n))
    lags = np.logspace(0, n, num_lags, dtype=int)
    autocorrelation_values = [0] * num_lags
    for idx in range(num_lags):
        cov = series.cov(series.shift(-lags[idx]))
        autocorrelation_values[idx] = cov
    result = pd.DataFrame()
    result["shifts"] = lags
    result["autocorrelation_values"] = autocorrelation_values
    return result