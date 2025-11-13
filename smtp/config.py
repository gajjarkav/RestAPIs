from pydantic_settings import BaseSettings
from pydantic import BaseModel, EmailStr
from typing import Optional

class Settings(BaseSettings):
    '''smtp env variable config'''

    SMTP_HOST: Optional[str] = 'smtp.gmail.com'
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()

class EmailSchema(BaseModel):
    from_email: EmailStr
    to: EmailStr
    subject: str
    body: str