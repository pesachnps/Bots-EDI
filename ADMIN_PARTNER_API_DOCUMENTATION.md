# Admin Dashboard & Partner Portal API Documentation

Version: 1.0  
Base URL: `http://localhost:8080/modern-edi/api/v1`

## Overview

This document covers the REST API endpoints for:
- **Modern EDI Interface**: Transaction management with 5-folder workflow
- **Admin Dashboard**: System administration and analytics
- **Partner Portal**: Self-service partner interface

## Authentication

### Admin Dashboard & Modern EDI Interface

Uses Django session authentication:

```bash
# Login via Django admin first
# Session cookie automatically included in requests
```

**Required**: User must be authenticated and have staff status.

### Partner Portal

Uses custom partner authentication:

```bash
# Login via Partner Portal API
POST /modern-edi/api/v1/partner-portal/auth/login
# Session cookie returned and used for subsequent requests
```

**Required**: Valid partner user account.

## Modern EDI Interface API

### Transaction Management

#### List Transactions

**Endpoint:** `GET /modern-edi/api/v1/transactions/`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `folder` (optional): Filter by folder (inbox, processing, outbox, sent, error)
- `search` (optional): Search by PO number, partner name, or document type
- `partner` (optional): Filter by partner ID
- `document_type` (optional): Filter by document type (850, 810, etc.)
- `status` (optional): Filter by status
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
  "count": 150,
  "results": [
    {
      "id": "abc123",
      "folder": "inbox",
      "partner_name": "Acme Corp",
      "document_type": "850",
      "po_number": "PO-2025-001",
      "status": "pending",
      "created_at": "2025-11-06T10:30:00Z",
      "file_size": 2048,
      "has_acknowledgment": false
    }
  ]
}
```

#### Get Transaction Details

**Endpoint:** `GET /modern-edi/api/v1/transactions/<id>/`

**Authentication:** Django session (staff required)

**Response (200 OK):**
```json
{
  "id": "abc123",
  "folder": "inbox",
  "partner_name": "Acme Corp",
  "partner_id": "123",
  "document_type": "850",
  "po_number": "PO-2025-001",
  "status": "pending",
  "created_at": "2025-11-06T10:30:00Z",
  "updated_at": "2025-11-06T10:30:00Z",
  "file_path": "/path/to/file.edi",
  "file_size": 2048,
  "raw_content": "ISA*00*...",
  "parsed_data": {...},
  "history": [
    {
      "timestamp": "2025-11-06T10:30:00Z",
      "action": "created",
      "user": "admin",
      "notes": "File uploaded"
    }
  ],
  "acknowledgment": null
}
```


#### Create Transaction

**Endpoint:** `POST /modern-edi/api/v1/transactions/`

**Authentication:** Django session (staff required)

**Request Body:**
```json
{
  "partner_id": "123",
  "document_type": "850",
  "po_number": "PO-2025-001",
  "file_content": "ISA*00*...",
  "folder": "inbox"
}
```

**Response (201 Created):**
```json
{
  "id": "abc123",
  "message": "Transaction created successfully"
}
```

#### Update Transaction

**Endpoint:** `PUT /modern-edi/api/v1/transactions/<id>/`

**Authentication:** Django session (staff required)

**Request Body:**
```json
{
  "status": "processed",
  "notes": "Updated status"
}
```

**Response (200 OK):**
```json
{
  "id": "abc123",
  "message": "Transaction updated successfully"
}
```

#### Move Transaction

**Endpoint:** `POST /modern-edi/api/v1/transactions/<id>/move/`

**Authentication:** Django session (staff required)

**Request Body:**
```json
{
  "folder": "outbox",
  "notes": "Ready to send"
}
```

**Response (200 OK):**
```json
{
  "id": "abc123",
  "folder": "outbox",
  "message": "Transaction moved successfully"
}
```

#### Delete Transaction

**Endpoint:** `DELETE /modern-edi/api/v1/transactions/<id>/`

**Authentication:** Django session (staff required)

**Response (204 No Content)**


### Folder Operations

#### Get Folder Statistics

**Endpoint:** `GET /modern-edi/api/v1/folders/<folder_name>/stats/`

**Authentication:** Django session (staff required)

**Path Parameters:**
- `folder_name`: inbox, processing, outbox, sent, or error

**Response (200 OK):**
```json
{
  "folder": "inbox",
  "count": 25,
  "total_size": 51200,
  "oldest_transaction": "2025-11-01T10:00:00Z",
  "newest_transaction": "2025-11-06T10:30:00Z"
}
```

## Admin Dashboard API

### Dashboard Metrics

#### Get Dashboard Overview

**Endpoint:** `GET /modern-edi/api/v1/admin/dashboard/metrics`

**Authentication:** Django session (staff required)

**Response (200 OK):**
```json
{
  "total_partners": 45,
  "total_transactions": 12847,
  "success_rate": 98.5,
  "error_rate": 1.5,
  "recent_errors": [
    {
      "id": 567,
      "partner_name": "Acme Corp",
      "error_type": "Parse Error",
      "timestamp": "2025-11-06T10:30:00Z"
    }
  ],
  "system_status": {
    "sftp_polling": "healthy",
    "api_services": "healthy",
    "database": "healthy"
  }
}
```

#### Get Dashboard Charts

**Endpoint:** `GET /modern-edi/api/v1/admin/dashboard/charts`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `period` (optional): day, week, month (default: month)

**Response (200 OK):**
```json
{
  "transaction_volume": [
    {"date": "2025-10-07", "count": 234},
    {"date": "2025-10-08", "count": 198}
  ],
  "top_partners": [
    {"id": 1, "name": "Acme Corp", "transaction_count": 1234}
  ]
}
```


### Partner Management

#### List Partners

**Endpoint:** `GET /modern-edi/api/v1/admin/partners/`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `search` (optional): Search by name or ID
- `status` (optional): active, inactive, suspended
- `communication_method` (optional): sftp, api

**Response (200 OK):**
```json
{
  "count": 45,
  "results": [
    {
      "id": "123",
      "name": "Acme Corp",
      "communication_method": "sftp",
      "status": "active",
      "transaction_count": 1234,
      "last_activity": "2025-11-06T10:00:00Z"
    }
  ]
}
```

#### Get Partner Analytics

**Endpoint:** `GET /modern-edi/api/v1/admin/partners/<id>/analytics`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
  "partner_id": "123",
  "partner_name": "Acme Corp",
  "total_transactions": 1234,
  "sent_count": 600,
  "received_count": 634,
  "success_rate": 98.5,
  "failure_rate": 1.5,
  "avg_processing_time": 2.5,
  "document_types": {
    "850": 500,
    "810": 400,
    "997": 334
  }
}
```

#### List Partner Users

**Endpoint:** `GET /modern-edi/api/v1/admin/partners/<id>/users`

**Authentication:** Django session (staff required)

**Response (200 OK):**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "username": "acme_john",
      "email": "john@acme.com",
      "first_name": "John",
      "last_name": "Smith",
      "role": "partner_admin",
      "is_active": true,
      "last_login": "2025-11-06T09:00:00Z"
    }
  ]
}
```


#### Create Partner User

**Endpoint:** `POST /modern-edi/api/v1/admin/partners/<id>/users`

**Authentication:** Django session (staff required)

**Request Body:**
```json
{
  "username": "acme_jane",
  "email": "jane@acme.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "password": "SecurePass123!",
  "role": "partner_user",
  "phone": "+1-555-0123"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "username": "acme_jane",
  "message": "User created successfully"
}
```

### User Management

#### Update User

**Endpoint:** `PUT /modern-edi/api/v1/admin/users/<id>`

**Authentication:** Django session (staff required)

**Request Body:**
```json
{
  "email": "jane.doe@acme.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+1-555-0124",
  "role": "partner_admin",
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "id": 2,
  "message": "User updated successfully"
}
```

#### Delete User

**Endpoint:** `DELETE /modern-edi/api/v1/admin/users/<id>`

**Authentication:** Django session (staff required)

**Response (204 No Content)**

#### Reset User Password

**Endpoint:** `POST /modern-edi/api/v1/admin/users/<id>/reset-password`

**Authentication:** Django session (staff required)

**Response (200 OK):**
```json
{
  "temporary_password": "TempPass789!",
  "message": "Password reset successfully"
}
```


#### Update User Permissions

**Endpoint:** `PUT /modern-edi/api/v1/admin/users/<id>/permissions`

**Authentication:** Django session (staff required)

**Request Body:**
```json
{
  "can_view_transactions": true,
  "can_upload_files": true,
  "can_download_files": true,
  "can_view_reports": true,
  "can_manage_settings": false
}
```

**Response (200 OK):**
```json
{
  "id": 2,
  "permissions": {
    "can_view_transactions": true,
    "can_upload_files": true,
    "can_download_files": true,
    "can_view_reports": true,
    "can_manage_settings": false
  },
  "message": "Permissions updated successfully"
}
```

### Analytics

#### Get Transaction Analytics

**Endpoint:** `GET /modern-edi/api/v1/admin/analytics/transactions`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)
- `period` (optional): day, week, month
- `export` (optional): csv, pdf

**Response (200 OK):**
```json
{
  "period": "month",
  "data": [
    {"date": "2025-10-01", "count": 450, "success": 445, "failed": 5},
    {"date": "2025-10-02", "count": 423, "success": 420, "failed": 3}
  ]
}
```

#### Get Partner Analytics

**Endpoint:** `GET /modern-edi/api/v1/admin/analytics/partners`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
  "partners": [
    {
      "id": "123",
      "name": "Acme Corp",
      "transaction_count": 1234,
      "success_rate": 98.5,
      "failure_rate": 1.5
    }
  ]
}
```


#### Get Document Type Analytics

**Endpoint:** `GET /modern-edi/api/v1/admin/analytics/documents`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
  "document_types": [
    {"type": "850", "count": 5000, "percentage": 40.5},
    {"type": "810", "count": 4000, "percentage": 32.4},
    {"type": "997", "count": 3347, "percentage": 27.1}
  ]
}
```

### Activity Logs

#### List Activity Logs

**Endpoint:** `GET /modern-edi/api/v1/admin/activity-logs`

**Authentication:** Django session (staff required)

**Query Parameters:**
- `user_type` (optional): admin, partner
- `user_id` (optional): Filter by user ID
- `action` (optional): login, logout, upload, download, etc.
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)
- `search` (optional): Search in user name or details
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 50)

**Response (200 OK):**
```json
{
  "count": 1500,
  "next": "/api/v1/admin/activity-logs?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "timestamp": "2025-11-06T10:30:00Z",
      "user_type": "partner",
      "user_id": 2,
      "user_name": "acme_jane",
      "action": "upload",
      "resource_type": "transaction",
      "resource_id": "abc123",
      "details": {"file_name": "invoice.edi", "size": 2048},
      "ip_address": "192.168.1.100"
    }
  ]
}
```

#### Export Activity Logs

**Endpoint:** `GET /modern-edi/api/v1/admin/activity-logs/export`

**Authentication:** Django session (staff required)

**Query Parameters:** Same as List Activity Logs

**Response (200 OK):**
- Content-Type: `text/csv`
- Content-Disposition: `attachment; filename="activity_logs.csv"`
- Body: CSV file content


## Partner Portal API

### Authentication

#### Login

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/auth/login`

**Authentication:** None (public endpoint)

**Request Body:**
```json
{
  "username": "acme_john",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "acme_john",
    "email": "john@acme.com",
    "first_name": "John",
    "last_name": "Smith",
    "role": "partner_admin",
    "partner_id": "123",
    "partner_name": "Acme Corp"
  },
  "permissions": {
    "can_view_transactions": true,
    "can_upload_files": true,
    "can_download_files": true,
    "can_view_reports": true,
    "can_manage_settings": true
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account locked (too many failed attempts)

#### Logout

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/auth/logout`

**Authentication:** Partner session required

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### Get Current User

**Endpoint:** `GET /modern-edi/api/v1/partner-portal/auth/me`

**Authentication:** Partner session required

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "acme_john",
  "email": "john@acme.com",
  "first_name": "John",
  "last_name": "Smith",
  "role": "partner_admin",
  "partner_id": "123",
  "partner_name": "Acme Corp",
  "permissions": {
    "can_view_transactions": true,
    "can_upload_files": true,
    "can_download_files": true,
    "can_view_reports": true,
    "can_manage_settings": true
  }
}
```


#### Forgot Password

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/auth/forgot-password`

**Authentication:** None (public endpoint)

**Request Body:**
```json
{
  "username": "acme_john"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset link sent to your email"
}
```

#### Reset Password

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/auth/reset-password`

**Authentication:** None (requires valid token)

**Request Body:**
```json
{
  "token": "reset-token-from-email",
  "new_password": "NewSecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid or expired token
- `400 Bad Request`: Password does not meet requirements

#### Change Password

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/auth/change-password`

**Authentication:** Partner session required

**Request Body:**
```json
{
  "current_password": "OldPass123!",
  "new_password": "NewSecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Current password incorrect
- `400 Bad Request`: New password does not meet requirements


### Dashboard

#### Get Partner Dashboard Metrics

**Endpoint:** `GET /modern-edi/api/v1/partner-portal/dashboard/metrics`

**Authentication:** Partner session required

**Response (200 OK):**
```json
{
  "sent_count": 600,
  "received_count": 634,
  "pending_count": 15,
  "error_count": 8,
  "recent_transactions": [
    {
      "id": "abc123",
      "date": "2025-11-06T10:30:00Z",
      "type": "850",
      "po_number": "PO-2025-001",
      "status": "sent",
      "direction": "sent"
    }
  ],
  "partner_info": {
    "name": "Acme Corp",
    "contact_email": "contact@acme.com",
    "connection_status": "active",
    "last_connection": "2025-11-06T10:00:00Z"
  }
}
```

### Transactions

#### List Partner Transactions

**Endpoint:** `GET /modern-edi/api/v1/partner-portal/transactions`

**Authentication:** Partner session required

**Query Parameters:**
- `search` (optional): Search by PO number or document type
- `status` (optional): pending, sent, acknowledged, failed
- `direction` (optional): sent, received
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 50)

**Response (200 OK):**
```json
{
  "count": 234,
  "next": "/api/v1/partner-portal/transactions?page=2",
  "previous": null,
  "results": [
    {
      "id": "abc123",
      "date": "2025-11-06T09:15:00Z",
      "type": "850",
      "po_number": "PO-2025-001",
      "status": "acknowledged",
      "direction": "sent",
      "file_size": 2048
    }
  ]
}
```

#### Get Transaction Details

**Endpoint:** `GET /modern-edi/api/v1/partner-portal/transactions/<id>`

**Authentication:** Partner session required

**Response (200 OK):**
```json
{
  "id": "abc123",
  "date": "2025-11-06T09:15:00Z",
  "type": "850",
  "po_number": "PO-2025-001",
  "status": "acknowledged",
  "direction": "sent",
  "file_size": 2048,
  "raw_content": "ISA*00*...",
  "parsed_data": {...},
  "acknowledgment": {
    "status": "accepted",
    "timestamp": "2025-11-06T09:20:00Z",
    "message": "Transaction accepted"
  }
}
```


### File Operations

#### Upload File

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/files/upload`

**Authentication:** Partner session required

**Permission Required:** `can_upload_files`

**Request:**
- Content-Type: `multipart/form-data`
- Body Parameters:
  - `file` (required): The EDI file to upload
  - `document_type` (required): Document type (850, 810, etc.)
  - `po_number` (optional): Purchase order number

**Response (201 Created):**
```json
{
  "success": true,
  "transaction_id": "abc123",
  "message": "File uploaded successfully"
}
```

**Error Responses:**
- `400 Bad Request`: File too large (max 10 MB)
- `400 Bad Request`: Invalid file format
- `403 Forbidden`: Insufficient permissions

#### List Downloadable Files

**Endpoint:** `GET /modern-edi/api/v1/partner-portal/files/download`

**Authentication:** Partner session required

**Permission Required:** `can_download_files`

**Response (200 OK):**
```json
{
  "count": 15,
  "files": [
    {
      "id": "def456",
      "name": "invoice_001.edi",
      "document_type": "810",
      "date": "2025-11-06T08:00:00Z",
      "size": 3072,
      "downloaded": false,
      "download_timestamp": null
    }
  ]
}
```

#### Download File

**Endpoint:** `GET /modern-edi/api/v1/partner-portal/files/download/<id>`

**Authentication:** Partner session required

**Permission Required:** `can_download_files`

**Response (200 OK):**
- Content-Type: `application/octet-stream`
- Content-Disposition: `attachment; filename="invoice_001.edi"`
- Body: File contents

#### Bulk Download

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/files/download/bulk`

**Authentication:** Partner session required

**Permission Required:** `can_download_files`

**Request Body:**
```json
{
  "file_ids": ["def456", "def457", "def458"]
}
```

**Response (200 OK):**
- Content-Type: `application/zip`
- Content-Disposition: `attachment; filename="files.zip"`
- Body: ZIP archive containing selected files


### Settings

#### Get Partner Settings

**Endpoint:** `GET /modern-edi/api/v1/partner-portal/settings`

**Authentication:** Partner session required

**Response (200 OK):**
```json
{
  "partner": {
    "id": "123",
    "name": "Acme Corp",
    "contact_name": "John Smith",
    "contact_email": "john@acme.com",
    "contact_phone": "+1-555-0123"
  },
  "connection": {
    "type": "sftp",
    "status": "active",
    "last_connection": "2025-11-06T10:00:00Z"
  },
  "api_documentation_url": "/docs/api"
}
```

#### Update Contact Information

**Endpoint:** `PUT /modern-edi/api/v1/partner-portal/settings/contact`

**Authentication:** Partner session required

**Permission Required:** `can_manage_settings`

**Request Body:**
```json
{
  "contact_name": "John Smith",
  "contact_email": "john.smith@acme.com",
  "contact_phone": "+1-555-0124"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Contact information updated successfully"
}
```

**Error Responses:**
- `403 Forbidden`: Insufficient permissions (requires partner_admin role)

#### Test Connection

**Endpoint:** `POST /modern-edi/api/v1/partner-portal/settings/test-connection`

**Authentication:** Partner session required

**Permission Required:** `can_manage_settings`

**Response (200 OK):**
```json
{
  "success": true,
  "connection_type": "sftp",
  "status": "connected",
  "message": "Connection test successful",
  "details": {
    "host": "sftp.acme.com",
    "port": 22,
    "response_time_ms": 150
  }
}
```

**Error Response (Connection Failed):**
```json
{
  "success": false,
  "connection_type": "sftp",
  "status": "failed",
  "message": "Connection test failed",
  "error": "Unable to connect to host"
}
```


## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful deletion) |
| 400 | Bad Request - Invalid parameters or validation error |
| 401 | Unauthorized - Not authenticated |
| 403 | Forbidden - Insufficient permissions or account locked |
| 404 | Not Found - Resource does not exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## Common Error Responses

### Authentication Errors

**Invalid Credentials:**
```json
{
  "error": "INVALID_CREDENTIALS",
  "message": "Invalid username or password"
}
```

**Account Locked:**
```json
{
  "error": "ACCOUNT_LOCKED",
  "message": "Account locked due to too many failed login attempts. Try again in 15 minutes."
}
```

**Session Expired:**
```json
{
  "error": "SESSION_EXPIRED",
  "message": "Your session has expired. Please log in again."
}
```

### Permission Errors

**Insufficient Permissions:**
```json
{
  "error": "PERMISSION_DENIED",
  "message": "You do not have permission to perform this action"
}
```

### Validation Errors

**File Too Large:**
```json
{
  "error": "FILE_TOO_LARGE",
  "message": "File size exceeds maximum limit of 10 MB"
}
```

**Invalid File Format:**
```json
{
  "error": "INVALID_FILE_TYPE",
  "message": "File format not supported. Accepted formats: .edi, .x12, .txt, .xml"
}
```

**Password Requirements:**
```json
{
  "error": "INVALID_PASSWORD",
  "message": "Password must be at least 8 characters and contain uppercase, lowercase, number, and special character"
}
```


## Security Features

### Session Management

**Admin & Modern EDI:**
- Django session cookies
- HttpOnly and Secure flags
- SameSite attribute for CSRF protection
- Session expires on browser close

**Partner Portal:**
- Custom session management
- 30-minute inactivity timeout
- Automatic logout on timeout
- Session invalidated on password change

### Account Security

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

**Account Lockout:**
- 5 failed login attempts trigger lockout
- 15-minute lockout duration
- Automatic unlock after duration
- Admin can manually unlock

### Data Isolation

**Partner Portal:**
- All queries automatically filtered by partner_id
- Users can only access their partner's data
- No cross-partner data visibility
- Enforced at middleware level

### Activity Logging

All actions are logged with:
- Timestamp
- User identification
- Action performed
- Resource affected
- IP address
- User agent

## Rate Limiting

**Partner Portal:**
- Login attempts: 5 per 15 minutes per username
- File uploads: 100 per hour per user
- API requests: 1000 per hour per user

**Admin Dashboard:**
- No rate limiting (trusted internal users)

## Best Practices

### For Administrators

1. **Regular Audits**: Review activity logs weekly
2. **Permission Reviews**: Audit user permissions quarterly
3. **Monitor Metrics**: Check dashboard daily for anomalies
4. **Secure Passwords**: Enforce strong password policies
5. **Prompt Offboarding**: Deactivate users immediately when they leave

### For Partner Users

1. **Strong Passwords**: Use unique, complex passwords
2. **Regular Changes**: Change password every 90 days
3. **Secure Logout**: Always log out when finished
4. **Report Issues**: Contact admin for suspicious activity
5. **Keep Contact Info Current**: Update email and phone promptly

### For API Integration

1. **Use HTTPS**: Always use HTTPS in production
2. **Secure Credentials**: Store credentials securely
3. **Handle Errors**: Implement proper error handling
4. **Respect Rate Limits**: Implement backoff strategies
5. **Monitor Logs**: Review activity logs regularly


## Code Examples

### Python - Admin Dashboard

```python
import requests

# Login to Django admin first to get session cookie
session = requests.Session()
session.post('http://localhost:8080/admin/login/', data={
    'username': 'admin',
    'password': 'password'
})

# Get dashboard metrics
response = session.get('http://localhost:8080/modern-edi/api/v1/admin/dashboard/metrics')
metrics = response.json()
print(f"Total Partners: {metrics['total_partners']}")
print(f"Success Rate: {metrics['success_rate']}%")

# List partners
response = session.get('http://localhost:8080/modern-edi/api/v1/admin/partners/')
partners = response.json()
for partner in partners['results']:
    print(f"{partner['name']}: {partner['transaction_count']} transactions")

# Create partner user
response = session.post(
    'http://localhost:8080/modern-edi/api/v1/admin/partners/123/users',
    json={
        'username': 'new_user',
        'email': 'user@partner.com',
        'first_name': 'New',
        'last_name': 'User',
        'password': 'SecurePass123!',
        'role': 'partner_user'
    }
)
print(response.json())
```

### Python - Partner Portal

```python
import requests

# Login
session = requests.Session()
response = session.post(
    'http://localhost:8080/modern-edi/api/v1/partner-portal/auth/login',
    json={
        'username': 'partner_user',
        'password': 'password'
    }
)
user_data = response.json()
print(f"Logged in as: {user_data['user']['first_name']}")

# Get dashboard metrics
response = session.get(
    'http://localhost:8080/modern-edi/api/v1/partner-portal/dashboard/metrics'
)
metrics = response.json()
print(f"Sent: {metrics['sent_count']}, Received: {metrics['received_count']}")

# Upload file
with open('purchase_order.edi', 'rb') as f:
    response = session.post(
        'http://localhost:8080/modern-edi/api/v1/partner-portal/files/upload',
        files={'file': f},
        data={'document_type': '850', 'po_number': 'PO-2025-001'}
    )
print(response.json())

# List transactions
response = session.get(
    'http://localhost:8080/modern-edi/api/v1/partner-portal/transactions',
    params={'status': 'sent', 'page_size': 10}
)
transactions = response.json()
for txn in transactions['results']:
    print(f"{txn['po_number']}: {txn['status']}")

# Download file
response = session.get(
    'http://localhost:8080/modern-edi/api/v1/partner-portal/files/download/def456'
)
with open('invoice.edi', 'wb') as f:
    f.write(response.content)

# Logout
session.post('http://localhost:8080/modern-edi/api/v1/partner-portal/auth/logout')
```


### JavaScript - Partner Portal

```javascript
// Login
async function login(username, password) {
  const response = await fetch(
    'http://localhost:8080/modern-edi/api/v1/partner-portal/auth/login',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
      credentials: 'include' // Important: include cookies
    }
  );
  return response.json();
}

// Get dashboard metrics
async function getDashboardMetrics() {
  const response = await fetch(
    'http://localhost:8080/modern-edi/api/v1/partner-portal/dashboard/metrics',
    { credentials: 'include' }
  );
  return response.json();
}

// Upload file
async function uploadFile(file, documentType, poNumber) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('document_type', documentType);
  if (poNumber) formData.append('po_number', poNumber);
  
  const response = await fetch(
    'http://localhost:8080/modern-edi/api/v1/partner-portal/files/upload',
    {
      method: 'POST',
      body: formData,
      credentials: 'include'
    }
  );
  return response.json();
}

// List transactions
async function listTransactions(filters = {}) {
  const params = new URLSearchParams(filters);
  const response = await fetch(
    `http://localhost:8080/modern-edi/api/v1/partner-portal/transactions?${params}`,
    { credentials: 'include' }
  );
  return response.json();
}

// Download file
async function downloadFile(fileId) {
  const response = await fetch(
    `http://localhost:8080/modern-edi/api/v1/partner-portal/files/download/${fileId}`,
    { credentials: 'include' }
  );
  const blob = await response.blob();
  
  // Trigger download
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = response.headers.get('Content-Disposition').split('filename=')[1];
  a.click();
}

// Usage
(async () => {
  await login('partner_user', 'password');
  const metrics = await getDashboardMetrics();
  console.log('Dashboard metrics:', metrics);
  
  const transactions = await listTransactions({ status: 'sent' });
  console.log('Transactions:', transactions);
})();
```

## Related Documentation

- [Admin Dashboard Guide](ADMIN_DASHBOARD_GUIDE.md) - User guide for administrators
- [Partner Portal Guide](PARTNER_PORTAL_GUIDE.md) - User guide for partners
- [User Management Guide](USER_MANAGEMENT_GUIDE.md) - Managing users and permissions
- [API Documentation](API_DOCUMENTATION.md) - Original REST API documentation
- [Security Guide](SECURITY.md) - Security best practices

## Support

For additional assistance:
- Review user guides
- Check system logs
- Contact system administrator
- Submit GitHub issues
