# Scratch paper for playing with data

from os import set_blocking
import requests
import pandas as pd
import numpy as np
from datetime import date
import plotly.graph_objects as go

# Import data and convert date column to datetime datatype
historic_sentiment_analysis = pd.read_csv('historic_sentiment_analysis.csv')
historic_sentiment_analysis['date'] = pd.to_datetime(historic_sentiment_analysis['date'])
# historic_sentiment_analysis.head()

def plot_sentiment_trends(df = historic_sentiment_analysis):
    '''
    Input: dataframe
    Output: 3 trend graphs (Bullish, Bearish, Neutral)
    '''
    sentiment_list = ['Bullish', 'Bearish', 'Neutral', 'Total_Compound']

    for sentiment in sentiment_list:
        fig = go.Figure()
        for stock in historic_sentiment_analysis['stock'].unique():

            fig.add_trace(go.Line(x=historic_sentiment_analysis[historic_sentiment_analysis['stock'] == stock]['date'],
                                y=historic_sentiment_analysis[historic_sentiment_analysis['stock'] == stock][sentiment],
                                mode='lines',
                                name=f'{stock}'))

        fig.update_layout(title=f'WSB {sentiment} Sentiment',
                        xaxis_title='Date',
                        yaxis_title='Sentiment Score')

        fig.show()

plot_sentiment_trends(historic_sentiment_analysis)