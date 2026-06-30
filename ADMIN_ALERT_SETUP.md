# Email Service - Admin Alert Setup

## Summary

The email service has been configured and tested to send admin alerts when new users sign up. The admin email is set to **ceo@analyticsavenue.in** as configured in the `.env` file.

## Configuration

### Environment Variables (.env)

```
RESEND_API_KEY=re_RaMLK4Tk_Bpjumujv4XymYR9HMqczDMQg
FROM_EMAIL=rnd@analyticsavenue.in
ADMIN_EMAIL=ceo@analyticsavenue.in
WEBSITE_URL=https://www.analyticsavenuerd.in
LOG_LEVEL=INFO
```

**Key Settings:**
- **ADMIN_EMAIL**: `ceo@analyticsavenue.in` - Where admin alerts are sent
- **FROM_EMAIL**: `rnd@analyticsavenue.in` - Sender email address
- **RESEND_API_KEY**: API key for Resend email service

## Available Email Endpoints

### 1. Send Admin Alert (Auto) - ⭐ Recommended for Signups

**Endpoint:** `POST /api/email/send-admin-alert-auto`

Automatically uses the `ADMIN_EMAIL` from environment. Perfect for new user signup workflows.

**Request Body:**
```json
{
  "user_email": "newuser@example.com",
  "user_name": "John Doe",
  "details": {
    "source": "web_signup",
    "signup_date": "2026-05-27"
  }
}
```

**Response:**
```json
{
  "ok": true,
  "sent_to": "ceo@analyticsavenue.in"
}
```

### 2. Send Admin Alert (Manual)

**Endpoint:** `POST /api/email/send-admin-alert`

Allows specifying a custom admin email in the request.

**Request Body:**
```json
{
  "admin_email": "specific.admin@example.com",
  "user_email": "newuser@example.com",
  "user_name": "John Doe",
  "details": {}
}
```

### 3. Send Welcome Email

**Endpoint:** `POST /api/email/send-welcome`

Sends a welcome email to the new user.

**Request Body:**
```json
{
  "recipient": "user@example.com",
  "name": "Jane Smith",
  "signup_source": "web"
}
```

### 4. Send Approval Email

**Endpoint:** `POST /api/email/send-approval`

Notifies user their account has been approved.

**Request Body:**
```json
{
  "recipient": "user@example.com",
  "name": "Jane Smith",
  "approved_by": "Admin Name"
}
```

### 5. Send Rejection Email

**Endpoint:** `POST /api/email/send-rejection`

Notifies user their account request was rejected.

**Request Body:**
```json
{
  "recipient": "user@example.com",
  "name": "Jane Smith",
  "reason": "Does not meet requirements"
}
```

### 6. Debug Environment

**Endpoint:** `GET /api/email/debug-env?show_values=true`

Returns current environment variables (useful for debugging).

**Response:**
```json
{
  "env": {
    "RESEND_API_KEY": "***hidden***",
    "FROM_EMAIL": "rnd@analyticsavenue.in",
    "ADMIN_EMAIL": "ceo@analyticsavenue.in",
    "WEBSITE_URL": "https://www.analyticsavenuerd.in",
    "LOG_LEVEL": "INFO"
  },
  "present": {
    "RESEND_API_KEY": true,
    "FROM_EMAIL": true,
    "ADMIN_EMAIL": true,
    "WEBSITE_URL": true,
    "LOG_LEVEL": true
  }
}
```

## Testing

Run the test suite to verify all endpoints:

```bash
python test_email_service.py
```

Quick test for admin alert:

```bash
python test_admin_alert.py
```

## How It Works

### User Signup Flow (Recommended)

1. User signs up through the web interface
2. The IDP service calls `/api/email/send-admin-alert-auto` with user details
3. Admin alert email automatically goes to `ceo@analyticsavenue.in`
4. Admin reviews the signup and approves/rejects
5. If approved, `/api/email/send-approval` email is sent to user
6. If rejected, `/api/email/send-rejection` email is sent to user

### Email Templates

- `welcome.html` - Welcome email template
- `admin_alert.html` - Admin notification template
- `approval.html` - Account approval template
- `rejection.html` - Account rejection template
- `access.html` - POC access grant template
- `full_access.html` - Full platform access template

## Recent Changes

### Fixed Issues
1. ✅ Fixed UTF-8 BOM encoding in `.env` file
2. ✅ Fixed environment variable loading with `override=True`
3. ✅ Updated ADMIN_EMAIL to `ceo@analyticsavenue.in`

### New Features
1. ✅ Added `/api/email/send-admin-alert-auto` endpoint
2. ✅ This endpoint automatically uses ADMIN_EMAIL from environment
3. ✅ Perfect for signup workflows - no need to hardcode admin email

## Server Status

**Service:** Running on `http://0.0.0.0:8000`

**Active Endpoints:**
- All email endpoints are operational
- Environment variables are correctly loaded
- Resend API key is configured and validated

## Integration with IDP Service

When integrating with the IDP (Identity Provider) service, use the auto endpoint:

```python
# Example: IDP service sending admin alert
import requests

def notify_admin_of_signup(user_email, user_name, details):
    response = requests.post(
        "http://email-service:8000/api/email/send-admin-alert-auto",
        json={
            "user_email": user_email,
            "user_name": user_name,
            "details": details
        }
    )
    return response.json()
```

## Render Deployment

For Render, use the email service root folder `backend/email-service` and set the service to start with:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Render environment variables

Set these env vars in Render for the email service:

```env
RESEND_API_KEY=your_resend_api_key
FROM_EMAIL=rnd@analyticsavenue.in
ADMIN_EMAIL=ceo@analyticsavenue.in
WEBSITE_URL=https://www.analyticsavenuerd.in
LOG_LEVEL=INFO
```

### Notes

- `RESEND_API_KEY` must remain on the backend only.
- `VITE_ADMIN_EMAIL` is only for frontend/local use and does not affect Render backend startup.
- The command above uses `$PORT` so Render can assign the correct port automatically.

## Troubleshooting

### Admin alert not being received
1. Verify ADMIN_EMAIL in `.env` is correct: `cat .env | grep ADMIN_EMAIL`
2. Check service logs: Look for any errors in the uvicorn output
3. Test via debug endpoint: `curl http://localhost:8000/api/email/debug-env?show_values=true`
4. Verify Resend API key is valid

### Service not starting
1. Check Python environment: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Verify .env file exists and is readable
4. Check for port conflicts: `netstat -ano | findstr :8000`

### Emails not sending
1. Verify Resend API key is correct
2. Check email addresses are valid
3. Review the admin_alert.html template
4. Check service logs for detailed error messages

## Contact

For issues or questions about the email service, refer to the logs or check the debug endpoint.
