import pandas as pd
import numpy as np

from .util import robust_vol

def ewmac(price, l, s, vol_days = 20):
    fast_ewma = price.ewm(span=l).mean()
    slow_ewma = price.ewm(span=s).mean()
    raw_ewmac = fast_ewma - slow_ewma
    vol = robust_vol(price, vol_days)
    return raw_ewmac / vol.ffill()




