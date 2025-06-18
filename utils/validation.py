
def sanitize_user_input(text: str, max_length: int = 10000) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    if len(text) > max_length:
        raise ValueError(f"Input too long: {len(text)} > {max_length}")
    # Add more sanitization as needed
    return text.strip()