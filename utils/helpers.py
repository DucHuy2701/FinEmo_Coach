def format_vnd(amount: float | int) -> str:
    """
    Format số tiền VND: 1500000 → "1.500.000"
    """
    if amount is None:
        return "0"
    return f"{int(amount):,}".replace(",", ".")