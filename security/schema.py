from pydantic import BaseModel, EmailStr


class PasswordGenSchema(BaseModel):
    length: int = 12
    uppercase: bool = True
    lowercase: bool = True
    digits: bool = True
    symbols: bool = True


class PasswordStrengthSchema(BaseModel):
    password: str

class OtpSchema(BaseModel):
    email: EmailStr

class OtpVerifySchema(BaseModel):
    email: EmailStr
    otp: str