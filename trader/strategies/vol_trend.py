import pandas as pd
import numpy as np

def vol_trend(price, volume, s, l, v = 20):
    signal = price.ewm(l).mean() - price.ewm(s).mean()
    vol = price.diff().ewm(v).std()
    forecast = signal /vol
    v_signal = volume.rolling(l).mean() - volume.rolling(s).mean()
    v_signal /= volume.diff().ewm(v).std()
    forecast =  forecast * v_signal
    forecast[forecast < 0] = 0
    forecast[forecast > 20] = 20
    return forecast