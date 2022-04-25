from firstMT5 import *
from second2 import *
import ta
import numpy as np
import warnings
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5

warnings.filterwarnings("ignore")
mt5.initialize()

def svm_reg_trading(symbol):

    def feature_engineering(df):
        """Create new variables"""

        #We copy teh dataframe t avoidinterferences in the data
        df_copy = df.dropna().copy()

        #Create the returns
        df_copy["returns"] = df_copy["close"].pct_change(1)

        #Create the SMAs
        df_indicators = ta.add_all_ta_features(
            df, open="open", high="high", low="low", close="close", volume="volume", fillna=True).shift

        dfc = pd.concat((df_indicators, df_copy), axis = 1)

        return dfc.dropna()

    #Import the data
    df = MT5.get_data(symbol, 3500)[["open", "high", "low", "close", "tick_volume"]]

    df.columns = ["open", "high", "low", "close", "volume"]

    dfc = feature_engineering(df)

    #Percentage train set
    split = int(0.99*len(dfc))

    #Train set creation
    x_train = dfc.iloc[:split, 6:dfc.shape[1]-1]
    y_train = dfc[["returns"]].iloc[:split]

    #Test set creation
    x_test = dfc.iloc[split:, 6:dfc.shape[1]-1]
    y_test = dfc[["returns"]].iloc[split:]
        