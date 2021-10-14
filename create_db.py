import sqlite3, secrets

# Connect to database
connection = sqlite3.connect(secrets.DB_FILE_PATH)

# Create cursor object
cursor = connection.cursor()

# Execute SQL commands
cursor.execute(***REMOVED***
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        marginable NOT NULL,
        shortable NOT NULL,
        status NOT NULL,
        tradable NOT NULL
    )
***REMOVED***)

cursor.execute(***REMOVED***
    CREATE TABLE IF NOT EXISTS daily_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL,
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
***REMOVED***)

cursor.execute(***REMOVED***
    CREATE TABLE IF NOT EXISTS sentiment (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        bearish REAL,
        neutral REAL,
        bullish REAL,
        compound REAL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
***REMOVED***)

cursor.execute(***REMOVED***
    CREATE TABLE IF NOT EXISTS fundamentals (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
***REMOVED***)

connection.commit()