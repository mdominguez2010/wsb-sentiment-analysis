import shutil
import requests
import pandas as pd
from secrets import client_id

def load_data(df_path):
    """
    Load data from csv into dataframe
    """

    return pd.read_csv(df_path, index_col=0)

# The Quotes api call retrieves ticker information (price, etc.)
# The Fundamentals api call retrieves company information (market cap, p/e ratio, etc.)

def make_api_call(parameters, url):
    """
    Makes api call and returns JSON file
    """

    return requests.get(url = url, params = parameters).json()

def create_dataframe(json_dict):
    """
    Creates and cleans dataframe
    """
    dataframe = pd.DataFrame.from_dict(json_dict, orient='index')
    dataframe.reset_index(inplace=True)
    dataframe.drop('index', axis=1, inplace=True)

    return dataframe

def create_columns(json_dict, stocks_list):
    """
    Create columns, which will be used to create a dataframe
    """
    fund_cols = []
    for column in [x for x in [*json_dict[stocks_list[0]]['fundamental']]]:
        fund_cols.append(column)

    return fund_cols

def append_dataframe(json_dict, stocks_list, dataframe, columns):
    """
    Appends json information to a dataframe
    """
    for stock in stocks_list:
        dataframe = dataframe.append(
            pd.Series(
                json_dict[stock]['fundamental'], index=columns
                ), ignore_index=True
            )

    return dataframe

def combine_dataframe(df1, df2, df3):
    """
    Combined multiple dataframes
    """
    combined_df = pd.concat([df1, df2, df3], axis=1)
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated]

    return combined_df

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


if __name__ == "__main__":

    df = load_data('df.csv')

    # Stocks list
    stocks_list = list(df['stock'])

    # parameters
    parameters_quotes = {
        'apikey': client_id,
        'symbol': stocks_list,
    }

    parameters_fundamental = {
        'apikey': client_id,
        'symbol': stocks_list,
        'projection': 'fundamental'
    }

    # Urls
    quotes_url = f'https://api.tdameritrade.com/v1/marketdata/quotes?apikey={client_id}'
    fundamental_url = f'https://api.tdameritrade.com/v1/instruments?apikey={client_id}'

    data_quotes = make_api_call(parameters_quotes, quotes_url)
    data_fundamental = make_api_call(parameters_fundamental, fundamental_url)

    # Price quotes dataframe
    df_quotes = create_dataframe(data_quotes)

    # Create columns for fundamentals dataframe
    fund_cols = create_columns(data_fundamental, stocks_list)

    # Create dataframe columns for fundamental data
    df_fundamental = pd.DataFrame(columns = fund_cols)

    # Append data to dataframe
    df_fundamental = append_dataframe(data_fundamental, stocks_list, df_fundamental, fund_cols)

    # Combine dataframes
    combined_df = combine_dataframe(df, df_quotes, df_fundamental)

