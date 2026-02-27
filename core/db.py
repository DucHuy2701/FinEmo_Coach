import sqlite3

conn = sqlite3.connect('finemo.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amount REAL,
        category TEXT,
        type TEXT,
        description TEXT
    )
''')
conn.commit()

def get_db_connection():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    return conn

def get_cursor(conn):
    return conn.cursor()