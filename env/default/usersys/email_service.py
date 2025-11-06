"""
Email Service for Partner Portal
Handles sending emails for password resets and notifications
"""

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    def send_password_reset_email(user, reset_token):
        """
        Send password reset email to partner user
        
        Args:
            user: PartnerUser instance
            reset_token: PasswordResetToken instance
        """
        try:
            # Build reset URL
            base_url = getattr(settings, 'SITE_URL', 'http://localhost:8080')
            reset_url = f"{base_url}/modern-edi/partner-portal/reset-password?token={reset_token.token}"
            
            # Email context
            context = {
                'user': user,
                'reset_url': reset_url,
                'expiry_hours': 24,
                'site_name': getattr(settings, 'SITE_NAME', 'EDI System'),
            }
            
            # Render email templates
            subject = f"Password Reset Request - {context['site_name']}"
            html_message = EmailService._render_password_reset_html(context)
            plain_message = EmailService._render_password_reset_text(context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Password reset email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email: {str(e)}")
            return False
    
    @staticmethod
    def _render_password_reset_html(context):
        """Render HTML email template for password reset"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4F46E5;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background-color: #4F46E5;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }}
        .warning {{
            background-color: #FEF3C7;
            border-left: 4px solid #F59E0B;
            padding: 12px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{context['site_name']}</h1>
        </div>
        <div class="content">
            <h2>Password Reset Request</h2>
            <p>Hello {context['user'].first_name},</p>
            <p>We received a request to reset your password for your {context['site_name']} account.</p>
            <p>Click the button below to reset your password:</p>
            <p style="text-align: center;">
                <a href="{context['reset_url']}" class="button">Reset Password</a>
            </p>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #4F46E5;">{context['reset_url']}</p>
            <div class="warning">
                <strong>Important:</strong> This link will expire in {context['expiry_hours']} hours.
                If you didn't request this password reset, please ignore this email.
            </div>
            <p>If you have any questions, please contact your system administrator.</p>
        </div>
        <div class="footer">
            <p>&copy; 2025 {context['site_name']}. All rights reserved.</p>
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _render_password_reset_text(context):
        """Render plain text email template for password reset"""
        return f"""
{context['site_name']} - Password Reset Request

Hello {context['user'].first_name},

We received a request to reset your password for your {context['site_name']} account.

To reset your password, please visit the following link:
{context['reset_url']}

IMPORTANT: This link will expire in {context['expiry_hours']} hours.

If you didn't request this password reset, please ignore this email.

If you have any questions, please contact your system administrator.

---
{context['site_name']}
This is an automated message. Please do not reply to this email.
"""
    
    @staticmethod
    def send_account_created_email(user, temporary_password):
        """
        Send account created email to new partner user
        
        Args:
            user: PartnerUser instance
            temporary_password: Temporary password string
        """
        try:
            base_url = getattr(settings, 'SITE_URL', 'http://localhost:8080')
            login_url = f"{base_url}/modern-edi/partner-portal/login"
            
            context = {
                'user': user,
                'temporary_password': temporary_password,
                'login_url': login_url,
                'site_name': getattr(settings, 'SITE_NAME', 'EDI System'),
            }
            
            subject = f"Welcome to {context['site_name']} Partner Portal"
            html_message = EmailService._render_account_created_html(context)
            plain_message = EmailService._render_account_created_text(context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Account created email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send account created email: {str(e)}")
            return False
    
    @staticmethod
    def _render_account_created_html(context):
        """Render HTML email template for account creation"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4F46E5;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background-color: #4F46E5;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin: 20px 0;
        }}
        .credentials {{
            background-color: #E0E7FF;
            border-left: 4px solid #4F46E5;
            padding: 15px;
            margin: 20px 0;
            font-family: monospace;
        }}
        .warning {{
            background-color: #FEF3C7;
            border-left: 4px solid #F59E0B;
            padding: 12px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to {context['site_name']}</h1>
        </div>
        <div class="content">
            <h2>Your Account Has Been Created</h2>
            <p>Hello {context['user'].first_name},</p>
            <p>Your account for the {context['site_name']} Partner Portal has been created.</p>
            <div class="credentials">
                <strong>Your Login Credentials:</strong><br>
                Username: {context['user'].username}<br>
                Temporary Password: {context['temporary_password']}
            </div>
            <div class="warning">
                <strong>Important:</strong> You will be required to change your password on first login.
                Please keep your credentials secure and do not share them with anyone.
            </div>
            <p style="text-align: center;">
                <a href="{context['login_url']}" class="button">Login to Partner Portal</a>
            </p>
            <p><strong>What you can do in the Partner Portal:</strong></p>
            <ul>
                <li>View your EDI transactions</li>
                <li>Upload EDI files</li>
                <li>Download received files</li>
                <li>View transaction reports</li>
                <li>Manage your account settings</li>
            </ul>
            <p>If you have any questions or need assistance, please contact your system administrator.</p>
        </div>
        <div class="footer">
            <p>&copy; 2025 {context['site_name']}. All rights reserved.</p>
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _render_account_created_text(context):
        """Render plain text email template for account creation"""
        return f"""
{context['site_name']} - Welcome to Partner Portal

Hello {context['user'].first_name},

Your account for the {context['site_name']} Partner Portal has been created.

YOUR LOGIN CREDENTIALS:
Username: {context['user'].username}
Temporary Password: {context['temporary_password']}

IMPORTANT: You will be required to change your password on first login.
Please keep your credentials secure and do not share them with anyone.

Login to Partner Portal:
{context['login_url']}

What you can do in the Partner Portal:
- View your EDI transactions
- Upload EDI files
- Download received files
- View transaction reports
- Manage your account settings

If you have any questions or need assistance, please contact your system administrator.

---
{context['site_name']}
This is an automated message. Please do not reply to this email.
"""
    
    @staticmethod
    def send_scheduled_report(report, file_content, filename):
        """
        Send scheduled report email with attachment
        
        Args:
            report: ScheduledReport instance
            file_content: bytes of the report file
            filename: name for the attachment
        """
        try:
            base_url = getattr(settings, 'SITE_URL', 'http://localhost:8080')
            site_name = getattr(settings, 'SITE_NAME', 'EDI System')
            
            context = {
                'report': report,
                'site_name': site_name,
                'base_url': base_url,
            }
            
            subject = f"{report.name} - {report.partner.name}"
            html_message = EmailService._render_scheduled_report_html(context)
            plain_message = EmailService._render_scheduled_report_text(context)
            
            # Create email with attachment
            email = EmailMessage(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=report.recipients
            )
            
            # Add HTML alternative
            email.attach_alternative(html_message, "text/html")
            
            # Determine MIME type based on format
            mime_types = {
                'csv': 'text/csv',
                'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'json': 'application/json',
                'xml': 'application/xml',
            }
            mime_type = mime_types.get(report.format, 'application/octet-stream')
            
            # Attach report file
            email.attach(filename, file_content, mime_type)
            
            # Send
            email.send(fail_silently=False)
            
            logger.info(f"Scheduled report '{report.name}' sent to {len(report.recipients)} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send scheduled report email: {str(e)}")
            return False
    
    @staticmethod
    def _render_scheduled_report_html(context):
        """Render HTML email template for scheduled report"""
        report = context['report']
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4F46E5;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
        }}
        .info-box {{
            background-color: #E0E7FF;
            border-left: 4px solid #4F46E5;
            padding: 15px;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        td {{
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}
        td:first-child {{
            font-weight: bold;
            width: 40%;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{context['site_name']}</h1>
            <p>Scheduled Report</p>
        </div>
        <div class="content">
            <h2>{report.name}</h2>
            <p>Your scheduled report has been generated and is attached to this email.</p>
            <div class="info-box">
                <table>
                    <tr>
                        <td>Partner:</td>
                        <td>{report.partner.name}</td>
                    </tr>
                    <tr>
                        <td>Report Type:</td>
                        <td>{report.get_report_type_display()}</td>
                    </tr>
                    <tr>
                        <td>Format:</td>
                        <td>{report.get_format_display()}</td>
                    </tr>
                    <tr>
                        <td>Date Range:</td>
                        <td>{report.date_range_days} days</td>
                    </tr>
                    <tr>
                        <td>Frequency:</td>
                        <td>{report.get_frequency_display()}</td>
                    </tr>
                    <tr>
                        <td>Generated At:</td>
                        <td>{report.last_run.strftime('%Y-%m-%d %H:%M:%S UTC') if report.last_run else 'N/A'}</td>
                    </tr>
                </table>
            </div>
            {f'<p><strong>Description:</strong> {report.description}</p>' if report.description else ''}
            <p>The report is attached to this email. If you have any questions about this report, please contact your system administrator.</p>
        </div>
        <div class="footer">
            <p>&copy; 2025 {context['site_name']}. All rights reserved.</p>
            <p>This is an automated report. You can manage your report subscriptions in the partner portal.</p>
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def _render_scheduled_report_text(context):
        """Render plain text email template for scheduled report"""
        report = context['report']
        return f"""
{context['site_name']} - Scheduled Report

{report.name}

Your scheduled report has been generated and is attached to this email.

REPORT DETAILS:
Partner: {report.partner.name}
Report Type: {report.get_report_type_display()}
Format: {report.get_format_display()}
Date Range: {report.date_range_days} days
Frequency: {report.get_frequency_display()}
Generated At: {report.last_run.strftime('%Y-%m-%d %H:%M:%S UTC') if report.last_run else 'N/A'}

{f'Description: {report.description}' if report.description else ''}

The report is attached to this email. If you have any questions about this report, please contact your system administrator.

---
{context['site_name']}
This is an automated report. You can manage your report subscriptions in the partner portal.
"""
