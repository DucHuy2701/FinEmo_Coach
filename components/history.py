import sqlite3

import streamlit as st
import pandas as pd
from core.db import get_db_connection

def render_history():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    with st.expander("Xem lịch sử giao dịch gần đây", expanded=True):
        st.subheader("Danh sách giao dịch")
        df = pd.read_sql_query("""
            SELECT id, date, amount, category, type, description
            FROM transactions
            ORDER BY date DESC, id DESC
            LIMIT 50
        """, conn)
        
        if df.empty:
            st.info("Chưa có giao dịch nào.")
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
                key="transaction_table"
            )
            
            selected_rows = edited_df[edited_df['select'] == True]
            selected_ids = selected_rows['id'].tolist()
            
            if selected_ids:
                if st.button("Xóa các giao dịch đã chọn", type="primary"):
                    for tid in selected_ids:
                        c.execute("DELETE FROM transactions WHERE id = ?", (tid,))
                    conn.commit()
                    conn.close()
                    st.success(f"Đã xóa {len(selected_ids)} giao dịch!")
                    st.rerun()
            else:
                st.info("Chưa chọn giao dịch nào. Hãy tick cột 'Chọn'.")