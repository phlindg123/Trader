from binance import Client
import pandas as pd
import numpy as np
import configparser



class Binance:
    def __init__(self, test=True):
        cfg = configparser.ConfigParser()
        cfg.read(r"../trader/data/config.cfg")
        self.client = client = Client(cfg.get("KEYS", "binance_key", raw=""), cfg.get("SECRETS", "binance_secret", raw=""))

    def _get_bars(self, symbol, start, end, interval = "1d"):
        bars = self.client.get_historical_klines(symbol=symbol, interval=interval,limit=1000, start_str = str(int(start.timestamp())), end_str=str(int(end.timestamp())))
        cols = ["OpenTime","Open", "High","Low","Close","Volume","CloseTime","QuoteVolume","NumTrades","TakerBaseVolume","TakerQuoteVolue","Ignore"]
        df = pd.DataFrame(bars, columns=cols)
        df.OpenTime = pd.to_datetime(df.OpenTime, unit="ms")
        df.CloseTime = pd.to_datetime(df.CloseTime, unit="ms").dt.ceil(interval)
        df = df.drop(columns = ["Ignore"])
        for col, dtype in df.dtypes.items():
            if dtype == "object":
                df[col] = df[col].astype(np.float64)
        df["Symbol"] = symbol
        return df

    def get_bars(self, symbols, start, end, interval="1d"):
        if isinstance(symbols, str):
            symbols = [symbols]
        df = []
        for symbol in symbols:
            bars = self._get_bars(symbol, start, end, interval)
            df.append(bars)
        return pd.concat(df).reset_index(drop=True)

