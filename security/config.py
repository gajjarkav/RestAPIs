from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADMIN_MAIL: str
    ADMIN_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()