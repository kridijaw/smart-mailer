import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-ZğüşöçİĞÜŞÖÇ]{2,}$'
    return bool(re.match(pattern, email))