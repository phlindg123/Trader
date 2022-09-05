import numpy as np
import pandas as pd

def breakout(price, lookback=10, smooth=None):
    if smooth is None:
        smooth = max(int(lookback / 4.0), 1)

    assert smooth < lookback

    roll_max = price.rolling(
        lookback, min_periods=int(min(len(price), np.ceil(lookback / 2.0)))
    ).max()
    roll_min = price.rolling(
        lookback, min_periods=int(min(len(price), np.ceil(lookback / 2.0)))
    ).min()

    roll_mean = (roll_max + roll_min) / 2.0

    # gives a nice natural scaling
    output = 40.0 * ((price - roll_mean) / (roll_max - roll_min))
    smoothed_output = output.ewm(span=smooth, min_periods=np.ceil(smooth / 2.0)).mean()
    #smoothed_output[smoothed_output < 0] = 0
    return smoothed_output