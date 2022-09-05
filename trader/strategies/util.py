import pandas as pd
import numpy as np

from ..backtest.pnl import PnL

def robust_vol(price, days=20):
    rets = price.diff()
    vol = rets.ewm(adjust=True, span=days, min_periods=10).std()
    vol[vol < 1e-6] = 1e-6
    vol_min = vol.rolling(min_periods=10, window=100).quantile(0.1)
    vol_min.iloc[0] = 0
    vol_min = vol_min.pad()
    return np.maximum(vol, vol_min)


class MultiForecast:
    """
    forecasts - dataframe with columns is strategy_parameters
    prices is series
    """
    def __init__(self, forecasts, price, long_only=True):
        self.forecasts = forecasts
        if long_only:
            self.forecasts = self.forecasts.clip(lower=0)
        self.price = price
        self.long_only = long_only
    
    def get_pnls(self):
        pnls = {}
        for col in self.forecasts.columns:
            forecast = self.forecasts.loc[:, col]
            pnls[col] = PnL(forecast, self.price).pnl
        return pd.concat(pnls, axis=1)

    def combine_simple(self):
        pnls = self.get_pnls()
        stds = 1/ pnls.std()
        w = stds / stds.sum()
        if self.long_only:
            w[w < 0] = 0
            w /= w.sum()
        self.weights = w
        return self.forecasts.dot(w)
    
    def combine(self):
        pnls = self.get_pnls()
        e = np.ones(pnls.shape[1])
        inv = np.linalg.pinv(pnls.cov())
        w = e.dot(inv) / (e.T.dot(inv).dot(e))
        if self.long_only:
            w[w < 0] = 0
            w /= w.sum()
        self.weights = w
        return self.forecasts.dot(w)