import pytest
from core.llm_chains import parse_chain

def test_parse_single_transaction():
    input_text = "vừa tiêu hết 400k ăn uống"
    try:
        parsed = parse_chain.invoke({"user_input": input_text})
        print("Parsed single:", parsed)  # in ra để xem
        assert parsed.has_transaction is True
        assert len(parsed.transactions) >= 1
        tx = parsed.transactions[0]
        assert tx.amount > 0
        assert tx.type == "Chi tiêu"
    except Exception as e:
        print("Exception in single test:", str(e))
        raise  # fail test nhưng in lỗi

def test_parse_multi_transaction():
    input_text = "nhận thưởng 500k, đi ăn hết 200k"
    try:
        parsed = parse_chain.invoke({"user_input": input_text})  # dùng .invoke() sync
        print("Parsed multi:", parsed)
        assert parsed.has_transaction is True
        assert len(parsed.transactions) >= 1
    except Exception as e:
        print("Exception in multi test:", str(e))
        raise

def test_no_transaction():
    input_text = "hôm nay vui quá không mua gì"
    try:
        parsed = parse_chain.invoke({"user_input": input_text})
        print("Parsed no transaction:", parsed)
        assert parsed.has_transaction is False
        assert len(parsed.transactions) == 0
    except Exception as e:
        print("Exception in no transaction test:", str(e))
        raise