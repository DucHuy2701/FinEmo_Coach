from datetime import datetime, timedelta
import sqlite3
import pandas as pd
from core.db import get_db_connection

def get_finance_summary(days=30):
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    since_date = (datetime.today() - timedelta(days=days)).isoformat()
    
    df = pd.read_sql_query("""
        SELECT date, amount, category, type
        FROM transactions
        WHERE date >= ?
        ORDER BY date DESC
    """, conn, params=(since_date,))
    
    conn.close()
    
    if df.empty:
        return "Chưa có giao dịch nào trong khoảng thời gian này!"
    
    income = df[df['type'] == 'Thu nhập']['amount'].sum()
    expense = df[df['type'] == 'Chi tiêu']['amount'].sum()
    balance = income - expense
    
    expense_by_cat = df[df['type'] == 'Chi tiêu'].groupby('category')['amount'].sum().sort_values(ascending=False).head(5)
    cat_summary = "\n".join([f"- {cat}: {amt:,.0f} VND" for cat, amt in expense_by_cat.items()])
    
    summary = f"""
Tóm tắt tài chính {days} ngày qua:
- Tổng thu nhập: {income:,.0f} VND
- Tổng chi tiêu: {expense:,.0f} VND
- Số dư: {balance:,.0f} VND
Top chi tiêu:
{cat_summary if cat_summary else "- Chưa có chi tiêu"}
    """
    return summary.strip()