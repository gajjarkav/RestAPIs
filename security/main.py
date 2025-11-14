from fastapi import FastAPI, HTTPException
from schema import PasswordGenSchema, PasswordStrengthSchema
from psswrd_generator import generate
from psswrd_strength import check
app = FastAPI(
    title= "Security APIs",
    description="basic security apis with password generator endpoint and password strength checker",
    version="1.1"
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