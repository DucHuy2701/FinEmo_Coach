import sqlite3

import streamlit as st
from datetime import datetime
from core.db import get_db_connection
from utils.helpers import format_vnd

def render_sidebar():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    
    st.header("Nhật ký chi tiêu")
    with st.form(key="add_transaction"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Số tiền (VND)", min_value=0.0, step=1000.0, format="%.0f")
        with col2:
            trans_type = st.selectbox("Loại", ["Chi tiêu", "Thu nhập"])
        category = st.selectbox("Danh mục", [
            "Ăn uống", "Giải trí", "Di chuyển", "Nhà cửa", "Tiết kiệm", "Thu nhập lương", "Mua sắm", "Khác"
        ])
        date = st.date_input("Ngày", value=datetime.today())
        description = st.text_input("Ghi chú / Mô tả")
        submitted = st.form_submit_button("Thêm ngay")
        
        if submitted and amount > 0:
            c.execute('''
                INSERT INTO transactions (date, amount, category, type, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (date.isoformat(), amount, category, trans_type, description))
            conn.commit()
            st.success(f"Đã thêm: {format_vnd(amount)} VND - {category} ({trans_type})")
    if st.button("Cập nhật dữ liệu (refresh)"):
        st.rerun()
    
    st.markdown("---")
    st.subheader("Đặt ngân sách tháng")

    current_month = datetime.today().strftime('%Y-%m')

    c.execute("SELECT budget_amount FROM budget WHERE month_year = ?", (current_month,))
    existing_budget = c.fetchone()

    if existing_budget:
        st.info(f"Ngân sách tháng {current_month}: {existing_budget[0]:,.0f} VND")
        if st.button("Chỉnh sửa ngân sách"):
            st.session_state.edit_budget = True
    else:
        st.session_state.edit_budget = True

    if st.session_state.get('edit_budget', False):
        budget_amount = st.number_input("Ngân sách tháng này (VND)", min_value=0.0, step=100000.0, format="%.0f")
        if st.button("Lưu ngân sách"):
            if existing_budget:
                c.execute("UPDATE budget SET budget_amount = ? WHERE month_year = ?", (budget_amount, current_month))
            else:
                c.execute("INSERT INTO budget (month_year, budget_amount, created_at) VALUES (?, ?, ?)",
                        (current_month, budget_amount, datetime.today().isoformat()))
            conn.commit()
            conn.close()
            
            st.success(f"Đã lưu ngân sách tháng {current_month}: {budget_amount:,.0f} VND")
            del st.session_state.edit_budget
            st.rerun()