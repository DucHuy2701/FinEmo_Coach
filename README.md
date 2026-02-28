# FinEmo Coach

**AI cá nhân hỗ trợ quản lý chi tiêu & cảm xúc tài chính** – chạy hoàn toàn local, miễn phí, bảo mật 100% (dùng Ollama LLM).

### Demo
<img width="1909" height="829" alt="image" src="https://github.com/user-attachments/assets/9b936e3f-0e8d-45c6-a1cf-4b49559fb368" />
<img width="1903" height="823" alt="image" src="https://github.com/user-attachments/assets/831a986a-202a-4042-8201-5eeeffa56668" />
<img width="1905" height="832" alt="image" src="https://github.com/user-attachments/assets/fbddb8df-1bfc-469a-ada5-b830955aed2d" />

### Tính năng chính
- 💬 Chat tự nhiên với AI để ghi chi tiêu/thu nhập (tự động parse & lưu)
- 📊 Dashboard tóm tắt thu/chi, biểu đồ phân bổ, xu hướng
- 📜 Lịch sử giao dịch có thể xem, chỉnh sửa, xóa
- ➕ Nhập thủ công qua sidebar (form đơn giản)
- 🔒 Chạy local hoàn toàn (Ollama + SQLite) – không gửi dữ liệu lên cloud
- 🧠 Phân tích cảm xúc & lời khuyên cân bằng tài chính + tinh thần

### Cài đặt & Chạy nhanh (Quick Start)

Yêu cầu:
- Python 3.10+
- Ollama đã cài[](https://ollama.com)
- Máy có RAM ≥ 16GB (nếu dùng GPU thì tốt hơn)

```bash
# 1. Clone repo
git clone https://github.com/username/finemo-coach.git
cd finemo-coach

# 2. Tạo venv & cài dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # hoặc pip install streamlit langchain langchain-ollama pandas plotly pydantic

# 3. Pull model Ollama (khuyến nghị qwen2.5:7b hoặc nhỏ hơn nếu máy yếu)
ollama pull qwen2.5:7b

# 4. Chạy app
streamlit run app.py
