# RestAPIs

A collection of FastAPI-based REST APIs providing security and SMTP email functionality.

## 📋 Overview

This repository contains two main API modules:
- **Security APIs** - Password generation, strength checking, token management, and OTP verification
- **SMTP API** - Asynchronous email sending functionality

## 🚀 Features

### Security APIs (v2.0)

#### Password Management
- **Password Generator** - Generate secure passwords with customizable options
  - Configurable length
  - Toggle uppercase/lowercase letters
  - Include/exclude digits and symbols
  - Uses cryptographically secure random generation

- **Password Strength Checker** - Analyze password security
  - Length validation (minimum 8 characters recommended)
  - Character type diversity check (uppercase, lowercase, digits, symbols)
  - Common password detection
  - Sequential character detection
  - Repeated character detection
  - Strength scoring (Weak/Medium/Strong/Very Strong)
  - Actionable feedback for improvement

#### Token Management
- **Token Generation** - Create various token types
  - UUID tokens
  - Hexadecimal tokens (128 characters)
  - Base64 URL-safe tokens
  - JWT-like tokens (header.payload format)
  - Configurable expiration time

- **Token Verification** - Validate token status
  - Check token existence
  - Verify expiration status
  - Check revocation status
  - Retrieve token metadata

- **Token Revocation** - Invalidate tokens
- **Token Listing** - View all generated tokens and their status

#### OTP (One-Time Password)
- **OTP Generation & Sending** - Generate and email 6-digit OTPs
  - 5-minute expiration window
  - SMTP email delivery
  - Secure random generation

- **OTP Verification** - Validate user-provided OTPs
  - Expiration checking
  - Status tracking (active/expired/verified)

### SMTP API (v1.0)

- **Asynchronous Email Sending** - Send emails using async/await pattern
  - Gmail SMTP support
  - TLS encryption
  - Connection pooling with context manager
  - Detailed error handling

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Python Version**: 3.13+
- **Key Dependencies**:
  - `fastapi[all]` - Web framework with all extras
  - `uvicorn[standard]` - ASGI server
  - `aiosmtplib` - Async SMTP client
  - `pydantic` - Data validation
  - `pydantic-settings` - Settings management
  - `python-multipart` - File upload support

## 📦 Installation

### Prerequisites
- Python 3.13 or higher
- UV package manager (recommended) or pip

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd RestAPIs
```

2. **Install dependencies**

Using UV (recommended):
```bash
uv sync
```

Using pip:
```bash
pip install -e .
```

3. **Environment Configuration**

Create a `.env` file in the root directory:

```env
# Security API Configuration
ADMIN_MAIL=your-email@gmail.com
ADMIN_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# SMTP API Configuration (optional, defaults to Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

> **Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## 🏃 Running the APIs

### Security API

```bash
cd security
uvicorn main:app --reload --port 8000
```

Access the API documentation at: `http://localhost:8000/docs`

### SMTP API

```bash
cd smtp
uvicorn smtp:app --reload --port 8001
```

Access the API documentation at: `http://localhost:8001/docs`

## 📚 API Endpoints

### Security API Endpoints

#### Password Endpoints

**POST** `/password-generator`
```json
{
  "length": 12,
  "uppercase": true,
  "lowercase": true,
  "digits": true,
  "symbols": true
}
```

**POST** `/password-strength`
```json
{
  "password": "YourPassword123!"
}
```

#### Token Endpoints

**POST** `/generate`
- Query Parameters:
  - `token_type`: uuid | hex | base64 | jwt (default: uuid)
  - `expires_in`: seconds (default: 3600)

**POST** `/verify-token`
- Query Parameter: `token` (string)

**POST** `/revoke`
- Query Parameter: `token` (string)

**GET** `/list`
- Returns all tokens in the database

#### OTP Endpoints

**POST** `/send-otp`
```json
{
  "email": "user@example.com"
}
```

**POST** `/verify-otp`
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

### SMTP API Endpoints

**GET** `/`
- Base endpoint health check

**POST** `/email`
```json
{
  "from_email": "sender@example.com",
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body content"
}
```

## 📁 Project Structure

```
RestAPIs/
├── security/
│   ├── main.py           # Security API routes and logic
│   ├── schema.py         # Pydantic schemas for validation
│   └── config.py         # Environment settings
├── smtp/
│   ├── smtp.py           # SMTP API routes
│   ├── connection.py     # Async SMTP connection manager
│   └── config.py         # SMTP settings
├── pyproject.toml        # Project dependencies
├── uv.lock              # Lock file for UV package manager
└── README.md            # This file
```

## 🔒 Security Considerations

- **In-Memory Storage**: Token and OTP databases are stored in memory and will be lost on server restart. For production, use a persistent database (Redis, PostgreSQL, etc.).
- **Environment Variables**: Never commit `.env` files to version control.
- **SMTP Credentials**: Use app-specific passwords for email services.
- **Token Security**: Tokens are generated using `secrets` module for cryptographic security.
- **Password Generation**: Uses `secrets.choice()` for secure random password generation.

## ⚠️ Limitations

- Token and OTP storage is in-memory only (not persistent)
- No authentication/authorization on API endpoints
- Single-user OTP tracking (one OTP per email at a time)
- JWT tokens are simplified (header.payload only, no signature)

## 🤝 Contributing

This is a personal project for learning and demonstration purposes.

## 📄 License

This project is provided as-is for educational purposes.

## 🔧 Development

Built with Python 3.13 and managed using UV package manager for fast dependency resolution.

---

**Note**: This codebase represents the current state of the project and includes working implementations of the described features.

