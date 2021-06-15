import shutil
import requests
import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt

# Load in df
df = pd.read_csv('df.csv', index_col=0)

# Request info from TD Ameritrade API
client_id = "***REMOVED***"
stocks_list = list(df['stock'])

# The Quotes api call retrieves ticker information (price, etc.)
# The Fundamentals api call retrieves company information (market cap, p/e ratio, etc.)

# parameters
parameters_quotes = {
    'apikey': client_id,
    'symbol': stocks_list,
}

parameters_fund = {
    'apikey': client_id,
    'symbol': stocks_list,
    'projection': 'fundamental'
}

quotes_url = f'https://api.tdameritrade.com/v1/marketdata/quotes?apikey={client_id}'
fundamental_url = f'https://api.tdameritrade.com/v1/instruments?apikey={client_id}'

data_quotes = requests.get(url = quotes_url, params = parameters_quotes).json()
data_fundamental = requests.get(url = fundamental_url, params = parameters_fund).json()

# quotes dataframe
df_q = pd.DataFrame.from_dict(data_quotes, orient = 'index')
df_q.reset_index(inplace=True)
df_q.drop('index', axis=1, inplace=True)

# Establish fund columns for datafrane
fund_cols = []
for column in [x for x in [*data_fundamental[stocks_list[0]]['fundamental']]]:
    fund_cols.append(column)

# Append data to dataframe
df_f = pd.DataFrame(columns = fund_cols)
for stock in stocks_list:
    df_f = df_f.append(pd.Series(data_fundamental[stock]['fundamental'], index=fund_cols), ignore_index=True)

# Combine both dataframes
# Remove duplicates
current = pd.concat([df, df_q, df_f], axis=1)
current = current.loc[:, ~current.columns.duplicated()]

# Before writing our new data to the file, let's make a copy of the file in case something goes wrong
shutil.copyfile('historic_sentiment_analysis.csv', 'historic_sentiment_analysis-copy.csv')

# Read csv
historic_sentiment_analysis = pd.read_csv('historic_sentiment_analysis.csv')
#historic_sentiment_analysis = historic_sentiment_analysis.iloc[:, 1:]

# Remove duplicates
#historic_sentiment_analysis = historic_sentiment_analysis.loc[:, ~historic_sentiment_analysis.duplicated()]

# Update csv
historic_sentiment_analysis = pd.concat([historic_sentiment_analysis, current], axis = 0, ignore_index=True)
historic_sentiment_analysis.to_csv('historic_sentiment_analysis.csv', index=False)


####################################################################################


# current_doubles = []
# for i in range(len(current.T.duplicated())):
#     if current.T.duplicated()[i]:
#         current_doubles.append(i)

# current.iloc[:, 9]
# current.loc[:,'symbol']
# historic_sentiment_analysis.loc[:, 'symbol']
# historic_doubles = []
# for i in range(len(historic_sentiment_analysis.T.duplicated())):
#     if historic_sentiment_analysis.T.duplicated()[i]:
#         historic_doubles.append(i)

# print(len(current_doubles))
# print(len(historic_doubles))