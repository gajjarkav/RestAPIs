from pydantic import BaseModel, constr, Field, EmailStr

class OTPRequest(BaseModel):
    email: EmailStr = Field(...)

class OTPVerify(BaseModel):
    email: EmailStr
    otp: constr(min_length=6, max_length=6)

class OTPResponse(BaseModel):
    message: str
    debug_otp: str | None=None