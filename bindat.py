from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df
import pandas as pd
import binkeys as bk

def dataset(sym, intrvl, sr, er):
    client = Client(api_key=bk.Akey, api_secret=bk.Skey)
    candles = client.futures_historical_klines(
        symbol=sym,
        interval=intrvl, # can play with this e.g. '1h', '4h', '1w', etc.
        start_str=sr,
        end_str=er
        )
    candles_data_frame = df(candles)

    candles_data_frame_date = candles_data_frame[0]

    final_date = []

    for time in candles_data_frame_date.unique():
        readable = datetime.fromtimestamp(int(time/1000))
        final_date.append(readable)

    candles_data_frame.pop(0)
    candles_data_frame.pop(11)

    dataframe_final_date = pd.DataFrame(final_date)

    dataframe_final_date.columns = ['Date']

    final_dataframe = candles_data_frame.join(dataframe_final_date)

    final_dataframe.set_index('Date', inplace=True)
    final_dataframe =final_dataframe.iloc[:,:4]
    final_dataframe.columns = ['Open', 'High', 'Low', 'Close']
    final_dataframe = final_dataframe.astype(str).astype(float)   
    return final_dataframe
