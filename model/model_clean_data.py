"""
Clean data and prep for modeling
"""
import pandas as pd
import numpy as np
import pickle


def import_data(file_path):
    """
    Imports csv file
    """
    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'])

    return data

def add_column(data, column_name, column):
    """
    Adds column to dataframe
    """
    data[column_name] = column

    return data

def drop_not_unique_columns(data, columns_list):
    """
    Searches column_list for columns with 1 unique value.
    Drops column if True
    """
    for column in columns_list:
        if data[column].nunique() <= 1:
            data.drop(column, axis=1, inplace=True)

    return data


if __name__ == "__main__":

    data = import_data('../historic_sentiment_analysis.csv')

    # Encode 1 for true and 0 for false
    data = add_column(data, 'paysDiv', np.where(data['divAmount'] > 0, 1, 0))

    # Drop remainder of dividend columns
    data.drop(
        [
            'divYield', 'divDate', 'dividendYield', 'dividendAmount', 'dividendDate', 'dividendPayDate', 'divGrowthRate3Year'
        ], axis=1, inplace=True
    )   

    # Drop identifiers, duplicates or empty coolumns
    data.drop(
        [
            'cusip', 'assetType', 'description', 'assetMainType', 'symbol', 'securityStatus', 'symbol.1', 'bidTick', 'exchangeName', 'peRatio.1'
        ], axis=1, inplace=True
    )

    # Drop columns with 1 unique value
    columns_list = list(data.columns)
    data = drop_not_unique_columns(data, columns_list)

    # Make sure there are not NaN values
    print("Number of NaN values: ", data.isna().sum().sum())

    # Pickle the data
    with open("data.pickle", 'wb') as f:
        pickle.dump(data, f)
