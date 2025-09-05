import sqlite3

# Connect to database
conn = sqlite3.connect('./data/authors.db')
print(conn.execute("SELECT sql FROM sqlite_master WHERE type='table';").fetchall())
conn.close()
cursor = conn.cursor()
