"""
Admin Dashboard API Views
Handles all admin dashboard endpoints for analytics, user management, and system monitoring
"""

import json
import csv
from io import StringIO
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q

from .analytics_service import AnalyticsService
from .user_manager import UserManager
from .activity_logger import ActivityLogger, log_activity
from .partner_models import Partner, PartnerUser, ActivityLog
from .sftp_config_service import SFTPConfigService


# Dashboard Overview Endpoints

@require_http_methods(["GET"])
def admin_dashboard_metrics(request):
    """
    Get dashboard overview metrics
    GET /api/v1/admin/dashboard/metrics?days=30
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        days = int(request.GET.get('days', 30))
        metrics = AnalyticsService.get_dashboard_metrics(days=days)
        
        return JsonResponse({
            'success': True,
            'metrics': metrics,
            'period_days': days
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def admin_dashboard_charts(request):
    """
    Get chart data for dashboard
    GET /api/v1/admin/dashboard/charts?days=30
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        days = int(request.GET.get('days', 30))
        
        # Get all chart data
        transaction_volume = AnalyticsService.get_transaction_volume_chart(days=days)
        top_partners = AnalyticsService.get_top_partners(limit=10, days=days)
        recent_errors = AnalyticsService.get_recent_errors(limit=10)
        system_status = AnalyticsService.get_system_status()
        
        return JsonResponse({
            'success': True,
            'charts': {
                'transaction_volume': transaction_volume,
                'top_partners': top_partners,
                'recent_errors': recent_errors,
                'system_status': system_status,
            },
            'period_days': days
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Partner Management Endpoints

@require_http_methods(["GET"])
def admin_partners_list(request):
    """
    List all partners with search and filter
    GET /api/v1/admin/partners?search=&status=&page=1
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        # Get query parameters
        search = request.GET.get('search', '').strip()
        status = request.GET.get('status', '').strip()
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 50))
        
        # Build query
        partners = Partner.objects.all()
        
        if search:
            partners = partners.filter(
                Q(name__icontains=search) |
                Q(partner_id__icontains=search) |
                Q(contact_email__icontains=search)
            )
        
        if status:
            partners = partners.filter(status=status)
        
        # Order by name
        partners = partners.order_by('name')
        
        # Paginate
        paginator = Paginator(partners, per_page)
        page_obj = paginator.get_page(page)
        
        # Serialize partners
        partners_data = []
        for partner in page_obj:
            partners_data.append({
                'id': str(partner.id),
                'partner_id': partner.partner_id,
                'name': partner.name,
                'display_name': partner.get_display_name(),
                'status': partner.status,
                'communication_method': partner.communication_method,
                'contact_email': partner.contact_email,
                'contact_name': partner.contact_name,
                'created_at': partner.created_at.isoformat(),
            })
        
        return JsonResponse({
            'success': True,
            'partners': partners_data,
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
def admin_partner_analytics(request, partner_id):
    """
    Get analytics for a specific partner
    GET /api/v1/admin/partners/<id>/analytics?days=30
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        days = int(request.GET.get('days', 30))
        analytics = AnalyticsService.get_partner_analytics(partner_id, days=days)
        
        return JsonResponse({
            'success': True,
            'analytics': analytics,
            'period_days': days
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def admin_partner_users(request, partner_id):
    """
    List all users for a partner
    GET /api/v1/admin/partners/<id>/users
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        users = UserManager.get_partner_users(partner_id)
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.get_full_name(),
                'phone': user.phone,
                'role': user.role,
                'is_active': user.is_active,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'created_at': user.created_at.isoformat(),
                'permissions': user.permissions.to_dict() if hasattr(user, 'permissions') else user.get_default_permissions(),
            })
        
        return JsonResponse({
            'success': True,
            'users': users_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def admin_create_partner_user(request, partner_id):
    """
    Create a new partner user
    POST /api/v1/admin/partners/<id>/users
    Body: {username, email, password, first_name, last_name, role, phone}
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        user = UserManager.create_user(
            partner_id=partner_id,
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role', 'partner_user'),
            phone=data.get('phone', ''),
            created_by=request.user
        )
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'partner_user_created',
            resource_type='partner_user',
            resource_id=str(user.id),
            details={'username': user.username, 'partner_id': str(partner_id)},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.get_full_name(),
                'role': user.role,
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# User Management Endpoints

@require_http_methods(["PUT"])
def admin_update_user(request, user_id):
    """
    Update a partner user
    PUT /api/v1/admin/users/<id>
    Body: {email, first_name, last_name, phone, role, is_active}
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        user = UserManager.update_user(user_id, **data)
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'partner_user_updated',
            resource_type='partner_user',
            resource_id=str(user.id),
            details={'username': user.username, 'changes': list(data.keys())},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.get_full_name(),
                'role': user.role,
                'is_active': user.is_active,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["DELETE"])
def admin_delete_user(request, user_id):
    """
    Delete a partner user
    DELETE /api/v1/admin/users/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        # Get user info before deleting
        user = PartnerUser.objects.get(id=user_id)
        username = user.username
        
        UserManager.delete_user(user_id)
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'partner_user_deleted',
            resource_type='partner_user',
            resource_id=str(user_id),
            details={'username': username},
            request=request
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
def admin_reset_user_password(request, user_id):
    """
    Reset a user's password
    POST /api/v1/admin/users/<id>/reset-password
    Body: {new_password}
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        new_password = data.get('new_password')
        
        if not new_password:
            return JsonResponse({'error': 'new_password is required'}, status=400)
        
        user = UserManager.reset_password(user_id, new_password)
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'partner_user_password_reset',
            resource_type='partner_user',
            resource_id=str(user.id),
            details={'username': user.username},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Password reset successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["PUT"])
def admin_update_user_permissions(request, user_id):
    """
    Update user permissions
    PUT /api/v1/admin/users/<id>/permissions
    Body: {can_view_transactions, can_upload_files, ...}
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        permissions = UserManager.update_permissions(user_id, data)
        
        # Log activity
        user = PartnerUser.objects.get(id=user_id)
        ActivityLogger.log_admin(
            request.user,
            'partner_user_permissions_updated',
            resource_type='partner_user',
            resource_id=str(user.id),
            details={'username': user.username, 'permissions': data},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'permissions': permissions.to_dict()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Analytics Endpoints

@require_http_methods(["GET"])
def admin_analytics_transactions(request):
    """
    Get transaction analytics
    GET /api/v1/admin/analytics/transactions?days=30
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        days = int(request.GET.get('days', 30))
        
        transaction_volume = AnalyticsService.get_transaction_volume_chart(days=days)
        processing_time = AnalyticsService.get_average_processing_time(days=days)
        
        return JsonResponse({
            'success': True,
            'analytics': {
                'transaction_volume': transaction_volume,
                'processing_time': processing_time,
            },
            'period_days': days
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def admin_analytics_partners(request):
    """
    Get partner analytics
    GET /api/v1/admin/analytics/partners?days=30
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        days = int(request.GET.get('days', 30))
        
        success_rates = AnalyticsService.get_partner_success_rates(days=days)
        top_partners = AnalyticsService.get_top_partners(limit=20, days=days)
        
        return JsonResponse({
            'success': True,
            'analytics': {
                'success_rates': success_rates,
                'top_partners': top_partners,
            },
            'period_days': days
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def admin_analytics_documents(request):
    """
    Get document type analytics
    GET /api/v1/admin/analytics/documents?days=30
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        days = int(request.GET.get('days', 30))
        
        document_breakdown = AnalyticsService.get_document_type_breakdown(days=days)
        activity_heatmap = AnalyticsService.get_activity_heatmap(days=days)
        
        return JsonResponse({
            'success': True,
            'analytics': {
                'document_breakdown': document_breakdown,
                'activity_heatmap': activity_heatmap,
            },
            'period_days': days
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Activity Log Endpoints

@require_http_methods(["GET"])
def admin_activity_logs(request):
    """
    Get activity logs with search and filter
    GET /api/v1/admin/activity-logs?search=&user_type=&action=&page=1
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        # Get query parameters
        search = request.GET.get('search', '').strip()
        user_type = request.GET.get('user_type', '').strip()
        action = request.GET.get('action', '').strip()
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 50))
        
        # Build query
        logs = ActivityLog.objects.all()
        
        if search:
            logs = logs.filter(
                Q(user_name__icontains=search) |
                Q(action__icontains=search) |
                Q(resource_type__icontains=search)
            )
        
        if user_type:
            logs = logs.filter(user_type=user_type)
        
        if action:
            logs = logs.filter(action=action)
        
        # Order by timestamp descending
        logs = logs.order_by('-timestamp')
        
        # Paginate
        paginator = Paginator(logs, per_page)
        page_obj = paginator.get_page(page)
        
        # Serialize logs
        logs_data = []
        for log in page_obj:
            logs_data.append({
                'id': log.id,
                'timestamp': log.timestamp.isoformat(),
                'user_type': log.user_type,
                'user_id': log.user_id,
                'user_name': log.user_name,
                'action': log.action,
                'resource_type': log.resource_type,
                'resource_id': log.resource_id,
                'details': log.details,
                'ip_address': log.ip_address,
            })
        
        return JsonResponse({
            'success': True,
            'logs': logs_data,
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
def admin_activity_logs_export(request):
    """
    Export activity logs to CSV
    GET /api/v1/admin/activity-logs/export?user_type=&action=
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        # Get query parameters
        user_type = request.GET.get('user_type', '').strip()
        action = request.GET.get('action', '').strip()
        
        # Build query
        logs = ActivityLog.objects.all()
        
        if user_type:
            logs = logs.filter(user_type=user_type)
        
        if action:
            logs = logs.filter(action=action)
        
        logs = logs.order_by('-timestamp')[:1000]  # Limit to 1000 records
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Timestamp', 'User Type', 'User Name', 'Action',
            'Resource Type', 'Resource ID', 'IP Address'
        ])
        
        # Write data
        for log in logs:
            writer.writerow([
                log.timestamp.isoformat(),
                log.user_type,
                log.user_name,
                log.action,
                log.resource_type,
                log.resource_id,
                log.ip_address or '',
            ])
        
        # Log export activity
        ActivityLogger.log_admin(
            request.user,
            'activity_logs_exported',
            details={'count': logs.count()},
            request=request
        )
        
        # Return CSV response
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="activity_logs.csv"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# SFTP Configuration Management Endpoints

@require_http_methods(["GET"])
def admin_partner_sftp_config(request, partner_id):
    """
    Get SFTP configuration for a partner
    GET /api/v1/admin/partners/<id>/sftp-config
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        sftp_config = SFTPConfigService.get_sftp_config(partner_id)
        
        if not sftp_config:
            return JsonResponse({
                'success': True,
                'has_config': False,
                'config': None
            })
        
        return JsonResponse({
            'success': True,
            'has_config': True,
            'config': sftp_config
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def admin_partner_sftp_config_create(request, partner_id):
    """
    Create SFTP configuration for a partner
    POST /api/v1/admin/partners/<id>/sftp-config
    Body: {
        "host": "sftp.example.com",
        "port": 22,
        "username": "partner_sftp",
        "auth_method": "password" | "key" | "both",
        "password": "...",  // if auth_method includes password
        "private_key_path": "/path/to/key",  // if auth_method includes key
        "inbound_directory": "/inbound",
        "outbound_directory": "/outbound",
        "archive_directory": "/archive",  // optional
        "inbound_file_pattern": "*.edi",
        "outbound_file_pattern": "{document_type}_{timestamp}.edi",
        "timeout": 30,
        "passive_mode": true,
        "poll_enabled": true,
        "poll_interval": 300
    }
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        sftp_config = SFTPConfigService.create_sftp_config(
            partner_id=partner_id,
            config_data=data,
            created_by=request.user
        )
        
        config_data = SFTPConfigService.get_sftp_config(partner_id)
        
        return JsonResponse({
            'success': True,
            'message': 'SFTP configuration created successfully',
            'config': config_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["PUT"])
def admin_partner_sftp_config_update(request, partner_id):
    """
    Update SFTP configuration for a partner
    PUT /api/v1/admin/partners/<id>/sftp-config
    Body: (any fields from create endpoint)
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        sftp_config = SFTPConfigService.update_sftp_config(
            partner_id=partner_id,
            config_data=data,
            updated_by=request.user
        )
        
        config_data = SFTPConfigService.get_sftp_config(partner_id)
        
        return JsonResponse({
            'success': True,
            'message': 'SFTP configuration updated successfully',
            'config': config_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["DELETE"])
def admin_partner_sftp_config_delete(request, partner_id):
    """
    Delete SFTP configuration for a partner
    DELETE /api/v1/admin/partners/<id>/sftp-config
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        SFTPConfigService.delete_sftp_config(
            partner_id=partner_id,
            deleted_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'SFTP configuration deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
def admin_partner_sftp_test_connection(request, partner_id):
    """
    Test SFTP connection for a partner
    POST /api/v1/admin/partners/<id>/sftp-config/test
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        result = SFTPConfigService.test_connection(
            partner_id=partner_id,
            test_by=request.user
        )
        
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def admin_generate_sftp_credentials(request):
    """
    Generate secure SFTP credentials
    POST /api/v1/admin/sftp/generate-credentials
    Body: {"username_prefix": "PARTNER001"}  // optional
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body) if request.body else {}
        username_prefix = data.get('username_prefix')
        
        credentials = SFTPConfigService.generate_credentials(username_prefix)
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'sftp_credentials_generated',
            details={'username': credentials['username']},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'credentials': credentials
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
