import sqlite3, secrets
import pandas as pd
import requests

# Connect to sqlite db
connection = sqlite3.connect(secrets.DB_FILE_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Make a list of all stock symbols and their name from current db
cursor.execute("""
    SELECT symbol, name FROM stock
""")
rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

# Establish list of assets to iterate through
tickers = pd.read_csv('tickers.csv')

# Last Sale column is an object, let's convert to float
tickers['Last Sale'] = tickers['Last Sale'].str.replace('$', '')
tickers['Last Sale'] = pd.to_numeric(tickers['Last Sale'], downcast='float')
type(tickers['Last Sale'][0])

# Filter out stocks >$3 and > $100 million cap
price_filter = tickers['Last Sale'] >= 3.00
cap_filter = tickers['Market Cap'] >= 100000000

# make set of unique symbols
assets = set(tickers[(price_filter) & (cap_filter)]['Symbol'])

# Make Alpha Vantage API call
######### API CALLS WILL NEED BE MADE IN CHUNKS
for asset in assets:
    try:
        if asset not in symbols:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={asset}&apikey={secrets.API_KEY_ALPHA_VANTAGE}'
            r = requests.get(url)
            data = r.json()
            cursor.execute(
                "INSERT INTO stock (symbol, name, industry, fiscalYearEnd) VALUES (?, ?, ?, ?)",
                (asset, data['Name'], data['Sector'], data['Industry'])
                )
            print("Added a new stock: ", asset, data['Name'])
    except Exception as e:
        print(asset)
        print(e)


# print(f"{data['Symbol']}, {data['Name']}, {data['Sector']}, {data['Industry']}")

connection.commit()
