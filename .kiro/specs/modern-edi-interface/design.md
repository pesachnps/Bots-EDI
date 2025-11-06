# Design Document - Modern EDI Interface

## Overview

The Modern EDI Interface is a new web-based user interface for the Bots EDI system that provides intuitive folder-based file management. The interface will be built as a separate Django application that integrates with the existing Bots system without modifying legacy functionality. It will use a modern frontend framework (React) with a RESTful API backend, providing a responsive single-page application (SPA) experience.

### Key Design Principles

1. **Non-Invasive Integration**: Operate alongside existing Django admin without modifications
2. **Separation of Concerns**: Clear separation between frontend UI and backend API
3. **Reusability**: Leverage existing Bots models and authentication
4. **Scalability**: Support for future enhancements and additional features
5. **User Experience**: Intuitive, modern interface with minimal learning curve

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Browser (Client)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         React SPA (Modern EDI Interface)               │ │
│  │  - Folder Views (Inbox, Received, Outbox, Sent, Del)  │ │
│  │  - Transaction Cards & Detail Views                    │ │
│  │  - File Management Actions                             │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django Backend Server                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Modern Interface API (New)                   │ │
│  │  - Transaction Management Endpoints                    │ │
│  │  - Folder Operations                                   │ │
│  │  - File Movement & Status Updates                      │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Transaction Manager (Business Logic)           │ │
│  │  - File Operations                                     │ │
│  │  - Status Management                                   │ │
│  │  - Validation & Parsing                                │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Data Models (New + Existing)              │ │
│  │  - EDITransaction (New)                                │ │
│  │  - TransactionMetadata (New)                           │ │
│  │  - Bots Models (Existing - report, ta, etc.)          │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Authentication (Existing)                      │ │
│  │  - Django Auth + API Key Auth                          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    File System & Database                    │
│  - SQLite/PostgreSQL/MySQL (Transaction metadata)           │
│  - File System (EDI files in folder structure)              │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- React 18+ (UI framework)
- React Router (client-side routing)
- Axios (HTTP client)
- TailwindCSS (styling)
- React Query (data fetching & caching)
- React Hook Form (form management)

**Backend:**
- Django 3.2+ (existing framework)
- Django REST Framework (API endpoints)
- Python 3.8+ (existing)
- Bots EDI Framework (existing)

**Database:**
- Existing Bots database (SQLite/PostgreSQL/MySQL)
- New tables for transaction metadata

## Components and Interfaces

### Frontend Components

#### 1. App Shell Component
**Purpose**: Main application container and routing

**Props**: None (root component)

**State**:
- `currentUser`: Authenticated user information
- `isAuthenticated`: Boolean authentication status

**Key Methods**:
- `handleLogin()`: Process user authentication
- `handleLogout()`: Clear session and redirect

#### 2. Dashboard Component
**Purpose**: Landing page with folder navigation

**Props**: None

**State**:
- `folderCounts`: Object with count of files in each folder

**UI Elements**:
- Five folder cards (Inbox, Received, Outbox, Sent, Deleted)
- Each card shows folder name, icon, and file count
- Click navigates to folder view

#### 3. FolderView Component
**Purpose**: Display transaction files in a specific folder

**Props**:
- `folderType`: String ('inbox' | 'received' | 'outbox' | 'sent' | 'deleted')

**State**:
- `transactions`: Array of transaction objects
- `loading`: Boolean loading state
- `searchQuery`: String for filtering
- `filters`: Object with active filters
- `selectedTransaction`: Currently selected transaction ID

**Key Methods**:
- `fetchTransactions()`: Load transactions for folder
- `handleSearch(query)`: Filter transactions by search
- `handleFilter(filterType, value)`: Apply filters
- `handleTransactionClick(id)`: Open detail view
- `handleMove(id, targetFolder)`: Move transaction
- `handleDelete(id)`: Move to deleted folder
- `handleSend(id)`: Send outgoing transaction

**UI Elements**:
- Search bar
- Filter controls (partner, date range, document type)
- Transaction cards grid
- Action buttons (Create, Refresh)
- Pagination controls

#### 4. TransactionCard Component
**Purpose**: Display summary of a single transaction

**Props**:
- `transaction`: Transaction object
- `folderType`: Current folder type
- `onMove`: Callback for move action
- `onDelete`: Callback for delete action
- `onSend`: Callback for send action (Outbox only)
- `onClick`: Callback for viewing details

**UI Elements**:
- Partner name
- Document type
- Date (received/sent/created)
- PO number (if applicable)
- Status indicator (for Sent folder - acknowledged/pending)
- Action menu (Move, Delete, Edit, Send)

#### 5. TransactionDetail Component
**Purpose**: Display full transaction details in modal

**Props**:
- `transactionId`: ID of transaction to display
- `onClose`: Callback to close modal

**State**:
- `transaction`: Full transaction object with all fields
- `loading`: Boolean loading state

**UI Elements**:
- Header with transaction metadata
- Tabbed interface:
  - Overview: Key fields and summary
  - Raw Data: Full EDI content
  - History: Status changes and movements
  - Acknowledgment: Status and details (Sent folder only)
- Close button
- Edit button (if in Inbox/Outbox)

#### 6. TransactionForm Component
**Purpose**: Create or edit transaction

**Props**:
- `mode`: 'create' | 'edit'
- `folderType`: Target folder ('inbox' | 'outbox')
- `transactionId`: ID for edit mode (optional)
- `onSave`: Callback after successful save
- `onCancel`: Callback to cancel

**State**:
- `formData`: Object with all form fields
- `errors`: Validation errors
- `partners`: List of available partners
- `documentTypes`: List of available document types

**Key Methods**:
- `handleSubmit()`: Validate and save transaction
- `handleFieldChange(field, value)`: Update form field
- `validateForm()`: Check all required fields

**UI Elements**:
- Partner selector
- Document type selector
- Dynamic form fields based on document type
- Save and Cancel buttons
- Validation error messages

#### 7. MoveDialog Component
**Purpose**: Select destination folder for moving transaction

**Props**:
- `currentFolder`: Current folder type
- `onMove`: Callback with selected folder
- `onCancel`: Callback to cancel

**UI Elements**:
- List of available destination folders
- Folder icons and names
- Confirm and Cancel buttons

### Backend Components

#### 1. Data Models

**EDITransaction Model**
```python
class EDITransaction(models.Model):
    """Main transaction model for modern interface"""
    
    # Identification
    id = UUIDField(primary_key=True)
    filename = CharField(max_length=255)
    
    # Folder Management
    folder = CharField(max_length=20, choices=FOLDER_CHOICES)
    # Choices: 'inbox', 'received', 'outbox', 'sent', 'deleted'
    
    # Transaction Data
    partner_name = CharField(max_length=255)
    partner_id = CharField(max_length=100, null=True)
    document_type = CharField(max_length=50)
    po_number = CharField(max_length=100, null=True)
    
    # File Information
    file_path = CharField(max_length=500)
    file_size = IntegerField()
    content_hash = CharField(max_length=64)  # SHA-256
    
    # Status
    status = CharField(max_length=20, choices=STATUS_CHOICES)
    # Choices: 'draft', 'ready', 'processing', 'sent', 'acknowledged', 'failed'
    
    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)
    received_at = DateTimeField(null=True)
    sent_at = DateTimeField(null=True)
    acknowledged_at = DateTimeField(null=True)
    deleted_at = DateTimeField(null=True)
    
    # Acknowledgment
    acknowledgment_status = CharField(max_length=20, null=True)
    acknowledgment_message = TextField(null=True)
    
    # Metadata
    metadata = JSONField(default=dict)  # Flexible storage for parsed data
    
    # Relationships
    created_by = ForeignKey(User, on_delete=SET_NULL, null=True)
    bots_ta_id = IntegerField(null=True)  # Link to Bots ta table
```

**TransactionHistory Model**
```python
class TransactionHistory(models.Model):
    """Track all changes to transactions"""
    
    transaction = ForeignKey(EDITransaction, on_delete=CASCADE)
    action = CharField(max_length=50)
    # Actions: 'created', 'moved', 'edited', 'sent', 'acknowledged', 'deleted'
    
    from_folder = CharField(max_length=20, null=True)
    to_folder = CharField(max_length=20, null=True)
    
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    timestamp = DateTimeField(auto_now_add=True)
    
    details = JSONField(default=dict)  # Additional context
```

#### 2. API Endpoints

**Base URL**: `/modern-edi/api/v1/`

**Transaction Endpoints**:

```
GET    /transactions/                    # List all transactions
GET    /transactions/{folder}/           # List transactions in folder
GET    /transactions/{id}/               # Get transaction details
POST   /transactions/                    # Create new transaction
PUT    /transactions/{id}/               # Update transaction
DELETE /transactions/{id}/               # Soft delete (move to deleted)
POST   /transactions/{id}/move/          # Move to different folder
POST   /transactions/{id}/send/          # Send outgoing transaction
POST   /transactions/{id}/permanent-delete/  # Permanently delete

GET    /transactions/{id}/history/       # Get transaction history
GET    /transactions/{id}/raw/           # Get raw EDI content
```

**Folder Endpoints**:

```
GET    /folders/                         # Get folder list with counts
GET    /folders/{folder}/stats/          # Get folder statistics
```

**Partner Endpoints**:

```
GET    /partners/                        # List all partners
GET    /partners/{id}/                   # Get partner details
```

**Document Type Endpoints**:

```
GET    /document-types/                  # List available document types
GET    /document-types/{type}/schema/    # Get schema for document type
```

**Search Endpoints**:

```
GET    /search/?q={query}&folder={folder}&partner={partner}&date_from={date}&date_to={date}
```

#### 3. Service Layer

**TransactionManager Service**
```python
class TransactionManager:
    """Business logic for transaction operations"""
    
    def create_transaction(folder, data, user):
        """Create new transaction with validation"""
        
    def update_transaction(transaction_id, data, user):
        """Update existing transaction"""
        
    def move_transaction(transaction_id, target_folder, user):
        """Move transaction between folders"""
        
    def send_transaction(transaction_id, user):
        """Send outgoing transaction via Bots"""
        
    def delete_transaction(transaction_id, user, permanent=False):
        """Soft or hard delete transaction"""
        
    def parse_edi_file(file_path):
        """Parse EDI file and extract metadata"""
        
    def generate_edi_file(transaction_id):
        """Generate EDI file from transaction data"""
        
    def check_acknowledgment(transaction_id):
        """Check if sent transaction was acknowledged"""
        
    def get_folder_stats(folder):
        """Get statistics for a folder"""
```

**FileManager Service**
```python
class FileManager:
    """Handle file system operations"""
    
    def save_file(content, folder, filename):
        """Save EDI file to appropriate folder"""
        
    def move_file(from_path, to_folder):
        """Move file between folders"""
        
    def delete_file(file_path, permanent=False):
        """Delete or archive file"""
        
    def read_file(file_path):
        """Read EDI file content"""
        
    def get_file_hash(file_path):
        """Calculate SHA-256 hash of file"""
```

## Data Models

### Database Schema

**EDITransaction Table**:
```sql
CREATE TABLE edi_transaction (
    id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    folder VARCHAR(20) NOT NULL,
    partner_name VARCHAR(255) NOT NULL,
    partner_id VARCHAR(100),
    document_type VARCHAR(50) NOT NULL,
    po_number VARCHAR(100),
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    modified_at TIMESTAMP NOT NULL,
    received_at TIMESTAMP,
    sent_at TIMESTAMP,
    acknowledged_at TIMESTAMP,
    deleted_at TIMESTAMP,
    acknowledgment_status VARCHAR(20),
    acknowledgment_message TEXT,
    metadata JSONB,
    created_by_id INTEGER REFERENCES auth_user(id),
    bots_ta_id INTEGER,
    
    INDEX idx_folder (folder),
    INDEX idx_partner (partner_name),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_po_number (po_number)
);
```

**TransactionHistory Table**:
```sql
CREATE TABLE transaction_history (
    id SERIAL PRIMARY KEY,
    transaction_id UUID REFERENCES edi_transaction(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,
    from_folder VARCHAR(20),
    to_folder VARCHAR(20),
    user_id INTEGER REFERENCES auth_user(id),
    timestamp TIMESTAMP NOT NULL,
    details JSONB,
    
    INDEX idx_transaction (transaction_id),
    INDEX idx_timestamp (timestamp)
);
```

### File System Structure

```
botssys/
├── modern-edi/
│   ├── inbox/              # Staging for new incoming files
│   │   └── {uuid}.edi
│   ├── received/           # Processed incoming files
│   │   └── {uuid}.edi
│   ├── outbox/             # Staging for outgoing files
│   │   └── {uuid}.edi
│   ├── sent/               # Transmitted files
│   │   └── {uuid}.edi
│   └── deleted/            # Soft-deleted files
│       └── {uuid}.edi
```

### Data Flow

**Creating a New Transaction (Inbox)**:
1. User fills out transaction form
2. Frontend validates and sends POST to `/transactions/`
3. Backend validates data
4. TransactionManager creates EDITransaction record
5. FileManager generates and saves EDI file
6. TransactionHistory records creation
7. Response returns transaction ID and details

**Moving Transaction Between Folders**:
1. User clicks move action on transaction card
2. User selects destination folder
3. Frontend sends POST to `/transactions/{id}/move/`
4. Backend validates move operation
5. TransactionManager updates folder field
6. FileManager moves physical file
7. TransactionHistory records movement
8. Response confirms success

**Sending Outgoing Transaction**:
1. User clicks send button on transaction in Outbox
2. Frontend sends POST to `/transactions/{id}/send/`
3. Backend validates transaction is ready
4. TransactionManager generates final EDI file
5. FileManager moves file to Bots outfile directory
6. Bots engine processes and sends file
7. Transaction moved to Sent folder
8. TransactionHistory records send action
9. Background job monitors for acknowledgment

## Error Handling

### Frontend Error Handling

**Network Errors**:
- Display toast notification with retry option
- Maintain local state until connection restored
- Show offline indicator in UI

**Validation Errors**:
- Display inline error messages on form fields
- Highlight invalid fields in red
- Prevent form submission until resolved

**API Errors**:
- Parse error response and display user-friendly message
- Log detailed error to console for debugging
- Provide contextual help or documentation links

### Backend Error Handling

**Validation Errors** (400):
```json
{
    "error": "validation_error",
    "message": "Invalid transaction data",
    "fields": {
        "partner_name": ["This field is required"],
        "po_number": ["Invalid format"]
    }
}
```

**Not Found Errors** (404):
```json
{
    "error": "not_found",
    "message": "Transaction not found",
    "transaction_id": "uuid"
}
```

**Permission Errors** (403):
```json
{
    "error": "permission_denied",
    "message": "You do not have permission to perform this action"
}
```

**Server Errors** (500):
```json
{
    "error": "server_error",
    "message": "An unexpected error occurred",
    "request_id": "uuid"
}
```

### Error Recovery Strategies

1. **Transaction Rollback**: Database transactions ensure atomicity
2. **File Cleanup**: Failed operations clean up partial file writes
3. **Retry Logic**: Automatic retry for transient failures (network, locks)
4. **Audit Trail**: All errors logged to TransactionHistory
5. **User Notification**: Clear error messages with actionable steps

## Testing Strategy

### Frontend Testing

**Unit Tests** (Jest + React Testing Library):
- Component rendering and props
- User interactions (clicks, form inputs)
- State management
- Utility functions
- API client functions

**Integration Tests**:
- Component interactions
- Form submission flows
- Navigation between views
- API integration with mock server

**E2E Tests** (Cypress):
- Complete user workflows
- Create transaction flow
- Move transaction flow
- Send transaction flow
- Search and filter functionality

### Backend Testing

**Unit Tests** (pytest):
- Model methods and properties
- Service layer functions
- Validation logic
- Utility functions

**Integration Tests**:
- API endpoint responses
- Database operations
- File system operations
- Bots integration

**API Tests**:
- Request/response formats
- Authentication and permissions
- Error handling
- Edge cases

### Test Coverage Goals

- Frontend: 80% code coverage
- Backend: 90% code coverage
- Critical paths: 100% coverage

### Testing Environments

1. **Development**: Local testing with SQLite
2. **Staging**: Full stack with PostgreSQL
3. **Production**: Smoke tests only

## Security Considerations

### Authentication & Authorization

- Reuse existing Django authentication
- Support both session-based (web) and token-based (API) auth
- Role-based access control for folder operations
- Audit all user actions

### Data Protection

- Validate all user inputs
- Sanitize file uploads
- Prevent path traversal attacks
- Use parameterized database queries
- Encrypt sensitive data in metadata JSON

### API Security

- CSRF protection for state-changing operations
- Rate limiting on API endpoints
- Input validation and sanitization
- Secure file upload handling
- Content-Type validation

### File Security

- Restrict file access to authenticated users
- Validate file types and sizes
- Scan uploaded files for malware (future enhancement)
- Use secure file naming (UUIDs)
- Prevent directory traversal

## Performance Considerations

### Frontend Optimization

- Lazy loading of components
- Virtual scrolling for large transaction lists
- Debounced search input
- Optimistic UI updates
- React Query caching

### Backend Optimization

- Database indexing on frequently queried fields
- Pagination for list endpoints (default 50 items)
- Eager loading of related objects
- Query optimization with select_related/prefetch_related
- Caching of folder statistics

### File System Optimization

- Asynchronous file operations where possible
- Batch file movements
- Periodic cleanup of deleted files
- File compression for archived transactions

## Deployment Considerations

### Static Files

- React build output served from Django static files
- CDN for production deployment (optional)
- Asset versioning for cache busting

### Database Migrations

- Django migrations for new models
- Backward compatible changes
- Data migration scripts for existing Bots data

### Configuration

- Environment variables for folder paths
- Feature flags for gradual rollout
- Configurable pagination limits
- Configurable file size limits

### Monitoring

- API endpoint performance metrics
- Error rate tracking
- User activity analytics
- File system usage monitoring

## Future Enhancements

1. **Bulk Operations**: Select and move/delete multiple transactions
2. **Advanced Search**: Full-text search on transaction content
3. **Export**: Download transactions as CSV/Excel
4. **Notifications**: Real-time alerts for acknowledgments
5. **Templates**: Save and reuse transaction templates
6. **Scheduling**: Schedule transactions for future sending
7. **Webhooks**: Notify external systems of events
8. **Mobile App**: Native mobile interface
9. **Collaboration**: Comments and notes on transactions
10. **Analytics Dashboard**: Visual reports and insights
