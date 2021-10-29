# wsb-sentiment-analysis
Stock Sentiment Analysis on r/Wallstreetbets using NLTK Vader

## Data
Reddit API text from subreddits:
  - r/wallstreetbets
  - r/stocks
  - r/investing
  - r/stockmarket


TDAmeritrade API price information and fundamental data

## Files
1. data.py --> program parameters and stock tickers to search
2. main.py --> sentiment score program
3. update-financials.py --> ticker price and fundamental information program
4. workbook.py --> trend visualizer
5. setup.sql --> database setup
7. df.csv --> placeholder for daily top 10 mentioned stocks
8. historic_sentiment_analysis.csv --> the final dataframe, updated daily
9. historic_sentiment_analysis-copy.csv --> a copy of the dataset is made daily
