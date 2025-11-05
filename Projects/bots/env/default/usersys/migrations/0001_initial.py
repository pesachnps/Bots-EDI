# Generated migration for API models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APIPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[
                    ('file_upload', 'Upload EDI Files'),
                    ('file_download', 'Download EDI Files'),
                    ('file_list', 'List Files'),
                    ('file_delete', 'Delete Files'),
                    ('route_execute', 'Execute Routes'),
                    ('route_list', 'List Routes'),
                    ('report_view', 'View Reports'),
                    ('report_download', 'Download Reports'),
                    ('partner_view', 'View Partners'),
                    ('partner_manage', 'Manage Partners'),
                    ('translate_view', 'View Translations'),
                    ('channel_view', 'View Channels'),
                    ('admin_access', 'Full Admin Access'),
                ], max_length=50, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'API Permission',
                'verbose_name_plural': 'API Permissions',
                'ordering': ['name'],
                'app_label': 'usersys',
            },
        ),
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Descriptive name for this API key', max_length=255)),
                ('key', models.CharField(editable=False, max_length=64, unique=True)),
                ('is_active', models.BooleanField(default=True, help_text='Enable/disable this API key')),
                ('rate_limit', models.IntegerField(default=1000, help_text='Requests per hour')),
                ('current_usage', models.IntegerField(default=0, editable=False)),
                ('usage_reset_time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(blank=True, null=True)),
                ('expires_at', models.DateTimeField(blank=True, help_text='Optional expiration date', null=True)),
                ('allowed_ips', models.TextField(blank=True, help_text='Comma-separated list of allowed IP addresses (leave blank for all)')),
                ('permissions', models.ManyToManyField(blank=True, related_name='api_keys', to='usersys.APIPermission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'API Key',
                'verbose_name_plural': 'API Keys',
                'ordering': ['-created_at'],
                'app_label': 'usersys',
            },
        ),
        migrations.CreateModel(
            name='APIAuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.CharField(max_length=255)),
                ('method', models.CharField(max_length=10)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('request_data', models.TextField(blank=True, help_text='Request parameters (sanitized)')),
                ('response_status', models.CharField(choices=[
                    ('success', 'Success'),
                    ('failed', 'Failed'),
                    ('denied', 'Access Denied'),
                    ('rate_limited', 'Rate Limited'),
                ], max_length=20)),
                ('response_code', models.IntegerField()),
                ('response_message', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('duration_ms', models.IntegerField(help_text='Request duration in milliseconds')),
                ('api_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to='usersys.APIKey')),
            ],
            options={
                'verbose_name': 'API Audit Log',
                'verbose_name_plural': 'API Audit Logs',
                'ordering': ['-timestamp'],
                'app_label': 'usersys',
            },
        ),
        migrations.AddIndex(
            model_name='apiauditlog',
            index=models.Index(fields=['-timestamp'], name='usersys_api_timesta_idx'),
        ),
        migrations.AddIndex(
            model_name='apiauditlog',
            index=models.Index(fields=['api_key', '-timestamp'], name='usersys_api_api_key_timesta_idx'),
        ),
        migrations.AddIndex(
            model_name='apiauditlog',
            index=models.Index(fields=['response_status'], name='usersys_api_respons_idx'),
        ),
    ]
