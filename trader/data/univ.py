import pandas as pd


class Universe:
    def __init__(self):

        self.setup()

    def setup(self):
        coins = {
            "btc" : ("Bitcoin", "Transaction"),
            "ltc" : ("Litecoin", "Transaction"),
            "bch" : ("Bitcoin Cash", "Transaction"),
            "xlm" : ("Stellar Lumens", "Transaction"),
            "xrp" : ("Ripple", "Transaction"),

            "eth" : ("Ethereum", "Smart contracts"),
            "sol" : ("Solana", "Smart contracts"),
            "algo" : ("Algorand", "Smart contracts"),
            "avax" : ("Avalanche", "Smart contracts"),
            "ada" : ("Cardano", "Smart contracts"),
            "matic" : ("Polygon", "Smart contracts"),
            "link" : ("Chainlink", "Smart contracts"),

            "uni" : ("Uniswap", "Exchange"),
            "sushi" : ("SushiSwap", "Exchange"),

            "aave" : ("Aave", "Lending"),
            "comp" : ("Compound", "Lending"),
            "yfi" : ("yearn.finance", "Lending"),

            "fil" : ("Filecoin", "Web3"),
            "Mana" : ("Decentraland", "Web3"),
            "axs" : ("Axie Infinity", "Web3"),

            "doge" : ("Dogecoin", "Meme"),
            "shib" : ("Shiba Inu", "Meme")
        }
        self.coins = pd.DataFrame(coins, index = ["Name", "Sector"]).T