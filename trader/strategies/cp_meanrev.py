import pandas as pd

from .util import robust_vol

def cp_meanrev(price, window):
    mean = price.rolling(window).mean()
    vol = robust_vol(price)
    signal = mean - price
    return signal / vol.pad()