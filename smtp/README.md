# SMTP Service

FastAPI-based microservice for sending emails using SMTP with connection pooling and automatic reconnection.

## Structure

```
smtp/
├── __init__.py          # Package version
├── main.py              # FastAPI application with lifespan management
├── service.py           # Async SMTP email service
└── config.py            # Configuration settings
```

## Tech Stack

- **FastAPI** - Web framework
- **aiosmtplib** - Async SMTP client
- **Pydantic** - Settings and data validation
- **asyncio** - Async lock for connection management

## Features

- Async SMTP connection with persistent pooling
- Automatic reconnection on connection loss
- STARTTLS encryption
- Thread-safe email sending with asyncio locks
- Graceful shutdown with connection cleanup
- Application lifespan management

## Architecture

**Service-Oriented Design:**
- **Main Module** (`main.py`) - FastAPI app with lifespan events
- **Service Module** (`service.py`) - SMTP connection and email operations
- **Config Module** (`config.py`) - Environment-based configuration

**Key Patterns:**
- Singleton SMTP connection stored in app state
- Asyncio lock for thread-safe operations
- Automatic reconnection with retry logic
- Context manager for connection lifecycle

## Configuration

Create `.env` file:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

Defaults:
- `SMTP_HOST`: smtp.gmail.com
- `SMTP_PORT`: 587

## API Endpoints

### POST `/send-email`
Send email to recipient.

**Request:**
```json
{
  "email": "recipient@example.com",
  "subject": "Test Email",
  "body": "This is a test email."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "email sent to recipient@example.com✅"
}
```

## Run

```bash
uvicorn smtp.main:app --reload
```

Or:
```bash
python main.py
```
