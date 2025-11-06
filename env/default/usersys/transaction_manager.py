"""
Transaction Manager Service
Business logic for EDI transaction operations
"""

import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError
from .modern_edi_models import EDITransaction, TransactionHistory


class TransactionManager:
    """Service class for managing EDI transactions"""
    
    def __init__(self):
        """Initialize the transaction manager"""
        self.botssys_dir = getattr(settings, 'BOTSSYS', 'botssys')
        self.modern_edi_base = os.path.join(self.botssys_dir, 'modern-edi')
    
    def _get_folder_path(self, folder):
        """Get the file system path for a folder"""
        return os.path.join(self.modern_edi_base, folder)
    
    def _validate_folder(self, folder):
        """Validate folder name"""
        valid_folders = ['inbox', 'received', 'outbox', 'sent', 'deleted']
        if folder not in valid_folders:
            raise ValidationError(f"Invalid folder: {folder}. Must be one of {valid_folders}")
    
    def _validate_transaction_data(self, data, folder):
        """Validate transaction data"""
        required_fields = ['partner_name', 'document_type']
        
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate folder-specific requirements
        if folder == 'outbox' and not data.get('metadata'):
            raise ValidationError("Outbox transactions require metadata")
        
        return True
    
    @transaction.atomic
    def create_transaction(self, folder, data, user=None):
        """
        Create a new transaction with validation
        
        Args:
            folder: Target folder ('inbox' or 'outbox')
            data: Dictionary with transaction data
            user: User creating the transaction
        
        Returns:
            EDITransaction instance
        """
        # Validate folder
        self._validate_folder(folder)
        if folder not in ['inbox', 'outbox']:
            raise ValidationError("Can only create transactions in inbox or outbox")
        
        # Validate data
        self._validate_transaction_data(data, folder)
        
        # Create transaction record
        txn = EDITransaction(
            folder=folder,
            partner_name=data['partner_name'],
            partner_id=data.get('partner_id'),
            document_type=data['document_type'],
            po_number=data.get('po_number'),
            filename=data.get('filename', f"{data['document_type']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.edi"),
            file_path='',  # Will be set after file is saved
            file_size=0,  # Will be updated after file is saved
            content_hash='',  # Will be calculated after file is saved
            status='draft',
            metadata=data.get('metadata', {}),
            created_by=user
        )
        
        # Save to get UUID
        txn.save()
        
        # Set file path with UUID
        folder_path = self._get_folder_path(folder)
        file_path = os.path.join(folder_path, f"{txn.id}.edi")
        txn.file_path = file_path
        txn.save()
        
        # Create history entry
        TransactionHistory.objects.create(
            transaction=txn,
            action='created',
            to_folder=folder,
            user=user,
            details={'initial_data': data}
        )
        
        return txn
    
    @transaction.atomic
    def update_transaction(self, transaction_id, data, user=None):
        """
        Update an existing transaction
        
        Args:
            transaction_id: UUID of transaction
            data: Dictionary with updated data
            user: User updating the transaction
        
        Returns:
            Updated EDITransaction instance
        """
        try:
            txn = EDITransaction.objects.get(id=transaction_id)
        except EDITransaction.DoesNotExist:
            raise ValidationError(f"Transaction {transaction_id} not found")
        
        # Check if transaction is editable
        if not txn.is_editable():
            raise ValidationError(f"Cannot edit transaction in {txn.folder} folder")
        
        # Store old values for history
        old_values = {
            'partner_name': txn.partner_name,
            'document_type': txn.document_type,
            'po_number': txn.po_number,
            'metadata': txn.metadata
        }
        
        # Update fields
        if 'partner_name' in data:
            txn.partner_name = data['partner_name']
        if 'partner_id' in data:
            txn.partner_id = data['partner_id']
        if 'document_type' in data:
            txn.document_type = data['document_type']
        if 'po_number' in data:
            txn.po_number = data['po_number']
        if 'metadata' in data:
            txn.metadata = data['metadata']
        
        txn.save()
        
        # Create history entry
        TransactionHistory.objects.create(
            transaction=txn,
            action='edited',
            user=user,
            details={
                'old_values': old_values,
                'new_values': data
            }
        )
        
        return txn
    
    @transaction.atomic
    def move_transaction(self, transaction_id, target_folder, user=None):
        """
        Move transaction between folders
        
        Args:
            transaction_id: UUID of transaction
            target_folder: Destination folder
            user: User moving the transaction
        
        Returns:
            Updated EDITransaction instance
        """
        try:
            txn = EDITransaction.objects.get(id=transaction_id)
        except EDITransaction.DoesNotExist:
            raise ValidationError(f"Transaction {transaction_id} not found")
        
        # Validate target folder
        self._validate_folder(target_folder)
        
        # Check if transaction is movable
        if not txn.is_movable():
            raise ValidationError(f"Cannot move transaction in {txn.folder} status")
        
        # Cannot move to same folder
        if txn.folder == target_folder:
            raise ValidationError(f"Transaction is already in {target_folder}")
        
        # Store old folder
        old_folder = txn.folder
        old_file_path = txn.file_path
        
        # Update folder
        txn.folder = target_folder
        
        # Update file path
        new_folder_path = self._get_folder_path(target_folder)
        new_file_path = os.path.join(new_folder_path, f"{txn.id}.edi")
        txn.file_path = new_file_path
        
        # Update timestamps based on target folder
        if target_folder == 'received':
            txn.received_at = datetime.now()
        elif target_folder == 'sent':
            txn.sent_at = datetime.now()
        elif target_folder == 'deleted':
            txn.deleted_at = datetime.now()
        
        txn.save()
        
        # Move physical file if it exists
        if os.path.exists(old_file_path):
            os.makedirs(new_folder_path, exist_ok=True)
            os.rename(old_file_path, new_file_path)
        
        # Create history entry
        TransactionHistory.objects.create(
            transaction=txn,
            action='moved',
            from_folder=old_folder,
            to_folder=target_folder,
            user=user,
            details={'reason': 'manual_move'}
        )
        
        return txn
    
    @transaction.atomic
    def send_transaction(self, transaction_id, user=None):
        """
        Send outgoing transaction via Bots
        
        Args:
            transaction_id: UUID of transaction
            user: User sending the transaction
        
        Returns:
            Updated EDITransaction instance
        """
        try:
            txn = EDITransaction.objects.get(id=transaction_id)
        except EDITransaction.DoesNotExist:
            raise ValidationError(f"Transaction {transaction_id} not found")
        
        # Check if transaction is sendable
        if not txn.is_sendable():
            raise ValidationError(f"Cannot send transaction in {txn.folder} folder with status {txn.status}")
        
        # Update status to processing
        txn.status = 'processing'
        txn.save()
        
        try:
            # Copy file to Bots outfile directory for processing
            bots_outfile = os.path.join(self.botssys_dir, 'outfile')
            os.makedirs(bots_outfile, exist_ok=True)
            
            dest_file = os.path.join(bots_outfile, f"{txn.id}.edi")
            
            if os.path.exists(txn.file_path):
                import shutil
                shutil.copy2(txn.file_path, dest_file)
            else:
                raise ValidationError(f"Transaction file not found: {txn.file_path}")
            
            # Execute Bots engine (this would trigger actual EDI transmission)
            # For now, we'll simulate success
            # In production, you would call: subprocess.run(['bots-engine'], ...)
            
            # Move to sent folder
            txn.folder = 'sent'
            txn.status = 'sent'
            txn.sent_at = datetime.now()
            
            # Update file path
            sent_folder_path = self._get_folder_path('sent')
            new_file_path = os.path.join(sent_folder_path, f"{txn.id}.edi")
            
            # Move physical file
            os.makedirs(sent_folder_path, exist_ok=True)
            if os.path.exists(txn.file_path):
                os.rename(txn.file_path, new_file_path)
            
            txn.file_path = new_file_path
            txn.save()
            
            # Create history entry
            TransactionHistory.objects.create(
                transaction=txn,
                action='sent',
                from_folder='outbox',
                to_folder='sent',
                user=user,
                details={'sent_at': txn.sent_at.isoformat()}
            )
            
            return txn
            
        except Exception as e:
            # Rollback status on failure
            txn.status = 'failed'
            txn.folder = 'outbox'
            txn.save()
            
            # Create history entry for failure
            TransactionHistory.objects.create(
                transaction=txn,
                action='sent',
                user=user,
                details={'error': str(e), 'status': 'failed'}
            )
            
            raise ValidationError(f"Failed to send transaction: {str(e)}")
    
    @transaction.atomic
    def delete_transaction(self, transaction_id, user=None, permanent=False):
        """
        Soft or hard delete transaction
        
        Args:
            transaction_id: UUID of transaction
            user: User deleting the transaction
            permanent: If True, permanently delete; if False, move to deleted folder
        
        Returns:
            None if permanent delete, updated EDITransaction if soft delete
        """
        try:
            txn = EDITransaction.objects.get(id=transaction_id)
        except EDITransaction.DoesNotExist:
            raise ValidationError(f"Transaction {transaction_id} not found")
        
        if permanent:
            # Permanent delete
            old_folder = txn.folder
            file_path = txn.file_path
            
            # Create history entry before deletion
            TransactionHistory.objects.create(
                transaction=txn,
                action='permanent_delete',
                from_folder=old_folder,
                user=user,
                details={'filename': txn.filename}
            )
            
            # Delete physical file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete database record
            txn.delete()
            
            return None
        else:
            # Soft delete - move to deleted folder
            return self.move_transaction(transaction_id, 'deleted', user)
    
    def parse_edi_file(self, file_path):
        """
        Parse EDI file and extract metadata
        
        Args:
            file_path: Path to EDI file
        
        Returns:
            Dictionary with parsed metadata
        """
        # This is a placeholder - actual implementation would parse EDI formats
        # For now, return basic file information
        
        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")
        
        metadata = {
            'file_size': os.path.getsize(file_path),
            'parsed_at': datetime.now().isoformat(),
            'format': 'unknown'  # Would be determined by parsing
        }
        
        # TODO: Implement actual EDI parsing using Bots grammars
        # This would extract partner info, PO numbers, line items, etc.
        
        return metadata
    
    def generate_edi_file(self, transaction_id):
        """
        Generate EDI file from transaction data
        
        Args:
            transaction_id: UUID of transaction
        
        Returns:
            Path to generated file
        """
        try:
            txn = EDITransaction.objects.get(id=transaction_id)
        except EDITransaction.DoesNotExist:
            raise ValidationError(f"Transaction {transaction_id} not found")
        
        # This is a placeholder - actual implementation would generate EDI
        # using Bots mappings and grammars
        
        # For now, create a simple text file with transaction data
        content = f"""EDI Transaction
Partner: {txn.partner_name}
Document Type: {txn.document_type}
PO Number: {txn.po_number or 'N/A'}
Created: {txn.created_at.isoformat()}

Metadata:
{txn.metadata}
"""
        
        # Write to file
        os.makedirs(os.path.dirname(txn.file_path), exist_ok=True)
        with open(txn.file_path, 'w') as f:
            f.write(content)
        
        # Update file size and hash
        import hashlib
        txn.file_size = os.path.getsize(txn.file_path)
        with open(txn.file_path, 'rb') as f:
            txn.content_hash = hashlib.sha256(f.read()).hexdigest()
        txn.save()
        
        return txn.file_path
    
    def check_acknowledgment(self, transaction_id):
        """
        Check if sent transaction was acknowledged
        
        Args:
            transaction_id: UUID of transaction
        
        Returns:
            Dictionary with acknowledgment status
        """
        try:
            txn = EDITransaction.objects.get(id=transaction_id)
        except EDITransaction.DoesNotExist:
            raise ValidationError(f"Transaction {transaction_id} not found")
        
        if txn.folder != 'sent':
            raise ValidationError("Can only check acknowledgment for sent transactions")
        
        # This is a placeholder - actual implementation would check Bots
        # for acknowledgment messages (997, CONTRL, etc.)
        
        # TODO: Implement actual acknowledgment checking
        # This would query Bots database for related acknowledgment messages
        
        return {
            'transaction_id': str(transaction_id),
            'acknowledgment_status': txn.acknowledgment_status or 'pending',
            'acknowledgment_message': txn.acknowledgment_message,
            'acknowledged_at': txn.acknowledged_at.isoformat() if txn.acknowledged_at else None
        }
    
    def get_folder_stats(self, folder):
        """
        Get statistics for a folder
        
        Args:
            folder: Folder name
        
        Returns:
            Dictionary with folder statistics
        """
        self._validate_folder(folder)
        
        transactions = EDITransaction.objects.filter(folder=folder)
        
        stats = {
            'folder': folder,
            'total_count': transactions.count(),
            'by_status': {},
            'by_document_type': {},
            'recent_count': transactions.filter(
                created_at__gte=datetime.now().replace(hour=0, minute=0, second=0)
            ).count()
        }
        
        # Count by status
        for status_choice in EDITransaction.STATUS_CHOICES:
            status = status_choice[0]
            count = transactions.filter(status=status).count()
            if count > 0:
                stats['by_status'][status] = count
        
        # Count by document type
        doc_types = transactions.values_list('document_type', flat=True).distinct()
        for doc_type in doc_types:
            count = transactions.filter(document_type=doc_type).count()
            stats['by_document_type'][doc_type] = count
        
        return stats
