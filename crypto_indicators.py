from pymongo import MongoClient
import pandas as pd
import ta  # Import the `ta` library

class CryptoTechnicalIndicators:
    def __init__(self, db_name, collection_name, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.data = None
        self.indicator_df = None

    def load_data(self):
        self.data = pd.DataFrame(list(self.collection.find()))
        
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])
            self.data.set_index('date', inplace=True)
            print("Data loaded successfully from MongoDB.")
        else:
            raise KeyError("The 'date' column is missing in the data.")

    def calculate_indicators(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        self.indicator_df = pd.DataFrame(index=self.data.index)

        # RSI with custom window (e.g., 14 periods)
        self.indicator_df['RSI'] = ta.momentum.RSIIndicator(close=self.data['close'], window=52).rsi()
        
        # MACD with custom short, long, and signal windows
        macd = ta.trend.MACD(close=self.data['close'], window_slow=52, window_fast=26, window_sign=9)
        self.indicator_df['MACD'] = macd.macd()
        
        # CCI with custom window (e.g., 20 periods)
        self.indicator_df['CCI'] = ta.trend.CCIIndicator(high=self.data['high'], low=self.data['low'], close=self.data['close'], window=52).cci()
        
        # ADX with custom window (e.g., 14 periods)
        self.indicator_df['ADX'] = ta.trend.ADXIndicator(high=self.data['high'], low=self.data['low'], close=self.data['close'], window=52).adx()
        
        # ATR with custom window (e.g., 14 periods)
        self.indicator_df['ATR'] = ta.volatility.AverageTrueRange(high=self.data['high'], low=self.data['low'], close=self.data['close'], window=52).average_true_range()
        
        # ROC with custom window (e.g., 12 periods)
        self.indicator_df['ROC'] = ta.momentum.ROCIndicator(close=self.data['close'], window=52).roc()
        
        # Standard Deviation over a custom rolling window (e.g., 20 periods)
        self.indicator_df['Stdev'] = self.data['close'].rolling(window=20).std()

        # Bollinger Bands with custom window and number of standard deviations
        bb = ta.volatility.BollingerBands(close=self.data['close'], window=40, window_dev=2)
        self.indicator_df['Bollinger_High'] = bb.bollinger_hband()
        self.indicator_df['Bollinger_Low'] = bb.bollinger_lband()
        
        # Exponential Moving Average (EMA) with custom window (e.g., 20 periods)
        self.indicator_df['EMA'] = ta.trend.EMAIndicator(close=self.data['close'], window=20).ema_indicator()
        
        # Williams %R with custom window (e.g., 14 periods)
        self.indicator_df['Williams_%R'] = ta.momentum.WilliamsRIndicator(high=self.data['high'], low=self.data['low'], close=self.data['close'], lbp=28).williams_r()
        
        # Momentum with a custom lag (e.g., difference from 10 periods ago)
        self.indicator_df['Momentum'] = self.data['close'].diff(40)

        print("Indicators calculated successfully.")

    def get_indicator_df(self):
        if self.indicator_df is None:
            raise ValueError("Indicators not calculated. Call calculate_indicators() first.")
        
        return self.indicator_df
