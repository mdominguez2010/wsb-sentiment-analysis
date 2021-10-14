***REMOVED***
Deletes database tables.
Useful when you want to start your db over from scratch
***REMOVED***

import sqlite3
import secrets

connection = sqlite3.connect(secrets.DB_FILE_PATH)
    
cursor = connection.cursor()

cursor.execute(***REMOVED***
    DROP TABLE stock
***REMOVED***)

cursor.execute(***REMOVED***
    DROP TABLE sentiment
***REMOVED***)

cursor.execute(***REMOVED***
    DROP TABLE daily_price
***REMOVED***)

cursor.execute(***REMOVED***
    DROP TABLE fundamentals
***REMOVED***)

connection.commit()

# Delete all stocks from stock database (does NOT delete the database)
# cursor.execute("DELETE FROM stock")