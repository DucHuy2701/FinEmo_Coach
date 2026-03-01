import sqlite3

import streamlit as st
import pandas as pd
from core.db import get_db_connection
from utils.helpers import format_vnd

def render_history():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    
    st.subheader("Danh sách Thu nhập/Chi tiêu")
    
    col_search, col_type, col_category, col_date_range = st.columns([3, 1.5, 1.5, 2])

    with col_search:
        search_query = st.text_input("Tìm kiếm (mô tả, danh mục, loại...)", placeholder="Tìm 'ăn uống', 'thưởng', '500k'...")

    with col_type:
        filter_type = st.selectbox("Loại", ["Tất cả", "Thu nhập", "Chi tiêu"])

    with col_category:
        filter_category = st.selectbox("Danh mục", ["Tất cả"] + ["Ăn uống", "Giải trí", "Di chuyển", "Nhà cửa", "Tiết kiệm", "Thu nhập lương", "Mua sắm", "Khác"])

    with col_date_range:
        date_range = st.date_input("Khoảng thời gian", value=(), min_value=None, max_value=None)
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = None

    query = "SELECT id, date, amount, category, type, description FROM transactions WHERE 1=1"
    params = []

    if search_query:
        query += " AND (description LIKE ? OR category LIKE ? OR type LIKE ?)"
        like_query = f"%{search_query}%"
        params.extend([like_query, like_query, like_query])

    if filter_type != "Tất cả":
        query += " AND type = ?"
        params.append(filter_type)

    if filter_category != "Tất cả":
        query += " AND category = ?"
        params.append(filter_category)

    if start_date and end_date:
        query += " AND date BETWEEN ? AND ?"
        params.extend([start_date.isoformat(), end_date.isoformat()])

    query += " ORDER BY date DESC, id DESC LIMIT 100"

    df = pd.read_sql_query(query, conn, params=params)

    if df.empty:
        st.info("Không tìm thấy giao dịch nào khớp với bộ lọc.")
    else:
        df['select'] = False

        edited_df = st.data_editor(
            df,
            column_config={
                "select": st.column_config.CheckboxColumn("Chọn", default=False),
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "date": st.column_config.TextColumn("Ngày", disabled=True),
                "amount": st.column_config.NumberColumn("Số tiền (VND)", format="%d"),
                "category": st.column_config.TextColumn("Danh mục"),
                "type": st.column_config.TextColumn("Loại"),
                "description": st.column_config.TextColumn("Mô tả"),
            },
            column_order=["select", "id", "date", "amount", "category", "type", "description"],
            hide_index=True,
            width='stretch',
            num_rows="fixed",
            key="filtered_transaction_table"
        )

        selected_rows = edited_df[edited_df['select'] == True]
        selected_ids = selected_rows['id'].tolist()

        if selected_ids:
            if st.button("Xóa các giao dịch đã chọn", type="primary"):
                conn_local = sqlite3.connect('finemo.db')
                c_local = conn_local.cursor()
                for tid in selected_ids:
                    c_local.execute("DELETE FROM transactions WHERE id = ?", (tid,))
                conn_local.commit()
                conn_local.close()
                st.success(f"Đã xóa {len(selected_ids)} giao dịch!")
                st.rerun()
        else:
            st.info("Chưa chọn giao dịch nào để xóa. Tick cột 'Chọn'.")