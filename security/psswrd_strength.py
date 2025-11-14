import re

common = {"password", "qwerty", "admin", "admin123", "1234567890", "123456"}

def seq_check(pwd: str) -> bool:
    sequences = ["123", "qwe", "abc"]
    return any(seq in pwd .lower() for seq in sequences)
def check(password: str) -> dict:
    score = 0
    feedback = []

    if len(password) < 8:
        feedback.append("You need at least 8 characters long password for more strength")

    if len(password) >= 8:
        score += 1
        feedback.append("Good Length of Password")

    if len(password) >= 12:
        score += 1
        feedback.append("Very Good Length of Password")

    if re.search(f"[a-z]", password):
        score += 1
    else:
        feedback.append("TIP: add lowercase letters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("TIP: add uppercase letters")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("TIP: add numbers")

    if re.search(r"^A-Za-z0-9", password):
        score += 1
    else:
        feedback.append("TIP: add special characters")


    if not any(word in password.lower() for word in common):
        score += 1
    else:
        feedback.append("TIP: try to use different password ignore common passwords")

    if not re.findall(r"(.)\1{2,}", password):
        score += 1
    else :
        feedback.append("TIP: try to avoid repeated chars")

    if not seq_check(password):
        score += 1
    else:
        feedback.append("TIP: try to avoid common sequence in password")

    if score <= 3:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    elif score <= 8:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "score": score,
        "strength": strength,
        "feedback": feedback
    }