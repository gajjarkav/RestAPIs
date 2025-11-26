from pydantic_settings import BaseSettings
from typing import Optional, ClassVar

class Settings(BaseSettings):
    REDIS_URL: ClassVar[str] = "redis://localhost:6379/0"
    OTP_EXPIRY: ClassVar[int] = 300
    RATELIMIT_DURATION: ClassVar[int] = 60
    MAX_REQUEST: ClassVar[int] = 3

    class Config:
        env_file= ".env"


settings = Settings()