import sqlite3
import streamlit as st
from core.llm_chains import response_chain, parse_chain
from utils.finance_summary import get_finance_summary
from core.db import get_db_connection

def render_chat():
    st.title("FinEmo Coach")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if user_input := st.chat_input("Bạn đang cảm thấy thế nào hôm nay? Hay có chi tiêu gì muốn cập nhật không?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        finance_summary = get_finance_summary(days=30)
        with st.chat_message("assistant"):
            with st.spinner("Coach đang suy nghĩ..."):
                response = response_chain.invoke({
                    "user_input": user_input,
                    "finance_summary": finance_summary
                })
                full_response = response.content
                
                try:
                    parsed_output = parse_chain.invoke({"user_input": user_input})
                    if parsed_output.has_transaction and parsed_output.transactions:
                        conn = sqlite3.connect('finemo.db', check_same_thread=False)
                        c = conn.cursor()
                        saved_count = 0
                        for tx in parsed_output.transactions:
                            c.execute('''
                                INSERT INTO transactions (date, amount, category, type, description)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (tx.date, tx.amount, tx.category, tx.type, tx.description))
                            conn.commit()
                            conn.close()
                            saved_count += 1
                        if saved_count > 0:
                            full_response += f"\n\n(Đã tự động ghi nhận {saved_count} giao dịch!)"
                except Exception as e:
                    print("Structured parse error:", str(e))
                
                st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})