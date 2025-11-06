# Partner Management System

## Overview

The Modern EDI Interface includes a comprehensive partner management system that supports multiple trading partners with flexible communication methods (SFTP and API).

## ✅ System Capabilities

### Multiple Partners Support
- ✅ **Unlimited Partners**: Add as many trading partners as needed
- ✅ **Unique Identification**: Each partner has a unique partner_id
- ✅ **Contact Management**: Store contact information for each partner
- ✅ **Status Tracking**: Active, Inactive, Testing, Suspended statuses

### Communication Methods

Each partner can be configured with:
- **SFTP Only**: Files exchanged via SFTP server
- **API Only**: Files exchanged via REST API
- **Both SFTP and API**: Dual communication channels
- **Manual**: Manual file upload/download

## Partner Model

### Basic Information
```python
Partner:
  - partner_id: Unique identifier (e.g., "ACME001")
  - name: Company name
  - display_name: Display name in UI
  - contact_name: Contact person
  - contact_email: Email address
  - contact_phone: Phone number
  - status: active | inactive | testing | suspended
```

### EDI Configuration
```python
  - edi_format: X12 | EDIFACT | XML | JSON
  - sender_id: ISA Sender ID (X12) or UNB Sender (EDIFACT)
  - receiver_id: ISA Receiver ID (X12) or UNB Receiver (EDIFACT)
  - supported_document_types: ["850", "810", "856", ...]
```

### Communication Settings
```python
  - communication_method: sftp | api | both | manual
```

## SFTP Configuration

### PartnerSFTPConfig Model

Each partner with SFTP support has a dedicated SFTP configuration:

```python
PartnerSFTPConfig:
  # Connection Settings
  - host: SFTP server hostname/IP
  - port: SFTP port (default: 22)
  - username: SFTP username
  
  # Authentication
  - auth_method: password | key | both
  - password: SFTP password (encrypted)
  - private_key_path: Path to SSH private key
  
  # Directory Settings
  - inbound_directory: /inbound (files FROM partner)
  - outbound_directory: /outbound (files TO partner)
  - archive_directory: /archive (optional)
  
  # File Patterns
  - inbound_file_pattern: *.edi
  - outbound_file_pattern: {document_type}_{timestamp}.edi
  
  # Polling Settings
  - poll_enabled: true/false
  - poll_interval: 300 seconds (5 minutes)
  
  # Connection Status
  - last_connection_test: timestamp
  - last_connection_status: success/failed
```

### SFTP Features

**Inbound (Receiving from Partner):**
- Automatic polling for new files
- Configurable file patterns
- Archive processed files
- Error handling and retry logic

**Outbound (Sending to Partner):**
- Automatic file upload
- Custom file naming patterns
- Delivery confirmation
- Retry on failure

**Security:**
- SSH key authentication (recommended)
- Password authentication
- Encrypted credentials storage
- Connection timeout settings

## API Configuration

### PartnerAPIConfig Model

Each partner with API support has a dedicated API configuration:

```python
PartnerAPIConfig:
  # Endpoint Settings
  - base_url: https://partner-api.example.com
  - inbound_endpoint: /edi/inbound
  - outbound_endpoint: /edi/outbound
  
  # Authentication
  - auth_method: none | basic | bearer | api_key | oauth2
  - api_key: API key for authentication
  - api_secret: API secret (encrypted)
  - username: For basic auth
  - password: For basic auth
  - bearer_token: For bearer token auth
  
  # OAuth 2.0 Settings
  - oauth_token_url: Token endpoint
  - oauth_client_id: Client ID
  - oauth_client_secret: Client secret
  - oauth_scope: Requested scopes
  
  # Request Settings
  - content_type: application/json
  - custom_headers: {...}
  - timeout: 30 seconds
  - retry_attempts: 3
  - retry_delay: 5 seconds
  
  # Webhook Settings
  - webhook_enabled: true/false
  - webhook_url: URL for partner callbacks
  - webhook_secret: Secret for validation
  
  # Connection Status
  - last_connection_test: timestamp
  - last_connection_status: success/failed
```

### API Features

**Inbound (Receiving from Partner):**
- Webhook support for push notifications
- REST API endpoint for file upload
- Authentication validation
- Automatic processing

**Outbound (Sending to Partner):**
- HTTP POST to partner's API
- Multiple auth methods supported
- Retry logic with exponential backoff
- Response validation

**Security:**
- Multiple authentication methods
- OAuth 2.0 support
- API key management
- Webhook signature validation
- HTTPS enforcement

## Partner Transaction Tracking

### PartnerTransaction Model

Links partners to transactions and tracks communication:

```python
PartnerTransaction:
  - partner: Link to Partner
  - transaction: Link to EDITransaction
  
  # Transmission Tracking
  - sent_via: sftp | api | manual
  - sent_at: timestamp
  - received_via: sftp | api | manual
  - received_at: timestamp
  
  # Status
  - transmission_status: pending | sent | acknowledged | failed
  - error_message: Error details if failed
  
  # Metadata
  - metadata: Additional tracking data
```

## Usage Examples

### Example 1: SFTP-Only Partner

```python
# Create partner
partner = Partner.objects.create(
    partner_id="ACME001",
    name="ACME Corporation",
    communication_method="sftp",
    status="active",
    edi_format="X12",
    sender_id="ACME",
    receiver_id="MYCOMPANY",
    supported_document_types=["850", "810", "856"]
)

# Configure SFTP
sftp_config = PartnerSFTPConfig.objects.create(
    partner=partner,
    host="sftp.acme.com",
    port=22,
    username="mycompany",
    auth_method="key",
    private_key_path="/keys/acme_rsa",
    inbound_directory="/from_acme",
    outbound_directory="/to_acme",
    poll_enabled=True,
    poll_interval=300
)
```

### Example 2: API-Only Partner

```python
# Create partner
partner = Partner.objects.create(
    partner_id="WIDGET001",
    name="Widget Industries",
    communication_method="api",
    status="active",
    edi_format="JSON",
    supported_document_types=["850", "810"]
)

# Configure API
api_config = PartnerAPIConfig.objects.create(
    partner=partner,
    base_url="https://api.widget.com",
    inbound_endpoint="/edi/receive",
    outbound_endpoint="/edi/send",
    auth_method="api_key",
    api_key="widget_api_key_12345",
    content_type="application/json",
    timeout=30,
    retry_attempts=3
)
```

### Example 3: Both SFTP and API

```python
# Create partner
partner = Partner.objects.create(
    partner_id="GLOBAL001",
    name="Global Trading Co",
    communication_method="both",
    status="active",
    edi_format="X12"
)

# Configure both SFTP and API
sftp_config = PartnerSFTPConfig.objects.create(
    partner=partner,
    host="sftp.global.com",
    # ... SFTP settings
)

api_config = PartnerAPIConfig.objects.create(
    partner=partner,
    base_url="https://api.global.com",
    # ... API settings
)
```

## Integration with Modern EDI Interface

### Transaction Creation

When creating a transaction, you can link it to a partner:

```python
from usersys.modern_edi_models import EDITransaction
from usersys.partner_models import Partner, PartnerTransaction

# Get partner
partner = Partner.objects.get(partner_id="ACME001")

# Create transaction
transaction = EDITransaction.objects.create(
    folder="outbox",
    partner_name=partner.name,
    partner_id=partner.partner_id,
    document_type="850",
    # ... other fields
)

# Link to partner
partner_txn = PartnerTransaction.objects.create(
    partner=partner,
    transaction=transaction,
    transmission_status="pending"
)
```

### Automatic Transmission

When sending a transaction, the system automatically:

1. Checks partner's communication method
2. Uses SFTP if configured
3. Falls back to API if SFTP fails (when both are configured)
4. Updates PartnerTransaction with transmission details
5. Tracks acknowledgments

## Management Commands

### Test Partner Connection

```bash
# Test SFTP connection
python manage.py test_partner_connection ACME001 --method sftp

# Test API connection
python manage.py test_partner_connection ACME001 --method api
```

### Poll for Inbound Files

```bash
# Poll all active SFTP partners
python manage.py poll_partner_files

# Poll specific partner
python manage.py poll_partner_files --partner ACME001
```

### Send Outbound Files

```bash
# Send all pending outbound files
python manage.py send_partner_files

# Send for specific partner
python manage.py send_partner_files --partner ACME001
```

## Admin Interface

Partners can be managed through Django admin:

```
http://localhost:8080/admin/usersys/partner/
```

Features:
- Add/edit/delete partners
- Configure SFTP settings
- Configure API settings
- Test connections
- View transaction history
- Monitor transmission status

## API Endpoints

### Partner Management API

```
GET    /modern-edi/api/v1/partners/              # List all partners
GET    /modern-edi/api/v1/partners/{id}/         # Get partner details
POST   /modern-edi/api/v1/partners/              # Create partner
PUT    /modern-edi/api/v1/partners/{id}/         # Update partner
DELETE /modern-edi/api/v1/partners/{id}/         # Delete partner

GET    /modern-edi/api/v1/partners/{id}/sftp/    # Get SFTP config
PUT    /modern-edi/api/v1/partners/{id}/sftp/    # Update SFTP config
POST   /modern-edi/api/v1/partners/{id}/sftp/test/  # Test SFTP connection

GET    /modern-edi/api/v1/partners/{id}/api/     # Get API config
PUT    /modern-edi/api/v1/partners/{id}/api/     # Update API config
POST   /modern-edi/api/v1/partners/{id}/api/test/   # Test API connection

GET    /modern-edi/api/v1/partners/{id}/transactions/  # Get partner transactions
```

## Security Considerations

### Credential Storage
- **Production**: Use Django's encryption or external secret management
- **Development**: Store in database (encrypted)
- **Best Practice**: Use environment variables or secret managers

### SFTP Security
- Prefer SSH key authentication over passwords
- Use strong passwords if password auth is required
- Restrict SFTP user permissions
- Use dedicated SFTP users per partner
- Monitor connection logs

### API Security
- Use HTTPS only (enforce in production)
- Rotate API keys regularly
- Implement rate limiting
- Validate webhook signatures
- Use OAuth 2.0 when available
- Monitor API usage

## Monitoring and Alerts

### Connection Monitoring
- Track last successful connection
- Alert on connection failures
- Monitor polling intervals
- Track transmission success rates

### Transaction Monitoring
- Monitor pending transactions
- Alert on failed transmissions
- Track acknowledgment rates
- Monitor processing times

## Troubleshooting

### SFTP Issues

**Connection Timeout:**
- Check firewall rules
- Verify host and port
- Test with SFTP client manually

**Authentication Failed:**
- Verify username/password
- Check SSH key permissions
- Ensure key format is correct

**File Not Found:**
- Verify directory paths
- Check file patterns
- Ensure proper permissions

### API Issues

**401 Unauthorized:**
- Verify API credentials
- Check token expiration
- Refresh OAuth tokens

**Timeout:**
- Increase timeout setting
- Check partner API status
- Verify network connectivity

**Invalid Response:**
- Check content-type
- Verify API endpoint
- Review partner API documentation

## Summary

The partner management system provides:

✅ **Multiple Partners**: Unlimited trading partners
✅ **SFTP Support**: Full SFTP configuration and automation
✅ **API Support**: REST API with multiple auth methods
✅ **Dual Communication**: Both SFTP and API per partner
✅ **Automatic Polling**: Scheduled file retrieval
✅ **Automatic Sending**: Scheduled file transmission
✅ **Connection Testing**: Test connectivity before use
✅ **Transaction Tracking**: Complete audit trail
✅ **Error Handling**: Retry logic and error reporting
✅ **Security**: Encrypted credentials and secure protocols

The system is production-ready and supports enterprise-level EDI operations!
