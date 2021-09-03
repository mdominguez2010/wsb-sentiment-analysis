***REMOVED***
Imports price and fundemantal data
***REMOVED***
from secrets import api_key

import requests
import pickle

import pandas as pd
import numpy as np
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

def load_pickle_file(pickle_file_path):
    ***REMOVED***
    Loads pickle file
    ***REMOVED***
    # Load pickled data file
    with open(pickle_file_path, 'rb') as f:
        data = pickle.load(f)

    return data


def get_raw_data(price_data, stocks_list, api_key, n_period):
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

        # Calc returns
        raw_data['1d-logreturn'] = np.log(raw_data['close'] / raw_data['close'].shift(1))
        raw_data['2d-logreturn'] = np.log(raw_data['close'] / raw_data['close'].shift(2))
        raw_data['5d-logreturn'] = np.log(raw_data['close'] / raw_data['close'].shift(5))

        # Determine direction of return
        raw_data['1d-direction'] = [1 if x > 0 else -1 if x < 0 else 0 for x in raw_data['1d-logreturn']]
        raw_data['2d-direction'] = [1 if x > 0 else -1 if x < 0 else 0 for x in raw_data['2d-logreturn']]
        raw_data['5d-direction'] = [1 if x > 0 else -1 if x < 0 else 0 for x in raw_data['5d-logreturn']]

        # Concat dataframes
        price_data = pd.concat([price_data, raw_data], ignore_index=True)
        price_data = price_data[['date',
                                'stock',
                                'close',
                                '1d-logreturn',
                                '1d-direction',
                                '2d-logreturn',
                                '2d-direction',
                                '5d-logreturn',
                                '5d-direction']]

    return price_data

def calc_direction(price_data):
    ***REMOVED***
    Calc direction for each stock in several intervals
    ***REMOVED***
    price_data['1d-direction'][0] = np.nan
    price_data['2d-direction'][0: 2] = [np.nan for x in price_data['2d-direction'][0: 2]]
    price_data['5d-direction'][0: 5] = [np.nan for x in price_data['5d-direction'][0: 5]]

    price_data['1d-logreturn'] = price_data['1d-logreturn'].shift(1)
    price_data['1d-direction'] = price_data['1d-direction'].shift(1)

    price_data['2d-logreturn'] = price_data['2d-logreturn'].shift(1)
    price_data['2d-direction'] = price_data['2d-direction'].shift(1)

    price_data['5d-logreturn'] = price_data['5d-logreturn'].shift(1)
    price_data['5d-direction'] = price_data['5d-direction'].shift(1)

    price_data.dropna(inplace=True)
    price_data.reset_index(inplace=True)
    price_data.drop('index', axis=1, inplace=True)

    return price_data

def date_match_filter(price_data):
    ***REMOVED***
    Create filter for price_data dataframe
    ***REMOVED***
    return (price_data['date'] >= data['date'].min().date()) & (price_data['date'] <= data['date'].max().date())

def combine_price_data(price_data, data):
    ***REMOVED***
    Combine both dataframes to prep for modeling
    ***REMOVED***
    # Instantiate empty dataframe to create combined dataframe
    column_list = list(price_data.columns) + list(data.columns)
    combined_df = pd.DataFrame(columns=column_list)

    # Iterate through both dataframes to match date and stock and append matching rows into combined_df
    for ind in price_data.index:
        for indx in data.index:
            if price_data['date'][ind] == data['date'][indx] and price_data['stock'][ind] == data['stock'][indx]:
                series_list = [
                    pd.to_datetime(price_data['date'][ind]),
                    price_data['stock'][ind],
                    price_data['close'][ind],
                    price_data['1d-logreturn'][ind],
                    price_data['1d-direction'][ind],
                    price_data['2d-logreturn'][ind],
                    price_data['2d-direction'][ind],
                    price_data['5d-logreturn'][ind],
                    price_data['5d-direction'][ind]] + list(data.iloc[indx])
                combined_df = combined_df.append(pd.Series(
                        series_list,
                        index=column_list
                    ), ignore_index=True)

    # We don't need duplicate 'date' and 'stock' columns anymore
    combined_df = combined_df.iloc[:, 2:]
    combined_df.sort_values(by='date', ignore_index=True, inplace=True)

    return combined_df

def convert_col_dypes(combined_df):
    ***REMOVED***
    Cleans up some of the columns
    ***REMOVED***
    int_list = [
        'bidSize', 'askSize', 'lastSize', 'totalVolume', 'regularMarketLastSize', '1d-direction', 'sharesOutstanding', 'vol1DayAvg', 'vol10DayAvg', 'vol3MonthAvg'
    ]

    for int_ in int_list:
        combined_df[int_] = pd.to_numeric(combined_df[int_])

    return combined_df

if __name__ == "__main__":
    # Load data file
    data = load_pickle_file('data.pickle')

    # Set Parameters
    N_PERIOD = 3
    API_KEY = api_key
    STOCKS_LIST = list(data['stock'].unique())

    # Establish dataframe to concat price data
    price_data = pd.DataFrame()

    # Bring in raw data and perform several calculations
    price_data = get_raw_data(price_data, STOCKS_LIST, API_KEY, N_PERIOD)

    # Calc direction
    price_data = calc_direction(price_data)

    # Filter out the dates to match those of the 'data' dataframe
    filter_ = date_match_filter(price_data)
    price_data = price_data[filter_]
    price_data.reset_index(inplace=True)
    price_data.drop('index', axis=1, inplace=True)

    # Combine dataframes
    combined_df = combine_price_data(price_data, data)

    # Clean columns
    combined_df = convert_col_dypes(combined_df)