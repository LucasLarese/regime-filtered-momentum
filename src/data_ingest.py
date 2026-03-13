import pandas as pd
from pandas_datareader import data as pdr

from src.config import CFG


def load_ohlcv(symbol: str = CFG.symbol, start: str = CFG.start) -> pd.DataFrame:
    df = pdr.DataReader(symbol, CFG.source, start=start)
    df = df.sort_index()
    df.index = pd.to_datetime(df.index)
    return df