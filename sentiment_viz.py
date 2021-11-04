"""
Visualizes the sentiment data
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def import_data(file_path):
    """
    Loads spreadsheet from a file into a dataframe object
    Cleans data column
    """
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

def trend_data(TREND_LENGTH):
    '''
    Input: integer for desired trend length (n_days)
    Output: dataframe with current n_days of trending data
    '''
    max_length = len(stock_data['date'].unique())

    try:
        return pd.concat(
        [stock_data[stock_data['date'] == stock_data['date'].unique()[-TREND_LENGTH:][i]] for i in range(TREND_LENGTH)]
        )
    except IndexError:
        print(f"The max trend length is {max_length} days! Please try again with a smaller trend length\n")

def trending_stocks(TREND_LENGTH):
    '''
    Input: desired length of trend (n_days)
    Output: List of stocks that appear in last n_days sentiment analysis
    '''
    trending_stocks_idx = np.where(trending_data['stock'].value_counts().values == TREND_LENGTH)

    return list(trending_data['stock'].value_counts().iloc[trending_stocks_idx].index)

def average_sentiment(trending_data, sentiment_type='Total_Compound'):
    '''
    Input: dataframe of trending data, sorted by desired sentiment_type
    Output: same dataframe, sorted by desired sentiment type, descending (displays top 5 stocks only)
    '''
    global summary_data # declare global variable
    
    print(f"Top 5 {sentiment_type.lower()} sentiments are: \n")
    summary_data = trending_data.groupby(['stock']).mean()[['Bullish', 'Bearish', 'Total_Compound']].reset_index()
    summary_data.sort_values(by=sentiment_type, ascending=False, inplace=True)
    print(summary_data.head())

def plot_average_sentiment():
    fig = go.Figure(data = [
        go.Bar(name='Bullish', x=summary_data.head()['stock'], y=summary_data.head()['Bullish']),
        go.Bar(name='Bearish', x=summary_data.head()['stock'], y=summary_data.head()['Bearish']),
        go.Bar(name='Total_Compound', x=summary_data.head()['stock'], y=summary_data.head()['Total_Compound'])
    ])

    fig.update_layout(title=f'Top Bullish Stocks Over Last 5 Days',
        xaxis_title='Ticker',
        yaxis_title='Avg Sentiment Score')

    fig.show()


########## Program Parameters ##########
TREND_LENGTH = 5
SENTIMENT_LIST = ["Bullish", "Bearish", "Total_Compound"]
#######################################


stock_data = import_data("./data/historic_sentiment_analysis.csv")
n_days_analyzed = len(stock_data['date'].unique())
print(f"Total days analyzed: {n_days_analyzed}")

trending_data = trend_data(TREND_LENGTH)
trending = trending_stocks(TREND_LENGTH)

average_sentiment(trending_data, sentiment_type=SENTIMENT_LIST[2])
plot_average_sentiment()