# wsb-sentiment-analysis
Stock Sentiment Analysis on r/Wallstreetbets using NLTK Vader
The goal is to use sentiment on reddit to determine if it can be used to predict stock price movements

## Data
Reddit API text from subreddits:
  - r/wallstreetbets
  - r/stocks
  - r/investing
  - r/stockmarket

## Files
- main.py --> sentiment score program
- update-financials.py --> ticker price and fundamental information program
- stocks_to_trade.py --> establishes stock universe
- sentiment_viz.py --> plots top 5 mentioned stocks and their average sentiment scores

## 'data' folder
- df.csv --> splace-holder for the day's sentiment score data
- price_data.pickle --> another stepping stone to arrive to our final dataset
- final_dataset.pickle --> cleaned and processed data, ready for modeling
- historic_sentiment_analysis.csv --> raw data, includes both sentiment scores and historic price data
- setup.sql --> database setup
- tickers.csv --> enormous list of stocks

## 'model' folder
- model.ipynb --> The modeling process in full detail
- model_interpretation.ipynb --> Understanding the model and it's predictors