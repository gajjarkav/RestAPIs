from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from service import AsyncEmailService
from smtp.config import settings

# schema validation model
class EmailSchema(BaseModel):
    email: str
    subject: str
    body: str


# environment variable configuration
host = settings.SMTP_HOST
port = settings.SMTP_PORT
user = settings.SMTP_USER
password = settings.SMTP_PASSWORD

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not user or not password:
        raise ValueError("username or password missing in .env file.🔴")
    print("initializing SMTP service..🚀")
    email_service = AsyncEmailService(host, port, user, password)

    try:
        await email_service.connect()
        app.state.email_service = email_service

    except Exception as e:
        print(f"❌failed to connect to SMTP service: {e}")

    yield

    print("🔴shutting down smtp service..")
    await email_service.close()

app = FastAPI(
    title="Microservice-smtp",
    description="",
    version="1.0",
    lifespan=lifespan
)

@app.post('/send-email')
async def send_email(payload: EmailSchema, request: Request):

    service: AsyncEmailService = request.app.state.email_service

    try:
        await service.send_mail(
            recipient=payload.email,
            subject=payload.subject,
            body=payload.body
        )
        return {
            "status": "success",
            "message": f"email sent to {payload.email}✅"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
