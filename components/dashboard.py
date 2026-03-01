import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from core.db import get_db_connection
from utils.finance_summary import get_budget_status
from utils.helpers import format_vnd

def render_dashboard():
    conn = sqlite3.connect('finemo.db', check_same_thread=False)

    st.subheader("Tổng quan tài chính (30 ngày gần nhất)")

    df = pd.read_sql_query("""
        SELECT date, amount, category, type
        FROM transactions
        WHERE date >= date('now', '-30 days')
        ORDER BY date DESC
    """, conn)

    if df.empty:
        st.info("Chưa có dữ liệu giao dịch trong 30 ngày gần đây để hiển thị dashboard.")
        return

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    total_income = df[df['type'] == 'Thu nhập']['amount'].sum()
    total_expense = df[df['type'] == 'Chi tiêu']['amount'].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tổng thu nhập", format_vnd(total_income), delta_color="normal")
    with col2:
        st.metric("Tổng chi tiêu", format_vnd(total_expense), delta_color="inverse")
    with col3:
        st.metric("Số dư", format_vnd(balance), delta_color="normal" if balance >= 0 else "inverse")

    st.subheader("Phân bổ chi tiêu theo danh mục")
    
    budget, total_expense, percentage = get_budget_status()
    if budget:
        st.metric("Ngân sách tháng", f"{budget:,.0f} VND")
        st.metric("Đã chi", f"{total_expense:,.0f} VND", delta=f"{percentage:.1f}%")
        if percentage > 100:
            st.error("⚠️ VƯỢT NGÂN SÁCH! Cần điều chỉnh ngay.")
        elif percentage > 80:
            st.warning("⚠️ Đã chi hơn 80% ngân sách.")
    
    expense_df = df[df['type'] == 'Chi tiêu']
    if not expense_df.empty:
        fig_pie = px.pie(
            expense_df,
            values='amount',
            names='category',
            title='Tỷ lệ chi tiêu theo danh mục',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, width='stretch')
    else:
        st.info("Chưa có chi tiêu trong 30 ngày.")

    st.subheader("Xu hướng thu/chi theo ngày")
    daily_summary = df.groupby([pd.Grouper(key='date', freq='D'), 'type'])['amount'].sum().unstack().fillna(0)
    daily_summary['Net'] = daily_summary.get('Thu nhập', 0) - daily_summary.get('Chi tiêu', 0)

    if not daily_summary.empty:
        fig_line = px.line(
            daily_summary,
            x=daily_summary.index,
            y=['Thu nhập', 'Chi tiêu', 'Net'],
            title='Xu hướng tài chính 30 ngày',
            labels={'value': 'Số tiền (VND)', 'date': 'Ngày'},
            color_discrete_map={'Thu nhập': '#00CC96', 'Chi tiêu': '#EF553B', 'Net': '#636EFA'}
        )
        fig_line.update_traces(mode='lines+markers')
        st.plotly_chart(fig_line, width='stretch')
    else:
        st.info("Chưa đủ dữ liệu để vẽ biểu đồ xu hướng.")

    st.markdown("---")
    st.subheader("Xuất/Nhập dữ liệu")

    # Export/Import CSV
    if st.button("Xuất toàn bộ dữ liệu ra CSV"):
        conn_export = sqlite3.connect('finemo.db')
        df_export = pd.read_sql_query("""
            SELECT id, date, amount, category, type, description
            FROM transactions
            ORDER BY date DESC
        """, conn_export)
        conn_export.close()

        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Tải file CSV",
            data=csv,
            file_name=f"finemo_all_transactions_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    current_month = datetime.today().strftime('%Y-%m')
    if st.button(f"Xuất dữ liệu tháng {current_month}"):
        conn_export = sqlite3.connect('finemo.db')
        df_month = pd.read_sql_query("""
            SELECT * FROM transactions
            WHERE strftime('%Y-%m', date) = ?
            ORDER BY date DESC
        """, conn_export, params=(current_month,))
        conn_export.close()

        if df_month.empty:
            st.warning("Tháng này chưa có giao dịch nào.")
        else:
            csv_month = df_month.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Tải file CSV tháng này",
                data=csv_month,
                file_name=f"finemo_{current_month}.csv",
                mime="text/csv"
            )

    st.subheader("Nhập dữ liệu từ CSV")
    uploaded_file = st.file_uploader("Chọn file CSV để import", type="csv")

    if uploaded_file is not None:
        try:
            df_import = pd.read_csv(uploaded_file)
            required_columns = ['date', 'amount', 'category', 'type', 'description']
            if not all(col in df_import.columns for col in required_columns):
                st.error("File CSV thiếu một số cột bắt buộc: date, amount, category, type, description")
            else:
                conn_import = sqlite3.connect('finemo.db')
                c_import = conn_import.cursor()
                inserted = 0
                for _, row in df_import.iterrows():
                    # Validate cơ bản
                    if pd.isna(row['amount']) or row['amount'] <= 0:
                        continue
                    if row['type'] not in ["Thu nhập", "Chi tiêu"]:
                        continue
                    if row['category'] not in ["Ăn uống", "Giải trí", "Di chuyển", "Nhà cửa", "Tiết kiệm", "Thu nhập lương", "Mua sắm", "Khác"]:
                        row['category'] = "Khác"

                    c_import.execute('''
                        INSERT INTO transactions (date, amount, category, type, description)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        str(row['date']),
                        float(row['amount']),
                        row['category'],
                        row['type'],
                        str(row['description']) if pd.notna(row['description']) else ""
                    ))
                    inserted += 1
                
                conn_import.commit()
                conn_import.close()
                st.success(f"Đã import thành công {inserted} giao dịch!")
                st.rerun()
        except Exception as e:
            st.error(f"Lỗi khi import file: {str(e)}")