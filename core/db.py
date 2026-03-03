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

c.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_year TEXT UNIQUE,  -- ví dụ '2026-02'
        budget_amount REAL,      -- ngân sách tháng (VND)
        created_at TEXT          -- ngày tạo
    )
''')
conn.commit()

c.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,          -- "user" hoặc "assistant"
        content TEXT NOT NULL,
        timestamp TEXT DEFAULT (datetime('now', 'localtime'))
    )
''')
conn.commit()

def get_db_connection():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    return conn

def get_cursor(conn):
    return conn.cursor()