# Partner Portal Guide

## Overview

The Partner Portal is a self-service web interface that allows trading partners to manage their EDI transactions, upload and download files, view reports, and manage their account settings. This guide provides comprehensive instructions for partner users.

## Table of Contents

- [Getting Started](#getting-started)
- [Dashboard](#dashboard)
- [Viewing Transactions](#viewing-transactions)
- [Uploading Files](#uploading-files)
- [Downloading Files](#downloading-files)
- [Managing Settings](#managing-settings)
- [Account Security](#account-security)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Accessing the Partner Portal

1. Navigate to `http://your-edi-system:8080/modern-edi/partner-portal/`
2. You will be directed to the login page

### First-Time Login

1. Enter the username provided by your system administrator
2. Enter your initial password
3. Click **"Login"**
4. You will be prompted to change your password on first login
5. Choose a strong password that meets the requirements:
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one number
   - At least one special character

### Forgot Password

If you forget your password:

1. Click **"Forgot Password?"** on the login page
2. Enter your username or email address
3. Click **"Send Reset Link"**
4. Check your email for a password reset link
5. Click the link (valid for 24 hours)
6. Enter and confirm your new password
7. Click **"Reset Password"**
8. Return to login page and sign in

### Account Lockout

For security, your account will be locked after 5 failed login attempts. The lockout lasts for 15 minutes. If you need immediate access, contact your system administrator.

## Dashboard

### Overview

The dashboard provides a quick overview of your EDI activity and quick access to common tasks.

### Metrics Cards

**Sent Transactions**:
- Count of transactions you've sent in the last 30 days
- Click to view detailed list

**Received Transactions**:
- Count of transactions received from your trading partners
- Click to view detailed list

**Pending Transactions**:
- Transactions awaiting processing or acknowledgment
- Requires attention if count is high

**Errors**:
- Failed transactions requiring investigation
- Click to view error details

### Recent Transactions

- Displays your 10 most recent transactions
- Shows: Date, Type, PO Number, Status
- Click on any transaction to view full details

### Quick Actions

**Upload File**:
- Quick access to file upload page
- Upload EDI files for processing

**Download Files**:
- Access files ready for download
- View available documents

**View Reports**:
- Access analytics and reports
- View transaction history

### Partner Information

- Your company name and partner ID
- Contact information
- Connection status (SFTP/API)
- Last successful connection timestamp

### Acknowledgment Status

- View acknowledgment status for sent transactions
- See which transactions have been acknowledged
- Identify transactions awaiting acknowledgment

## Viewing Transactions

### Transaction List

**Location**: Partner Portal → Transactions

**Display**:
- Transaction date and time
- Document type (850, 810, 997, etc.)
- PO number (if applicable)
- Status (Pending, Sent, Acknowledged, Failed)
- Direction (Sent or Received)

### Searching Transactions

**Search Options**:
- **PO Number**: Enter full or partial PO number
- **Document Type**: Select from dropdown (850, 810, 997, etc.)
- **Date Range**: Select start and end dates

**Example Searches**:
- Find all purchase orders from last month
- Search for specific PO number
- View all failed transactions

### Filtering Transactions

**Filter by Status**:
- **Pending**: Awaiting processing
- **Sent**: Successfully transmitted
- **Acknowledged**: Confirmed by recipient
- **Failed**: Processing error occurred

**Filter by Direction**:
- **Sent**: Transactions you sent
- **Received**: Transactions sent to you

### Transaction Details

Click on any transaction to view:

**Overview Tab**:
- Transaction ID
- Date and time
- Document type
- PO number
- Status and status history
- Direction (sent/received)
- File size
- Processing time

**Raw Data Tab**:
- Complete EDI file content
- Formatted for readability
- Copy to clipboard button
- Download raw file button

**Acknowledgment Tab** (for sent transactions):
- Acknowledgment status
- 997 Functional Acknowledgment details
- Acceptance/rejection status
- Error codes (if rejected)
- Acknowledgment timestamp

### Pagination

- Transactions are displayed 50 per page
- Use page navigation at bottom of list
- Jump to specific page number

## Uploading Files

### File Upload Page

**Location**: Partner Portal → Upload

### Supported File Formats

- `.edi` - EDI format files
- `.x12` - X12 format files
- `.txt` - Plain text EDI files
- `.xml` - XML format files

### File Size Limit

Maximum file size: **10 MB**

### Upload Process

1. Navigate to **Upload** page
2. Select document type from dropdown:
   - 850 (Purchase Order)
   - 810 (Invoice)
   - 856 (Advance Ship Notice)
   - 997 (Functional Acknowledgment)
   - Other types as configured
3. (Optional) Enter PO number for reference
4. Choose file upload method:

**Drag and Drop**:
- Drag file from your computer
- Drop into the upload area
- File will be validated automatically

**Browse**:
- Click **"Browse"** button
- Select file from your computer
- Click **"Open"**

5. Review file information:
   - File name
   - File size
   - Document type
6. Click **"Upload"** button

### Upload Progress

- Progress bar shows upload percentage
- Estimated time remaining
- Cancel button to abort upload

### Upload Success

Upon successful upload:
- Success message displayed
- Transaction ID provided
- File queued for processing
- Redirect option to view transaction

### Upload Errors

**File Too Large**:
- Reduce file size or split into multiple files
- Contact administrator if larger files needed

**Invalid File Format**:
- Verify file has correct extension
- Check file content is valid EDI format
- Contact administrator for format questions

**Validation Error**:
- File content does not meet EDI standards
- Review error message for specific issues
- Correct file and retry upload

## Downloading Files

### File Download Page

**Location**: Partner Portal → Download

### Available Files

The download page lists all files ready for download:
- File name
- Document type
- Date received
- File size
- Download status (New or Downloaded)

### Downloading Individual Files

1. Navigate to **Download** page
2. Locate desired file in the list
3. Click **"Download"** button next to file
4. File will download to your browser's download folder
5. File marked as "Downloaded" with timestamp

### Bulk Download

To download multiple files at once:

1. Select checkboxes next to desired files
2. Click **"Download Selected"** button
3. System creates a ZIP archive
4. ZIP file downloads to your computer
5. Extract ZIP to access individual files

### Download History

- Files remain available after first download
- Download multiple times if needed
- "Downloaded" timestamp shows first download
- Files retained according to retention policy

### File Organization

Downloaded files are named with:
- Document type
- Date
- Transaction ID
- Original filename

Example: `850_2025-11-06_12345_purchase_order.edi`

## Managing Settings

**Note**: Settings management requires **Partner Admin** role. If you don't see the Settings option, contact your administrator.

### Settings Page

**Location**: Partner Portal → Settings

### Contact Information

**Editable Fields**:
- Contact name
- Email address
- Phone number

**To Update**:
1. Navigate to **Settings** page
2. Click **"Edit Contact Info"**
3. Modify fields as needed
4. Click **"Save Changes"**
5. Confirmation message displayed

### Connection Settings

**View-Only Information**:
- Connection type (SFTP or API)
- Connection status (Active/Inactive)
- Last successful connection
- Configuration details (read-only)

**Note**: Connection settings can only be modified by system administrators for security reasons.

### Testing Connection

1. Navigate to **Settings** page
2. Click **"Test Connection"** button
3. System verifies connectivity
4. Results displayed:
   - **Success**: Connection is working
   - **Failed**: Error message with details

**If Test Fails**:
- Contact your system administrator
- Provide error message details
- Check if your systems are operational

### API Documentation

If your partner uses API integration:
- Click **"View API Documentation"** link
- Access technical documentation
- View webhook URL
- Review authentication requirements

### Changing Password

1. Navigate to **Settings** page
2. Click **"Change Password"**
3. Enter current password
4. Enter new password
5. Confirm new password
6. Click **"Update Password"**
7. You will be logged out
8. Log back in with new password

## Account Security

### Password Requirements

Your password must meet these requirements:
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special character (!@#$%^&*)

### Password Best Practices

1. **Use Unique Passwords**: Don't reuse passwords from other sites
2. **Change Regularly**: Update password every 90 days
3. **Avoid Common Words**: Don't use dictionary words or personal information
4. **Use Password Manager**: Consider using a password manager
5. **Don't Share**: Never share your password with anyone

### Session Security

- **Automatic Logout**: You'll be logged out after 30 minutes of inactivity
- **Manual Logout**: Always log out when finished
- **Secure Connection**: Always access via HTTPS
- **Public Computers**: Never save password on shared computers

### Recognizing Security Issues

Contact your administrator immediately if you notice:
- Unexpected login notifications
- Transactions you didn't initiate
- Changes to your account you didn't make
- Suspicious activity in activity logs

### Two-Factor Authentication

(If enabled by your administrator)
- Additional security layer beyond password
- Requires code from mobile device
- Setup instructions provided by administrator

## Troubleshooting

### Cannot Login

**Check**:
- Username is correct (case-sensitive)
- Password is correct (case-sensitive)
- Caps Lock is not on
- Account is not locked (wait 15 minutes or contact admin)
- Your partner account is active

### Upload Fails

**Common Causes**:
- File too large (max 10 MB)
- Invalid file format
- Network connection interrupted
- File contains validation errors

**Solutions**:
- Check file size and format
- Verify file content is valid EDI
- Try upload again
- Contact administrator if problem persists

### Cannot Download Files

**Check**:
- You have download permissions
- Files are available for your partner
- Browser allows downloads
- Sufficient disk space on your computer

**Solutions**:
- Check browser download settings
- Try different browser
- Contact administrator to verify permissions

### Transactions Not Appearing

**Possible Reasons**:
- Processing delay (allow 5-10 minutes)
- Filters hiding transactions
- Date range too narrow
- Transaction failed validation

**Solutions**:
- Refresh page
- Clear all filters
- Expand date range
- Check error logs

### Connection Test Fails

**Common Issues**:
- Network connectivity problems
- Firewall blocking connection
- Credentials changed
- Partner system offline

**Solutions**:
- Verify your systems are operational
- Check firewall settings
- Contact system administrator
- Retry after a few minutes

### Session Timeout

**Cause**: 30 minutes of inactivity

**Solution**:
- Log in again
- Keep browser tab active
- Save work frequently

### Page Not Loading

**Solutions**:
- Refresh browser (F5 or Ctrl+R)
- Clear browser cache
- Try different browser
- Check internet connection
- Contact administrator if issue persists

## Getting Help

### Support Resources

1. **This Guide**: Comprehensive user documentation
2. **System Administrator**: Your primary contact for issues
3. **API Documentation**: Technical integration details
4. **Training Materials**: Additional resources from your administrator

### Contacting Support

When contacting your system administrator:

**Provide**:
- Your username
- Partner name
- Description of issue
- Steps to reproduce problem
- Error messages (screenshot if possible)
- Browser and version
- Date and time of issue

### Reporting Issues

**Critical Issues** (system down, cannot login):
- Contact administrator immediately
- Use backup communication method if needed

**Non-Critical Issues** (minor bugs, questions):
- Email administrator with details
- Include screenshots if helpful
- Response within 1 business day

## Best Practices

### Daily Operations

1. **Check Dashboard**: Review metrics daily
2. **Monitor Pending**: Address pending transactions promptly
3. **Review Errors**: Investigate failed transactions
4. **Download Files**: Retrieve new files regularly
5. **Verify Acknowledgments**: Confirm sent transactions are acknowledged

### File Management

1. **Validate Before Upload**: Check files before uploading
2. **Use Correct Document Types**: Select appropriate type
3. **Include PO Numbers**: Add reference numbers when applicable
4. **Download Promptly**: Retrieve files within retention period
5. **Organize Downloads**: Maintain organized file structure locally

### Security

1. **Log Out**: Always log out when finished
2. **Secure Passwords**: Use strong, unique passwords
3. **Report Suspicious Activity**: Contact admin immediately
4. **Keep Contact Info Current**: Update email and phone
5. **Review Activity**: Check your transaction history regularly

### Communication

1. **Timely Processing**: Upload and download files promptly
2. **Monitor Acknowledgments**: Verify transactions are acknowledged
3. **Report Issues**: Notify administrator of problems
4. **Provide Feedback**: Share suggestions for improvement
5. **Stay Informed**: Read notifications from administrator

## Appendix

### Document Type Reference

Common EDI document types:
- **850**: Purchase Order
- **810**: Invoice
- **856**: Advance Ship Notice
- **997**: Functional Acknowledgment
- **855**: Purchase Order Acknowledgment
- **860**: Purchase Order Change
- **940**: Warehouse Shipping Order
- **945**: Warehouse Shipping Advice

### Transaction Status Definitions

- **Pending**: Awaiting processing
- **Processing**: Currently being processed
- **Sent**: Successfully transmitted
- **Acknowledged**: Confirmed by recipient (997 received)
- **Failed**: Processing error occurred
- **Rejected**: Rejected by recipient

### Keyboard Shortcuts

- `Ctrl/Cmd + K`: Quick search
- `Ctrl/Cmd + U`: Upload file
- `Ctrl/Cmd + D`: Download page
- `Esc`: Close modal dialogs

### Browser Compatibility

Supported browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Mobile Access

The Partner Portal is optimized for desktop use. Mobile access is available but some features may have limited functionality on small screens.

### Glossary

- **EDI**: Electronic Data Interchange
- **PO**: Purchase Order
- **ASN**: Advance Ship Notice
- **997**: Functional Acknowledgment (confirms receipt)
- **Transaction**: A single EDI document exchange
- **Partner**: Trading partner in EDI relationship
- **SFTP**: Secure File Transfer Protocol
- **API**: Application Programming Interface
