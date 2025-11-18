"""
Modern EDI Interface API Views
REST API endpoints for transaction management
"""

import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q

from .modern_edi_models import EDITransaction, TransactionHistory
from .partner_models import Partner
from .transaction_manager import TransactionManager
from .file_manager import FileManager
from .edi_parser import EDIParser


# Initialize services
transaction_manager = TransactionManager()
file_manager = FileManager()
edi_parser = EDIParser()


def json_response(data, status=200):
    """Helper to create JSON responses"""
    return JsonResponse(data, status=status, safe=False)


def error_response(message, status=400, **kwargs):
    """Helper to create error responses"""
    error_data = {'error': message, **kwargs}
    return JsonResponse(error_data, status=status)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def list_transactions(request):
    """
    List all transactions with pagination and filtering
    
    GET /modern-edi/api/v1/transactions/
    Query params:
        - page: Page number (default: 1)
        - page_size: Items per page (default: 50, max: 100)
        - folder: Filter by folder
        - partner: Filter by partner name
        - document_type: Filter by document type
        - status: Filter by status
        - search: Search in partner name, PO number, filename
        - date_from: Filter by created_at >= date
        - date_to: Filter by created_at <= date
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = min(int(request.GET.get('page_size', 50)), 100)
        folder = request.GET.get('folder')
        partner = request.GET.get('partner')
        document_type = request.GET.get('document_type')
        status = request.GET.get('status')
        search = request.GET.get('search')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        # Build query
        queryset = EDITransaction.objects.all()
        
        # Apply filters
        if folder:
            queryset = queryset.filter(folder=folder)
        if partner:
            queryset = queryset.filter(partner_name__icontains=partner)
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        if status:
            queryset = queryset.filter(status=status)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        # Apply search
        if search:
            queryset = queryset.filter(
                Q(partner_name__icontains=search) |
                Q(po_number__icontains=search) |
                Q(filename__icontains=search)
            )
        
        # Paginate
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        # Serialize transactions
        transactions = []
        for txn in page_obj:
            transactions.append({
                'id': str(txn.id),
                'filename': txn.filename,
                'folder': txn.folder,
                'partner_name': txn.partner_name,
                'partner_id': txn.partner_id,
                'document_type': txn.document_type,
                'po_number': txn.po_number,
                'status': txn.status,
                'file_size': txn.file_size,
                'created_at': txn.created_at.isoformat(),
                'modified_at': txn.modified_at.isoformat(),
                'sent_at': txn.sent_at.isoformat() if txn.sent_at else None,
                'received_at': txn.received_at.isoformat() if txn.received_at else None,
                'acknowledged_at': txn.acknowledged_at.isoformat() if txn.acknowledged_at else None,
                'acknowledgment_status': txn.acknowledgment_status,
                'is_editable': txn.is_editable(),
                'is_sendable': txn.is_sendable(),
            })
        
        return json_response({
            'success': True,
            'transactions': transactions,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
        
    except Exception as e:
        return error_response(f"Failed to list transactions: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def list_transactions_by_folder(request, folder):
    """
    List transactions in a specific folder
    
    GET /modern-edi/api/v1/transactions/{folder}/
    """
    # Validate folder
    valid_folders = ['inbox', 'received', 'outbox', 'sent', 'deleted']
    if folder not in valid_folders:
        return error_response(f"Invalid folder: {folder}", status=400)
    
    # Add folder to request GET params and call list_transactions
    request.GET = request.GET.copy()
    request.GET['folder'] = folder
    
    return list_transactions(request)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_transaction(request, transaction_id):
    """
    Get transaction details
    
    GET /modern-edi/api/v1/transactions/{id}/
    """
    try:
        txn = EDITransaction.objects.get(id=transaction_id)
        
        # Serialize transaction with full details
        data = {
            'success': True,
            'transaction': {
                'id': str(txn.id),
                'filename': txn.filename,
                'folder': txn.folder,
                'partner_name': txn.partner_name,
                'partner_id': txn.partner_id,
                'document_type': txn.document_type,
                'po_number': txn.po_number,
                'file_path': txn.file_path,
                'file_size': txn.file_size,
                'content_hash': txn.content_hash,
                'status': txn.status,
                'created_at': txn.created_at.isoformat(),
                'modified_at': txn.modified_at.isoformat(),
                'received_at': txn.received_at.isoformat() if txn.received_at else None,
                'sent_at': txn.sent_at.isoformat() if txn.sent_at else None,
                'acknowledged_at': txn.acknowledged_at.isoformat() if txn.acknowledged_at else None,
                'deleted_at': txn.deleted_at.isoformat() if txn.deleted_at else None,
                'acknowledgment_status': txn.acknowledgment_status,
                'acknowledgment_message': txn.acknowledgment_message,
                'metadata': txn.metadata,
                'created_by': txn.created_by.username if txn.created_by else None,
                'bots_ta_id': txn.bots_ta_id,
                'is_editable': txn.is_editable(),
                'is_sendable': txn.is_sendable(),
                'is_movable': txn.is_movable(),
            }
        }
        
        return json_response(data)
        
    except EDITransaction.DoesNotExist:
        return error_response(f"Transaction not found: {transaction_id}", status=404)
    except Exception as e:
        return error_response(f"Failed to get transaction: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_transaction(request):
    """
    Create a new transaction
    
    POST /modern-edi/api/v1/transactions/
    Body: {
        "folder": "inbox" or "outbox",
        "partner_name": "Partner Name",
        "partner_id": "PARTNER123",
        "document_type": "850",
        "po_number": "PO123456",
        "filename": "optional_filename.edi",
        "metadata": {...}
    }
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        
        # Validate required fields
        if 'folder' not in data:
            return error_response("Missing required field: folder", status=400)
        if 'partner_name' not in data:
            return error_response("Missing required field: partner_name", status=400)
        if 'document_type' not in data:
            return error_response("Missing required field: document_type", status=400)
        
        # Create transaction
        txn = transaction_manager.create_transaction(
            folder=data['folder'],
            data=data,
            user=request.user
        )
        
        # Generate EDI file if metadata provided
        if data.get('metadata'):
            transaction_manager.generate_edi_file(txn.id)
        
        return json_response({
            'success': True,
            'message': 'Transaction created successfully',
            'transaction': {
                'id': str(txn.id),
                'filename': txn.filename,
                'folder': txn.folder,
                'partner_name': txn.partner_name,
                'document_type': txn.document_type,
                'po_number': txn.po_number,
                'status': txn.status,
                'created_at': txn.created_at.isoformat(),
            }
        }, status=201)
        
    except ValidationError as e:
        return error_response(str(e), status=400)
    except Exception as e:
        return error_response(f"Failed to create transaction: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@login_required
def update_transaction(request, transaction_id):
    """
    Update an existing transaction
    
    PUT/PATCH /modern-edi/api/v1/transactions/{id}/
    Body: {
        "partner_name": "Updated Partner Name",
        "partner_id": "PARTNER456",
        "document_type": "810",
        "po_number": "PO789",
        "metadata": {...}
    }
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        
        # Update transaction
        txn = transaction_manager.update_transaction(
            transaction_id=transaction_id,
            data=data,
            user=request.user
        )
        
        # Regenerate EDI file if metadata changed
        if 'metadata' in data:
            transaction_manager.generate_edi_file(txn.id)
        
        return json_response({
            'success': True,
            'message': 'Transaction updated successfully',
            'transaction': {
                'id': str(txn.id),
                'filename': txn.filename,
                'folder': txn.folder,
                'partner_name': txn.partner_name,
                'document_type': txn.document_type,
                'po_number': txn.po_number,
                'status': txn.status,
                'modified_at': txn.modified_at.isoformat(),
            }
        })
        
    except ValidationError as e:
        return error_response(str(e), status=400)
    except Exception as e:
        return error_response(f"Failed to update transaction: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
def delete_transaction(request, transaction_id):
    """
    Soft delete transaction (move to deleted folder)
    
    DELETE /modern-edi/api/v1/transactions/{id}/
    """
    try:
        # Soft delete (move to deleted folder)
        txn = transaction_manager.delete_transaction(
            transaction_id=transaction_id,
            user=request.user,
            permanent=False
        )
        
        return json_response({
            'success': True,
            'message': 'Transaction moved to deleted folder',
            'transaction': {
                'id': str(txn.id),
                'folder': txn.folder,
                'deleted_at': txn.deleted_at.isoformat() if txn.deleted_at else None,
            }
        })
        
    except ValidationError as e:
        return error_response(str(e), status=400)
    except Exception as e:
        return error_response(f"Failed to delete transaction: {str(e)}", status=500)



@csrf_exempt
@require_http_methods(["POST"])
@login_required
def move_transaction(request, transaction_id):
    """
    Move transaction to different folder
    
    POST /modern-edi/api/v1/transactions/{id}/move/
    Body: {
        "target_folder": "sent"
    }
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        
        if 'target_folder' not in data:
            return error_response("Missing required field: target_folder", status=400)
        
        # Move transaction
        txn = transaction_manager.move_transaction(
            transaction_id=transaction_id,
            target_folder=data['target_folder'],
            user=request.user
        )
        
        return json_response({
            'success': True,
            'message': f'Transaction moved to {data["target_folder"]}',
            'transaction': {
                'id': str(txn.id),
                'folder': txn.folder,
                'file_path': txn.file_path,
                'modified_at': txn.modified_at.isoformat(),
            }
        })
        
    except ValidationError as e:
        return error_response(str(e), status=400)
    except Exception as e:
        return error_response(f"Failed to move transaction: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def send_transaction(request, transaction_id):
    """
    Send outgoing transaction
    
    POST /modern-edi/api/v1/transactions/{id}/send/
    """
    try:
        # Send transaction
        txn = transaction_manager.send_transaction(
            transaction_id=transaction_id,
            user=request.user
        )
        
        return json_response({
            'success': True,
            'message': 'Transaction sent successfully',
            'transaction': {
                'id': str(txn.id),
                'folder': txn.folder,
                'status': txn.status,
                'sent_at': txn.sent_at.isoformat() if txn.sent_at else None,
            }
        })
        
    except ValidationError as e:
        return error_response(str(e), status=400)
    except Exception as e:
        return error_response(f"Failed to send transaction: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def permanent_delete_transaction(request, transaction_id):
    """
    Permanently delete transaction
    
    POST /modern-edi/api/v1/transactions/{id}/permanent-delete/
    """
    try:
        # Permanent delete
        transaction_manager.delete_transaction(
            transaction_id=transaction_id,
            user=request.user,
            permanent=True
        )
        
        return json_response({
            'success': True,
            'message': 'Transaction permanently deleted',
            'transaction_id': transaction_id
        })
        
    except ValidationError as e:
        return error_response(str(e), status=400)
    except Exception as e:
        return error_response(f"Failed to permanently delete transaction: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_transaction_history(request, transaction_id):
    """
    Get transaction history
    
    GET /modern-edi/api/v1/transactions/{id}/history/
    """
    try:
        # Verify transaction exists
        txn = EDITransaction.objects.get(id=transaction_id)
        
        # Get history
        history = TransactionHistory.objects.filter(transaction=txn).order_by('-timestamp')
        
        # Serialize history
        history_data = []
        for entry in history:
            history_data.append({
                'id': entry.id,
                'action': entry.action,
                'from_folder': entry.from_folder,
                'to_folder': entry.to_folder,
                'user': entry.user.username if entry.user else None,
                'timestamp': entry.timestamp.isoformat(),
                'details': entry.details,
            })
        
        return json_response({
            'success': True,
            'transaction_id': transaction_id,
            'history': history_data
        })
        
    except EDITransaction.DoesNotExist:
        return error_response(f"Transaction not found: {transaction_id}", status=404)
    except Exception as e:
        return error_response(f"Failed to get transaction history: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_transaction_raw(request, transaction_id):
    """
    Get raw EDI content
    
    GET /modern-edi/api/v1/transactions/{id}/raw/
    """
    try:
        # Get transaction
        txn = EDITransaction.objects.get(id=transaction_id)
        
        # Read file content
        content = file_manager.read_file(txn.file_path)
        
        return json_response({
            'success': True,
            'transaction_id': transaction_id,
            'filename': txn.filename,
            'content': content,
            'file_size': txn.file_size,
            'content_hash': txn.content_hash,
        })
        
    except EDITransaction.DoesNotExist:
        return error_response(f"Transaction not found: {transaction_id}", status=404)
    except Exception as e:
        return error_response(f"Failed to get raw content: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_folders(request):
    """
    Get folder list with counts
    
    GET /modern-edi/api/v1/folders/
    """
    try:
        folders = ['inbox', 'received', 'outbox', 'sent', 'deleted']
        
        folder_data = []
        for folder in folders:
            count = EDITransaction.objects.filter(folder=folder).count()
            folder_data.append({
                'name': folder,
                'display_name': folder.capitalize(),
                'count': count,
            })
        
        return json_response({
            'success': True,
            'folders': folder_data
        })
        
    except Exception as e:
        return error_response(f"Failed to get folders: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_folder_stats(request, folder):
    """
    Get folder statistics
    
    GET /modern-edi/api/v1/folders/{folder}/stats/
    """
    try:
        # Validate folder
        valid_folders = ['inbox', 'received', 'outbox', 'sent', 'deleted']
        if folder not in valid_folders:
            return error_response(f"Invalid folder: {folder}", status=400)
        
        # Get stats
        stats = transaction_manager.get_folder_stats(folder)
        
        return json_response({
            'success': True,
            **stats
        })
        
    except Exception as e:
        return error_response(f"Failed to get folder stats: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_partners(request):
    """
    Get list of trading partners with stats
    
    GET /modern-edi/api/v1/partners/
    """
    try:
        # Get all partners
        partners_qs = Partner.objects.all().order_by('name')
        
        # Check for status filter
        status = request.GET.get('status')
        if status:
            partners_qs = partners_qs.filter(status=status)
        
        partner_data = []
        for partner in partners_qs:
            # Get transaction count for this partner
            count = EDITransaction.objects.filter(partner_name=partner.name).count()
            
            # Get most recent transaction
            recent_txn = EDITransaction.objects.filter(partner_name=partner.name).order_by('-created_at').first()
            
            partner_data.append({
                'id': str(partner.id),
                'partner_id': partner.partner_id,
                'name': partner.name,
                'communication_method': partner.communication_method,
                'status': partner.status,
                'transaction_count': count,
                'last_activity': recent_txn.created_at.isoformat() if recent_txn else None,
            })
            
        # Also find partners in transactions that are not in Partner model
        # This helps finding ad-hoc or legacy partners
        existing_names = set(p['name'] for p in partner_data)
        txn_partners = EDITransaction.objects.exclude(partner_name__in=existing_names).values_list('partner_name', flat=True).distinct()
        
        for partner_name in txn_partners:
            if not partner_name:
                continue
                
            count = EDITransaction.objects.filter(partner_name=partner_name).count()
            recent_txn = EDITransaction.objects.filter(partner_name=partner_name).order_by('-created_at').first()
            
            partner_data.append({
                'id': 'legacy_' + partner_name, # Mock ID
                'partner_id': 'Unknown',
                'name': partner_name,
                'communication_method': 'manual', # Assume manual
                'status': 'active', # Assume active if transacting
                'transaction_count': count,
                'last_activity': recent_txn.created_at.isoformat() if recent_txn else None,
            })
            
        # Sort by name again
        partner_data.sort(key=lambda x: x['name'])
        
        return json_response({
            'success': True,
            'partners': partner_data
        })
        
    except Exception as e:
        return error_response(f"Failed to get partners: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_document_types(request):
    """
    Get list of available document types
    
    GET /modern-edi/api/v1/document-types/
    """
    try:
        # Get unique document types
        doc_types = EDITransaction.objects.values_list('document_type', flat=True).distinct().order_by('document_type')
        
        doc_type_data = []
        for doc_type in doc_types:
            if doc_type:
                # Get transaction count for this type
                count = EDITransaction.objects.filter(document_type=doc_type).count()
                
                # Get display name from parser
                display_name = edi_parser.DOCUMENT_TYPES.get(doc_type, doc_type)
                
                doc_type_data.append({
                    'code': doc_type,
                    'name': display_name,
                    'transaction_count': count,
                })
        
        # Add common document types that might not be in database yet
        for code, name in edi_parser.DOCUMENT_TYPES.items():
            if not any(d['code'] == code for d in doc_type_data):
                doc_type_data.append({
                    'code': code,
                    'name': name,
                    'transaction_count': 0,
                })
        
        return json_response({
            'success': True,
            'document_types': doc_type_data
        })
        
    except Exception as e:
        return error_response(f"Failed to get document types: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def search_transactions(request):
    """
    Search transactions with filters
    
    GET /modern-edi/api/v1/search/?q={query}&folder={folder}&partner={partner}&date_from={date}&date_to={date}
    """
    # This is handled by list_transactions with search parameter
    return list_transactions(request)



@csrf_exempt
@require_http_methods(["GET"])
@login_required
def validate_transaction(request, transaction_id):
    """
    Validate transaction for processing
    
    GET /modern-edi/api/v1/transaction/{id}/validate/
    """
    try:
        txn = EDITransaction.objects.get(id=transaction_id)
        
        # Get validation results
        validation = txn.validate_for_processing()
        
        # Get acknowledgment errors if applicable
        ack_errors = txn.get_acknowledgment_errors()
        
        return json_response({
            'success': True,
            'transaction_id': str(transaction_id),
            'validation': validation,
            'acknowledgment_errors': ack_errors,
            'has_errors': not validation['valid'] or len(ack_errors) > 0
        })
        
    except EDITransaction.DoesNotExist:
        return error_response(f"Transaction not found: {transaction_id}", status=404)
    except Exception as e:
        return error_response(f"Validation failed: {str(e)}", status=500)


@csrf_exempt
@require_http_methods(["GET"])
@login_required
def serve_modern_edi_app(request):
    """
    Serve the Modern EDI React SPA
    
    GET /modern-edi/
    """
    from django.shortcuts import render
    return render(request, 'modern-edi/index.html')


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def process_transaction(request, transaction_id):
    """
    Process transaction to next stage
    Inbox -> Received
    Outbox -> Sent
    
    POST /modern-edi/api/v1/transaction/{id}/process/
    """
    try:
        txn = EDITransaction.objects.get(id=transaction_id)
        
        # Validate transaction first
        validation = txn.validate_for_processing()
        if not validation['valid']:
            return error_response(
                'Transaction validation failed',
                status=400,
                validation_errors=validation['errors']
            )
        
        # Determine target folder based on current folder
        if txn.folder == 'inbox':
            target_folder = 'received'
            txn.received_at = datetime.now()
        elif txn.folder == 'outbox':
            # Use the send_transaction method for outbox
            return send_transaction(request, transaction_id)
        else:
            return error_response(
                f"Cannot process transaction from {txn.folder} folder",
                status=400
            )
        
        # Move to target folder
        txn = transaction_manager.move_transaction(
            transaction_id=transaction_id,
            target_folder=target_folder,
            user=request.user
        )
        
        return json_response({
            'success': True,
            'message': f'Transaction processed to {target_folder}',
            'transaction': {
                'id': str(txn.id),
                'folder': txn.folder,
                'status': txn.status,
                'received_at': txn.received_at.isoformat() if txn.received_at else None,
            }
        })
        
    except ValidationError as e:
        return error_response(str(e), status=400)
    except EDITransaction.DoesNotExist:
        return error_response(f"Transaction not found: {transaction_id}", status=404)
    except Exception as e:
        return error_response(f"Processing failed: {str(e)}", status=500)
