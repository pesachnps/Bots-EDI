# Generated migration for partner users and permissions

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usersys', '0003_partner_management'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, help_text='Unique username for login', max_length=100, unique=True)),
                ('email', models.EmailField(help_text='User email address', max_length=254)),
                ('password_hash', models.CharField(help_text='Hashed password', max_length=255)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('role', models.CharField(choices=[('partner_admin', 'Partner Administrator'), ('partner_user', 'Partner User'), ('partner_readonly', 'Partner Read-Only')], db_index=True, default='partner_user', help_text='User role determines default permissions', max_length=20)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Whether this account is active')),
                ('last_login', models.DateTimeField(blank=True, help_text='Last successful login timestamp', null=True)),
                ('failed_login_attempts', models.IntegerField(default=0, help_text='Number of consecutive failed login attempts')),
                ('locked_until', models.DateTimeField(blank=True, help_text='Account locked until this timestamp', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='Admin user who created this partner user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_partner_users', to=settings.AUTH_USER_MODEL)),
                ('partner', models.ForeignKey(help_text='Partner this user belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='users', to='usersys.partner')),
            ],
            options={
                'verbose_name': 'Partner User',
                'verbose_name_plural': 'Partner Users',
                'ordering': ['partner__name', 'username'],
            },
        ),
        migrations.CreateModel(
            name='PartnerPermission',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='permissions', serialize=False, to='usersys.partneruser')),
                ('can_view_transactions', models.BooleanField(default=True, help_text='Can view transaction list and details')),
                ('can_upload_files', models.BooleanField(default=False, help_text='Can upload EDI files')),
                ('can_download_files', models.BooleanField(default=True, help_text='Can download EDI files')),
                ('can_view_reports', models.BooleanField(default=True, help_text='Can view reports and analytics')),
                ('can_manage_settings', models.BooleanField(default=False, help_text='Can manage partner settings (admin only)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Partner Permission',
                'verbose_name_plural': 'Partner Permissions',
            },
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True, help_text='When this action occurred')),
                ('user_type', models.CharField(choices=[('admin', 'Administrator'), ('partner', 'Partner User')], db_index=True, help_text='Type of user (admin or partner)', max_length=20)),
                ('user_id', models.IntegerField(db_index=True, help_text='ID of the user who performed the action')),
                ('user_name', models.CharField(help_text='Username for display', max_length=100)),
                ('action', models.CharField(db_index=True, help_text='Action performed (login, upload, download, etc.)', max_length=50)),
                ('resource_type', models.CharField(blank=True, help_text='Type of resource affected (transaction, partner, user, etc.)', max_length=50)),
                ('resource_id', models.CharField(blank=True, help_text='ID of the affected resource', max_length=100)),
                ('details', models.JSONField(blank=True, default=dict, help_text='Additional details about the action')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='IP address of the user', null=True)),
                ('user_agent', models.CharField(blank=True, help_text='Browser user agent string', max_length=500)),
            ],
            options={
                'verbose_name': 'Activity Log',
                'verbose_name_plural': 'Activity Logs',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, help_text='Unique reset token', max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When this token was created')),
                ('expires_at', models.DateTimeField(help_text='When this token expires')),
                ('used', models.BooleanField(default=False, help_text='Whether this token has been used')),
                ('used_at', models.DateTimeField(blank=True, help_text='When this token was used', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_tokens', to='usersys.partneruser')),
            ],
            options={
                'verbose_name': 'Password Reset Token',
                'verbose_name_plural': 'Password Reset Tokens',
                'ordering': ['-created_at'],
            },
        ),
        # Add indexes
        migrations.AddIndex(
            model_name='partneruser',
            index=models.Index(fields=['partner', 'is_active'], name='usersys_par_partner_idx'),
        ),
        migrations.AddIndex(
            model_name='partneruser',
            index=models.Index(fields=['username'], name='usersys_par_usernam_idx'),
        ),
        migrations.AddIndex(
            model_name='partneruser',
            index=models.Index(fields=['email'], name='usersys_par_email_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['-timestamp'], name='usersys_act_timesta_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['user_type', 'user_id'], name='usersys_act_user_ty_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['action'], name='usersys_act_action_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['resource_type', 'resource_id'], name='usersys_act_resourc_idx'),
        ),
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['token'], name='usersys_pas_token_idx'),
        ),
        migrations.AddIndex(
            model_name='passwordresettoken',
            index=models.Index(fields=['user', '-created_at'], name='usersys_pas_user_id_idx'),
        ),
    ]
