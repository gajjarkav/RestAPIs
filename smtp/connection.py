from contextlib import contextmanager
import aiosmtplib
from email.message import EmailMessage
from config import settings

smtp_host = settings.SMTP_HOST
smtp_port = settings.SMTP_PORT
username = settings.SMTP_USER
password = settings.SMTP_PASSWORD

@contextmanager
async def connection():
    smtp = aiosmtplib.SMTP(
        hostname=smtp_host,
        port=smtp_port,
        start_tls=True
    )
    await smtp.connect()
    await smtp.login(username, password)
    try:
        yield smtp
    finally:
        await smtp.quit()