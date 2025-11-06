# Admin Dashboard & Partner Portal - Design Document

## Overview

This design document outlines the architecture and implementation approach for two new web interfaces that extend the existing Modern EDI Interface:
- **Admin Dashboard**: Analytics and management interface for system administrators
- **Partner Portal**: Self-service interface for trading partners

Both interfaces will be built using Django for the backend and React for the frontend, following the same architectural patterns established in the Modern EDI Interface.

## Summary of Changes

### What We're Building On ✅

The system already has:
- ✅ Partner model with SFTP/API configuration
- ✅ EDITransaction model with 5-folder workflow
- ✅ Modern EDI Interface for internal staff
- ✅ Transaction management APIs
- ✅ File upload/download functionality
- ✅ Django admin interface
- ✅ React/Vite frontend infrastructure

### What We're Adding 🔨

**New Backend:**
- 🔨 PartnerUser model (user accounts for partners)
- 🔨 PartnerPermission model (granular permissions)
- 🔨 ActivityLog model (audit trail)
- 🔨 PasswordResetToken model
- 🔨 Admin dashboard API endpoints (analytics, metrics)
- 🔨 Partner portal API endpoints (auth, filtered data)
- 🔨 Partner authentication middleware
- 🔨 Analytics service (calculations for charts/metrics)
- 🔨 Activity logging service

**New Frontend:**
- 🔨 Admin dashboard pages (6 pages)
- 🔨 Partner portal pages (6 pages)
- 🔨 Admin-specific components (charts, tables, forms)
- 🔨 Partner-specific components (upload, download, settings)
- 🔨 New layouts for admin and partner interfaces
- 🔨 Route integration into existing React app

**Key Principle:** Extend, don't replace. We're adding new capabilities while preserving all existing functionality.

## Existing Infrastructure

### What Already Exists ✅

**Backend Models (partner_models.py):**
- ✅ `Partner` - Trading partner with communication settings
- ✅ `PartnerSFTPConfig` - SFTP configuration per partner
- ✅ `PartnerAPIConfig` - API configuration per partner
- ✅ `PartnerTransaction` - Links partners to transactions

**Backend Models (modern_edi_models.py):**
- ✅ `EDITransaction` - Transaction management with 5-folder workflow
- ✅ `TransactionHistory` - Audit trail for transactions

**Backend Services:**
- ✅ `TransactionManager` - Transaction business logic
- ✅ `FileManager` - File operations
- ✅ `EDIParser` - X12 and EDIFACT parsing
- ✅ `AcknowledgmentTracker` - Acknowledgment checking

**Frontend (Modern EDI Interface):**
- ✅ React SPA at `/modern-edi/`
- ✅ Dashboard with 5-folder cards
- ✅ Transaction CRUD operations
- ✅ Search and filtering
- ✅ File upload/download

**API Endpoints:**
- ✅ `/modern-edi/api/v1/transactions/*` - Transaction operations
- ✅ `/modern-edi/api/v1/folders/*` - Folder operations

### What Needs to Be Built 🔨

**New Backend Models:**
- 🔨 `PartnerUser` - User accounts for partners
- 🔨 `PartnerPermission` - Granular permissions per user
- 🔨 `ActivityLog` - Audit trail for all user actions
- 🔨 `PasswordResetToken` - Password reset functionality

**New Backend Services:**
- 🔨 `UserManager` - Partner user management logic
- 🔨 `AnalyticsService` - Metrics and analytics calculations
- 🔨 `ActivityLogger` - Activity logging service

**New API Endpoints:**
- 🔨 `/modern-edi/api/v1/admin/*` - Admin dashboard endpoints
- 🔨 `/modern-edi/api/v1/partner-portal/*` - Partner portal endpoints

**New Frontend Apps:**
- 🔨 Admin Dashboard pages and components
- 🔨 Partner Portal pages and components

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser                              │
│  ┌──────────────┬──────────────────┬──────────────────────┐│
│  │  Modern EDI  │  Admin Dashboard │  Partner Portal      ││
│  │  (Existing)  │  (NEW)           │  (NEW)               ││
│  │  /modern-edi/│  /modern-edi/    │  /modern-edi/        ││
│  │              │  admin/          │  partner-portal/     ││
│  └──────────────┴──────────────────┴──────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Django REST API Layer                           │
│  ┌──────────────┬──────────────────┬──────────────────────┐│
│  │  Existing    │  Admin API       │  Partner Portal API  ││
│  │  /api/v1/    │  /api/v1/admin/  │  /api/v1/partner-    ││
│  │  transactions│  (NEW)           │  portal/ (NEW)       ││
│  └──────────────┴──────────────────┴──────────────────────┘│
│  ┌──────────────────────────────────────────────────────────┤
│  │  Authentication & Authorization                          │
│  │  - Django Session Auth (Admin & Modern EDI)              │
│  │  - Partner Session Auth (NEW - Partner Portal)           │
│  └──────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django ORM / Models                        │
│  EXISTING:                                                   │
│  - Partner, PartnerSFTPConfig, PartnerAPIConfig             │
│  - PartnerTransaction                                        │
│  - EDITransaction, TransactionHistory                        │
│  - Django User (for admin)                                   │
│                                                              │
│  NEW:                                                        │
│  - PartnerUser, PartnerPermission                           │
│  - ActivityLog, PasswordResetToken                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Database (SQLite/PostgreSQL)            │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Django 3.2+ (existing framework)
- Django REST Framework for API endpoints
- Django sessions for admin authentication
- Custom authentication for partner portal

**Frontend:**
- React 18+ with Vite
- React Router for navigation
- Recharts for data visualization
- Tailwind CSS for styling
- Axios for API communication

**Deployment:**
- Admin Dashboard: Served at `/admin-dashboard/`
- Partner Portal: Served at `/partner-portal/`
- Both built as separate React SPAs

## Components and Interfaces

### Backend Components

#### 1. Django Models (NEW)

These models will be added to `partner_models.py` to extend the existing Partner infrastructure.

**PartnerUser Model** (NEW - links users to existing Partner model)
```python
class PartnerUser(models.Model):
    """User accounts for partner portal access"""
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='users')
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    
    # Role choices
    ROLE_CHOICES = [
        ('partner_admin', 'Partner Administrator'),
        ('partner_user', 'Partner User'),
        ('partner_readonly', 'Partner Read-Only'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='partner_user')
    
    # Account status
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Security
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
```

**PartnerPermission Model** (NEW)
```python
class PartnerPermission(models.Model):
    """Granular permissions for partner users"""
    user = models.OneToOneField(PartnerUser, on_delete=models.CASCADE, related_name='permissions')
    can_view_transactions = models.BooleanField(default=True)
    can_upload_files = models.BooleanField(default=False)
    can_download_files = models.BooleanField(default=True)
    can_view_reports = models.BooleanField(default=True)
    can_manage_settings = models.BooleanField(default=False)
    
    # Automatically set based on role, but can be customized
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**ActivityLog Model** (NEW)
```python
class ActivityLog(models.Model):
    """Audit trail for all user actions"""
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # User identification
    user_type = models.CharField(max_length=20)  # 'admin' or 'partner'
    user_id = models.IntegerField(db_index=True)
    user_name = models.CharField(max_length=100)
    
    # Action details
    action = models.CharField(max_length=50, db_index=True)  # 'login', 'upload', 'download', etc.
    resource_type = models.CharField(max_length=50)  # 'transaction', 'partner', 'user', etc.
    resource_id = models.CharField(max_length=100, blank=True)
    details = models.JSONField(default=dict)
    
    # Network info
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.CharField(max_length=500, blank=True)
```

**PasswordResetToken Model** (NEW)
```python
class PasswordResetToken(models.Model):
    """Tokens for password reset functionality"""
    user = models.ForeignKey(PartnerUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
```

#### 2. API Views Structure (NEW)

These endpoints will be added to extend the existing Modern EDI API.

**Admin API Endpoints** (`/modern-edi/api/v1/admin/`) - NEW
- `GET /api/v1/admin/dashboard/metrics` - Dashboard overview metrics
- `GET /api/v1/admin/dashboard/charts` - Chart data (transaction volume, etc.)
- `GET /api/v1/admin/partners` - List all partners (extends existing partner API)
- `GET /api/v1/admin/partners/<id>/analytics` - Partner-specific analytics
- `GET /api/v1/admin/partners/<id>/users` - List partner users
- `POST /api/v1/admin/partners/<id>/users` - Create partner user
- `PUT /api/v1/admin/users/<id>` - Update partner user
- `DELETE /api/v1/admin/users/<id>` - Delete partner user
- `POST /api/v1/admin/users/<id>/reset-password` - Reset user password
- `PUT /api/v1/admin/users/<id>/permissions` - Update user permissions
- `GET /api/v1/admin/analytics/transactions` - Transaction analytics
- `GET /api/v1/admin/analytics/partners` - Partner analytics
- `GET /api/v1/admin/analytics/documents` - Document type breakdown
- `GET /api/v1/admin/activity-logs` - Activity logs with search/filter
- `GET /api/v1/admin/activity-logs/export` - Export logs to CSV

**Partner Portal API Endpoints** (`/modern-edi/api/v1/partner-portal/`) - NEW
- `POST /api/v1/partner-portal/auth/login` - Partner login
- `POST /api/v1/partner-portal/auth/logout` - Partner logout
- `GET /api/v1/partner-portal/auth/me` - Get current user info
- `POST /api/v1/partner-portal/auth/forgot-password` - Password reset request
- `POST /api/v1/partner-portal/auth/reset-password` - Reset password with token
- `POST /api/v1/partner-portal/auth/change-password` - Change own password
- `GET /api/v1/partner-portal/dashboard/metrics` - Partner dashboard metrics
- `GET /api/v1/partner-portal/transactions` - List partner transactions (filtered)
- `GET /api/v1/partner-portal/transactions/<id>` - Get transaction details
- `POST /api/v1/partner-portal/files/upload` - Upload EDI file
- `GET /api/v1/partner-portal/files/download` - List downloadable files
- `GET /api/v1/partner-portal/files/download/<id>` - Download specific file
- `POST /api/v1/partner-portal/files/download/bulk` - Bulk download (ZIP)
- `GET /api/v1/partner-portal/settings` - Get partner settings (read-only for most)
- `PUT /api/v1/partner-portal/settings/contact` - Update contact information
- `POST /api/v1/partner-portal/settings/test-connection` - Test connection

**Integration with Existing APIs:**
- Reuse existing `/api/v1/transactions/*` endpoints with partner filtering
- Reuse existing `/api/v1/partners/*` endpoints for admin dashboard
- Add new authentication middleware for partner portal

#### 3. Authentication & Authorization (NEW)

**Admin Authentication:**
- ✅ Use existing Django session authentication (already in place for Modern EDI)
- ✅ Leverage existing Django User model for admins
- 🔨 Add middleware to verify admin/staff status on `/api/v1/admin/*` endpoints
- 🔨 Extend existing authentication to cover admin dashboard routes

**Partner Authentication:** (NEW)
- 🔨 Custom authentication using new PartnerUser model
- 🔨 Session-based with secure cookies (similar to admin auth)
- 🔨 Password hashing using Django's `make_password` and `check_password`
- 🔨 Account lockout after 5 failed attempts (15-minute lockout)
- 🔨 Session timeout after 30 minutes of inactivity
- 🔨 Separate session key to avoid conflicts with admin sessions

**Authorization Middleware:** (NEW)
```python
class PartnerAuthMiddleware:
    """Middleware for partner portal authentication"""
    def process_request(self, request):
        # Check if request is for partner portal
        if request.path.startswith('/modern-edi/api/v1/partner-portal/'):
            # Verify partner session exists
            partner_user_id = request.session.get('partner_user_id')
            if not partner_user_id:
                return JsonResponse({'error': 'Not authenticated'}, status=401)
            
            # Load partner user
            try:
                partner_user = PartnerUser.objects.get(id=partner_user_id, is_active=True)
                request.partner_user = partner_user
                request.partner = partner_user.partner
            except PartnerUser.DoesNotExist:
                return JsonResponse({'error': 'Invalid session'}, status=401)
            
            # Check account lockout
            if partner_user.locked_until and partner_user.locked_until > timezone.now():
                return JsonResponse({'error': 'Account locked'}, status=403)
            
            # Update last activity
            request.session['last_activity'] = timezone.now().isoformat()
            
        return None

class PartnerPermissionMiddleware:
    """Middleware for checking partner permissions"""
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check permissions based on endpoint
        if hasattr(request, 'partner_user'):
            permissions = request.partner_user.permissions
            
            # Map endpoints to required permissions
            if 'upload' in request.path and not permissions.can_upload_files:
                return JsonResponse({'error': 'Permission denied'}, status=403)
            if 'download' in request.path and not permissions.can_download_files:
                return JsonResponse({'error': 'Permission denied'}, status=403)
            # ... more permission checks
        
        return None
```

**Admin Authorization:** (NEW)
```python
class AdminAuthMiddleware:
    """Middleware for admin dashboard authentication"""
    def process_request(self, request):
        if request.path.startswith('/modern-edi/api/v1/admin/'):
            # Verify user is authenticated and is staff
            if not request.user.is_authenticated or not request.user.is_staff:
                return JsonResponse({'error': 'Admin access required'}, status=403)
        return None
```

### Frontend Components

#### Admin Dashboard Components

**Layout Components:**
- `AdminLayout` - Main layout with sidebar navigation
- `AdminSidebar` - Navigation menu
- `AdminHeader` - Top bar with user info and logout

**Dashboard Components:**
- `DashboardOverview` - Main dashboard with metrics cards
- `MetricCard` - Reusable metric display component
- `TransactionVolumeChart` - Line chart for transaction trends
- `TopPartnersTable` - Table showing top partners
- `RecentErrorsList` - List of recent errors
- `SystemStatusIndicators` - Health status indicators

**Partner Management Components:**
- `PartnerList` - Searchable/filterable partner table
- `PartnerForm` - Create/edit partner form
- `PartnerDetail` - Detailed partner view with tabs
- `PartnerUserList` - List of users for a partner
- `PartnerUserForm` - Create/edit partner user
- `PermissionMatrix` - Visual permission management
- `ConnectionTester` - Test SFTP/API connection

**Analytics Components:**
- `AnalyticsDashboard` - Analytics page layout
- `TransactionVolumeChart` - Multi-period volume chart
- `DocumentTypeBreakdown` - Pie chart for document types
- `PartnerSuccessRates` - Bar chart for partner performance
- `ActivityHeatmap` - Heatmap for usage patterns
- `ReportExporter` - Export functionality

**Activity Log Components:**
- `ActivityLogTable` - Searchable activity log
- `ActivityLogFilters` - Filter controls
- `ActivityLogExporter` - CSV export

#### Partner Portal Components

**Layout Components:**
- `PartnerLayout` - Main layout with top navigation
- `PartnerHeader` - Header with logo and user menu
- `PartnerNav` - Navigation tabs

**Authentication Components:**
- `LoginForm` - Partner login page
- `ForgotPasswordForm` - Password reset request
- `PasswordResetForm` - Set new password

**Dashboard Components:**
- `PartnerDashboard` - Overview with metrics
- `PartnerMetricCard` - Metric display
- `RecentTransactionsList` - Recent transactions
- `QuickActions` - Action buttons

**Transaction Components:**
- `TransactionList` - Searchable transaction table
- `TransactionDetail` - Full transaction view
- `TransactionFilters` - Search and filter controls

**File Management Components:**
- `FileUploader` - Drag-and-drop file upload
- `UploadProgress` - Upload progress indicator
- `FileDownloadList` - Available files for download
- `BulkDownloader` - Bulk download interface

**Settings Components:**
- `PartnerSettings` - Settings page (admin role only)
- `ContactInfoForm` - Edit contact information
- `ConnectionStatus` - View connection settings
- `ConnectionTester` - Test connection button

## Data Models

### Database Schema (NEW Tables Only)

These tables will be added via a new migration `0004_partner_users_permissions.py`:

```sql
-- Partner Users (NEW)
CREATE TABLE usersys_partneruser (
    id INTEGER PRIMARY KEY,
    partner_id UUID REFERENCES usersys_partner(id),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_id INTEGER REFERENCES auth_user(id)
);

-- Partner Permissions (NEW)
CREATE TABLE usersys_partnerpermission (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES usersys_partneruser(id) UNIQUE,
    can_view_transactions BOOLEAN DEFAULT TRUE,
    can_upload_files BOOLEAN DEFAULT FALSE,
    can_download_files BOOLEAN DEFAULT TRUE,
    can_view_reports BOOLEAN DEFAULT TRUE,
    can_manage_settings BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activity Logs (NEW)
CREATE TABLE usersys_activitylog (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_type VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL,
    user_name VARCHAR(100),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    details TEXT,  -- JSON
    ip_address VARCHAR(45),
    user_agent VARCHAR(500)
);

-- Password Reset Tokens (NEW)
CREATE TABLE usersys_passwordresettoken (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES usersys_partneruser(id),
    token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE
);

-- Indexes for performance
CREATE INDEX idx_partneruser_partner ON usersys_partneruser(partner_id);
CREATE INDEX idx_partneruser_username ON usersys_partneruser(username);
CREATE INDEX idx_activitylog_timestamp ON usersys_activitylog(timestamp);
CREATE INDEX idx_activitylog_user ON usersys_activitylog(user_type, user_id);
CREATE INDEX idx_activitylog_action ON usersys_activitylog(action);
CREATE INDEX idx_resettoken_token ON usersys_passwordresettoken(token);
```

**Existing Tables (No Changes):**
- `usersys_partner` - Already exists
- `usersys_partneraftpconfig` - Already exists
- `usersys_partnerapiconfig` - Already exists
- `usersys_partnertransaction` - Already exists
- `usersys_editransaction` - Already exists
- `usersys_transactionhistory` - Already exists

### Data Flow Examples

**Partner Login Flow:**
1. User submits username/password to `/api/partner/auth/login`
2. Backend validates credentials, checks account status
3. If valid, create session and return user info + permissions
4. Frontend stores session, redirects to dashboard
5. Activity log records successful login

**File Upload Flow:**
1. Partner user selects file and document type
2. Frontend validates file size/format
3. POST to `/api/partner/files/upload` with multipart form data
4. Backend creates EDITransaction in 'inbox' folder
5. File saved to appropriate directory
6. Activity log records upload
7. Return transaction ID to frontend

**Admin Permission Change Flow:**
1. Admin modifies permissions in UI
2. PUT to `/api/admin/users/<id>/permissions` with new permissions
3. Backend validates admin session
4. Update PartnerPermission record
5. Activity log records change with before/after values
6. Return updated permissions

## Error Handling

### Backend Error Responses

All API endpoints return consistent error format:
```json
{
    "error": "Error message",
    "code": "ERROR_CODE",
    "details": {}
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 401: Unauthorized (not authenticated)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 429: Too Many Requests (rate limiting)
- 500: Internal Server Error

**Common Error Codes:**
- `INVALID_CREDENTIALS`: Login failed
- `ACCOUNT_LOCKED`: Too many failed attempts
- `PERMISSION_DENIED`: Insufficient permissions
- `INVALID_FILE_TYPE`: Unsupported file format
- `FILE_TOO_LARGE`: File exceeds size limit
- `PARTNER_NOT_FOUND`: Partner doesn't exist
- `CONNECTION_FAILED`: SFTP/API test failed

### Frontend Error Handling

**Error Display Strategy:**
- Toast notifications for transient errors
- Inline validation errors on forms
- Error pages for critical failures (404, 500)
- Retry mechanisms for network failures

**Error Logging:**
- Log all API errors to console in development
- Send critical errors to backend logging endpoint
- Track error frequency for monitoring

## Testing Strategy

### Backend Testing

**Unit Tests:**
- Model validation and methods
- Authentication logic (password hashing, lockout)
- Permission checking functions
- Data aggregation for analytics

**Integration Tests:**
- API endpoint responses
- Authentication middleware
- File upload/download flows
- Database transactions

**Test Coverage Goals:**
- Models: 90%+
- Views: 85%+
- Authentication: 95%+
- Overall: 85%+

### Frontend Testing

**Component Tests:**
- Render tests for all components
- User interaction tests (clicks, form submissions)
- Permission-based rendering
- Error state handling

**Integration Tests:**
- Login/logout flows
- File upload with progress
- Transaction search and filtering
- Permission matrix updates

**E2E Tests (Optional):**
- Complete user journeys
- Admin creating partner and user
- Partner uploading and downloading files

### Manual Testing Checklist

**Admin Dashboard:**
- [ ] Dashboard loads with correct metrics
- [ ] Create new partner with SFTP config
- [ ] Create new partner with API config
- [ ] Test SFTP connection (success and failure)
- [ ] Create partner user with each role
- [ ] Modify user permissions
- [ ] Reset user password
- [ ] View analytics charts
- [ ] Export activity logs
- [ ] Search and filter partners

**Partner Portal:**
- [ ] Login with valid credentials
- [ ] Login fails with invalid credentials
- [ ] Account locks after 5 failed attempts
- [ ] Dashboard shows correct metrics
- [ ] Upload EDI file successfully
- [ ] Upload fails with invalid file type
- [ ] View transaction list
- [ ] Search transactions by PO number
- [ ] Download single file
- [ ] Bulk download multiple files
- [ ] Update contact information (admin role)
- [ ] Settings hidden for non-admin role
- [ ] Session timeout after 30 minutes

## Security Considerations

### Authentication Security

- Password hashing using Django's PBKDF2 algorithm
- Secure session cookies with HttpOnly and Secure flags
- CSRF protection on all state-changing requests
- Account lockout after failed login attempts
- Password complexity requirements enforced
- Session timeout for inactivity

### Authorization Security

- Role-based access control (RBAC)
- Permission checks on every API endpoint
- Partner data isolation (users only see their partner's data)
- Admin-only endpoints protected by middleware
- Activity logging for audit trail

### Data Security

- SQL injection prevention via Django ORM
- XSS prevention via React's automatic escaping
- File upload validation (type, size, content)
- Secure file storage with access controls
- HTTPS enforcement in production

### API Security

- Rate limiting on authentication endpoints
- IP-based restrictions (optional)
- Request size limits
- Input validation and sanitization
- Error messages don't leak sensitive info

## Performance Considerations

### Backend Optimization

- Database indexing on frequently queried fields:
  - `partner_user.username`
  - `partner_user.partner_id`
  - `activity_log.timestamp`
  - `activity_log.user_id`
- Query optimization using `select_related` and `prefetch_related`
- Caching for dashboard metrics (60-second TTL)
- Pagination for large result sets (50 items per page)
- Async file processing for uploads

### Frontend Optimization

- Code splitting by route
- Lazy loading for charts and heavy components
- Debounced search inputs
- Virtual scrolling for large tables
- Optimistic UI updates
- Service worker for offline capability (optional)

### Scalability

- Stateless API design for horizontal scaling
- Session storage in database or Redis
- File storage on shared filesystem or S3
- Background jobs for report generation
- CDN for static assets

## Deployment Strategy

### Integration with Existing Modern EDI Interface

Both new interfaces will be integrated into the existing Modern EDI React application rather than separate apps:

**Directory Structure:**
```
env/default/usersys/static/modern-edi/
├── src/
│   ├── pages/
│   │   ├── Dashboard.jsx              # Existing
│   │   ├── FolderView.jsx             # Existing
│   │   ├── admin/                     # NEW
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── PartnerManagement.jsx
│   │   │   ├── UserManagement.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── ActivityLog.jsx
│   │   └── partner-portal/            # NEW
│   │       ├── PartnerLogin.jsx
│   │       ├── PartnerDashboard.jsx
│   │       ├── PartnerTransactions.jsx
│   │       ├── PartnerUpload.jsx
│   │       ├── PartnerDownload.jsx
│   │       └── PartnerSettings.jsx
│   ├── components/
│   │   ├── Layout.jsx                 # Existing
│   │   ├── AdminLayout.jsx            # NEW
│   │   └── PartnerPortalLayout.jsx    # NEW
│   └── App.jsx                        # Update with new routes
```

### Build Process

**Single Build (Existing + New Features):**
```bash
cd env/default/usersys/static/modern-edi
npm install
npm run build
# Output: dist/ directory with all features
```

### Django Integration

**URL Configuration:**
```python
# env/default/usersys/urls.py
urlpatterns = [
    # Existing Modern EDI routes
    path('modern-edi/api/v1/', include('usersys.modern_edi_urls')),
    
    # NEW: Admin dashboard API routes
    path('modern-edi/api/v1/admin/', include('usersys.admin_urls')),
    
    # NEW: Partner portal API routes
    path('modern-edi/api/v1/partner-portal/', include('usersys.partner_portal_urls')),
    
    # Serve React SPA (catch-all for client-side routing)
    re_path(r'^modern-edi/.*', TemplateView.as_view(template_name='modern-edi/index.html')),
]
```

### Database Migrations

```bash
cd env/default
python manage.py makemigrations usersys
python manage.py migrate usersys
```

**Migration file:** `0004_partner_users_permissions.py`

### Initial Data Setup

**Management Command:** `init_partner_portal.py`
```bash
python manage.py init_partner_portal
```

This will:
- Create default permission sets for each role
- Optionally create sample partner users for testing
- Set up activity log retention policy

### Environment Configuration

**Add to existing .env file:**
```
# Partner Portal Settings
PARTNER_SESSION_TIMEOUT=1800  # 30 minutes
PARTNER_MAX_UPLOAD_SIZE=10485760  # 10 MB
PARTNER_FAILED_LOGIN_LOCKOUT=5
PARTNER_LOCKOUT_DURATION=900  # 15 minutes
PARTNER_PASSWORD_MIN_LENGTH=8
```

## Future Enhancements

### Phase 2 Features

- Two-factor authentication (2FA) for admin and partners
- Email notifications for transaction events
- Webhook configuration for partners
- Advanced analytics with custom date ranges
- Partner-specific branding (logo, colors)
- Mobile-responsive design improvements
- Real-time notifications using WebSockets
- API rate limiting per partner
- Scheduled report generation
- Data retention policies

### Integration Opportunities

- SSO integration (SAML, OAuth)
- Integration with external monitoring tools
- Export to business intelligence platforms
- Automated partner onboarding workflow
- Integration with CRM systems

## Appendix

### Role Definitions

**Admin Roles:**
- `superuser`: Full system access (Django superuser)

**Partner Roles:**
- `partner_admin`: Full access to partner portal, can manage settings
- `partner_user`: Standard access, can upload/download files
- `partner_readonly`: View-only access, cannot upload files

### Default Permission Sets

**partner_admin:**
- can_view_transactions: true
- can_upload_files: true
- can_download_files: true
- can_view_reports: true
- can_manage_settings: true

**partner_user:**
- can_view_transactions: true
- can_upload_files: true
- can_download_files: true
- can_view_reports: true
- can_manage_settings: false

**partner_readonly:**
- can_view_transactions: true
- can_upload_files: false
- can_download_files: true
- can_view_reports: true
- can_manage_settings: false

### API Response Examples

**Dashboard Metrics Response:**
```json
{
    "total_partners": 45,
    "total_transactions": 12847,
    "success_rate": 98.5,
    "error_rate": 1.5,
    "transaction_volume_30d": [
        {"date": "2025-10-07", "count": 234},
        {"date": "2025-10-08", "count": 198}
    ],
    "top_partners": [
        {"id": 1, "name": "Acme Corp", "transaction_count": 1234}
    ],
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

**Partner Transaction List Response:**
```json
{
    "count": 234,
    "next": "/api/partner/transactions?page=2",
    "previous": null,
    "results": [
        {
            "id": 1234,
            "date": "2025-11-06T09:15:00Z",
            "type": "850",
            "po_number": "PO-2025-001",
            "status": "acknowledged",
            "direction": "sent"
        }
    ]
}
```
