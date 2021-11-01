# wsb-sentiment-analysis
Stock Sentiment Analysis on r/Wallstreetbets using NLTK Vader

## Data
Reddit API text from subreddits:
  - r/wallstreetbets
  - r/stocks
  - r/investing
  - r/stockmarket

## Files
1. data.py --> program parameters and stock tickers to search
2. main.py --> sentiment score program
3. update-financials.py --> ticker price and fundamental information program
4. workbook.py --> trend visualizer
5. setup.sql --> database setup
7. df.csv --> placeholder for daily top 10 mentioned stocks
8. historic_sentiment_analysis.csv --> the final dataframe, updated daily
9. historic_sentiment_analysis-copy.csv --> a copy of the dataset is made daily

## 'data' folder
1. combined_df.pickle --> final dataset, serialized

## 'model' folder
1.  data.pickle --> serialized data
2. model_clean_data.py --> script to clean dataset prior to modeling
3. model_prep_data.py -->script to preprocess dataset prior to modeling
4. model.ipynb --> The modeling process in full detail
5. price_data.csv --> another stepping stone to arrive to our final dataset