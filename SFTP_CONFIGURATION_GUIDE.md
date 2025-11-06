# SFTP Configuration Management Guide

This guide explains how to configure and manage SFTP access for trading partners in the Bots EDI system.

## Table of Contents
1. [Overview](#overview)
2. [Admin Configuration](#admin-configuration)
3. [API Endpoints](#api-endpoints)
4. [Configuration Fields](#configuration-fields)
5. [Authentication Methods](#authentication-methods)
6. [Directory Structure](#directory-structure)
7. [Testing Connections](#testing-connections)
8. [Security Best Practices](#security-best-practices)
9. [Troubleshooting](#troubleshooting)

## Overview

The SFTP Configuration Management system allows administrators to set up secure SFTP access for each trading partner. Partners can use SFTP to:
- Upload inbound EDI files (POs, invoices, etc.)
- Download outbound EDI files (acknowledgments, shipping notices, etc.)
- Archive processed files

### Key Features
- ✅ Per-partner SFTP configuration
- ✅ Multiple authentication methods (password, SSH key, both)
- ✅ Customizable directory structure
- ✅ File pattern matching
- ✅ Automatic polling
- ✅ Connection testing
- ✅ Activity logging

## Admin Configuration

### Creating SFTP Configuration

**Endpoint**: `POST /api/v1/admin/partners/{partner_id}/sftp-config`

**Required Steps**:
1. Log in to the admin dashboard
2. Navigate to Partner Management
3. Select the partner
4. Click "Configure SFTP"
5. Fill in the configuration form

**Example Request**:
```json
{
  "host": "sftp.example.com",
  "port": 22,
  "username": "partner001_sftp",
  "auth_method": "password",
  "password": "SecureP@ssw0rd!123",
  "inbound_directory": "/partners/partner001/inbound",
  "outbound_directory": "/partners/partner001/outbound",
  "archive_directory": "/partners/partner001/archive",
  "inbound_file_pattern": "*.edi",
  "outbound_file_pattern": "{document_type}_{timestamp}.edi",
  "timeout": 30,
  "passive_mode": true,
  "poll_enabled": true,
  "poll_interval": 300
}
```

**Example Response**:
```json
{
  "success": true,
  "message": "SFTP configuration created successfully",
  "config": {
    "host": "sftp.example.com",
    "port": 22,
    "username": "partner001_sftp",
    "auth_method": "password",
    "inbound_directory": "/partners/partner001/inbound",
    "outbound_directory": "/partners/partner001/outbound",
    "connection_string": "sftp://partner001_sftp@sftp.example.com:22",
    "is_active": true,
    "created_at": "2025-11-06T20:00:00Z"
  }
}
```

### Updating SFTP Configuration

**Endpoint**: `PUT /api/v1/admin/partners/{partner_id}/sftp-config`

Update any configuration field. Only include fields you want to change.

**Example Request**:
```json
{
  "password": "NewSecureP@ssw0rd!456",
  "poll_interval": 600,
  "is_active": true
}
```

### Deleting SFTP Configuration

**Endpoint**: `DELETE /api/v1/admin/partners/{partner_id}/sftp-config`

Removes SFTP configuration for a partner. The partner's communication method will be updated accordingly.

### Viewing SFTP Configuration

**Endpoint**: `GET /api/v1/admin/partners/{partner_id}/sftp-config`

Returns current SFTP configuration (passwords are not returned, only a flag indicating if password is set).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/partners/{id}/sftp-config` | Get SFTP configuration |
| POST | `/api/v1/admin/partners/{id}/sftp-config` | Create SFTP configuration |
| PUT | `/api/v1/admin/partners/{id}/sftp-config` | Update SFTP configuration |
| DELETE | `/api/v1/admin/partners/{id}/sftp-config` | Delete SFTP configuration |
| POST | `/api/v1/admin/partners/{id}/sftp-config/test` | Test SFTP connection |
| POST | `/api/v1/admin/sftp/generate-credentials` | Generate secure credentials |

## Configuration Fields

### Connection Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `host` | string | Yes | - | SFTP server hostname or IP address |
| `port` | integer | No | 22 | SFTP port number |
| `username` | string | Yes | - | SFTP username |
| `timeout` | integer | No | 30 | Connection timeout in seconds |
| `passive_mode` | boolean | No | true | Use passive mode for SFTP |

### Authentication Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `auth_method` | string | No | key | Authentication method: `password`, `key`, or `both` |
| `password` | string | Conditional | - | Password (required if auth_method is `password` or `both`) |
| `private_key_path` | string | Conditional | - | Path to SSH private key (required if auth_method is `key` or `both`) |

### Directory Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `inbound_directory` | string | No | /inbound | Directory to pick up files from partner |
| `outbound_directory` | string | No | /outbound | Directory to send files to partner |
| `archive_directory` | string | No | - | Directory to archive processed files (optional) |

### File Pattern Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `inbound_file_pattern` | string | No | *.edi | Pattern for inbound files (e.g., `*.edi`, `PO_*.x12`) |
| `outbound_file_pattern` | string | No | {document_type}_{timestamp}.edi | Pattern for outbound files (supports variables) |

#### Outbound File Pattern Variables
- `{document_type}` - Document type (850, 810, 856, etc.)
- `{timestamp}` - Current timestamp
- `{partner_id}` - Partner identifier
- `{date}` - Current date (YYYYMMDD)
- `{time}` - Current time (HHMMSS)

**Examples**:
- `{document_type}_{partner_id}_{timestamp}.edi`  → `850_ACME001_20251106120000.edi`
- `PO_{date}_{time}.x12` → `PO_20251106_120000.x12`
- `{partner_id}_{document_type}.edi` → `ACME001_850.edi`

### Polling Settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `poll_enabled` | boolean | No | true | Enable automatic polling for new files |
| `poll_interval` | integer | No | 300 | Polling interval in seconds (5 minutes) |

### Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `is_active` | boolean | Whether SFTP configuration is active |
| `last_connection_test` | datetime | Timestamp of last connection test |
| `last_connection_status` | string | Result of last connection test (`success`, `failed`, `auth_failed`) |

## Authentication Methods

### Password Authentication

Most straightforward method. Partner uses username and password to connect.

**Configuration**:
```json
{
  "auth_method": "password",
  "password": "SecureP@ssw0rd!123"
}
```

**Partner Connection**:
```bash
sftp -P 22 partner001_sftp@sftp.example.com
# Enter password when prompted
```

### SSH Key Authentication

More secure method using public/private key pairs.

**Configuration**:
```json
{
  "auth_method": "key",
  "private_key_path": "/etc/bots/keys/partner001_rsa"
}
```

**Setup Steps**:
1. Generate SSH key pair on SFTP server
2. Add partner's public key to authorized_keys
3. Provide private key path in configuration (for Bots to use)
4. Give partner their private key

**Partner Connection**:
```bash
sftp -i ~/.ssh/partner001_rsa -P 22 partner001_sftp@sftp.example.com
```

### Combined Authentication

Requires both password and key for maximum security.

**Configuration**:
```json
{
  "auth_method": "both",
  "password": "SecureP@ssw0rd!123",
  "private_key_path": "/etc/bots/keys/partner001_rsa"
}
```

## Directory Structure

### Recommended Structure

```
/partners/
├── partner001/
│   ├── inbound/         # Partner uploads files here
│   ├── outbound/        # Bots places files here for partner
│   └── archive/         # Processed files moved here
├── partner002/
│   ├── inbound/
│   ├── outbound/
│   └── archive/
└── ...
```

### Directory Permissions

**Inbound Directory**:
- Partner: Read, Write, Execute
- Bots: Read, Execute
- Purpose: Partner uploads files; Bots reads them

**Outbound Directory**:
- Partner: Read, Execute
- Bots: Read, Write, Execute
- Purpose: Bots writes files; Partner downloads them

**Archive Directory**:
- Partner: No access
- Bots: Read, Write, Execute
- Purpose: Bots moves processed files here

### Creating Directories

Directories must be created on the SFTP server manually or via automation script:

```bash
# On SFTP server
sudo mkdir -p /partners/partner001/{inbound,outbound,archive}
sudo chown sftpuser:sftpgroup /partners/partner001/{inbound,outbound,archive}
sudo chmod 755 /partners/partner001/{inbound,outbound,archive}
```

## Testing Connections

### Test Connection Endpoint

**Endpoint**: `POST /api/v1/admin/partners/{partner_id}/sftp-config/test`

Tests SFTP connection and verifies directory access.

**Example Response** (Success):
```json
{
  "success": true,
  "message": "Connection successful",
  "details": {
    "connection_string": "sftp://partner001_sftp@sftp.example.com:22",
    "auth_method": "password",
    "directories": [
      {
        "path": "/partners/partner001/inbound",
        "exists": true,
        "type": "inbound"
      },
      {
        "path": "/partners/partner001/outbound",
        "exists": true,
        "type": "outbound"
      },
      {
        "path": "/partners/partner001/archive",
        "exists": false,
        "type": "archive"
      }
    ]
  }
}
```

**Example Response** (Authentication Failed):
```json
{
  "success": false,
  "message": "Authentication failed. Please check credentials.",
  "details": {
    "error": "Authentication failed."
  }
}
```

**Example Response** (Connection Failed):
```json
{
  "success": false,
  "message": "Connection failed: [Errno 111] Connection refused",
  "details": {
    "error": "[Errno 111] Connection refused"
  }
}
```

### Manual Testing

Test SFTP connection manually from command line:

```bash
# Test with password
sftp -P 22 username@hostname

# Test with key
sftp -i /path/to/private_key -P 22 username@hostname

# List files in directory
sftp> ls /inbound

# Upload file
sftp> put test.edi /inbound/

# Download file
sftp> get /outbound/850_20251106.edi

# Exit
sftp> exit
```

## Security Best Practices

### 1. Use Strong Passwords
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Use password generator (available via API)

**Generate Credentials**:
```bash
POST /api/v1/admin/sftp/generate-credentials
{
  "username_prefix": "PARTNER001"
}
```

**Response**:
```json
{
  "success": true,
  "credentials": {
    "username": "PARTNER001_a3f9e2b8",
    "password": "Xy7!mK#9pL@2nQ$5"
  }
}
```

### 2. Prefer SSH Key Authentication
- More secure than passwords
- Harder to compromise
- Can be rotated easily

### 3. Use Unique Credentials Per Partner
- Never reuse credentials
- Easier to revoke access
- Better auditability

### 4. Regular Password Rotation
- Change passwords every 90 days
- Rotate SSH keys annually
- Notify partners in advance

### 5. Monitor Activity
- Review connection logs regularly
- Check for failed login attempts
- Set up alerts for suspicious activity

### 6. Restrict IP Access (Optional)
- Whitelist partner IPs on firewall
- Use VPN if possible
- Reduces attack surface

### 7. Enable File Scanning
- Scan uploaded files for malware
- Validate EDI format before processing
- Quarantine suspicious files

### 8. Archive Processed Files
- Keep processed files for audit trail
- Set retention policy (e.g., 90 days)
- Compress old archives

## Troubleshooting

### Connection Refused

**Error**: `Connection failed: [Errno 111] Connection refused`

**Possible Causes**:
- SFTP server is down
- Firewall blocking port 22
- Wrong hostname or port

**Solutions**:
1. Verify SFTP server is running: `sudo systemctl status sshd`
2. Check firewall rules: `sudo firewall-cmd --list-ports`
3. Test connectivity: `telnet sftp.example.com 22`
4. Verify hostname resolves: `nslookup sftp.example.com`

### Authentication Failed

**Error**: `Authentication failed. Please check credentials.`

**Possible Causes**:
- Wrong username or password
- SSH key mismatch
- User account locked or expired

**Solutions**:
1. Verify credentials are correct
2. Check user account status on SFTP server
3. Verify SSH key permissions (600 for private key)
4. Check authorized_keys file on server

### Directory Not Found

**Error**: Directory `/inbound` doesn't exist

**Solutions**:
1. Create directory on SFTP server
2. Verify directory path in configuration
3. Check user permissions for directory
4. Test directory access manually

### Permission Denied

**Error**: `Permission denied` when accessing directory

**Solutions**:
1. Check directory permissions: `ls -la /partners/partner001/`
2. Verify user ownership: `chown sftpuser:sftpgroup /partners/partner001/inbound`
3. Set correct permissions: `chmod 755 /partners/partner001/inbound`
4. Check parent directory permissions

### Timeout Errors

**Error**: `Connection timeout after 30 seconds`

**Solutions**:
1. Increase timeout value in configuration
2. Check network latency
3. Verify no firewall issues
4. Test from different network

### Files Not Being Picked Up

**Problem**: Files uploaded by partner but not processed

**Solutions**:
1. Verify polling is enabled: `poll_enabled: true`
2. Check polling interval (default 5 minutes)
3. Verify file pattern matches uploaded files
4. Check Bots logs for processing errors
5. Verify directory path is correct

## Partner Portal View

Partners can view their SFTP credentials in the partner portal (read-only).

**Endpoint**: `GET /api/v1/partner-portal/sftp-config`

**Response**:
```json
{
  "success": true,
  "sftp_config": {
    "host": "sftp.example.com",
    "port": 22,
    "username": "partner001_sftp",
    "connection_string": "sftp://partner001_sftp@sftp.example.com:22",
    "inbound_directory": "/partners/partner001/inbound",
    "outbound_directory": "/partners/partner001/outbound",
    "last_connection_test": "2025-11-06T19:45:00Z",
    "last_connection_status": "success"
  }
}
```

**Note**: Password and private key are never exposed to partners. They receive credentials securely via email when account is created.

## Activity Logging

All SFTP configuration changes are logged:

**Logged Actions**:
- `sftp_config_created` - Configuration created
- `sftp_config_updated` - Configuration modified
- `sftp_config_deleted` - Configuration removed
- `sftp_connection_tested` - Connection test performed
- `sftp_credentials_generated` - New credentials generated

**View Logs**:
```bash
GET /api/v1/admin/activity-logs?action=sftp_config_created
```

## Integration with Bots EDI

### Automatic File Polling

When `poll_enabled` is true, Bots will automatically:
1. Poll inbound directory every `poll_interval` seconds
2. Download new files matching `inbound_file_pattern`
3. Process files through configured routes
4. Move processed files to archive (if configured)

### Outbound File Delivery

When Bots generates outbound EDI files:
1. Apply `outbound_file_pattern` to generate filename
2. Upload file to partner's outbound directory
3. Log delivery activity
4. Optionally notify partner via email

## Example Workflow

### Complete Setup Example

```python
# 1. Generate credentials
POST /api/v1/admin/sftp/generate-credentials
{
  "username_prefix": "ACME001"
}

# Response: {"username": "ACME001_d7f2a9e1", "password": "Rt9@pL#3kM$7nQ!2"}

# 2. Create SFTP configuration
POST /api/v1/admin/partners/a1b2c3d4-e5f6-7890-abcd-1234567890ab/sftp-config
{
  "host": "sftp.bots-edi.com",
  "port": 22,
  "username": "ACME001_d7f2a9e1",
  "auth_method": "password",
  "password": "Rt9@pL#3kM$7nQ!2",
  "inbound_directory": "/partners/ACME001/inbound",
  "outbound_directory": "/partners/ACME001/outbound",
  "archive_directory": "/partners/ACME001/archive",
  "inbound_file_pattern": "PO_*.edi",
  "outbound_file_pattern": "{document_type}_{date}_{time}.edi",
  "poll_enabled": true,
  "poll_interval": 300
}

# 3. Test connection
POST /api/v1/admin/partners/a1b2c3d4-e5f6-7890-abcd-1234567890ab/sftp-config/test

# 4. Notify partner
# Send email to partner with:
# - SFTP hostname: sftp.bots-edi.com
# - Username: ACME001_d7f2a9e1
# - Password: Rt9@pL#3kM$7nQ!2
# - Inbound directory: /partners/ACME001/inbound
# - Outbound directory: /partners/ACME001/outbound
```

## Support

For additional help:
- Check activity logs for detailed error messages
- Review SFTP server logs
- Contact system administrator
- Reference Bots EDI documentation

## Related Documentation
- [Partner Management Guide](PARTNER_MANAGEMENT.md)
- [Admin Dashboard Guide](ADMIN_DASHBOARD_GUIDE.md)
- [Security Guide](SECURITY.md)
- [API Documentation](API_DOCUMENTATION.md)
