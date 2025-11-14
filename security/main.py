from fastapi import FastAPI, HTTPException
from schema import PasswordGenSchema
from psswrd_generator import generate
app = FastAPI(
    title= "Security APIs",
    description="basic security apis with password generator endpoint",
    version="1.0"
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
