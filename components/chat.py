from datetime import datetime
import re
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
            with st.spinner("Coach đang đưa ra lời khuyên..."):
                response = response_chain.invoke({
                    "user_input": user_input,
                    "finance_summary": finance_summary
                })
                full_response = response.content

                saved_count = 0
                if re.search(r'\d+[.,]?\d*', user_input):
                    try:
                        parsed_output = parse_chain.invoke({"user_input": user_input})
                        print("Structured parsed:", parsed_output)

                        if parsed_output.has_transaction and parsed_output.transactions:
                            today_str = datetime.today().strftime('%Y-%m-%d')
                            
                            for tx in parsed_output.transactions:
                                if tx.date.lower() in ["hôm nay", "today", "ngày hôm nay", "2026-02-26"]:
                                    tx.date = today_str
                                
                                conn_local = sqlite3.connect('finemo.db')
                                c_local = conn_local.cursor()
                                c_local.execute('''
                                    INSERT INTO transactions (date, amount, category, type, description)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (
                                    tx.date,
                                    tx.amount,
                                    tx.category,
                                    tx.type,
                                    tx.description
                                ))
                                conn_local.commit()
                                conn_local.close()
                            saved_count = len(parsed_output.transactions)
                            full_response += f"\n\n(Đã tự động ghi nhận {saved_count} giao dịch từ tin nhắn!)"
                    except Exception as e:
                        print("Structured parse error:", str(e))

                st.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})