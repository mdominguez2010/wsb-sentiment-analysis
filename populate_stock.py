# import sqlite3, secrets
# import pandas as pd
# import requests
# import time

# # Connect to sqlite db
# connection = sqlite3.connect(secrets.DB_FILE_PATH)
# connection.row_factory = sqlite3.Row
# cursor = connection.cursor()

# # Make a list of all stock symbols and their name from current db
# cursor.execute("""
#     SELECT symbol, name FROM stock
# """)

# rows = cursor.fetchall()
# symbols = [row['symbol'] for row in rows]

# # Establish list of assets to iterate through
# tickers = pd.read_csv('tickers.csv')

# # Last Sale column is an object, let's convert to float
# tickers['Last Sale'] = tickers['Last Sale'].str.replace('$', '')
# tickers['Last Sale'] = pd.to_numeric(tickers['Last Sale'], downcast='float')
# type(tickers['Last Sale'][0])

# # Filter out stocks >$3 and > $100 million cap
# price_filter = tickers['Last Sale'] >= 3.00
# cap_filter = tickers['Market Cap'] >= 100000000

# # Make set of unique symbols
# assets = list(set(tickers[(price_filter) & (cap_filter)]['Symbol']))
# print(assets[:10])

# # Make Alpha Vantage API call in chunks
# for asset in assets[0:3]:
#     url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={asset}&apikey={secrets.API_KEY_ALPHA_VANTAGE}'
#     r = requests.get(url)
#     data = r.json()
#     print(data)

# for asset in assets:
#     try:
#         if asset not in symbols:
#             url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={asset}&apikey={secrets.API_KEY_ALPHA_VANTAGE}'
#             r = requests.get(url)
#             data = r.json()
#             cursor.execute(
#                 "INSERT INTO stock (symbol, name, industry, fiscalYearEnd) VALUES (?, ?, ?, ?)",
#                 (asset, data['Name'], data['Sector'], data['Industry'])
#                 )
#             print("Added a new stock: ", asset, data['Name'])
#     except Exception as e:
#         print(asset)
#         print(e)


# print(f"{data['Symbol']}, {data['Name']}, {data['Sector']}, {data['Industry']}")

# connection.commit()

'''
Populates and updates db when run.
Searches our current db for symbols already existing,
adds new symbols and their company names
'''
import sqlite3
import alpaca_trade_api as tradeapi
import secrets

connection = sqlite3.connect(secrets.DB_FILE_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stock
""")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

api = tradeapi.REST(secrets.APCA_API_KEY_ID, secrets.APCA_API_SECRET_KEY, base_url=secrets.APCA_API_BASE_URL)
assets = api.list_assets()
new_count = 0

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and len(asset.symbol) <= 4 and asset.symbol not in symbols:
            cursor.execute(
                "INSERT INTO stock (symbol, name, marginable, shortable, status, tradable) VALUES (?, ?, ?, ?, ?, ?)",
                (asset.symbol, asset.name, asset.marginable, asset.shortable, asset.status, asset.tradable)
            )
            print("Added a new stock: ", asset.symbol, asset.name)
            new_count += 1
    except Exception as e:
        print(asset.symbol)
        print(e)

print("\nTotal new stocks added: ", new_count, '\n')

connection.commit()
