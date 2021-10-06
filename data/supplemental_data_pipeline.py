import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pickle

import requests
from secrets import api_key_alpha
import datetime
import time

def make_api_call(api_key, stock):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={stock}&apikey={api_key}'
    r = requests.get(url)
    print(r.status_code)

    return r.json()

def get_list_of_stocks(filepath):
    dataframe = pd.read_csv(filepath)
    list_of_stocks = list(dataframe['stock'].unique())

    return list_of_stocks

if __name__ == "__main__":
    # list_of_stocks = get_list_of_stocks('../historic_sentiment_analysis.csv')

    # for stock in list_of_stocks:
    #     stock_data = make_api_call(api_key = api_key_alpha, stock=stock)

    #     with open(f'./Weekly/{stock}.pickle', 'wb') as f:
    #         pickle.dump(stock_data, f)

    with open('./Weekly/AFRM.pickle', 'rb') as f:
        AFRM_data = pickle.load(f)

    print(AFRM_data)