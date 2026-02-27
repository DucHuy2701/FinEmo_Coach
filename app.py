import streamlit as st
from components.sidebar import render_sidebar
from components.history import render_history
from components.dashboard import render_dashboard
from components.chat import render_chat

st.set_page_config(page_title="FinEmo Coach", layout="wide")

tab1, tab2, tab3 = st.tabs(["Chat & Lời khuyên", "Lịch sử giao dịch", "Dashboard tài chính"])

with tab1:
    render_chat()

with tab2:
    render_history()

with tab3:
    render_dashboard()

# Sidebar luôn hiển thị
with st.sidebar:
    render_sidebar()