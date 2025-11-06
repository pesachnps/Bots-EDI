# Scheduled Reports System Guide

## Overview

The Scheduled Reports system allows admins and partners to set up automatic email delivery of reports in multiple formats (CSV, Excel, JSON, XML).

## Report Types

| Report Type | Description | Data Included |
|-------------|-------------|---------------|
| **inventory_846** | 846 Inventory Report | Current inventory levels, SKUs, quantities, warehouses |
| **analytics_summary** | Analytics Summary | Transaction counts, success rates, document type breakdown |
| **transaction_history** | Transaction History | Complete transaction log with dates, statuses, errors |
| **partner_activity** | Partner Activity | User activity log, actions, timestamps, IP addresses |
| **error_summary** | Error Summary | Failed transactions with error messages |
| **document_summary** | Document Summary by Type | Document type distribution and percentages |

## Export Formats

- **CSV**: Simple comma-separated format, opens in Excel
- **Excel (XLSX)**: Styled worksheets with headers, auto-width columns
- **JSON**: Pretty-printed JSON with metadata
- **XML**: Well-formed XML with proper encoding

## Scheduling Options

### Frequency
- **Daily**: Runs every day at specified time
- **Weekly**: Runs on specific day of week (0=Monday, 6=Sunday)
- **Monthly**: Runs on specific day of month (1-31, or -1 for last day)
- **On Demand**: Only runs when manually triggered

### Timezone Support
All schedules respect the configured timezone. Defaults to UTC.

## API Endpoints

### Admin Endpoints

```
GET    /api/v1/admin/scheduled-reports              # List all reports
POST   /api/v1/admin/scheduled-reports              # Create report
PUT    /api/v1/admin/scheduled-reports/<id>         # Update report
DELETE /api/v1/admin/scheduled-reports/<id>         # Delete report
POST   /api/v1/admin/scheduled-reports/<id>/run     # Run now
POST   /api/v1/admin/scheduled-reports/<id>/preview # Preview (no email)
```

### Partner Endpoints

```
GET    /api/v1/partner-portal/scheduled-reports        # List my reports
POST   /api/v1/partner-portal/scheduled-reports        # Create report
PUT    /api/v1/partner-portal/scheduled-reports/<id>   # Update my report
DELETE /api/v1/partner-portal/scheduled-reports/<id>   # Delete my report
POST   /api/v1/partner-portal/scheduled-reports/<id>/run # Run now
```

## Creating a Report

### Example Request

```json
POST /api/v1/admin/scheduled-reports
{
  "partner_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
  "name": "Weekly Analytics Report",
  "description": "Weekly summary of all transactions",
  "report_type": "analytics_summary",
  "format": "excel",
  "recipients": ["partner@example.com", "admin@example.com"],
  "frequency": "weekly",
  "day_of_week": 1,
  "time_of_day": "09:00:00",
  "timezone": "America/New_York",
  "date_range_days": 7,
  "filters": {},
  "is_active": true
}
```

### Example Response

```json
{
  "success": true,
  "message": "Scheduled report created successfully",
  "report_id": 42,
  "next_run": "2025-11-11T14:00:00Z"
}
```

## Setting Up the Cron Job

The system requires a cron job to check for due reports:

### Linux/Mac

Add to crontab (`crontab -e`):
```bash
*/5 * * * * cd /path/to/bots && python manage.py run_scheduled_reports
```

### Windows

Use Task Scheduler or create a PowerShell script:
```powershell
# run_reports.ps1
cd C:\path\to\bots
python manage.py run_scheduled_reports
```

Schedule to run every 5 minutes in Task Scheduler.

## Email Configuration

Reports are sent via Django's email system. Configure in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@example.com'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'EDI Reports <noreply@example.com>'
```

## Dependencies

### Required
- Python 3.7+
- Django 3.2+
- pytz (for timezone support)

### Optional
- openpyxl (for Excel export)

Install: `pip install openpyxl`

##Usage Examples

### Daily Error Summary (CSV)

```json
{
  "name": "Daily Error Report",
  "report_type": "error_summary",
  "format": "csv",
  "frequency": "daily",
  "time_of_day": "08:00:00",
  "timezone": "UTC",
  "date_range_days": 1,
  "recipients": ["ops@example.com"]
}
```

### Monthly Inventory Report (Excel)

```json
{
  "name": "Monthly Inventory - End of Month",
  "report_type": "inventory_846",
  "format": "excel",
  "frequency": "monthly",
  "day_of_month": -1,
  "time_of_day": "23:00:00",
  "timezone": "America/Los_Angeles",
  "date_range_days": 30,
  "recipients": ["inventory@example.com", "manager@example.com"]
}
```

### On-Demand Transaction History (JSON)

```json
{
  "name": "Transaction Export for Integration",
  "report_type": "transaction_history",
  "format": "json",
  "frequency": "on_demand",
  "date_range_days": 90,
  "recipients": ["api@example.com"]
}
```

## Email Template

Recipients receive a professional email with:
- Report name and description
- Partner name
- Report type and format
- Date range covered
- Frequency information
- Last generated timestamp
- Report file attached

## Troubleshooting

### Reports Not Running

1. Check cron job is active: `crontab -l`
2. Check Django logs for errors
3. Verify `is_active=true` for report
4. Check `next_run` timestamp is in the past

### Email Not Sending

1. Verify email configuration in settings.py
2. Check SMTP credentials
3. Test email manually: `python manage.py sendtestemail recipient@example.com`
4. Check spam folder

### Excel Export Fails

Install openpyxl: `pip install openpyxl`

### Reports Missing Data

1. Verify partner has transactions in date range
2. Check `date_range_days` setting
3. Review `filters` configuration
4. Check partner permissions

## Activity Logging

All report operations are logged:
- `scheduled_report_created` - Report schedule created
- `scheduled_report_updated` - Report schedule modified
- `scheduled_report_deleted` - Report schedule removed
- `scheduled_report_executed` - Report ran automatically
- `scheduled_report_run_manually` - Report triggered manually

View logs: `GET /api/v1/admin/activity-logs?action=scheduled_report_executed`

## Security

- Partners can only view/edit their own reports
- Admins can manage all reports
- Recipients list is validated (must be valid emails)
- Report files are generated fresh each time (not cached)
- Activity logging for compliance

## Performance

- Reports are limited to 1000 records (configurable in code)
- Large reports use pagination internally
- CSV/JSON are memory-efficient
- Excel export may use more memory for large datasets
- Recommended: Run reports during off-peak hours

## Related Documentation

- [Partner Management Guide](PARTNER_MANAGEMENT.md)
- [Admin Dashboard Guide](ADMIN_DASHBOARD_GUIDE.md)
- [Email Service Documentation](email_service.py)
- [API Documentation](API_DOCUMENTATION.md)
