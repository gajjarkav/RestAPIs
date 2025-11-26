from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from core.redis_client import get_redis
from services.otp_service import OTPService
from schemas.otp import OTPVerify, OTPResponse, OTPRequest

router = APIRouter()

def get_otp_service(redis: Redis = Depends(get_redis)) -> OTPService:
    return OTPService(redis)

@router.post('/send', response_model=OTPResponse)
async def send_otp(
        request: OTPRequest,
        debug: OTPService = Depends(get_otp_service)
):
    otp = await send_otp(request.email)

    return OTPResponse(
        message="otp sent successfully.",
        debug_otp=otp
    )

@router.post('/verify', response_model=OTPResponse)
async def verify_otp(
        request: OTPVerify,
        service: OTPService = Depends(get_otp_service)
):
    is_valid = await service.verify_otp(request.email, request.code)
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP code."
        )

    return OTPResponse(
        message="otp sent successfully."
    )