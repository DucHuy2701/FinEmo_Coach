import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from core.db import get_db_connection

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
        st.metric("Tổng thu nhập", f"{total_income:,.0f} VND", delta_color="normal")
    with col2:
        st.metric("Tổng chi tiêu", f"{total_expense:,.0f} VND", delta_color="inverse")
    with col3:
        st.metric("Số dư", f"{balance:,.0f} VND", delta_color="normal" if balance >= 0 else "inverse")

    st.subheader("Phân bổ chi tiêu theo danh mục")
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

    if st.button("Export dữ liệu 30 ngày ra CSV"):
        df_export = pd.read_sql_query("""
            SELECT * FROM transactions 
            WHERE date >= date('now', '-30 days')
            ORDER BY date DESC
        """, conn)
        conn.close()
        
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Tải file CSV",
            data=csv,
            file_name=f"finemo_30days_{datetime.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )