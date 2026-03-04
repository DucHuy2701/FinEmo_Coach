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
```

Mở browser: http://localhost:8501

### HƯỚNG DẪN SỬ DỤNG
1. Nhập thủ công: Dùng form trong sidebar → "Thêm ngay".
2. Chat với AI: Gõ tự nhiên (ví dụ: "vừa nhận lương 15tr, tiêu 2tr ăn uống") → AI tự parse, lưu DB, và đưa lời khuyên.
3. Xem lịch sử: Mở tab "Lịch sử giao dịch" → tick checkbox để xóa.
4. Dashboard: Tab "Dashboard tài chính" → biểu đồ & số liệu 30 ngày, có thể export/import CSV để theo dõi.

### TECH STACK
- Frontend: Streamlit
- AI: Ollama + LangChain (model Qwen2.5 7B local)
- Database: SQLite
- Data & Chart: Pandas, Plotly Express

### PHÁT TRIỂN & ĐÓNG GÓP
- Fork repo → tạo branch feature/ten-tinh-nang
- Commit với message rõ ràng
- Pull Request với mô tả thay đổi
- Coding style: Black + Ruff

### DOCKERIZE
1. Cài Docker Desktop: https://www.docker.com/products/docker-desktop
2. Tải dự án:
   git clone https://github.com/DucHuy2701/finemo-coach.git
   cd finemo-coach
3. Chạy:
   docker compose up
4. Mở trình duyệt: http://localhost:8501
5. Update app mới:
   docker compose pull
   docker compose up -d

### THANKS
Cảm ơn cộng đồng Ollama, LangChain, Streamlit đã cung cấp công cụ miễn phí tuyệt vời.
Nếu bạn dùng thử và thấy hay, hãy star repo hoặc share cảm nhận nhé! ❤️
