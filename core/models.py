from pydantic import BaseModel, Field
from typing import List

class Transaction(BaseModel):
    date: str = Field(description="Ngày giao dịch, định dạng YYYY-MM-DD")
    amount: float = Field(description="Số tiền (VND)")
    category: str = Field(description="Danh mục: Ăn uống, Giải trí, Di chuyển, Nhà cửa, Tiết kiệm, Thu nhập lương, Mua sắm, Khác")
    type: str = Field(description="Thu nhập hoặc Chi tiêu")
    description: str = Field(description="Mô tả ngắn gọn")

class TransactionOutput(BaseModel):
    has_transaction: bool = Field(description="Có giao dịch được trích xuất hay không")
    transactions: List[Transaction] = Field(description="Danh sách các giao dịch (có thể rỗng)")