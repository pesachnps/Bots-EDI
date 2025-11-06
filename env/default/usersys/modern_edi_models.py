"""
Modern EDI Interface Models
Database models for folder-based EDI transaction management
"""

import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EDITransaction(models.Model):
    """Main transaction model for modern interface"""
    
    FOLDER_CHOICES = [
        ('inbox', 'Inbox'),
        ('received', 'Received'),
        ('outbox', 'Outbox'),
        ('sent', 'Sent'),
        ('deleted', 'Deleted'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('processing', 'Processing'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('failed', 'Failed'),
    ]
    
    # Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    
    # Folder Management
    folder = models.CharField(max_length=20, choices=FOLDER_CHOICES, db_index=True)
    
    # Transaction Data
    partner_name = models.CharField(max_length=255, db_index=True)
    partner_id = models.CharField(max_length=100, null=True, blank=True)
    document_type = models.CharField(max_length=50)
    po_number = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    
    # File Information
    file_path = models.CharField(max_length=500)
    file_size = models.IntegerField()
    content_hash = models.CharField(max_length=64)  # SHA-256
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, db_index=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)
    received_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Acknowledgment
    acknowledgment_status = models.CharField(max_length=20, null=True, blank=True)
    acknowledgment_message = models.TextField(null=True, blank=True)
    
    # Metadata (flexible storage for parsed EDI data)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Relationships
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_transactions'
    )
    bots_ta_id = models.IntegerField(null=True, blank=True)  # Link to Bots ta table
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "EDI Transaction"
        verbose_name_plural = "EDI Transactions"
        app_label = 'usersys'
        indexes = [
            models.Index(fields=['folder', '-created_at']),
            models.Index(fields=['partner_name', '-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['po_number']),
        ]
    
    def __str__(self):
        return f"{self.document_type} - {self.partner_name} ({self.folder})"
    
    def is_editable(self):
        """Check if transaction can be edited"""
        return self.folder in ['inbox', 'outbox']
    
    def is_sendable(self):
        """Check if transaction can be sent"""
        return self.folder == 'outbox' and self.status in ['draft', 'ready', 'failed']
    
    def is_movable(self):
        """Check if transaction can be moved"""
        return self.folder != 'processing'
    
    def get_display_date(self):
        """Get the most relevant date for display"""
        if self.folder == 'sent' and self.sent_at:
            return self.sent_at
        elif self.folder == 'received' and self.received_at:
            return self.received_at
        return self.created_at
    
    def validate_for_processing(self):
        """
        Validate if transaction has all required data for processing
        
        Returns:
            dict with 'valid' (bool) and 'errors' (list of error messages)
        """
        errors = []
        
        # Required fields for all transactions
        if not self.partner_name or not self.partner_name.strip():
            errors.append({
                'field': 'partner_name',
                'message': 'Partner name is required'
            })
        
        if not self.document_type or not self.document_type.strip():
            errors.append({
                'field': 'document_type',
                'message': 'Document type is required'
            })
        
        # Check if file exists and has content
        if not self.file_path or not os.path.exists(self.file_path):
            errors.append({
                'field': 'file_path',
                'message': 'EDI file is missing'
            })
        elif self.file_size == 0:
            errors.append({
                'field': 'file_size',
                'message': 'EDI file is empty'
            })
        
        # Folder-specific validation
        if self.folder in ['outbox', 'sent']:
            # Outgoing transactions need more data
            if not self.po_number or not self.po_number.strip():
                errors.append({
                    'field': 'po_number',
                    'message': 'PO number is required for outgoing transactions'
                })
            
            if not self.metadata or not isinstance(self.metadata, dict):
                errors.append({
                    'field': 'metadata',
                    'message': 'Transaction metadata is required'
                })
            else:
                # Check for required metadata fields
                if not self.metadata.get('buyer_name'):
                    errors.append({
                        'field': 'metadata.buyer_name',
                        'message': 'Buyer name is required in metadata'
                    })
                if not self.metadata.get('seller_name'):
                    errors.append({
                        'field': 'metadata.seller_name',
                        'message': 'Seller name is required in metadata'
                    })
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def get_acknowledgment_errors(self):
        """
        Get errors for unacknowledged or rejected transactions
        
        Returns:
            list of error dictionaries
        """
        errors = []
        
        if self.folder == 'sent':
            if not self.acknowledgment_status:
                errors.append({
                    'field': 'acknowledgment_status',
                    'message': 'No acknowledgment received yet',
                    'severity': 'warning'
                })
            elif self.acknowledgment_status == 'rejected':
                errors.append({
                    'field': 'acknowledgment_status',
                    'message': self.acknowledgment_message or 'Transaction was rejected by trading partner',
                    'severity': 'error'
                })
        
        if self.folder == 'received':
            # Check for processing errors
            if self.status == 'failed':
                errors.append({
                    'field': 'status',
                    'message': 'Transaction processing failed',
                    'severity': 'error'
                })
            
            # Validate received data
            validation = self.validate_for_processing()
            if not validation['valid']:
                errors.extend([{**e, 'severity': 'error'} for e in validation['errors']])
        
        return errors


class TransactionHistory(models.Model):
    """Track all changes to transactions"""
    
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('moved', 'Moved'),
        ('edited', 'Edited'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('deleted', 'Deleted'),
        ('restored', 'Restored'),
        ('permanent_delete', 'Permanently Deleted'),
    ]
    
    transaction = models.ForeignKey(
        EDITransaction, 
        on_delete=models.CASCADE,
        related_name='history'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    
    from_folder = models.CharField(max_length=20, null=True, blank=True)
    to_folder = models.CharField(max_length=20, null=True, blank=True)
    
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Additional context (JSON for flexibility)
    details = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Transaction History"
        verbose_name_plural = "Transaction Histories"
        app_label = 'usersys'
        indexes = [
            models.Index(fields=['transaction', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.transaction.filename} at {self.timestamp}"
