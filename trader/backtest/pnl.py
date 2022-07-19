import pandas as pd
import numpy as np


def robust_vol(price):
    rets = price.diff()
    vol = rets.ewm(adjust=True, span=20, min_periods=10).std()
    vol[vol < 1e-6] = 1e-6
    vol_min = vol.rolling(min_periods=30, window=100).quantile(0.1)
    vol_min.iloc[0] = 0
    vol_min = vol_min.pad()
    return np.maximum(vol, vol_min)

class PnL:
    def __init__(self, forecast, price, cash=1.0, vol_target=0.2):
        self._cash = cash
        self.price = price
        self.forecast = forecast
        self.vol_target = vol_target
        
        self.pnl = self.get_pnl()
    
    def get_position(self):
        daily_risk_target = self.vol_target / np.sqrt(365)
        daily_cash_vol = daily_risk_target * self.cash
        
        instrument_vol = robust_vol(self.price)
        position = daily_cash_vol / instrument_vol
        
        position = position.reindex(self.forecast.index, method="pad")
        return position * self.forecast
    
    def get_pnl(self):
        pos = self.get_position()
        price_ret = self.price_returns
        pos = pos.reindex(price_ret.index, method="pad")
        rets = pos.shift(1) * price_ret
        rets[pd.isna(rets)] = 0.0
        return rets
    
    @property
    def sharpe(self):
        return self.pnl.mean() / self.pnl.std() * np.sqrt(365)
    
    @property
    def cash(self):
        return pd.Series(self._cash, index=self.price.index)
    
    @property
    def price_returns(self):
        return self.price.pad().diff()

    