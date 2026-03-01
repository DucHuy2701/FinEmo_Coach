import pytest
from utils.finance_summary import get_finance_summary
from datetime import datetime, timedelta
import pandas as pd

def test_get_finance_summary_no_data(monkeypatch):
    def mock_read_sql(*args, **kwargs):
        return pd.DataFrame()
    
    monkeypatch.setattr(pd, "read_sql_query", mock_read_sql)
    summary = get_finance_summary(days=30)
    assert "chưa có giao dịch" in summary.lower()

def test_get_finance_summary_with_data(monkeypatch):
    mock_df = pd.DataFrame({
        'amount': [500000, 2000000],
        'type': ['Thu nhập', 'Chi tiêu'],
        'category': ['Thu nhập lương', 'Mua sắm']
    })
    
    def mock_read_sql(*args, **kwargs):
        return mock_df
    
    monkeypatch.setattr(pd, "read_sql_query", mock_read_sql)
    summary = get_finance_summary(days=30)
    assert "Thu nhập: 500,000 VND" in summary
    assert "Chi tiêu: 2,000,000 VND" in summary
    assert "Số dư: -1,500,000 VND" in summary