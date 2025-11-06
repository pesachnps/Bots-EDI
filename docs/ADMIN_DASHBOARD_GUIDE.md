# Admin Dashboard Guide

## Overview

The Admin Dashboard provides system administrators with comprehensive tools to monitor, manage, and analyze the EDI system. It offers real-time metrics, partner management, user administration, analytics, and complete audit trails.

## Table of Contents

- [Accessing the Admin Dashboard](#accessing-the-admin-dashboard)
- [Dashboard Overview](#dashboard-overview)
- [Partner Management](#partner-management)
- [User Management](#user-management)
- [Permissions Management](#permissions-management)
- [Analytics and Reporting](#analytics-and-reporting)
- [Activity Logs](#activity-logs)
- [Best Practices](#best-practices)

## Accessing the Admin Dashboard

### Prerequisites

- Admin account with staff privileges
- Access to the system at `http://your-domain:8080`

### Login Process

1. Navigate to `http://your-domain:8080/admin`
2. Enter your Django admin credentials
3. Once authenticated, access the Admin Dashboard at `http://your-domain:8080/modern-edi/admin/`

### Authentication

The Admin Dashboard uses Django's built-in session authentication. Your session will remain active until you log out or close your browser.

## Dashboard Overview

### Key Metrics

The main dashboard displays four critical metrics:

1. **Total Partners**: Number of active trading partners
2. **Total Transactions**: Cumulative transaction count
3. **Success Rate**: Percentage of successfully processed transactions
4. **Error Rate**: Percentage of failed transactions

### Transaction Volume Chart

- **View**: Line chart showing transaction volume over the last 30 days
- **Interaction**: Hover over data points to see exact counts
- **Refresh**: Auto-refreshes every 60 seconds

### Top Partners

- **Display**: Table showing top 10 partners by transaction volume
- **Columns**: Partner name, ID, transaction count
- **Action**: Click on a partner to view detailed analytics

### Recent Errors

- **Display**: List of most recent transaction errors
- **Information**: Partner name, error type, timestamp
- **Action**: Click to view full error details

### System Status

Real-time health indicators for:
- **SFTP Polling**: Status of SFTP directory monitoring
- **API Services**: REST API availability
- **Database**: Database connection health

## Partner Management

### Viewing Partners

**Location**: Admin Dashboard → Partners

**Features**:
- Searchable list of all trading partners
- Filter by status (active, inactive, suspended)
- Filter by communication method (SFTP, API)
- Sort by name, ID, or transaction count

### Adding a New Partner

1. Click **"Add Partner"** button
2. Fill in required fields:
   - Partner name
   - Partner ID (unique identifier)
   - Communication method (SFTP or API)
   - Contact information
3. Configure communication settings:
   - **For SFTP**: Host, port, username, password, directories
   - **For API**: Webhook URL, authentication method
4. Click **"Save"** to create the partner

### Editing Partner Information

1. Click on a partner row in the list
2. Navigate to the **"Information"** tab
3. Click **"Edit"** button
4. Modify fields as needed
5. Click **"Save Changes"**

### Testing Connections

**SFTP Connection Test**:
1. Open partner detail view
2. Navigate to **"Configuration"** tab
3. Click **"Test SFTP Connection"**
4. System will verify:
   - Host reachability
   - Authentication credentials
   - Directory access permissions

**API Connection Test**:
1. Open partner detail view
2. Navigate to **"Configuration"** tab
3. Click **"Test API Connection"**
4. System will send a test webhook to verify endpoint

### Partner Status Management

**Activate Partner**:
- Enables transaction processing for the partner
- Resumes SFTP polling or API acceptance

**Deactivate Partner**:
- Temporarily disables transaction processing
- Preserves all configuration and history

**Suspend Partner**:
- Immediately halts all processing
- Used for security or compliance issues
- Requires admin approval to reactivate

### Viewing Partner Analytics

1. Click on a partner in the list
2. Navigate to **"Analytics"** tab
3. View metrics:
   - Total transactions sent/received
   - Success/failure rates
   - Average processing time
   - Document type breakdown
   - Transaction volume trends

## User Management

### Overview

User management allows you to create and manage partner user accounts that access the Partner Portal.

### Creating Partner Users

1. Navigate to **Partner Management**
2. Select a partner
3. Click **"Users"** tab
4. Click **"Create User"** button
5. Fill in user details:
   - Username (must be unique)
   - Email address
   - First and last name
   - Phone number (optional)
   - Initial password
   - Role (Partner Admin, Partner User, or Partner Read-Only)
6. Click **"Create"**

### User Roles

**Partner Admin**:
- Full access to Partner Portal
- Can manage partner settings
- Can update contact information
- Can test connections

**Partner User**:
- Standard access to Partner Portal
- Can upload and download files
- Can view transactions and reports
- Cannot modify settings

**Partner Read-Only**:
- View-only access
- Can view transactions and reports
- Cannot upload files
- Cannot modify any settings

### Editing User Information

1. Navigate to partner's user list
2. Click on a user
3. Click **"Edit"** button
4. Modify fields:
   - Name and contact information
   - Role assignment
   - Active status
5. Click **"Save Changes"**

### Resetting User Passwords

**Admin-Initiated Reset**:
1. Navigate to user detail view
2. Click **"Reset Password"** button
3. System generates a temporary password
4. Copy the password and securely share with the user
5. User must change password on first login

**User-Initiated Reset**:
- Users can request password reset through Partner Portal
- Reset link sent to registered email address
- Link expires after 24 hours

### Activating/Deactivating Users

**Deactivate User**:
- Immediately revokes access to Partner Portal
- Preserves user account and history
- Can be reactivated at any time

**Reactivate User**:
- Restores access to Partner Portal
- All permissions and settings remain intact

### Viewing User Activity

1. Navigate to user detail view
2. View **"Last Login"** timestamp
3. Click **"View Activity"** to see:
   - Login history
   - File uploads/downloads
   - Settings changes
   - Failed login attempts

## Permissions Management

### Permission Categories

The system supports five permission categories:

1. **View Transactions**: Access to transaction list and details
2. **Upload Files**: Ability to upload EDI files
3. **Download Files**: Ability to download EDI files
4. **View Reports**: Access to analytics and reports
5. **Manage Settings**: Ability to modify partner settings

### Default Role Permissions

**Partner Admin**:
- ✅ View Transactions
- ✅ Upload Files
- ✅ Download Files
- ✅ View Reports
- ✅ Manage Settings

**Partner User**:
- ✅ View Transactions
- ✅ Upload Files
- ✅ Download Files
- ✅ View Reports
- ❌ Manage Settings

**Partner Read-Only**:
- ✅ View Transactions
- ❌ Upload Files
- ✅ Download Files
- ✅ View Reports
- ❌ Manage Settings

### Customizing Permissions

1. Navigate to **Permissions Management** page
2. Select a user
3. View current permissions (defaults based on role)
4. Toggle individual permissions as needed
5. Click **"Save Changes"**
6. System logs the permission change

### Permission Matrix View

The permission matrix provides a visual overview:
- **Rows**: Users
- **Columns**: Permission categories
- **Cells**: Checkboxes indicating granted permissions
- **Bulk Actions**: Update multiple users simultaneously

### Permission Change History

All permission changes are logged with:
- Timestamp
- Admin who made the change
- User affected
- Before/after permission states

Access via: User Detail → Permissions → View History

## Analytics and Reporting

### Transaction Volume Analytics

**Location**: Admin Dashboard → Analytics → Transaction Volume

**Features**:
- View by day, week, or month
- Line chart visualization
- Hover for exact counts
- Export to CSV or PDF

**Use Cases**:
- Identify peak transaction periods
- Monitor growth trends
- Capacity planning

### Document Type Breakdown

**Location**: Admin Dashboard → Analytics → Document Types

**Features**:
- Pie chart showing distribution of document types (850, 810, 997, etc.)
- Percentage and count for each type
- Filter by date range
- Export data

**Use Cases**:
- Understand transaction mix
- Identify most common document types
- Partner-specific document analysis

### Partner Performance

**Location**: Admin Dashboard → Analytics → Partners

**Features**:
- Bar chart showing success/failure rates by partner
- Sort by success rate, failure rate, or volume
- Drill down to partner-specific details
- Export report

**Use Cases**:
- Identify partners with high error rates
- Proactive partner support
- Performance benchmarking

### Processing Time Metrics

**Location**: Admin Dashboard → Analytics → Performance

**Features**:
- Average processing time per document type
- Trend analysis over time
- Identify bottlenecks

**Use Cases**:
- System performance monitoring
- Optimization opportunities
- SLA compliance tracking

### Custom Date Range Reports

1. Navigate to **Analytics** page
2. Click **"Custom Report"**
3. Select date range
4. Choose metrics to include
5. Select visualization type
6. Click **"Generate Report"**
7. Export as CSV or PDF

### Partner Activity Heatmap

**Location**: Admin Dashboard → Analytics → Activity Heatmap

**Features**:
- Visual representation of transaction activity by hour and day
- Identify peak usage times
- Color-coded intensity

**Use Cases**:
- Maintenance window planning
- Resource allocation
- Partner behavior analysis

## Activity Logs

### Overview

Activity logs provide a complete audit trail of all user actions in the system.

### Viewing Activity Logs

**Location**: Admin Dashboard → Activity Logs

**Display**:
- Timestamp
- User (admin or partner user)
- Action type
- Resource affected
- Details
- IP address

### Searching Logs

**Search Fields**:
- User name
- Action type
- Resource type
- Date range

**Example Searches**:
- All logins by a specific user
- All file uploads in the last week
- All permission changes
- Failed login attempts

### Filtering Logs

**Filter Options**:
- **User Type**: Admin or Partner
- **Action Type**: Login, Logout, Upload, Download, Edit, Delete
- **Date Range**: Last 24 hours, Last 7 days, Last 30 days, Custom
- **Resource Type**: Transaction, Partner, User, Permission

### Exporting Logs

1. Apply desired filters
2. Click **"Export"** button
3. Select format (CSV)
4. Download file

**Use Cases**:
- Compliance audits
- Security investigations
- Usage analysis
- Troubleshooting

### Log Retention

- Activity logs are retained for **90 days** by default
- Older logs are automatically archived
- Retention period configurable in settings

## Best Practices

### Security

1. **Regular Password Changes**: Encourage users to change passwords every 90 days
2. **Monitor Failed Logins**: Review failed login attempts regularly
3. **Principle of Least Privilege**: Grant minimum necessary permissions
4. **Regular Audits**: Review user accounts and permissions quarterly
5. **Deactivate Unused Accounts**: Remove access for inactive users

### Partner Management

1. **Test Connections Regularly**: Verify SFTP/API connectivity monthly
2. **Monitor Partner Performance**: Review analytics weekly
3. **Proactive Communication**: Contact partners with high error rates
4. **Document Configuration**: Keep notes on partner-specific requirements
5. **Regular Reviews**: Audit partner list quarterly

### User Management

1. **Onboarding Process**: Provide training for new partner users
2. **Role Assignment**: Carefully consider appropriate role for each user
3. **Contact Information**: Keep user contact details current
4. **Access Reviews**: Verify user access rights quarterly
5. **Offboarding**: Promptly deactivate accounts for departed users

### Analytics

1. **Regular Monitoring**: Review dashboard metrics daily
2. **Trend Analysis**: Look for patterns in transaction volume
3. **Error Investigation**: Investigate spikes in error rates immediately
4. **Performance Tracking**: Monitor processing times for degradation
5. **Reporting**: Generate monthly reports for stakeholders

### Activity Logging

1. **Regular Reviews**: Check activity logs weekly
2. **Anomaly Detection**: Look for unusual patterns
3. **Security Monitoring**: Watch for suspicious login attempts
4. **Compliance**: Maintain logs for required retention period
5. **Export Regularly**: Back up logs for long-term storage

## Troubleshooting

### Common Issues

**Cannot Access Admin Dashboard**:
- Verify you have staff privileges in Django admin
- Check that you're logged in
- Clear browser cache and cookies

**Partner Connection Test Fails**:
- Verify SFTP/API credentials are correct
- Check network connectivity
- Confirm firewall rules allow connection
- Verify partner's server is operational

**User Cannot Login to Partner Portal**:
- Check if account is active
- Verify account is not locked (5 failed attempts)
- Confirm password is correct
- Check if partner is active

**Metrics Not Updating**:
- Verify auto-refresh is enabled
- Check browser console for errors
- Refresh page manually
- Contact system administrator if issue persists

**Export Fails**:
- Check date range is not too large
- Verify sufficient disk space
- Try smaller data set
- Check browser download settings

## Support

For additional assistance:
- Review the [Partner Portal Guide](PARTNER_PORTAL_GUIDE.md)
- Review the [User Management Guide](USER_MANAGEMENT_GUIDE.md)
- Check the [API Documentation](API_DOCUMENTATION.md)
- Contact system administrator

## Appendix

### Keyboard Shortcuts

- `Ctrl/Cmd + K`: Quick search
- `Ctrl/Cmd + R`: Refresh dashboard
- `Esc`: Close modal dialogs

### Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Mobile Access

The Admin Dashboard is optimized for desktop use. Mobile access is available but some features may have limited functionality on small screens.
