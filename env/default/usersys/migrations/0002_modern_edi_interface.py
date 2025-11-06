# Generated migration for Modern EDI Interface models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('usersys', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EDITransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('folder', models.CharField(choices=[
                    ('inbox', 'Inbox'),
                    ('received', 'Received'),
                    ('outbox', 'Outbox'),
                    ('sent', 'Sent'),
                    ('deleted', 'Deleted'),
                ], db_index=True, max_length=20)),
                ('partner_name', models.CharField(db_index=True, max_length=255)),
                ('partner_id', models.CharField(blank=True, max_length=100, null=True)),
                ('document_type', models.CharField(max_length=50)),
                ('po_number', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('file_path', models.CharField(max_length=500)),
                ('file_size', models.IntegerField()),
                ('content_hash', models.CharField(max_length=64)),
                ('status', models.CharField(choices=[
                    ('draft', 'Draft'),
                    ('ready', 'Ready'),
                    ('processing', 'Processing'),
                    ('sent', 'Sent'),
                    ('acknowledged', 'Acknowledged'),
                    ('failed', 'Failed'),
                ], db_index=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('acknowledged_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('acknowledgment_status', models.CharField(blank=True, max_length=20, null=True)),
                ('acknowledgment_message', models.TextField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('bots_ta_id', models.IntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='created_transactions',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'EDI Transaction',
                'verbose_name_plural': 'EDI Transactions',
                'ordering': ['-created_at'],
                'app_label': 'usersys',
            },
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[
                    ('created', 'Created'),
                    ('moved', 'Moved'),
                    ('edited', 'Edited'),
                    ('sent', 'Sent'),
                    ('acknowledged', 'Acknowledged'),
                    ('deleted', 'Deleted'),
                    ('restored', 'Restored'),
                    ('permanent_delete', 'Permanently Deleted'),
                ], max_length=50)),
                ('from_folder', models.CharField(blank=True, max_length=20, null=True)),
                ('to_folder', models.CharField(blank=True, max_length=20, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('details', models.JSONField(blank=True, default=dict)),
                ('transaction', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='history',
                    to='usersys.EDITransaction'
                )),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Transaction History',
                'verbose_name_plural': 'Transaction Histories',
                'ordering': ['-timestamp'],
                'app_label': 'usersys',
            },
        ),
        # Add indexes for EDITransaction
        migrations.AddIndex(
            model_name='editransaction',
            index=models.Index(fields=['folder', '-created_at'], name='usersys_edi_folder_created_idx'),
        ),
        migrations.AddIndex(
            model_name='editransaction',
            index=models.Index(fields=['partner_name', '-created_at'], name='usersys_edi_partner_created_idx'),
        ),
        migrations.AddIndex(
            model_name='editransaction',
            index=models.Index(fields=['status', '-created_at'], name='usersys_edi_status_created_idx'),
        ),
        migrations.AddIndex(
            model_name='editransaction',
            index=models.Index(fields=['po_number'], name='usersys_edi_po_number_idx'),
        ),
        # Add indexes for TransactionHistory
        migrations.AddIndex(
            model_name='transactionhistory',
            index=models.Index(fields=['transaction', '-timestamp'], name='usersys_txn_transaction_time_idx'),
        ),
        migrations.AddIndex(
            model_name='transactionhistory',
            index=models.Index(fields=['-timestamp'], name='usersys_txn_timestamp_idx'),
        ),
    ]
