from pydantic import BaseModel

class PasswordGenSchema(BaseModel):
    length: int = 12
    uppercase: bool = True
    lowercase: bool = True
    digits: bool = True
    symbols: bool = True


class PasswordStrengthSchema(BaseModel):
    password: str
