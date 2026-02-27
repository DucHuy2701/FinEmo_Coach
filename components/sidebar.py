import sqlite3

import streamlit as st
from datetime import datetime
from core.db import get_db_connection

def render_sidebar():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    st.header("Nhật ký chi tiêu nhanh")
    
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
            conn.close()
            st.success(f"Đã thêm: {amount:,.0f} VND - {category} ({trans_type})")