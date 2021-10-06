import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pickle

import requests
from secrets import api_key_alpha
import datetime
import time

def make_api_call(params, stock):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey={api_key_alpha}'
    r = requests.get(url, params=params)
    data = r.json()

    return data

if __name__ == "__main__":
    STOCK = 'TSLA'
    PARAMS = {
        'function': 'OVERVIEW',
        'symbol': STOCK,
        'apikey': api_key_alpha
    }

    data = make_api_call(params=PARAMS, stock=STOCK)
    print(data)