import sqlite3

import pandas as pd

def format_vnd(amount: float | int) -> str:
    """
    Format số tiền VND: 1500000 → "1.500.000"
    """
    if amount is None:
        return "0"
    return f"{int(amount):,}".replace(",", ".")

def load_chat_history():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    df = pd.read_sql_query("""
        SELECT role, content, timestamp
        FROM chat_history
        ORDER BY id ASC
    """, conn)
    conn.close()
    return [{"role": row["role"], "content": row["content"]} for _, row in df.iterrows()]

def save_message(role, content):
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        INSERT INTO chat_history (role, content)
        VALUES (?, ?)
    ''', (role, content))
    conn.commit()
    conn.close()