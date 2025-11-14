from pydantic import BaseModel
from typing import Optional

class PasswordGenSchema(BaseModel):
    length: int = 12
    uppercase: bool = True
    lowercase: bool = True
    digits: bool = True
    symbols: bool = True

    