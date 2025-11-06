"""
Partner Management Models
Models for managing trading partners with SFTP and API configurations
"""

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Partner(models.Model):
    """Trading Partner model with communication settings"""
    
    COMMUNICATION_METHODS = [
        ('sftp', 'SFTP'),
        ('api', 'API'),
        ('both', 'SFTP and API'),
        ('manual', 'Manual'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('testing', 'Testing'),
        ('suspended', 'Suspended'),
    ]
    
    # Basic Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner_id = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Unique partner identifier (e.g., ACME001)"
    )
    name = models.CharField(max_length=255, help_text="Partner company name")
    display_name = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Display name (defaults to name if empty)"
    )
    
    # Contact Information
    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    
    # Communication Settings
    communication_method = models.CharField(
        max_length=20,
        choices=COMMUNICATION_METHODS,
        default='both',
        help_text="How this partner sends/receives files"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_index=True
    )
    
    # EDI Settings
    edi_format = models.CharField(
        max_length=50,
        default='X12',
        help_text="Primary EDI format (X12, EDIFACT, etc.)"
    )
    sender_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ISA Sender ID for X12 or UNB Sender for EDIFACT"
    )
    receiver_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ISA Receiver ID for X12 or UNB Receiver for EDIFACT"
    )
    
    # Document Types
    supported_document_types = models.JSONField(
        default=list,
        blank=True,
        help_text="List of supported document types (850, 810, etc.)"
    )
    
    # Metadata
    notes = models.TextField(blank=True)
    configuration = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional partner-specific configuration"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_partners'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = "Trading Partner"
        verbose_name_plural = "Trading Partners"
        app_label = 'usersys'
        indexes = [
            models.Index(fields=['partner_id']),
            models.Index(fields=['status']),
            models.Index(fields=['communication_method']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.partner_id})"
    
    def save(self, *args, **kwargs):
        # Set display_name to name if not provided
        if not self.display_name:
            self.display_name = self.name
        super().save(*args, **kwargs)
    
    def get_display_name(self):
        """Get the display name for this partner"""
        return self.display_name or self.name
    
    def supports_sftp(self):
        """Check if partner uses SFTP"""
        return self.communication_method in ['sftp', 'both']
    
    def supports_api(self):
        """Check if partner uses API"""
        return self.communication_method in ['api', 'both']
    
    def is_active(self):
        """Check if partner is active"""
        return self.status == 'active'


class PartnerSFTPConfig(models.Model):
    """SFTP configuration for a partner"""
    
    partner = models.OneToOneField(
        Partner,
        on_delete=models.CASCADE,
        related_name='sftp_config'
    )
    
    # SFTP Connection Settings
    host = models.CharField(max_length=255, help_text="SFTP server hostname or IP")
    port = models.IntegerField(default=22, help_text="SFTP port (default: 22)")
    username = models.CharField(max_length=255, help_text="SFTP username")
    
    # Authentication
    auth_method = models.CharField(
        max_length=20,
        choices=[
            ('password', 'Password'),
            ('key', 'SSH Key'),
            ('both', 'Password and Key'),
        ],
        default='key'
    )
    password = models.CharField(
        max_length=255,
        blank=True,
        help_text="SFTP password (encrypted in production)"
    )
    private_key_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Path to SSH private key file"
    )
    
    # Directory Settings
    inbound_directory = models.CharField(
        max_length=500,
        default='/inbound',
        help_text="Directory to pick up files from partner"
    )
    outbound_directory = models.CharField(
        max_length=500,
        default='/outbound',
        help_text="Directory to send files to partner"
    )
    archive_directory = models.CharField(
        max_length=500,
        blank=True,
        help_text="Directory to archive processed files (optional)"
    )
    
    # File Patterns
    inbound_file_pattern = models.CharField(
        max_length=255,
        default='*.edi',
        help_text="Pattern for inbound files (e.g., *.edi, PO_*.x12)"
    )
    outbound_file_pattern = models.CharField(
        max_length=255,
        default='{document_type}_{timestamp}.edi',
        help_text="Pattern for outbound files (supports variables)"
    )
    
    # Connection Settings
    timeout = models.IntegerField(
        default=30,
        help_text="Connection timeout in seconds"
    )
    passive_mode = models.BooleanField(
        default=True,
        help_text="Use passive mode for SFTP"
    )
    
    # Polling Settings
    poll_enabled = models.BooleanField(
        default=True,
        help_text="Enable automatic polling for new files"
    )
    poll_interval = models.IntegerField(
        default=300,
        help_text="Polling interval in seconds (default: 5 minutes)"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    last_connection_test = models.DateTimeField(null=True, blank=True)
    last_connection_status = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Partner SFTP Configuration"
        verbose_name_plural = "Partner SFTP Configurations"
        app_label = 'usersys'
    
    def __str__(self):
        return f"SFTP Config for {self.partner.name}"
    
    def get_connection_string(self):
        """Get SFTP connection string"""
        return f"sftp://{self.username}@{self.host}:{self.port}"


class PartnerAPIConfig(models.Model):
    """API configuration for a partner"""
    
    partner = models.OneToOneField(
        Partner,
        on_delete=models.CASCADE,
        related_name='api_config'
    )
    
    # API Endpoint Settings
    base_url = models.URLField(
        max_length=500,
        help_text="Base URL for partner's API"
    )
    inbound_endpoint = models.CharField(
        max_length=500,
        default='/edi/inbound',
        help_text="Endpoint to receive files from partner"
    )
    outbound_endpoint = models.CharField(
        max_length=500,
        default='/edi/outbound',
        help_text="Endpoint to send files to partner"
    )
    
    # Authentication
    auth_method = models.CharField(
        max_length=20,
        choices=[
            ('none', 'None'),
            ('basic', 'Basic Auth'),
            ('bearer', 'Bearer Token'),
            ('api_key', 'API Key'),
            ('oauth2', 'OAuth 2.0'),
        ],
        default='api_key'
    )
    
    # Credentials
    api_key = models.CharField(
        max_length=500,
        blank=True,
        help_text="API key for authentication"
    )
    api_secret = models.CharField(
        max_length=500,
        blank=True,
        help_text="API secret (encrypted in production)"
    )
    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)
    bearer_token = models.TextField(blank=True)
    
    # OAuth 2.0 Settings
    oauth_token_url = models.URLField(max_length=500, blank=True)
    oauth_client_id = models.CharField(max_length=255, blank=True)
    oauth_client_secret = models.CharField(max_length=255, blank=True)
    oauth_scope = models.CharField(max_length=255, blank=True)
    
    # Request Settings
    content_type = models.CharField(
        max_length=100,
        default='application/json',
        help_text="Content-Type header for requests"
    )
    custom_headers = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional custom headers"
    )
    
    # Connection Settings
    timeout = models.IntegerField(
        default=30,
        help_text="Request timeout in seconds"
    )
    retry_attempts = models.IntegerField(
        default=3,
        help_text="Number of retry attempts on failure"
    )
    retry_delay = models.IntegerField(
        default=5,
        help_text="Delay between retries in seconds"
    )
    
    # Webhook Settings
    webhook_enabled = models.BooleanField(
        default=False,
        help_text="Enable webhook for receiving files"
    )
    webhook_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="URL for partner to send webhooks"
    )
    webhook_secret = models.CharField(
        max_length=255,
        blank=True,
        help_text="Secret for webhook validation"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    last_connection_test = models.DateTimeField(null=True, blank=True)
    last_connection_status = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Partner API Configuration"
        verbose_name_plural = "Partner API Configurations"
        app_label = 'usersys'
    
    def __str__(self):
        return f"API Config for {self.partner.name}"
    
    def get_full_inbound_url(self):
        """Get full inbound URL"""
        return f"{self.base_url.rstrip('/')}/{self.inbound_endpoint.lstrip('/')}"
    
    def get_full_outbound_url(self):
        """Get full outbound URL"""
        return f"{self.base_url.rstrip('/')}/{self.outbound_endpoint.lstrip('/')}"


class PartnerTransaction(models.Model):
    """Link between partners and transactions for tracking"""
    
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction = models.ForeignKey(
        'EDITransaction',
        on_delete=models.CASCADE,
        related_name='partner_links'
    )
    
    # Communication tracking
    sent_via = models.CharField(
        max_length=20,
        choices=[
            ('sftp', 'SFTP'),
            ('api', 'API'),
            ('manual', 'Manual'),
        ],
        blank=True
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    received_via = models.CharField(
        max_length=20,
        choices=[
            ('sftp', 'SFTP'),
            ('api', 'API'),
            ('manual', 'Manual'),
        ],
        blank=True
    )
    received_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    transmission_status = models.CharField(
        max_length=50,
        default='pending',
        help_text="Status of transmission (pending, sent, acknowledged, failed)"
    )
    error_message = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Partner Transaction"
        verbose_name_plural = "Partner Transactions"
        app_label = 'usersys'
        indexes = [
            models.Index(fields=['partner', '-created_at']),
            models.Index(fields=['transaction']),
        ]
    
    def __str__(self):
        return f"{self.partner.name} - {self.transaction.filename}"


class PartnerUser(models.Model):
    """User accounts for partner portal access"""
    
    ROLE_CHOICES = [
        ('partner_admin', 'Partner Administrator'),
        ('partner_user', 'Partner User'),
        ('partner_readonly', 'Partner Read-Only'),
    ]
    
    # Link to partner
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='users',
        help_text="Partner this user belongs to"
    )
    
    # User credentials
    username = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique username for login"
    )
    email = models.EmailField(help_text="User email address")
    password_hash = models.CharField(
        max_length=255,
        help_text="Hashed password"
    )
    
    # Personal information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    
    # Role and permissions
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='partner_user',
        db_index=True,
        help_text="User role determines default permissions"
    )
    
    # Account status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this account is active"
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last successful login timestamp"
    )
    
    # Security
    failed_login_attempts = models.IntegerField(
        default=0,
        help_text="Number of consecutive failed login attempts"
    )
    locked_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Account locked until this timestamp"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_partner_users',
        help_text="Admin user who created this partner user"
    )
    
    class Meta:
        verbose_name = "Partner User"
        verbose_name_plural = "Partner Users"
        app_label = 'usersys'
        ordering = ['partner__name', 'username']
        indexes = [
            models.Index(fields=['partner', 'is_active']),
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.partner.name})"
    
    def get_full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_locked(self):
        """Check if account is currently locked"""
        from django.utils import timezone
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False
    
    def reset_failed_attempts(self):
        """Reset failed login attempts counter"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    def increment_failed_attempts(self):
        """Increment failed login attempts and lock if threshold reached"""
        from django.utils import timezone
        from datetime import timedelta
        
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=15)
        
        self.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    def get_default_permissions(self):
        """Get default permissions based on role"""
        if self.role == 'partner_admin':
            return {
                'can_view_transactions': True,
                'can_upload_files': True,
                'can_download_files': True,
                'can_view_reports': True,
                'can_manage_settings': True,
            }
        elif self.role == 'partner_user':
            return {
                'can_view_transactions': True,
                'can_upload_files': True,
                'can_download_files': True,
                'can_view_reports': True,
                'can_manage_settings': False,
            }
        else:  # partner_readonly
            return {
                'can_view_transactions': True,
                'can_upload_files': False,
                'can_download_files': True,
                'can_view_reports': True,
                'can_manage_settings': False,
            }


class PartnerPermission(models.Model):
    """Granular permissions for partner users"""
    
    user = models.OneToOneField(
        PartnerUser,
        on_delete=models.CASCADE,
        related_name='permissions',
        primary_key=True
    )
    
    # Permission flags
    can_view_transactions = models.BooleanField(
        default=True,
        help_text="Can view transaction list and details"
    )
    can_upload_files = models.BooleanField(
        default=False,
        help_text="Can upload EDI files"
    )
    can_download_files = models.BooleanField(
        default=True,
        help_text="Can download EDI files"
    )
    can_view_reports = models.BooleanField(
        default=True,
        help_text="Can view reports and analytics"
    )
    can_manage_settings = models.BooleanField(
        default=False,
        help_text="Can manage partner settings (admin only)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Partner Permission"
        verbose_name_plural = "Partner Permissions"
        app_label = 'usersys'
    
    def __str__(self):
        return f"Permissions for {self.user.username}"
    
    def to_dict(self):
        """Convert permissions to dictionary"""
        return {
            'can_view_transactions': self.can_view_transactions,
            'can_upload_files': self.can_upload_files,
            'can_download_files': self.can_download_files,
            'can_view_reports': self.can_view_reports,
            'can_manage_settings': self.can_manage_settings,
        }


class ActivityLog(models.Model):
    """Audit trail for all user actions"""
    
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('partner', 'Partner User'),
    ]
    
    # Timestamp
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When this action occurred"
    )
    
    # User identification
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        db_index=True,
        help_text="Type of user (admin or partner)"
    )
    user_id = models.IntegerField(
        db_index=True,
        help_text="ID of the user who performed the action"
    )
    user_name = models.CharField(
        max_length=100,
        help_text="Username for display"
    )
    
    # Action details
    action = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Action performed (login, upload, download, etc.)"
    )
    resource_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="Type of resource affected (transaction, partner, user, etc.)"
    )
    resource_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID of the affected resource"
    )
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional details about the action"
    )
    
    # Network information
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the user"
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        help_text="Browser user agent string"
    )
    
    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        app_label = 'usersys'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user_type', 'user_id']),
            models.Index(fields=['action']),
            models.Index(fields=['resource_type', 'resource_id']),
        ]
    
    def __str__(self):
        return f"{self.user_name} - {self.action} - {self.timestamp}"


class PasswordResetToken(models.Model):
    """Tokens for password reset functionality"""
    
    user = models.ForeignKey(
        PartnerUser,
        on_delete=models.CASCADE,
        related_name='reset_tokens'
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Unique reset token"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this token was created"
    )
    expires_at = models.DateTimeField(
        help_text="When this token expires"
    )
    used = models.BooleanField(
        default=False,
        help_text="Whether this token has been used"
    )
    used_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this token was used"
    )
    
    class Meta:
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Password Reset Tokens"
        app_label = 'usersys'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    def is_valid(self):
        """Check if token is still valid"""
        from django.utils import timezone
        if self.used:
            return False
        if self.expires_at < timezone.now():
            return False
        return True
    
    def mark_as_used(self):
        """Mark token as used"""
        from django.utils import timezone
        self.used = True
        self.used_at = timezone.now()
        self.save(update_fields=['used', 'used_at'])


class ScheduledReport(models.Model):
    """Scheduled reports that can be emailed to recipients"""
    
    REPORT_TYPE_CHOICES = [
        ('inventory_846', '846 Inventory Report'),
        ('analytics_summary', 'Analytics Summary'),
        ('transaction_history', 'Transaction History'),
        ('partner_activity', 'Partner Activity'),
        ('error_summary', 'Error Summary'),
        ('document_summary', 'Document Summary by Type'),
        ('custom', 'Custom Report'),
    ]
    
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel (XLSX)'),
        ('json', 'JSON'),
        ('xml', 'XML'),
    ]
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('on_demand', 'On Demand Only'),
    ]
    
    # Basic Information
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='scheduled_reports',
        help_text="Partner this report is for"
    )
    name = models.CharField(
        max_length=255,
        help_text="Descriptive name for this report"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of what this report contains"
    )
    
    # Report Configuration
    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPE_CHOICES,
        db_index=True,
        help_text="Type of report to generate"
    )
    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        default='csv',
        help_text="Output format for the report"
    )
    
    # Recipients
    recipients = models.JSONField(
        default=list,
        help_text="List of email addresses to send report to"
    )
    
    # Schedule Settings
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='weekly',
        db_index=True,
        help_text="How often to run this report"
    )
    day_of_week = models.IntegerField(
        null=True,
        blank=True,
        help_text="For weekly reports: 0=Monday, 6=Sunday"
    )
    day_of_month = models.IntegerField(
        null=True,
        blank=True,
        help_text="For monthly reports: 1-31 or -1 for last day"
    )
    time_of_day = models.TimeField(
        default='09:00:00',
        help_text="Time to run the report (HH:MM:SS)"
    )
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text="Timezone for scheduling"
    )
    
    # Filters
    filters = models.JSONField(
        default=dict,
        blank=True,
        help_text="Filters to apply to the report data"
    )
    date_range_days = models.IntegerField(
        default=30,
        help_text="Number of days to include in report"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this schedule is active"
    )
    last_run = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this report was last executed"
    )
    last_run_status = models.CharField(
        max_length=50,
        blank=True,
        help_text="Status of last run (success, failed, etc.)"
    )
    last_run_error = models.TextField(
        blank=True,
        help_text="Error message from last run if failed"
    )
    next_run = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this report is scheduled to run next"
    )
    run_count = models.IntegerField(
        default=0,
        help_text="Total number of times this report has been executed"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_reports'
    )
    
    class Meta:
        verbose_name = "Scheduled Report"
        verbose_name_plural = "Scheduled Reports"
        app_label = 'usersys'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['partner', '-created_at']),
            models.Index(fields=['report_type']),
            models.Index(fields=['is_active', 'next_run']),
            models.Index(fields=['frequency']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.partner.name}) - {self.get_frequency_display()}"
    
    def calculate_next_run(self):
        """Calculate the next run time based on frequency"""
        from django.utils import timezone
        from datetime import timedelta, time, datetime
        import pytz
        
        if self.frequency == 'on_demand':
            self.next_run = None
            return
        
        tz = pytz.timezone(self.timezone)
        now = timezone.now().astimezone(tz)
        
        # Combine date with configured time
        target_time = self.time_of_day
        
        if self.frequency == 'daily':
            # Next occurrence of the target time
            next_run = datetime.combine(now.date(), target_time)
            if next_run <= now:
                next_run += timedelta(days=1)
        
        elif self.frequency == 'weekly':
            # Next occurrence of the specified day of week
            days_ahead = (self.day_of_week - now.weekday()) % 7
            if days_ahead == 0:
                # Today is the day, check if time has passed
                next_run = datetime.combine(now.date(), target_time)
                if next_run <= now:
                    days_ahead = 7
            next_run = datetime.combine(now.date() + timedelta(days=days_ahead), target_time)
        
        elif self.frequency == 'monthly':
            # Next occurrence of the specified day of month
            from calendar import monthrange
            
            if self.day_of_month == -1:
                # Last day of month
                last_day = monthrange(now.year, now.month)[1]
                target_day = last_day
            else:
                target_day = self.day_of_month
            
            try:
                next_run = datetime.combine(
                    now.replace(day=target_day).date(),
                    target_time
                )
                if next_run <= now:
                    # Move to next month
                    if now.month == 12:
                        next_month = now.replace(year=now.year + 1, month=1)
                    else:
                        next_month = now.replace(month=now.month + 1)
                    
                    if self.day_of_month == -1:
                        last_day = monthrange(next_month.year, next_month.month)[1]
                        target_day = last_day
                    
                    next_run = datetime.combine(
                        next_month.replace(day=target_day).date(),
                        target_time
                    )
            except ValueError:
                # Day doesn't exist in current month, move to next month
                if now.month == 12:
                    next_month = now.replace(year=now.year + 1, month=1, day=1)
                else:
                    next_month = now.replace(month=now.month + 1, day=1)
                next_run = datetime.combine(next_month.date(), target_time)
        
        else:
            next_run = now
        
        # Convert to UTC for storage
        self.next_run = tz.localize(next_run).astimezone(pytz.UTC)
    
    def mark_as_run(self, status='success', error=None):
        """Mark report as executed"""
        from django.utils import timezone
        self.last_run = timezone.now()
        self.last_run_status = status
        self.last_run_error = error or ''
        self.run_count += 1
        self.calculate_next_run()
        self.save(update_fields=['last_run', 'last_run_status', 'last_run_error', 'run_count', 'next_run'])
