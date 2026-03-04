from datetime import datetime
import re
import sqlite3
import streamlit as st
from core.llm_chains import response_chain, parse_chain, emotion_chain, classify_chain
from utils.finance_summary import extract_numbers, get_budget_status, get_finance_summary
from core.db import get_db_connection
from utils.helpers import load_chat_history, save_message

def render_chat():
    st.title("FinEmo Coach")
    
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if user_input := st.chat_input("Bạn đang cảm thấy thế nào hôm nay? Hay có chi tiêu gì muốn cập nhật không?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        save_message("user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)
        
        finance_summary = get_finance_summary(days=30)
        with st.chat_message("assistant"):
            with st.spinner("Coach đang phân tích..."):
                
                finance_summary_text = get_finance_summary(days=30)
                finance_data = extract_numbers(finance_summary_text)
                
                response = response_chain.invoke({
                    "user_input": user_input,
                    "finance_summary": finance_summary,
                    "income": finance_data["income"],
                    "expense": finance_data["expense"],
                    "balance": finance_data["balance"]
                })
                full_response = response.content
                
                try:
                    emotion = emotion_chain.invoke({"user_input": user_input}).content.strip().lower()
                    if emotion not in ["vui", "buồn", "stress", "tiếc nuối", "impulsive", "bình thường", "khác"]:
                        emotion = "khác"
                    
                    emotion_display = {
                        "vui": "Vui vẻ",
                        "buồn": "Buồn bã",
                        "stress": "Stress",
                        "tiếc nuối": "Tiếc nuối",
                        "impulsive": "Bốc đồng",
                        "bình thường": "Bình thường",
                        "khác": "Khác"
                    }.get(emotion, "Khác")
                    
                    full_response += f"\n\n**Cảm xúc của bạn hôm nay**: {emotion_display}"
                except Exception as e:
                    print("Emotion detection error:", str(e))

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
                                
                                try:
                                    suggested_category = classify_chain.invoke({"description": tx.description}).content.strip()
                                    if suggested_category in ["Ăn uống", "Giải trí", "Di chuyển", "Nhà cửa", "Tiết kiệm", "Thu nhập lương", "Mua sắm", "Khác"]:
                                        tx.category = suggested_category
                                    else:
                                        tx.category = "Khác"
                                except Exception as e:
                                    print("Lỗi phân loại danh mục:", str(e))
                                    tx.category = "Khác"
                                
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
            budget, total_expense, percentage = get_budget_status()
            if budget:
                status_text = f"\n\n**Ngân sách tháng này**: {budget:,.0f} VND\n"
                status_text += f"Đã chi: {total_expense:,.0f} VND ({percentage:.1f}%)\n"
                
                if percentage > 100:
                    status_text += "⚠️ **VƯỢT NGÂN SÁCH** – Hãy kiểm soát chi tiêu ngay!"
                elif percentage > 80:
                    status_text += "⚠️ Đã chi hơn 80% ngân sách – Cẩn thận nhé!"
                elif percentage > 50:
                    status_text += "Đã chi hơn 50% – Tiếp tục theo dõi tốt đấy!"
                
                full_response += status_text

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_message("assistant", full_response)