'''
>> smtp code {async}
>> it can
'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
import aiosmtplib
from config import settings, EmailSchema
from connection import connection

app = FastAPI(
    title="SMTP API",
    description="A SimpleMailTransferProtocol api using asynchronous coding",
    version="1.0"
)


async def send_email(from_email: EmailStr, to: str, subject: str, body: str):
    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        async with connection() as smtp_connection:
            await smtp_connection.sendmessage(msg)

        return {'status': 'success', 'message': f"email sent to {to}"}
    except aiosmtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"SMTP Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error found: {e}")


@app.get('/')
def home():
    return {"message": "base endpoint"}

@app.post('/email')
async def email(schema: EmailSchema):
    return await send_email(**schema.dict())