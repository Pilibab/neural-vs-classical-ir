import re

def clean_text(input_string: str) -> str:
    # Remove non-ASCII characters (emojis, special symbols, etc.)
    # [^\x00-\x7f] matches any character outside the standard ASCII range
    ascii_only = re.sub(r'[^\x00-\x7f]', '', input_string)
    
    # Replace multiple whitespaces (2 or more) with a single space
    # .strip() removes leading/trailing spaces if any were left behind
    cleaned = re.sub(r'\s{2,}', ' ', ascii_only).strip()
    
    return cleaned
