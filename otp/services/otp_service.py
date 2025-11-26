import secrets
import string
from fastapi import HTTPException, status
from redis.asyncio import Redis
from core.config import settings
from typing import Optional

class OTPService:
    def __init__(self, redis: Redis):
        self.redis = redis

    def _generate_code(self, length: Optional[int] = 6) -> str:
        """securely generate a 6 digit code"""
        return "".join(secrets.choice(string.digits) for _ in range(length))

    async def check_rate_limit(self, email: str):
        """
        enforce rate limit using rate limit.
        key concept: we use a separate key for tracking attempts
        """

        rate_key = f"rate_limit : {email}"

        current_requests = await self.redis.get(rate_key)

        if current_requests and int(current_requests) >= settings.MAX_REQUEST:
            ttl = await self.redis.ttl(rate_key)
            raise HTTPException(
                status_code= status.HTTP_429_TOO_MANY_REQUESTS,
                detail= f"rate limit exceeded, try again in {ttl} seconds",
            )

    async def send_otp(self, email: str):
        """
        check rate limit -> generate otp -> store otp -> increment rate limit
        """

        await self.check_rate_limit(email)

        otp_code = self._generate_code()
        otp_key = f"otp:{email}"
        rate_key = f"rate limit : {email}"

        async with self.redis.pipeline() as pipe:
            pipe.set(otp_key, otp_code, ex=settings.OTP_EXPIRY)

            pipe.incr(rate_key)

            pipe.expire(rate_key, settings.RATELIMIT_DURATION, nx=True)

            await pipe.execute()

        print(f"sending otp to: {email}, your code is {otp_code}")

        return otp_code

    async def verify_otp(self, email:str, otp: str) -> bool:
        otp_key = f"otp:{email}"
        stored_otp = await self.redis.get(otp_key)

        if not stored_otp:
            return False

        if stored_otp != otp:
            return False

        await self.redis.delete(otp_key)
        return True
