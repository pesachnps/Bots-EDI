"""
Partner Portal API Views
Handles all partner portal endpoints for transactions, files, and settings
"""

import json
import os
import zipfile
from io import BytesIO
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .analytics_service import AnalyticsService
from .activity_logger import ActivityLogger
from .modern_edi_models import EDITransaction
from .partner_models import Partner
from .file_manager import FileManager
from .transaction_manager import TransactionManager


# Dashboard Endpoints

@require_http_methods(["GET"])
def partner_dashboard_metrics(request):
    """
    Get dashboard metrics for partner
    GET /api/v1/partner-portal/dashboard/metrics?days=30
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        days = int(request.GET.get('days', 30))
        partner_id = request.partner.id
        
        # Get partner-specific analytics
        analytics = AnalyticsService.get_partner_analytics(partner_id, days=days)
        
        # Get recent transactions
        recent_transactions = EDITransaction.objects.filter(
            partner_id=partner_id
        ).order_by('-created_at')[:10]
        
        transactions_data = []
        for txn in recent_transactions:
            transactions_data.append({
                'id': str(txn.id),
                'date': txn.created_at.isoformat(),
                'type': txn.document_type,
                'po_number': txn.po_number,
                'status': txn.folder,
                'direction': 'sent' if txn.folder in ['outbox', 'sent'] else 'received',
            })
        
        return JsonResponse({
            'success': True,
            'metrics': analytics,
            'recent_transactions': transactions_data,
            'partner': {
                'id': str(request.partner.id),
                'name': request.partner.name,
                'partner_id': request.partner.partner_id,
            },
            'period_days': days
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Transaction Endpoints

@require_http_methods(["GET"])
def partner_transactions_list(request):
    """
    List partner transactions with search and filter
    GET /api/v1/partner-portal/transactions?search=&status=&type=&page=1
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not request.partner_permissions.can_view_transactions:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Get query parameters
        search = request.GET.get('search', '').strip()
        status = request.GET.get('status', '').strip()
        doc_type = request.GET.get('type', '').strip()
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 50))
        
        # Build query - filter by partner
        transactions = EDITransaction.objects.filter(partner_id=request.partner.id)
        
        if search:
            transactions = transactions.filter(
                Q(po_number__icontains=search) |
                Q(filename__icontains=search) |
                Q(document_type__icontains=search)
            )
        
        if status:
            transactions = transactions.filter(folder=status)
        
        if doc_type:
            transactions = transactions.filter(document_type=doc_type)
        
        # Order by created date descending
        transactions = transactions.order_by('-created_at')
        
        # Paginate
        paginator = Paginator(transactions, per_page)
        page_obj = paginator.get_page(page)
        
        # Serialize transactions
        transactions_data = []
        for txn in page_obj:
            transactions_data.append({
                'id': str(txn.id),
                'date': txn.created_at.isoformat(),
                'type': txn.document_type,
                'po_number': txn.po_number,
                'status': txn.folder,
                'direction': 'sent' if txn.folder in ['outbox', 'sent'] else 'received',
                'filename': txn.filename,
                'acknowledgment_status': txn.acknowledgment_status,
            })
        
        # Log activity
        ActivityLogger.log_partner(
            request.partner_user,
            'transactions_viewed',
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'transactions': transactions_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginator.count,
                'pages': paginator.num_pages,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def partner_transaction_detail(request, transaction_id):
    """
    Get transaction details
    GET /api/v1/partner-portal/transactions/<id>
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not request.partner_permissions.can_view_transactions:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Get transaction - ensure it belongs to this partner
        transaction = EDITransaction.objects.get(
            id=transaction_id,
            partner_id=request.partner.id
        )
        
        # Read file content if exists
        file_content = ''
        if transaction.file_path and os.path.exists(transaction.file_path):
            try:
                with open(transaction.file_path, 'r') as f:
                    file_content = f.read()
            except Exception:
                file_content = '[Unable to read file content]'
        
        # Get history
        history = transaction.history.all().order_by('-timestamp')
        history_data = []
        for h in history:
            history_data.append({
                'timestamp': h.timestamp.isoformat(),
                'action': h.action,
                'from_folder': h.from_folder,
                'to_folder': h.to_folder,
                'user': h.user,
                'details': h.details,
            })
        
        # Log activity
        ActivityLogger.log_partner(
            request.partner_user,
            'transaction_viewed',
            resource_type='transaction',
            resource_id=str(transaction.id),
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'transaction': {
                'id': str(transaction.id),
                'folder': transaction.folder,
                'partner_name': transaction.partner_name,
                'document_type': transaction.document_type,
                'po_number': transaction.po_number,
                'filename': transaction.filename,
                'file_size': transaction.file_size,
                'file_content': file_content,
                'created_at': transaction.created_at.isoformat(),
                'modified_at': transaction.modified_at.isoformat(),
                'sent_at': transaction.sent_at.isoformat() if transaction.sent_at else None,
                'received_at': transaction.received_at.isoformat() if transaction.received_at else None,
                'acknowledgment_status': transaction.acknowledgment_status,
                'acknowledgment_message': transaction.acknowledgment_message,
                'metadata': transaction.metadata,
                'history': history_data,
            }
        })
    except EDITransaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# File Upload Endpoints

@require_http_methods(["POST"])
def partner_file_upload(request):
    """
    Upload EDI file
    POST /api/v1/partner-portal/files/upload
    Form data: file, document_type, po_number (optional)
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not request.partner_permissions.can_upload_files:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Get uploaded file
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        document_type = request.POST.get('document_type', '')
        po_number = request.POST.get('po_number', '')
        
        # Validate file size (10 MB max)
        max_size = 10 * 1024 * 1024  # 10 MB
        if uploaded_file.size > max_size:
            return JsonResponse({'error': 'File too large (max 10 MB)'}, status=400)
        
        # Validate file extension
        allowed_extensions = ['.edi', '.x12', '.txt', '.xml']
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in allowed_extensions:
            return JsonResponse({
                'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'
            }, status=400)
        
        # Create transaction in inbox
        transaction = TransactionManager.create_transaction(
            folder='inbox',
            partner_name=request.partner.name,
            partner_id=str(request.partner.id),
            document_type=document_type,
            po_number=po_number,
            filename=uploaded_file.name,
            user=request.partner_user.username
        )
        
        # Save file
        file_content = uploaded_file.read()
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8', errors='ignore')
        
        FileManager.save_file(transaction, file_content)
        
        # Log activity
        ActivityLogger.log_partner(
            request.partner_user,
            'file_uploaded',
            resource_type='transaction',
            resource_id=str(transaction.id),
            details={
                'filename': uploaded_file.name,
                'size': uploaded_file.size,
                'document_type': document_type
            },
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'transaction': {
                'id': str(transaction.id),
                'filename': transaction.filename,
                'document_type': transaction.document_type,
                'po_number': transaction.po_number,
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# File Download Endpoints

@require_http_methods(["GET"])
def partner_files_list(request):
    """
    List files available for download
    GET /api/v1/partner-portal/files/download
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not request.partner_permissions.can_download_files:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Get files in received and sent folders for this partner
        files = EDITransaction.objects.filter(
            partner_id=request.partner.id,
            folder__in=['received', 'sent']
        ).order_by('-created_at')
        
        files_data = []
        for txn in files:
            files_data.append({
                'id': str(txn.id),
                'filename': txn.filename,
                'document_type': txn.document_type,
                'date': txn.created_at.isoformat(),
                'size': txn.file_size,
                'folder': txn.folder,
                'downloaded': txn.metadata.get('downloaded', False),
                'download_count': txn.metadata.get('download_count', 0),
            })
        
        return JsonResponse({
            'success': True,
            'files': files_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def partner_file_download(request, transaction_id):
    """
    Download a specific file
    GET /api/v1/partner-portal/files/download/<id>
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not request.partner_permissions.can_download_files:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Get transaction - ensure it belongs to this partner
        transaction = EDITransaction.objects.get(
            id=transaction_id,
            partner_id=request.partner.id
        )
        
        # Check file exists
        if not transaction.file_path or not os.path.exists(transaction.file_path):
            return JsonResponse({'error': 'File not found'}, status=404)
        
        # Mark as downloaded
        metadata = transaction.metadata or {}
        metadata['downloaded'] = True
        metadata['download_count'] = metadata.get('download_count', 0) + 1
        metadata['last_download'] = timezone.now().isoformat()
        transaction.metadata = metadata
        transaction.save(update_fields=['metadata'])
        
        # Log activity
        ActivityLogger.log_partner(
            request.partner_user,
            'file_downloaded',
            resource_type='transaction',
            resource_id=str(transaction.id),
            details={'filename': transaction.filename},
            request=request
        )
        
        # Return file
        response = FileResponse(open(transaction.file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{transaction.filename}"'
        return response
        
    except EDITransaction.DoesNotExist:
        return JsonResponse({'error': 'File not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def partner_files_bulk_download(request):
    """
    Bulk download files as ZIP
    POST /api/v1/partner-portal/files/download/bulk
    Body: {transaction_ids: [...]}
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not request.partner_permissions.can_download_files:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        transaction_ids = data.get('transaction_ids', [])
        
        if not transaction_ids:
            return JsonResponse({'error': 'No files selected'}, status=400)
        
        # Get transactions - ensure they belong to this partner
        transactions = EDITransaction.objects.filter(
            id__in=transaction_ids,
            partner_id=request.partner.id
        )
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for txn in transactions:
                if txn.file_path and os.path.exists(txn.file_path):
                    zip_file.write(txn.file_path, txn.filename)
        
        # Log activity
        ActivityLogger.log_partner(
            request.partner_user,
            'files_bulk_downloaded',
            details={'count': len(transactions)},
            request=request
        )
        
        # Return ZIP
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="edi_files.zip"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Settings Endpoints

@require_http_methods(["GET"])
def partner_settings_get(request):
    """
    Get partner settings
    GET /api/v1/partner-portal/settings
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        partner = request.partner
        
        # Get connection configs (read-only for partners)
        sftp_config = None
        api_config = None
        
        if hasattr(partner, 'sftp_config'):
            sftp_config = {
                'host': partner.sftp_config.host,
                'port': partner.sftp_config.port,
                'username': partner.sftp_config.username,
                'status': partner.sftp_config.last_connection_status,
                'last_test': partner.sftp_config.last_connection_test.isoformat() if partner.sftp_config.last_connection_test else None,
            }
        
        if hasattr(partner, 'api_config'):
            api_config = {
                'base_url': partner.api_config.base_url,
                'status': partner.api_config.last_connection_status,
                'last_test': partner.api_config.last_connection_test.isoformat() if partner.api_config.last_connection_test else None,
            }
        
        return JsonResponse({
            'success': True,
            'settings': {
                'partner': {
                    'id': str(partner.id),
                    'partner_id': partner.partner_id,
                    'name': partner.name,
                    'contact_name': partner.contact_name,
                    'contact_email': partner.contact_email,
                    'contact_phone': partner.contact_phone,
                    'communication_method': partner.communication_method,
                },
                'sftp_config': sftp_config,
                'api_config': api_config,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["PUT"])
def partner_settings_update_contact(request):
    """
    Update partner contact information
    PUT /api/v1/partner-portal/settings/contact
    Body: {contact_name, contact_email, contact_phone}
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if not request.partner_permissions.can_manage_settings:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        partner = request.partner
        
        # Update contact info
        if 'contact_name' in data:
            partner.contact_name = data['contact_name'].strip()
        if 'contact_email' in data:
            partner.contact_email = data['contact_email'].strip()
        if 'contact_phone' in data:
            partner.contact_phone = data['contact_phone'].strip()
        
        partner.save()
        
        # Log activity
        ActivityLogger.log_partner(
            request.partner_user,
            'settings_updated',
            resource_type='partner',
            resource_id=str(partner.id),
            details={'fields': list(data.keys())},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Contact information updated'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def partner_settings_test_connection(request):
    """
    Test partner connection (SFTP or API)
    POST /api/v1/partner-portal/settings/test-connection
    """
    if not hasattr(request, 'partner_user'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        partner = request.partner
        results = {}
        
        # Test SFTP if configured
        if partner.supports_sftp() and hasattr(partner, 'sftp_config'):
            # In production, implement actual SFTP test
            results['sftp'] = {
                'status': 'success',
                'message': 'SFTP connection test not implemented'
            }
        
        # Test API if configured
        if partner.supports_api() and hasattr(partner, 'api_config'):
            # In production, implement actual API test
            results['api'] = {
                'status': 'success',
                'message': 'API connection test not implemented'
            }
        
        # Log activity
        ActivityLogger.log_partner(
            request.partner_user,
            'connection_tested',
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'results': results
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
