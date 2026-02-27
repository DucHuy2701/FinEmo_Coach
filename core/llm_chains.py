from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from core.models import TransactionOutput

llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)

response_prompt = ChatPromptTemplate.from_messages([
    ("system", """
Bạn là FinEmo Coach - người bạn hỗ trợ tài chính và cảm xúc.
**Trả lời hoàn toàn bằng TIẾNG VIỆT, không dùng tiếng Trung hoặc tiếng Anh trừ khi người dùng yêu cầu.**
Trả lời thân thiện, đồng cảm, ngắn gọn.
Dữ liệu tài chính gần đây:
{finance_summary}
Đồng cảm với cảm xúc người dùng, đưa lời khuyên cân bằng tài chính + tinh thần.
Nếu họ đề cập chi tiêu/thu nhập, bạn có thể nhắc lại để xác nhận.
    """),
    ("human", "{user_input}")
])
response_chain = response_prompt | llm

parse_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""
Bạn là trợ lý trích xuất thông tin giao dịch từ tin nhắn người dùng.
Trích xuất tất cả giao dịch có trong tin nhắn (có thể nhiều).
Nếu không có giao dịch nào → {{"has_transaction": false, "transactions": []}}

Hướng dẫn chi tiết:
- date: dùng ngày hôm nay nếu không được đề cập rõ (định dạng YYYY-MM-DD, ví dụ {datetime.today().strftime('%Y-%m-%d')}).
- amount: chỉ lấy số tiền, chuyển về số nguyên (80k → 80000, 3 triệu → 3000000, 1.2tr → 1200000).
- type: PHẢI PHÂN BIỆT DỰA VÀO NGỮ CẢNH:
  - "Thu nhập" nếu có từ: nhận, lương, thưởng, cầm tiền, được, vào tài khoản, bonus...
  - "Chi tiêu" nếu có từ: mua, chi, tiêu, ra làm, hết, xài, shopping, tốn, mất...
  - Nếu câu có cả thu và chi → tách riêng từng transaction.
- category: chọn chính xác nhất từ danh sách: Ăn uống, Giải trí, Di chuyển, Nhà cửa, Tiết kiệm, Thu nhập lương, Mua sắm, Khác.
  Ví dụ: gear, đồ công nghệ → Mua sắm; ăn uống → Ăn uống; lương/thưởng → Thu nhập lương.
- description: tóm tắt ngắn gọn hành động/ý nghĩa từ câu.
- Có thể có nhiều transaction trong 1 tin nhắn → luôn trả về mảng (array), dù chỉ 1 phần tử.

Few-shot examples (học theo cách này):
- Input: "Hôm nay ăn phở 80k với bạn"
  Output: {{"has_transaction": true, "transactions": [{{"date": "{datetime.today().strftime('%Y-%m-%d')}", "amount": 80000, "category": "Ăn uống", "type": "Chi tiêu", "description": "ăn phở với bạn"}}]}}

- Input: "Vừa nhận thưởng 4 triệu, sau đó đi mua sắm hết 2 triệu"
  Output: {{"has_transaction": true, "transactions": [{{"date": "{datetime.today().strftime('%Y-%m-%d')}", "amount": 4000000, "category": "Thu nhập lương", "type": "Thu nhập", "description": "nhận thưởng"}}, {{"date": "{datetime.today().strftime('%Y-%m-%d')}", "amount": 2000000, "category": "Mua sắm", "type": "Chi tiêu", "description": "đi mua sắm"}}]}}

- Input: "Vừa chi 1tr thì sếp gọi nhận thưởng 2tr"
  Output: {{"has_transaction": true, "transactions": [{{"date": "{datetime.today().strftime('%Y-%m-%d')}", "amount": 1000000, "category": "Khác", "type": "Chi tiêu", "description": "chi tiêu"}}, {{"date": "{datetime.today().strftime('%Y-%m-%d')}", "amount": 2000000, "category": "Thu nhập lương", "type": "Thu nhập", "description": "thưởng"}}]}}

- Input: "vừa cầm tiền thưởng là ra làm ngay 3 triệu tiền gear rồi, thích quá"
  Output: {{"has_transaction": true, "transactions": [{{"date": "{datetime.today().strftime('%Y-%m-%d')}", "amount": 3000000, "category": "Mua sắm", "type": "Chi tiêu", "description": "mua tiền gear"}}]}}

- Input: "Buồn quá, không mua gì cả"
  Output: {{"has_transaction": false, "transactions": []}}
"""),
    ("human", "{user_input}")
])

parse_chain = parse_prompt | llm.with_structured_output(TransactionOutput)