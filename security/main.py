from config import settings

from fastapi import FastAPI, HTTPException
from schema import *
import re
from datetime import datetime, timedelta
import string
import secrets
import random
import smtplib
from email.mime.multipart import MIMEMultipart

import uuid
import base64

from smtp.config import settings

token_db = {}
app = FastAPI(
    title= "Security APIs",
    description="basic security apis with password generator endpoint and password strength checker, JWT related apis",
    version="2.0"
)


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

    if re.search(r"[^A-Za-z0-9]", password):
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
@app.post("/password-generator")
async def password_generator(data: PasswordGenSchema):
    try:
        password = generate(
            data.length,
            data.uppercase,
            data.lowercase,
            data.digits,
            data.symbols
        )
        return {"password": password}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/password-strength")
async def password_strength(data: PasswordStrengthSchema):
    try:
        result = check(data.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def token_generate(token_type: str, expires_in: int):
    if token_type == "uuid":
        token = str(uuid.uuid4())
    elif token_type == "hex":
        token = secrets.token_hex(64)
    elif token_type == "base64":
        token = base64.urlsafe_b64encode(secrets.token_bytes(64)).decode()
    elif token_type == "jwt":
        header = base64.urlsafe_b64encode(b'{"alg":"none"}').decode()
        payload = base64.urlsafe_b64encode(f'{{"exp": {int(datetime.now().timestamp()) + expires_in}}}'.encode()).decode()
        token = header + "." + payload

    else:
        raise HTTPException(400, "Invalid Token type")

    return token
@app.post("/generate")
def generate_token(token_type: str = "uuid", expires_in: int = 3600):
    token = token_generate(token_type, expires_in)

    token_db[token] = {
        "type": token_type,
        "created_at": datetime.utcnow().isoformat(),
        "expires_in": datetime.utcnow() + timedelta(seconds=expires_in),
        "token": token,
        "status": "active"
    }

    return {"token": token, "type": token_type,"expires_in": expires_in}

@app.post("/verify-token")
def verify_token(token: str):
    if token not in token_db:
        raise HTTPException(status_code=404, detail="Token not found")

    token_data = token_db[token]

    if token_data["status"] != "active":
        return {"valid": False, "Reason": "Token Revoked"}

    if datetime.utcnow() > token_data["expires_in"]:
        return {"valid": False, "Reason": "Token Expired"}

    return {"valid": True, "details": token_data}

@app.post("/revoke")
def revoke_token(token: str):
    if token not in token_db:
        raise HTTPException(status_code=404, detail="Token not found")
    token_db[token]["status"] ="revoked"

    return {"message" : "Token Revoked Successfully"}

@app.get("/list")
def token_list():
    return token_db


otp_db = {}
def generate_otp():
    return str(random.randint(100000, 999999))

def send_mail(email: str,otp: str):
    msg = MIMEMultipart()
    msg["From"] = settings.ADMIN_MAIL
    msg["To"] = email
    msg["Subject"] = "OTP"
    msg.attach(MIMEText(otp, "plain"))

    try:
        server = smtplib.SMTP(host=settings.SMTP_SERVER, port=settings.SMTP_PORT)
        server.starttls()
        server.login(settings.ADMIN_MAIL, settings.ADMIN_PASSWORD)
        server.sendmail(settings.ADMIN_MAIL, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send-otp")
def send_otp(data: OtpSchema):
    otp = generate_otp()
    sent = send_mail(data.email, otp)
    if not sent :
        raise HTTPException(status_code=400, detail="OTP Failed")

    otp_db[data.email] = {
        "otp": otp,
        "created_at": datetime.utcnow().isoformat(),
        "expires_in": datetime.utcnow() + timedelta(minutes=5),
        "status": "active"
    }
    return {"message": "otp sent successfully"}


@app.post("/verify-otp")
def verify(data : OtpVerifySchema):
    if data.email not in otp_db:
        raise HTTPException(status_code=404, detail="Email not found")

    otp_data = otp_db[data.email]

    if datetime.utcnow() > otp_data["expires_in"]:
        otp_data["status"] = "expired"
        raise HTTPException(status_code=400, detail="OTP Expired")

    if otp_data["otp"] != data.otp:
        return {"valid": False, "Reason": "invalid otp"}

    otp_data["status"] = "verified"
    return {"valid": True, "details": otp_data}

