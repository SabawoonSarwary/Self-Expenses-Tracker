import sqlite3

# Connect to SQLite database (will create it if it doesn't exist)
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Read schema and execute
with open('schema.sql') as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Database initialized successfully.")
