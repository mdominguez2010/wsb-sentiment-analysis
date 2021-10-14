"""
Populates prices and updates app.db
"""

import sqlite3
import alpaca_trade_api as tradeapi
import secrets

# Connect to database
connection = sqlite3.connect(secrets.DB_FILE_PATH)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Select all stocks to reference from stock table
cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

# Keep track of id (referenced in stock table)
symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(secrets.APCA_API_KEY_ID, secrets.APCA_API_SECRET_KEY, base_url=secrets.APCA_API_BASE_URL)

# Make api calls in chunks
chunk_size = 50
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    barsets = api.get_barset(symbol_chunk, '1D', limit=1000)
    for symbol in barsets:
        print(f"processing symbol {symbol}")
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            cursor.execute("""
                INSERT INTO daily_price (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

connection.commit()
