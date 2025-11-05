# Bots EDI REST API Documentation

Version: 1.0  
Base URL: `http://localhost:8080/api`

## Authentication

All API endpoints require authentication using an API key.

### API Key Header
```
X-API-Key: your-api-key-here
```

### Rate Limiting
- Default: 1000 requests per hour per API key
- Rate limit resets hourly
- Exceeding the limit returns HTTP 429

### Response Format
All responses are in JSON format.

**Success Response:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error Response:**
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

## Endpoints

### 1. File Upload

Upload an EDI file for processing.

**Endpoint:** `POST /api/v1/files/upload`

**Permission Required:** `file_upload`

**Request:**
- Content-Type: `multipart/form-data`
- Body Parameters:
  - `file` (required): The EDI file to upload
  - `route` (optional): Route name to process the file
  - `partner` (optional): Trading partner identifier
  - `messagetype` (optional): Message type identifier

**Example:**
```bash
curl -X POST http://localhost:8080/api/v1/files/upload \
  -H "X-API-Key: your-api-key" \
  -F "file=@invoice.edi" \
  -F "route=invoice_route" \
  -F "partner=PARTNER001"
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "file": {
    "name": "invoice.edi",
    "size": 2048,
    "path": "/path/to/infile/invoice.edi",
    "route": "invoice_route",
    "partner": "PARTNER001",
    "messagetype": ""
  }
}
```

**Error Responses:**
- `400 Bad Request`: No file provided
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Upload failed

---

### 2. File Download

Download a processed EDI file.

**Endpoint:** `GET /api/v1/files/download/<file_id>`

**Permission Required:** `file_download`

**Path Parameters:**
- `file_id`: Relative path to the file in the outfile directory

**Example:**
```bash
curl http://localhost:8080/api/v1/files/download/processed/invoice_out.xml \
  -H "X-API-Key: your-api-key" \
  -o invoice_out.xml
```

**Response (200 OK):**
- Content-Type: `application/octet-stream`
- Content-Disposition: `attachment; filename="invoice_out.xml"`
- Body: File contents

**Error Responses:**
- `404 Not Found`: File does not exist
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Download failed

---

### 3. List Files

List available files in infile or outfile directories.

**Endpoint:** `GET /api/v1/files/list`

**Permission Required:** `file_list`

**Query Parameters:**
- `type` (optional): `infile` or `outfile` (default: `outfile`)

**Example:**
```bash
curl "http://localhost:8080/api/v1/files/list?type=outfile" \
  -H "X-API-Key: your-api-key"
```

**Response (200 OK):**
```json
{
  "success": true,
  "type": "outfile",
  "count": 3,
  "files": [
    {
      "name": "invoice_001.xml",
      "path": "processed/invoice_001.xml",
      "size": 4096,
      "modified": 1699564800.0
    },
    {
      "name": "order_002.json",
      "path": "processed/order_002.json",
      "size": 2048,
      "modified": 1699564900.0
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: List operation failed

---

### 4. Execute Route

Execute a Bots translation route.

**Endpoint:** `POST /api/v1/routes/execute`

**Permission Required:** `route_execute`

**Request:**
- Content-Type: `application/json`
- Body:
  ```json
  {
    "route": "route_name"
  }
  ```

**Example:**
```bash
curl -X POST http://localhost:8080/api/v1/routes/execute \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"route": "invoice_route"}'
```

**Response (200 OK):**
```json
{
  "success": true,
  "route": "invoice_route",
  "output": "Engine execution output...",
  "errors": null
}
```

**Response (with errors):**
```json
{
  "success": false,
  "route": "invoice_route",
  "output": "Engine execution output...",
  "errors": "Error details..."
}
```

**Error Responses:**
- `400 Bad Request`: Route name required
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `504 Gateway Timeout`: Route execution timeout (5 minutes)
- `500 Internal Server Error`: Execution failed

---

### 5. Get Reports

Retrieve translation reports.

**Endpoint:** `GET /api/v1/reports`

**Permission Required:** `report_view`

**Query Parameters:**
- `limit` (optional): Maximum number of reports to return (default: 100)
- `status` (optional): Filter by status (`success`, `error`)

**Example:**
```bash
curl "http://localhost:8080/api/v1/reports?limit=50&status=success" \
  -H "X-API-Key: your-api-key"
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 50,
  "reports": [
    {
      "id": 12345,
      "timestamp": "2025-11-05T10:30:00Z",
      "status": "success",
      "type": "INVOIC",
      "partner": "PARTNER001",
      "filename": "invoice_001.edi"
    },
    {
      "id": 12346,
      "timestamp": "2025-11-05T10:31:00Z",
      "status": "error",
      "type": "ORDERS",
      "partner": "PARTNER002",
      "filename": "order_002.edi"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Report retrieval failed

---

### 6. API Status

Get API key status and usage information.

**Endpoint:** `GET /api/v1/status`

**Permission Required:** None (any valid API key)

**Example:**
```bash
curl http://localhost:8080/api/v1/status \
  -H "X-API-Key: your-api-key"
```

**Response (200 OK):**
```json
{
  "success": true,
  "api_key": {
    "name": "Production API Key",
    "user": "admin",
    "is_active": true,
    "rate_limit": 1000,
    "current_usage": 42,
    "usage_reset_time": "2025-11-05T11:00:00Z",
    "last_used": "2025-11-05T10:45:30Z",
    "created_at": "2025-11-01T09:00:00Z",
    "permissions": [
      "file_upload",
      "file_download",
      "file_list",
      "route_execute",
      "report_view"
    ]
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing API key

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing API key |
| 403 | Forbidden - Insufficient permissions or IP not allowed |
| 404 | Not Found - Resource does not exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 504 | Gateway Timeout - Operation took too long |

## Permissions

| Permission | Description |
|------------|-------------|
| `file_upload` | Upload EDI files to the system |
| `file_download` | Download processed EDI files |
| `file_list` | List available files |
| `file_delete` | Delete files (not yet implemented) |
| `route_execute` | Execute Bots translation routes |
| `route_list` | List available routes (not yet implemented) |
| `report_view` | View translation reports |
| `report_download` | Download reports (not yet implemented) |
| `partner_view` | View trading partners (not yet implemented) |
| `partner_manage` | Manage trading partners (not yet implemented) |
| `translate_view` | View translation status (not yet implemented) |
| `channel_view` | View communication channels (not yet implemented) |
| `admin_access` | Full administrative access |

## Security Features

### IP Whitelisting
API keys can be restricted to specific IP addresses. Configure in the Django admin interface.

### Rate Limiting
Each API key has a configurable rate limit (default: 1000 requests/hour). The limit resets every hour.

### Audit Logging
All API requests are logged with:
- Timestamp
- API key used
- Endpoint accessed
- Request method
- IP address
- Response status
- Duration

Access audit logs via:
```bash
python usersys/api_management.py audit 100
```

## Best Practices

1. **Secure API Keys**: Store API keys securely, never commit to version control
2. **Use HTTPS**: Always use HTTPS in production
3. **Rotate Keys**: Regularly rotate API keys
4. **Minimal Permissions**: Grant only necessary permissions
5. **Monitor Usage**: Review audit logs regularly
6. **Set Expiration**: Use expiration dates for temporary access
7. **IP Restrictions**: Whitelist known IP addresses when possible

## Examples

### Python Example
```python
import requests

API_KEY = "your-api-key"
BASE_URL = "http://localhost:8080/api/v1"

headers = {
    "X-API-Key": API_KEY
}

# Upload file
with open("invoice.edi", "rb") as f:
    files = {"file": f}
    data = {"route": "invoice_route"}
    response = requests.post(
        f"{BASE_URL}/files/upload",
        headers=headers,
        files=files,
        data=data
    )
    print(response.json())

# List files
response = requests.get(
    f"{BASE_URL}/files/list",
    headers=headers,
    params={"type": "outfile"}
)
print(response.json())

# Execute route
response = requests.post(
    f"{BASE_URL}/routes/execute",
    headers=headers,
    json={"route": "invoice_route"}
)
print(response.json())
```

### JavaScript Example
```javascript
const API_KEY = "your-api-key";
const BASE_URL = "http://localhost:8080/api/v1";

// Upload file
const formData = new FormData();
formData.append("file", fileInput.files[0]);
formData.append("route", "invoice_route");

fetch(`${BASE_URL}/files/upload`, {
  method: "POST",
  headers: {
    "X-API-Key": API_KEY
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// List files
fetch(`${BASE_URL}/files/list?type=outfile`, {
  headers: {
    "X-API-Key": API_KEY
  }
})
.then(response => response.json())
.then(data => console.log(data));

// Execute route
fetch(`${BASE_URL}/routes/execute`, {
  method: "POST",
  headers: {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ route: "invoice_route" })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Support

For issues or questions:
- Check the main README.md
- Review Bots EDI documentation
- Submit GitHub issues
