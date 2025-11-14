import string
import secrets

def generate(length: int, uppercase: bool, lowercase: bool, digits: bool, symbols: bool) -> str:
    chars = ""

    if uppercase:
        chars += string.ascii_uppercase
    if lowercase:
        chars += string.ascii_lowercase
    if digits:
        chars += string.digits
    if symbols:
        chars += string.punctuation

    if not chars:
        raise ValueError("chars cannot be empty")

    password = ''.join(secrets.choice(chars) for _ in range(length))

    return password