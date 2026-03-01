import pytest
import sqlite3
from datetime import datetime

@pytest.fixture
def test_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            type TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    yield conn, c
    conn.close()

def test_insert_transaction(test_db):
    conn, c = test_db
    date = datetime.today().strftime('%Y-%m-%d')
    c.execute("INSERT INTO transactions (date, amount, category, type, description) VALUES (?, ?, ?, ?, ?)",
              (date, 500000, "Ăn uống", "Chi tiêu", "ăn phở"))
    conn.commit()
    
    c.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    assert row is not None
    assert row[1] == date
    assert row[2] == 500000
    assert row[3] == "Ăn uống"
    assert row[4] == "Chi tiêu"

def test_delete_transaction(test_db):
    conn, c = test_db
    c.execute("INSERT INTO transactions (date, amount, category, type, description) VALUES (?, ?, ?, ?, ?)",
              ("2026-02-28", 1000000, "Mua sắm", "Chi tiêu", "mua gear"))
    conn.commit()
    
    c.execute("SELECT id FROM transactions ORDER BY id DESC LIMIT 1")
    tid = c.fetchone()[0]
    
    c.execute("DELETE FROM transactions WHERE id = ?", (tid,))
    conn.commit()
    
    c.execute("SELECT * FROM transactions WHERE id = ?", (tid,))
    assert c.fetchone() is None