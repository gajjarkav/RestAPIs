from fastapi import FastAPI
from api.endpoint import router as otpRouter

app = FastAPI(
    title="OTP API",
    description="OTP API",
    version="1.0",
)

app.include_router(otpRouter, prefix="/otp", tags=["otp"])

@app.get('/')
async def root():
    return {'message': 'Welcome to OTP API!'}
