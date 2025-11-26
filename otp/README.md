# OTP Service

FastAPI-based microservice for OTP generation, verification, and rate limiting.

## Structure

```
otp/
├── main.py              # FastAPI application entry point
├── api/
│   └── endpoint.py      # OTP endpoints (send, verify)
├── core/
│   ├── config.py        # Configuration settings
│   └── redis_client.py  # Redis connection pool
├── schemas/
│   └── otp.py           # Pydantic models
└── services/
    └── otp_service.py   # OTP business logic
```

## Tech Stack

- **FastAPI** - Web framework
- **Redis** - OTP storage and rate limiting
- **Pydantic** - Data validation
- **redis.asyncio** - Async Redis client

## Features

- Secure 6-digit OTP generation using `secrets` module
- Redis-based OTP storage with expiration (5 minutes)
- Rate limiting (3 requests per 60 seconds per email)
- Email validation
- Automatic OTP cleanup after verification

## Architecture

**Layered Architecture:**
- **API Layer** (`endpoint.py`) - HTTP request handling
- **Service Layer** (`otp_service.py`) - Business logic
- **Data Layer** (`redis_client.py`) - Redis operations
- **Schema Layer** (`otp.py`) - Request/response validation

**Key Patterns:**
- Dependency injection for Redis connection
- Connection pooling for Redis
- Pipeline operations for atomic Redis updates

## Configuration

Environment variables in `.env`:
```
REDIS_URL=redis://localhost:6379/0
```

Defaults:
- `OTP_EXPIRY`: 300 seconds
- `RATELIMIT_DURATION`: 60 seconds
- `MAX_REQUEST`: 3 attempts

## API Endpoints

### POST `/otp/send`
Generate and send OTP to email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "otp sent successfully.",
  "debug_otp": "123456"
}
```

### POST `/otp/verify`
Verify OTP code.

**Request:**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response:**
```json
{
  "message": "otp sent successfully."
}
```

## Run

```bash
uvicorn main:app --reload
```
