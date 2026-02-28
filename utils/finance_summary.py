from datetime import datetime, timedelta
import sqlite3
import pandas as pd
from core.db import get_db_connection

def get_finance_summary(days=30):
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    
    today = datetime.today()
    current_month = today.strftime('%Y-%m')
    since_date = (today - timedelta(days=days)).isoformat()

    df = pd.read_sql_query("""
        SELECT date, amount, category, type
        FROM transactions
        WHERE date >= ?
        ORDER BY date DESC
    """, conn, params=(since_date,))
    conn.close()

    if df.empty:
        return "Hiện chưa có giao dịch nào trong 30 ngày gần đây."

    income = df[df['type'] == 'Thu nhập']['amount'].sum()
    expense = df[df['type'] == 'Chi tiêu']['amount'].sum()
    balance = income - expense

    expense_by_cat = df[df['type'] == 'Chi tiêu'].groupby('category')['amount'].sum().sort_values(ascending=False).head(5)
    cat_summary = "\n".join([f"- {cat}: {amt:,.0f} VND" for cat, amt in expense_by_cat.items()]) or "- Chưa có chi tiêu"

    # Trả về format dễ parse (số ở đầu dòng, không bold để model dễ lấy)
    summary = f"""
        Tổng quan tài chính tháng {current_month} (30 ngày gần nhất):
        Thu nhập: {income:,.0f} VND
        Chi tiêu: {expense:,.0f} VND
        Số dư: {balance:,.0f} VND

        Top chi tiêu:
        {cat_summary}
    """
    return summary.strip()

def extract_numbers(summary_text):
    income = 0
    expense = 0
    balance = 0

    lines = summary_text.split('\n')
    for line in lines:
        line = line.strip()
        if "Thu nhập:" in line:
            try:
                income = float(line.split(':')[1].strip().replace(',', '').replace(' VND', ''))
            except:
                pass
        if "Chi tiêu:" in line:
            try:
                expense = float(line.split(':')[1].strip().replace(',', '').replace(' VND', ''))
            except:
                pass
        if "Số dư:" in line:
            try:
                balance = float(line.split(':')[1].strip().replace(',', '').replace(' VND', ''))
            except:
                pass

    return {
        "income": income,
        "expense": expense,
        "balance": balance,
        "summary_text": summary_text
    }

def get_budget_status():
    current_month = datetime.today().strftime('%Y-%m')
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute("SELECT budget_amount FROM budget WHERE month_year = ?", (current_month,))
    budget_row = c.fetchone()
    if not budget_row:
        return None, 0, 0
    
    budget = budget_row[0]
    
    df_month = pd.read_sql_query("""
        SELECT amount
        FROM transactions
        WHERE type = 'Chi tiêu'
        AND strftime('%Y-%m', date) = ?
    """, conn, params=(current_month,))
    
    total_expense = df_month['amount'].sum()
    percentage = (total_expense / budget * 100) if budget > 0 else 0
    
    conn.close()
    return budget, total_expense, percentage