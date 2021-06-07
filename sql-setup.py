# scratch paper to help with db setup

import pandas as pd
import numpy as np

df = pd.read_csv('historic_sentiment_analysis.csv')
df = df.iloc[:, 1:]

for column in df.columns:    
    print(column, 'text,')