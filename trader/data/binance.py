from binance import Client
import pandas as pd
import numpy as np
import configparser



class Binance:
    def __init__(self, test=True):
        cfg = configparser.ConfigParser()
        cfg.read(r"../trader/data/config.cfg")
        self.client = client = Client(cfg.get("KEYS", "binance_key", raw=""), cfg.get("SECRETS", "binance_secret", raw=""))

