import sqlite3
import streamlit as st
from components.sidebar import render_sidebar
from components.history import render_history
from components.dashboard import render_dashboard
from components.chat import render_chat

st.markdown("""
<style>
    /* Khung chat history scrollable */
    .stChatMessageContainer {
        overflow-y: auto !important;
        max-height: calc(100vh - 160px) !important;  /* trừ input + header */
        padding: 1rem 1rem 120px 320px !important;  /* padding-left = width sidebar */
        scrollbar-width: thin;
        scrollbar-color: #444 #1e1e1e;
    }

    /* Input chat cố định dưới cùng, chạm đúng sidebar */
    .stChatInput {
        position: fixed !important;
        bottom: 0 !important;
        left: 320px !important;  /* bắt đầu từ mép phải sidebar */
        right: 0 !important;
        z-index: 999 !important;
        background: #0e1117 !important;
        padding: 1rem 1rem 1rem 1rem !important;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.6) !important;
        border-top: 1px solid #333 !important;
        transition: left 0.3s ease, padding 0.3s ease;
    }

    /* Input box bên trong */
    .stChatInput > div > div > input {
        background: #1e1e1e !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 16px !important;
        height: 52px !important;
    }

    /* Tạo khoảng trống dưới để input không đè tin nhắn */
    .block-container {
        padding-bottom: 120px !important;
        padding-left: 20px !important;  /* khớp sidebar */
        padding-right: 1rem !important;
    }

    /* Sidebar cố định bên trái */
    .stSidebar {
        z-index: 1 !important;
        width: 320px !important;
        background: #111 !important;
    }

    /* Responsive: màn hình nhỏ (sidebar collapse) */
    @media (max-width: 992px) {
        .stChatInput {
            left: 0 !important;  /* full width khi sidebar ẩn */
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .stChatMessageContainer {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-height: calc(100vh - 140px) !important;
        }

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 100px !important;
        }

        .stSidebar {
            width: 100% !important;  /* sidebar full width trên mobile */
            position: relative !important;
        }
    }
</style>
""", unsafe_allow_html=True)

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