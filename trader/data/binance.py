from binance import Client, enums
import pandas as pd
import numpy as np
import configparser



class Binance:
    def __init__(self, test=True):
        cfg = configparser.ConfigParser()
        cfg.read(r"../trader/data/config.cfg")
        if test:
            self.client = Client(cfg.get("KEYS", "binance_test_key", raw=""), cfg.get("SECRETS", "binance_test_secret", raw=""))
            self.client.API_URL = 'https://testnet.binance.vision/api'
        else:
            self.client = Client(cfg.get("KEYS", "binance_key", raw=""), cfg.get("SECRETS", "binance_secret", raw=""))

    def create_market_order(self, symbol, side, quantity, test=True):
        if side.lower() == "b":
            side = enums.SIDE_BUY
        elif side.lower() == "s":
            side = enums.SIDE_SELL
        if test:
            return self.client.create_test_order(symbol=symbol, side=side, quantity=quantity, type = enums.ORDER_TYPE_MARKET)
        return self.client.create_order(symbol=symbol, side=side, quantity=quantity, type = enums.ORDER_TYPE_MARKET)
    
    def get_account(self, include_zero = False):
        acc = self.client.get_account()
        acc = pd.DataFrame(acc["balances"])
        acc = acc.set_index("asset").free.astype(np.float64)
        if not include_zero:
            acc = acc[acc > 0]
        return acc

    def _get_bars(self, symbol, start, end, interval = "1d", typ="SPOT"):
        if typ.upper() == "SPOT":
            kline_typ = enums.HistoricalKlinesType.SPOT
        elif typ.upper() == "FUTURE":
            kline_typ = enums.HistoricalKlinesType.FUTURES
        bars = self.client.get_historical_klines(symbol=symbol, interval=interval,limit=1000, start_str = str(int(start.timestamp())), end_str=str(int(end.timestamp())), klines_type=kline_typ)
        cols = ["OpenTime","Open", "High","Low","Close","Volume","CloseTime","QuoteVolume","NumTrades","TakerBaseVolume","TakerQuoteVolue","Ignore"]
        df = pd.DataFrame(bars, columns=cols)
        df.OpenTime = pd.to_datetime(df.OpenTime, unit="ms")
        df.CloseTime = pd.to_datetime(df.CloseTime, unit="ms").dt.ceil(interval)
        df = df.drop(columns = ["Ignore"])
        for col, dtype in df.dtypes.items():
            if dtype == "object":
                df[col] = df[col].astype(np.float64)
        df["Return"] = df.Close.pct_change()
        df["Symbol"] = symbol
        return df

    def get_bars(self, symbols, start, end, interval="1d", typ="SPOT"):
        if isinstance(symbols, str):
            symbols = [symbols]
        df = []
        for symbol in symbols:
            bars = self._get_bars(symbol, start, end, interval, typ)
            df.append(bars)
        return pd.concat(df).reset_index(drop=True)

