# Modern EDI Interface - Setup Guide

## Backend Setup Complete ✅

The backend for the Modern EDI Interface has been fully implemented with the following components:

### Completed Components

1. **Database Models** (`modern_edi_models.py`)
   - EDITransaction model with folder management
   - TransactionHistory model for audit trail
   - Database migration file created

2. **Service Layer**
   - `transaction_manager.py` - Business logic for transactions
   - `file_manager.py` - File system operations
   - `edi_parser.py` - EDI parsing (X12 & EDIFACT)

3. **REST API** (`modern_edi_views.py`, `modern_edi_urls.py`)
   - Transaction CRUD endpoints
   - Transaction actions (move, send, delete)
   - Folder and metadata endpoints
   - Search functionality

4. **Security & Middleware** (`modern_edi_middleware.py`)
   - Rate limiting
   - Security headers
   - Audit logging

5. **Acknowledgment Tracking** (`acknowledgment_tracker.py`)
   - Background job for checking acknowledgments
   - Django management command
   - Statistics and retry logic

6. **File System Structure**
   - `/botssys/modern-edi/inbox/`
   - `/botssys/modern-edi/received/`
   - `/botssys/modern-edi/outbox/`
   - `/botssys/modern-edi/sent/`
   - `/botssys/modern-edi/deleted/`

## Installation Steps

### 1. Run Database Migrations

```bash
cd env/default
python init_modern_edi.py
```

This will:
- Create the folder structure
- Run database migrations
- Verify the setup

### 2. Update Django Settings

The following has already been added to `config/settings.py`:
- `'usersys'` added to `INSTALLED_APPS`

You may want to add these optional settings:

```python
# Modern EDI Configuration
MODERN_EDI_RATE_LIMIT = 60  # Requests per minute
MODERN_EDI_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # React dev server
    'http://localhost:8080',  # Production
]
```

### 3. Configure URL Routing

Add to your main `urls.py` (typically in `bots/urls.py`):

```python
from django.urls import path, include

urlpatterns = [
    # ... existing patterns ...
    path('modern-edi/', include('usersys.modern_edi_urls')),
]
```

### 4. Add Middleware (Optional)

Add to `MIDDLEWARE` in `settings.py`:

```python
MIDDLEWARE = [
    # ... existing middleware ...
    'usersys.modern_edi_middleware.RateLimitMiddleware',
    'usersys.modern_edi_middleware.SecurityHeadersMiddleware',
    'usersys.modern_edi_middleware.AuditLoggingMiddleware',
]
```

### 5. Set Up Acknowledgment Checking

Add to crontab for periodic acknowledgment checking:

```bash
# Check acknowledgments every 5 minutes
*/5 * * * * cd /path/to/env/default && python manage.py check_acknowledgments
```

Or run manually:

```bash
python manage.py check_acknowledgments
python manage.py check_acknowledgments --stats
python manage.py check_acknowledgments --transaction-id <uuid>
```

## API Endpoints

Base URL: `http://localhost:8080/modern-edi/api/v1/`

### Transaction Endpoints

- `GET /transactions/` - List all transactions
- `GET /transactions/{folder}/` - List transactions in folder
- `GET /transaction/{id}/` - Get transaction details
- `POST /transaction/create/` - Create new transaction
- `PUT /transaction/{id}/update/` - Update transaction
- `DELETE /transaction/{id}/delete/` - Soft delete transaction

### Action Endpoints

- `POST /transaction/{id}/move/` - Move to different folder
- `POST /transaction/{id}/send/` - Send outgoing transaction
- `POST /transaction/{id}/permanent-delete/` - Permanently delete
- `GET /transaction/{id}/history/` - Get transaction history
- `GET /transaction/{id}/raw/` - Get raw EDI content

### Metadata Endpoints

- `GET /folders/` - List folders with counts
- `GET /folders/{folder}/stats/` - Get folder statistics
- `GET /partners/` - List trading partners
- `GET /document-types/` - List document types
- `GET /search/` - Search transactions

## Testing the API

### Create a Transaction

```bash
curl -X POST http://localhost:8080/modern-edi/api/v1/transaction/create/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your-session-id" \
  -d '{
    "folder": "inbox",
    "partner_name": "ACME Corp",
    "partner_id": "ACME001",
    "document_type": "850",
    "po_number": "PO123456",
    "metadata": {
      "buyer_name": "ACME Corp",
      "seller_name": "Your Company"
    }
  }'
```

### List Transactions

```bash
curl http://localhost:8080/modern-edi/api/v1/transactions/ \
  -H "Cookie: sessionid=your-session-id"
```

### Get Folder Stats

```bash
curl http://localhost:8080/modern-edi/api/v1/folders/inbox/stats/ \
  -H "Cookie: sessionid=your-session-id"
```

## Next Steps - Frontend Development

The backend is complete. Next steps are to build the React frontend:

### Task 6: Set up React Frontend Project
- Initialize React app with Vite or Create React App
- Configure TailwindCSS
- Set up React Router
- Configure Axios and React Query

### Task 7: Build Core Frontend Components
- App shell and routing
- Dashboard with folder cards
- FolderView with transaction list
- TransactionCard component
- TransactionDetail modal
- TransactionForm for create/edit
- MoveDialog for folder selection

### Task 8: Implement Frontend API Integration
- Create API client service
- Create React Query hooks
- Implement error handling

### Tasks 9-15: Implement Features
- Search and filter
- File movement workflow
- Send transaction workflow
- Delete and recovery workflow
- UI styling and polish
- Integration with existing Bots system
- Configuration and deployment

### Tasks 16-17: Documentation and Testing
- User guide
- API documentation
- Automated tests

## Troubleshooting

### Database Migration Issues

If migrations fail:

```bash
python manage.py makemigrations usersys
python manage.py migrate usersys
```

### Permission Issues

Ensure the modern-edi directories are writable:

```bash
chmod -R 750 botssys/modern-edi/
```

### Import Errors

If you get import errors, ensure usersys is in INSTALLED_APPS and restart the server.

## Development Tips

1. **Use Django Shell for Testing**:
   ```bash
   python manage.py shell
   >>> from usersys.transaction_manager import TransactionManager
   >>> tm = TransactionManager()
   >>> # Test your code
   ```

2. **Check Logs**:
   - API requests are logged to `modern_edi.api` logger
   - Acknowledgments are logged to `modern_edi.acknowledgment` logger

3. **Database Queries**:
   ```python
   from usersys.modern_edi_models import EDITransaction
   EDITransaction.objects.filter(folder='inbox').count()
   ```

## Support

For issues or questions:
1. Check the logs in `botssys/logging/`
2. Review the API documentation
3. Test endpoints with curl or Postman
4. Check Django admin for database records

---

**Status**: Backend Complete ✅ | Frontend Pending ⏳
**Last Updated**: 2025-11-06
