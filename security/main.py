from fastapi import FastAPI, HTTPException
from schema import PasswordGenSchema, PasswordStrengthSchema
from psswrd_generator import generate
from psswrd_strength import check
from datetime import datetime, timedelta

import uuid
import secrets
import base64

token_db = {}
app = FastAPI(
    title= "Security APIs",
    description="basic security apis with password generator endpoint and password strength checker, JWT related apis",
    version="2.0"
)


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
        token = header + "." + payload + "."

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
