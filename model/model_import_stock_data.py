***REMOVED***
Imports price and fundemantal data
***REMOVED***
from secrets import api_key

import requests
import pickle

import pandas as pd
import numpy as np

def load_pickle_file(pickle_file_path):
    ***REMOVED***
    Loads pickle file
    ***REMOVED***
    # Load pickled data file
    with open(pickle_file_path, 'rb') as f:
        data = pickle.load(f)

    return data


def get_raw_data(stocks_list, api_key, n_period):
    ***REMOVED***
    Gets raw data and puts in dataframe
    ***REMOVED***
    for stock in stocks_list:
        url = f'https://api.tdameritrade.com/v1/marketdata/{stock}/pricehistory?apikey={api_key}&periodType=month&period={n_period}&frequencyType=daily&frequency=1'
        raw_data = requests.get(url).json()
        raw_data = pd.json_normalize(raw_data, record_path=['candles'])
        raw_data.rename(columns = {'datetime': 'date'}, inplace=True)
        raw_data['date'] = pd.to_datetime(raw_data['date'], unit='ms')
        raw_data['date'] = [raw_data['date'][i].date() for i in range(len(raw_data['date']))]
        raw_data['stock'] = [stock for x in range(len(raw_data))]

    return raw_data


if __name__ == "__main__":
    # Load data file
    data = load_pickle_file('data.pickle')

    # Set Parameters
    N_PERIOD = 3
    API_KEY = api_key
    STOCKS_LIST = list(data['stock'].unique())

    # Bring in raw data
    raw_data = get_raw_data(STOCKS_LIST, API_KEY, N_PERIOD)

    print(raw_data)