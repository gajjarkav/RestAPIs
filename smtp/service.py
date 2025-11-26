import asyncio
import aiosmtplib
from email.message import EmailMessage


class AsyncEmailService:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.lock = asyncio.Lock()

    async def connect(self):
        """
        smtp connection
        """
        if self.client and self.client.is_connected():
            return

        print('Connecting to SMTP server🔃')
        self.client = aiosmtplib.SMTP(hostname=self.hostname, port=self.port)

        await self.client.connect()
        await self.client.starttls()
        await self.client.login(self.username, self.password)

        print("connected and logged in✅")

    async def send_mail(self, recipient: str, subject: str, body: str):
        """
        main method to send mail to recipient
        """

        msg = EmailMessage()
        msg["From"] = self.username
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        async with self.lock:
            if not self.client or not self.client.is_connected():
                print("⚠️ connection lost, reconnecting..🔃")
                await self.connect()

            try:
                await self.client.send_message(msg)
                print(f"email sent to : {recipient} ✅")
            except aiosmtplib.SMTPServerDisconnected as e:
                print(f"❌ server diconnected unexpectedly. retrying..🔃 (error: {e})")
                await self.connect()
                await self.client.send_message(msg)

    async def close(self):
        """
        disconnect the connection
        """
        if self.client and self.client.is_connected():
            await self.client.quit()
            print("🔴connection closed")