import sqlite3
import streamlit as st
from components.sidebar import render_sidebar
from components.history import render_history
from components.dashboard import render_dashboard
from components.chat import render_chat

st.set_page_config(page_title="FinEmo Coach", layout="wide")

if st.sidebar.button("🗑️ Xóa toàn bộ lịch sử chat"):
    conn = sqlite3.connect('finemo.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()
    st.session_state.messages = []
    st.success("Đã xóa toàn bộ lịch sử chat!")
    st.rerun()

tab1, tab2, tab3 = st.tabs(["Chat & Lời khuyên", "Lịch sử giao dịch", "Dashboard tài chính"])

with tab1:
    render_chat()

with tab2:
    render_history()

with tab3:
    render_dashboard()

with st.sidebar:
    render_sidebar()