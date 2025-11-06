# User Management Guide

## Overview

This guide provides comprehensive instructions for managing user accounts in the EDI system. It covers creating users, assigning roles and permissions, managing access, and maintaining security.

## Table of Contents

- [User Types](#user-types)
- [Creating Users](#creating-users)
- [Managing Roles](#managing-roles)
- [Permissions System](#permissions-system)
- [User Lifecycle](#user-lifecycle)
- [Security Management](#security-management)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## User Types

### Admin Users

**Purpose**: System administrators who manage the EDI system

**Access**:
- Admin Dashboard
- Modern EDI Interface
- Django Admin
- Full system access

**Authentication**: Django session authentication

**Creation**: Via Django admin or `manage_users.py` script

### Partner Users

**Purpose**: Trading partner employees who access the Partner Portal

**Access**:
- Partner Portal only
- Limited to their partner's data
- Role-based permissions

**Authentication**: Partner Portal authentication

**Creation**: Via Admin Dashboard by system administrators

## Creating Users

### Creating Admin Users

**Method 1: Using init_database.py Script**

```bash
cd env/default
python scripts/init_database.py
```

Follow prompts to create initial admin user.

**Method 2: Using manage_users.py Script**

```bash
cd env/default
python manage_users.py create <username> <password>
```

Example:
```bash
python manage_users.py create admin SecurePass123!
```

**Method 3: Via Django Admin**

1. Log in to Django admin at `/admin`
2. Navigate to **Users**
3. Click **"Add User"**
4. Enter username and password
5. Click **"Save"**
6. Check **"Staff status"** to grant admin access
7. Check **"Superuser status"** for full access
8. Click **"Save"**

### Creating Partner Users

**Prerequisites**:
- Partner must exist in the system
- You must have admin access

**Steps**:

1. Log in to Admin Dashboard
2. Navigate to **Partner Management**
3. Select the partner
4. Click **"Users"** tab
5. Click **"Create User"** button
6. Fill in required information:

**Required Fields**:
- **Username**: Unique identifier (e.g., `acme_john`)
- **Email**: Valid email address
- **First Name**: User's first name
- **Last Name**: User's last name
- **Password**: Initial password (user must change on first login)
- **Role**: Select appropriate role

**Optional Fields**:
- **Phone**: Contact phone number

7. Click **"Create"**
8. Securely share credentials with the user

### Bulk User Creation

For creating multiple users:

1. Prepare CSV file with user data:
```csv
username,email,first_name,last_name,role,partner_id
acme_john,john@acme.com,John,Smith,partner_user,123
acme_jane,jane@acme.com,Jane,Doe,partner_admin,123
```

2. Use management command:
```bash
cd env/default
python manage.py import_partner_users users.csv
```

## Managing Roles

### Available Roles

#### Partner Admin

**Capabilities**:
- Full access to Partner Portal
- View all transactions
- Upload files
- Download files
- View reports and analytics
- Manage partner settings
- Update contact information
- Test connections
- Change own password

**Use Cases**:
- Primary contact for trading partner
- IT administrators at partner company
- Users who need full self-service capabilities

**Default Permissions**:
- ✅ View Transactions
- ✅ Upload Files
- ✅ Download Files
- ✅ View Reports
- ✅ Manage Settings

#### Partner User

**Capabilities**:
- Standard access to Partner Portal
- View transactions
- Upload files
- Download files
- View reports
- Change own password

**Restrictions**:
- Cannot manage settings
- Cannot update contact information
- Cannot test connections

**Use Cases**:
- Day-to-day operational users
- Staff who process EDI transactions
- Users who need upload/download access

**Default Permissions**:
- ✅ View Transactions
- ✅ Upload Files
- ✅ Download Files
- ✅ View Reports
- ❌ Manage Settings

#### Partner Read-Only

**Capabilities**:
- View-only access to Partner Portal
- View transactions
- Download files
- View reports
- Change own password

**Restrictions**:
- Cannot upload files
- Cannot manage settings
- Cannot modify any data

**Use Cases**:
- Auditors
- Management oversight
- Users who only need visibility

**Default Permissions**:
- ✅ View Transactions
- ❌ Upload Files
- ✅ Download Files
- ✅ View Reports
- ❌ Manage Settings

### Assigning Roles

**During User Creation**:
- Select role from dropdown when creating user
- Default permissions applied automatically

**Changing User Role**:

1. Navigate to user detail view
2. Click **"Edit"** button
3. Select new role from dropdown
4. Click **"Save Changes"**
5. Permissions updated automatically
6. Change logged in activity log

### Role Best Practices

1. **Principle of Least Privilege**: Assign minimum necessary role
2. **Regular Reviews**: Audit role assignments quarterly
3. **Document Decisions**: Note why specific roles were assigned
4. **Limit Admins**: Minimize number of Partner Admin users
5. **Temporary Elevation**: Use time-limited role changes when needed

## Permissions System

### Permission Categories

The system uses five granular permission categories:

#### 1. View Transactions

**Grants Access To**:
- Transaction list page
- Transaction detail view
- Transaction search and filtering
- Transaction history

**Required For**:
- All partner portal users
- Viewing EDI documents
- Monitoring transaction status

#### 2. Upload Files

**Grants Access To**:
- File upload page
- Drag-and-drop upload
- Document type selection
- Upload progress monitoring

**Required For**:
- Users who send EDI documents
- Operational staff
- Transaction initiators

#### 3. Download Files

**Grants Access To**:
- File download page
- Individual file downloads
- Bulk download functionality
- Download history

**Required For**:
- Users who receive EDI documents
- Processing staff
- Document retrieval

#### 4. View Reports

**Grants Access To**:
- Analytics dashboard
- Transaction reports
- Performance metrics
- Export functionality

**Required For**:
- Management oversight
- Performance monitoring
- Compliance reporting

#### 5. Manage Settings

**Grants Access To**:
- Settings page
- Contact information updates
- Connection testing
- API documentation access

**Required For**:
- Partner administrators
- IT contacts
- Configuration management

### Customizing Permissions

**When to Customize**:
- User needs differ from role defaults
- Temporary access requirements
- Special circumstances
- Compliance requirements

**How to Customize**:

1. Navigate to **Permissions Management** page
2. Select user
3. View current permissions (based on role)
4. Toggle individual permissions:
   - Click checkbox to grant permission
   - Uncheck to revoke permission
5. Click **"Save Changes"**
6. Confirm changes in dialog
7. System logs the change

**Example Scenarios**:

**Scenario 1**: Partner User needs temporary upload access
- User role: Partner Read-Only
- Custom permission: Enable "Upload Files" temporarily
- Duration: 30 days
- Revert after period

**Scenario 2**: Partner Admin should not manage settings
- User role: Partner Admin
- Custom permission: Disable "Manage Settings"
- Reason: Security policy
- Permanent change

### Permission Matrix

The permission matrix provides visual overview:

**Access**:
1. Navigate to **Permissions Management**
2. Click **"Matrix View"**

**Display**:
- Rows: All users for selected partner
- Columns: Five permission categories
- Cells: Checkboxes (checked = granted)

**Bulk Operations**:
1. Select multiple users (checkboxes in first column)
2. Choose permission to modify
3. Select "Grant" or "Revoke"
4. Click **"Apply"**
5. Confirm bulk change
6. All changes logged

### Permission Inheritance

Permissions are inherited from roles but can be customized:

1. **Role Assignment**: User assigned a role
2. **Default Permissions**: Role's default permissions applied
3. **Customization**: Admin can modify individual permissions
4. **Override**: Custom permissions override role defaults
5. **Role Change**: Changing role resets to new role's defaults

### Permission Change History

All permission changes are tracked:

**Logged Information**:
- Timestamp
- Admin who made change
- User affected
- Permission modified
- Before state
- After state
- Reason (optional)

**Accessing History**:
1. Navigate to user detail view
2. Click **"Permissions"** tab
3. Click **"View History"**
4. Review chronological list of changes

**Use Cases**:
- Audit compliance
- Troubleshooting access issues
- Security investigations
- Change tracking

## User Lifecycle

### Onboarding

**Step 1: Account Creation**
- Admin creates user account
- Assigns appropriate role
- Sets initial password

**Step 2: Credential Delivery**
- Securely share username and password
- Provide Partner Portal URL
- Include user guide link

**Step 3: First Login**
- User logs in with initial credentials
- System prompts password change
- User sets personal password

**Step 4: Training**
- Provide Partner Portal Guide
- Conduct training session (optional)
- Answer questions
- Verify access to needed features

**Step 5: Verification**
- Confirm user can log in
- Verify permissions are correct
- Test key workflows
- Document completion

### Active Use

**Regular Activities**:
- Monitor user activity via activity logs
- Review login patterns
- Check for failed login attempts
- Verify appropriate usage

**Periodic Reviews**:
- Quarterly access reviews
- Verify role still appropriate
- Check for inactive accounts
- Update contact information

**Support**:
- Respond to access issues
- Reset passwords when needed
- Adjust permissions as required
- Provide guidance on features

### Role Changes

**When to Change Roles**:
- Job responsibilities change
- Temporary coverage needed
- Promotion or demotion
- Security requirements

**Process**:
1. Document reason for change
2. Update role in system
3. Notify user of change
4. Verify new permissions work
5. Log change in notes

### Offboarding

**When User Leaves**:

**Step 1: Immediate Actions**
- Deactivate account immediately
- Revoke all access
- Log the deactivation

**Step 2: Knowledge Transfer**
- Document user's responsibilities
- Transfer ownership of processes
- Update contact information

**Step 3: Account Retention**
- Keep account for audit purposes
- Maintain activity history
- Follow retention policy

**Step 4: Final Cleanup** (after retention period)
- Archive user data
- Remove from active lists
- Document completion

### Reactivation

**When to Reactivate**:
- User returns from leave
- Temporary deactivation ends
- Error correction

**Process**:
1. Verify reactivation is appropriate
2. Check if permissions need updating
3. Reactivate account
4. Reset password (security best practice)
5. Notify user
6. Verify access works

## Security Management

### Password Management

**Initial Passwords**:
- Generate strong random passwords
- Never use predictable patterns
- Securely communicate to user
- Force change on first login

**Password Resets**:

**Admin-Initiated**:
1. Navigate to user detail view
2. Click **"Reset Password"**
3. System generates temporary password
4. Copy password (shown once)
5. Securely share with user
6. User must change on next login

**User-Initiated**:
1. User clicks "Forgot Password" on login page
2. Enters username or email
3. System sends reset link to registered email
4. Link valid for 24 hours
5. User sets new password
6. Old password immediately invalidated

**Password Policies**:
- Minimum 8 characters
- Complexity requirements enforced
- No password reuse (last 5 passwords)
- Expire after 90 days (optional)
- Cannot contain username

### Account Lockout

**Automatic Lockout**:
- Triggered after 5 failed login attempts
- Lockout duration: 15 minutes
- Automatic unlock after duration
- All attempts logged

**Manual Unlock**:
1. Navigate to user detail view
2. Click **"Unlock Account"**
3. Confirm unlock
4. User can immediately log in
5. Consider investigating cause

**Monitoring**:
- Review failed login attempts regularly
- Look for patterns (brute force attempts)
- Contact users with multiple failures
- Investigate suspicious activity

### Session Management

**Session Settings**:
- Timeout: 30 minutes of inactivity
- Secure cookies (HTTPS only)
- HttpOnly flag (prevents XSS)
- SameSite attribute (CSRF protection)

**Session Termination**:
- Automatic after timeout
- Manual logout by user
- Admin can force logout (future feature)
- Password change logs out all sessions

### Activity Monitoring

**What to Monitor**:
- Login patterns (time, frequency)
- Failed login attempts
- File upload/download activity
- Permission changes
- Settings modifications
- Unusual behavior

**Red Flags**:
- Logins from unusual locations
- Multiple failed attempts
- Activity outside normal hours
- Bulk downloads
- Rapid permission changes

**Response Actions**:
1. Investigate suspicious activity
2. Contact user to verify
3. Temporarily suspend if needed
4. Reset password if compromised
5. Document incident

### Compliance

**Audit Requirements**:
- Maintain complete activity logs
- Track all permission changes
- Document access reviews
- Retain logs per policy (90 days default)

**Regular Audits**:
- Quarterly user access reviews
- Annual security audits
- Permission appropriateness checks
- Inactive account cleanup

**Documentation**:
- User creation justification
- Role assignment rationale
- Permission customization reasons
- Deactivation documentation

## Best Practices

### User Creation

1. **Verify Need**: Confirm user requires access
2. **Appropriate Role**: Choose least privileged role
3. **Strong Passwords**: Generate secure initial passwords
4. **Secure Delivery**: Use secure channel for credentials
5. **Document**: Record reason for account creation

### Role Assignment

1. **Job Function**: Match role to job responsibilities
2. **Least Privilege**: Start with minimum access
3. **Review Regularly**: Audit role assignments quarterly
4. **Document Changes**: Note reason for role changes
5. **Limit Admins**: Minimize Partner Admin accounts

### Permission Management

1. **Default First**: Use role defaults when possible
2. **Justify Customization**: Document why custom permissions needed
3. **Time-Limited**: Set expiration for temporary permissions
4. **Regular Review**: Audit custom permissions monthly
5. **Principle of Least Privilege**: Grant minimum necessary access

### Security

1. **Strong Passwords**: Enforce complexity requirements
2. **Regular Changes**: Encourage 90-day password rotation
3. **Monitor Activity**: Review logs weekly
4. **Prompt Offboarding**: Deactivate accounts immediately
5. **Incident Response**: Have plan for security issues

### Communication

1. **Clear Instructions**: Provide comprehensive onboarding
2. **Responsive Support**: Answer questions promptly
3. **Proactive Notifications**: Inform users of changes
4. **Training**: Offer training for new users
5. **Feedback**: Collect and act on user feedback

## Troubleshooting

### User Cannot Login

**Possible Causes**:
- Incorrect username or password
- Account locked (5 failed attempts)
- Account deactivated
- Partner deactivated
- Session issues

**Solutions**:
1. Verify username is correct
2. Check if account is locked (unlock if needed)
3. Verify account is active
4. Verify partner is active
5. Reset password if needed
6. Clear browser cache/cookies

### User Cannot Access Feature

**Possible Causes**:
- Insufficient permissions
- Role doesn't include permission
- Custom permission revoked
- Feature disabled for partner

**Solutions**:
1. Check user's role
2. Review permission matrix
3. Verify feature is enabled
4. Grant necessary permission
5. Test access after change

### Password Reset Not Working

**Possible Causes**:
- Email not received
- Reset link expired (24 hours)
- Email address incorrect
- Email in spam folder

**Solutions**:
1. Check spam/junk folder
2. Verify email address is correct
3. Generate new reset link
4. Admin reset as alternative
5. Update email address if needed

### Permissions Not Taking Effect

**Possible Causes**:
- Browser cache
- Session not refreshed
- Permission change not saved
- System delay

**Solutions**:
1. User logs out and back in
2. Clear browser cache
3. Verify change was saved
4. Check activity log for change
5. Wait 1-2 minutes and retry

### Activity Log Missing Entries

**Possible Causes**:
- Logging service issue
- Database connection problem
- Retention policy deleted old logs
- Filter hiding entries

**Solutions**:
1. Check system status
2. Verify logging service running
3. Clear filters
4. Expand date range
5. Contact system administrator

## Appendix

### User Management Commands

**List all users**:
```bash
cd env/default
python manage_users.py list
```

**Create admin user**:
```bash
python manage_users.py create <username> <password>
```

**Reset admin password**:
```bash
python manage_users.py reset <username> <new_password>
```

**Initialize partner portal**:
```bash
python manage.py init_partner_portal
```

### Database Tables

**Partner Users**: `usersys_partneruser`
**Permissions**: `usersys_partnerpermission`
**Activity Logs**: `usersys_activitylog`
**Password Reset Tokens**: `usersys_passwordresettoken`

### API Endpoints

**User Management**:
- `GET /api/v1/admin/partners/<id>/users` - List users
- `POST /api/v1/admin/partners/<id>/users` - Create user
- `PUT /api/v1/admin/users/<id>` - Update user
- `DELETE /api/v1/admin/users/<id>` - Delete user
- `POST /api/v1/admin/users/<id>/reset-password` - Reset password
- `PUT /api/v1/admin/users/<id>/permissions` - Update permissions

### Related Documentation

- [Admin Dashboard Guide](ADMIN_DASHBOARD_GUIDE.md)
- [Partner Portal Guide](PARTNER_PORTAL_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Security Guide](SECURITY.md)

### Support

For additional assistance:
- Review system documentation
- Check activity logs
- Contact system administrator
- Review Django admin interface
