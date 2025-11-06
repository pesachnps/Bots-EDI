# Generated migration for Partner Management models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('usersys', '0002_modern_edi_interface'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('partner_id', models.CharField(help_text='Unique partner identifier (e.g., ACME001)', max_length=100, unique=True)),
                ('name', models.CharField(help_text='Partner company name', max_length=255)),
                ('display_name', models.CharField(blank=True, help_text='Display name (defaults to name if empty)', max_length=255)),
                ('contact_name', models.CharField(blank=True, max_length=255)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=50)),
                ('communication_method', models.CharField(choices=[('sftp', 'SFTP'), ('api', 'API'), ('both', 'SFTP and API'), ('manual', 'Manual')], default='both', help_text='How this partner sends/receives files', max_length=20)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('testing', 'Testing'), ('suspended', 'Suspended')], db_index=True, default='active', max_length=20)),
                ('edi_format', models.CharField(default='X12', help_text='Primary EDI format (X12, EDIFACT, etc.)', max_length=50)),
                ('sender_id', models.CharField(blank=True, help_text='ISA Sender ID for X12 or UNB Sender for EDIFACT', max_length=100)),
                ('receiver_id', models.CharField(blank=True, help_text='ISA Receiver ID for X12 or UNB Receiver for EDIFACT', max_length=100)),
                ('supported_document_types', models.JSONField(blank=True, default=list, help_text='List of supported document types (850, 810, etc.)')),
                ('notes', models.TextField(blank=True)),
                ('configuration', models.JSONField(blank=True, default=dict, help_text='Additional partner-specific configuration')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_partners', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Trading Partner',
                'verbose_name_plural': 'Trading Partners',
                'ordering': ['name'],
                'app_label': 'usersys',
            },
        ),
        migrations.CreateModel(
            name='PartnerSFTPConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(help_text='SFTP server hostname or IP', max_length=255)),
                ('port', models.IntegerField(default=22, help_text='SFTP port (default: 22)')),
                ('username', models.CharField(help_text='SFTP username', max_length=255)),
                ('auth_method', models.CharField(choices=[('password', 'Password'), ('key', 'SSH Key'), ('both', 'Password and Key')], default='key', max_length=20)),
                ('password', models.CharField(blank=True, help_text='SFTP password (encrypted in production)', max_length=255)),
                ('private_key_path', models.CharField(blank=True, help_text='Path to SSH private key file', max_length=500)),
                ('inbound_directory', models.CharField(default='/inbound', help_text='Directory to pick up files from partner', max_length=500)),
                ('outbound_directory', models.CharField(default='/outbound', help_text='Directory to send files to partner', max_length=500)),
                ('archive_directory', models.CharField(blank=True, help_text='Directory to archive processed files (optional)', max_length=500)),
                ('inbound_file_pattern', models.CharField(default='*.edi', help_text='Pattern for inbound files (e.g., *.edi, PO_*.x12)', max_length=255)),
                ('outbound_file_pattern', models.CharField(default='{document_type}_{timestamp}.edi', help_text='Pattern for outbound files (supports variables)', max_length=255)),
                ('timeout', models.IntegerField(default=30, help_text='Connection timeout in seconds')),
                ('passive_mode', models.BooleanField(default=True, help_text='Use passive mode for SFTP')),
                ('poll_enabled', models.BooleanField(default=True, help_text='Enable automatic polling for new files')),
                ('poll_interval', models.IntegerField(default=300, help_text='Polling interval in seconds (default: 5 minutes)')),
                ('is_active', models.BooleanField(default=True)),
                ('last_connection_test', models.DateTimeField(blank=True, null=True)),
                ('last_connection_status', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('partner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sftp_config', to='usersys.Partner')),
            ],
            options={
                'verbose_name': 'Partner SFTP Configuration',
                'verbose_name_plural': 'Partner SFTP Configurations',
                'app_label': 'usersys',
            },
        ),
        migrations.CreateModel(
            name='PartnerAPIConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_url', models.URLField(help_text="Base URL for partner's API", max_length=500)),
                ('inbound_endpoint', models.CharField(default='/edi/inbound', help_text='Endpoint to receive files from partner', max_length=500)),
                ('outbound_endpoint', models.CharField(default='/edi/outbound', help_text='Endpoint to send files to partner', max_length=500)),
                ('auth_method', models.CharField(choices=[('none', 'None'), ('basic', 'Basic Auth'), ('bearer', 'Bearer Token'), ('api_key', 'API Key'), ('oauth2', 'OAuth 2.0')], default='api_key', max_length=20)),
                ('api_key', models.CharField(blank=True, help_text='API key for authentication', max_length=500)),
                ('api_secret', models.CharField(blank=True, help_text='API secret (encrypted in production)', max_length=500)),
                ('username', models.CharField(blank=True, max_length=255)),
                ('password', models.CharField(blank=True, max_length=255)),
                ('bearer_token', models.TextField(blank=True)),
                ('oauth_token_url', models.URLField(blank=True, max_length=500)),
                ('oauth_client_id', models.CharField(blank=True, max_length=255)),
                ('oauth_client_secret', models.CharField(blank=True, max_length=255)),
                ('oauth_scope', models.CharField(blank=True, max_length=255)),
                ('content_type', models.CharField(default='application/json', help_text='Content-Type header for requests', max_length=100)),
                ('custom_headers', models.JSONField(blank=True, default=dict, help_text='Additional custom headers')),
                ('timeout', models.IntegerField(default=30, help_text='Request timeout in seconds')),
                ('retry_attempts', models.IntegerField(default=3, help_text='Number of retry attempts on failure')),
                ('retry_delay', models.IntegerField(default=5, help_text='Delay between retries in seconds')),
                ('webhook_enabled', models.BooleanField(default=False, help_text='Enable webhook for receiving files')),
                ('webhook_url', models.URLField(blank=True, help_text='URL for partner to send webhooks', max_length=500)),
                ('webhook_secret', models.CharField(blank=True, help_text='Secret for webhook validation', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('last_connection_test', models.DateTimeField(blank=True, null=True)),
                ('last_connection_status', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('partner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='api_config', to='usersys.Partner')),
            ],
            options={
                'verbose_name': 'Partner API Configuration',
                'verbose_name_plural': 'Partner API Configurations',
                'app_label': 'usersys',
            },
        ),
        migrations.CreateModel(
            name='PartnerTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_via', models.CharField(blank=True, choices=[('sftp', 'SFTP'), ('api', 'API'), ('manual', 'Manual')], max_length=20)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('received_via', models.CharField(blank=True, choices=[('sftp', 'SFTP'), ('api', 'API'), ('manual', 'Manual')], max_length=20)),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('transmission_status', models.CharField(default='pending', help_text='Status of transmission (pending, sent, acknowledged, failed)', max_length=50)),
                ('error_message', models.TextField(blank=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='usersys.Partner')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partner_links', to='usersys.EDITransaction')),
            ],
            options={
                'verbose_name': 'Partner Transaction',
                'verbose_name_plural': 'Partner Transactions',
                'app_label': 'usersys',
            },
        ),
        # Add indexes
        migrations.AddIndex(
            model_name='partner',
            index=models.Index(fields=['partner_id'], name='usersys_par_partner_idx'),
        ),
        migrations.AddIndex(
            model_name='partner',
            index=models.Index(fields=['status'], name='usersys_par_status_idx'),
        ),
        migrations.AddIndex(
            model_name='partner',
            index=models.Index(fields=['communication_method'], name='usersys_par_comm_method_idx'),
        ),
        migrations.AddIndex(
            model_name='partnertransaction',
            index=models.Index(fields=['partner', '-created_at'], name='usersys_ptx_partner_created_idx'),
        ),
        migrations.AddIndex(
            model_name='partnertransaction',
            index=models.Index(fields=['transaction'], name='usersys_ptx_transaction_idx'),
        ),
    ]
