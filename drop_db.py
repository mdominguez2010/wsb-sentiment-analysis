"""
Deletes database tables.
Useful when you want to start your db over from scratch
"""

import sqlite3
import secrets

connection = sqlite3.connect(secrets.DB_FILE_PATH)
    
cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock
""")

cursor.execute("""
    DROP TABLE sentiment
""")

cursor.execute("""
    DROP TABLE daily_price
""")

cursor.execute("""
    DROP TABLE fundamentals
""")

connection.commit()

# Delete all stocks from stock database (does NOT delete the database)
# cursor.execute("DELETE FROM stock")