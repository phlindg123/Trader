import numpy as np
import pandas as pd

def cp_trend(price):
    p1 = 10
    p2 = 20
    p3 = 60
    s1 = np.sign(price / price.shift(p1) - 1)# * 10.0
    s2 = np.sign(price / price.shift(p2) - 1)# * 10.0
    s3 = np.sign(price / price.shift(p3) - 1)# * 10.0
    s = (s1 + s2 + s3) / 3.0 / price.pct_change().ewm(20, min_periods=10).std()
    s[s < 0] = 0
    s[s > 20] = 20
    return s