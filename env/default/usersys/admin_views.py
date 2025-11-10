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
from .partner_models import Partner, PartnerUser, ActivityLog, ScheduledReport
from .sftp_config_service import SFTPConfigService
from .report_service import ReportScheduler


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
            'results': logs_data,
            'count': paginator.count,
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


# Scheduled Reports Management Endpoints

@require_http_methods(["GET"])
def admin_scheduled_reports_list(request):
    """
    List all scheduled reports with filtering
    GET /api/v1/admin/scheduled-reports?partner_id=&report_type=&is_active=
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        partner_id = request.GET.get('partner_id')
        report_type = request.GET.get('report_type')
        is_active = request.GET.get('is_active')
        
        reports = ScheduledReport.objects.select_related('partner').all()
        
        if partner_id:
            reports = reports.filter(partner_id=partner_id)
        if report_type:
            reports = reports.filter(report_type=report_type)
        if is_active is not None:
            reports = reports.filter(is_active=is_active.lower() == 'true')
        
        reports = reports.order_by('-created_at')
        
        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'partner_id': str(report.partner.id),
                'partner_name': report.partner.name,
                'name': report.name,
                'description': report.description,
                'report_type': report.report_type,
                'format': report.format,
                'frequency': report.frequency,
                'recipients': report.recipients,
                'is_active': report.is_active,
                'last_run': report.last_run.isoformat() if report.last_run else None,
                'last_run_status': report.last_run_status,
                'next_run': report.next_run.isoformat() if report.next_run else None,
                'run_count': report.run_count,
                'created_at': report.created_at.isoformat(),
            })
        
        return JsonResponse({
            'success': True,
            'reports': reports_data,
            'count': len(reports_data)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def admin_scheduled_report_create(request):
    """
    Create a new scheduled report
    POST /api/v1/admin/scheduled-reports
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        report = ScheduledReport.objects.create(
            partner_id=data['partner_id'],
            name=data['name'],
            description=data.get('description', ''),
            report_type=data['report_type'],
            format=data.get('format', 'csv'),
            recipients=data.get('recipients', []),
            frequency=data.get('frequency', 'weekly'),
            day_of_week=data.get('day_of_week'),
            day_of_month=data.get('day_of_month'),
            time_of_day=data.get('time_of_day', '09:00:00'),
            timezone=data.get('timezone', 'UTC'),
            filters=data.get('filters', {}),
            date_range_days=data.get('date_range_days', 30),
            is_active=data.get('is_active', True),
            created_by=request.user
        )
        
        # Calculate next run
        report.calculate_next_run()
        report.save()
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'scheduled_report_created',
            details={
                'report_id': report.id,
                'report_name': report.name,
                'partner': report.partner.name
            },
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Scheduled report created successfully',
            'report_id': report.id,
            'next_run': report.next_run.isoformat() if report.next_run else None
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["PUT"])
def admin_scheduled_report_update(request, report_id):
    """
    Update a scheduled report
    PUT /api/v1/admin/scheduled-reports/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        report = ScheduledReport.objects.get(id=report_id)
        data = json.loads(request.body)
        
        # Update fields
        if 'name' in data:
            report.name = data['name']
        if 'description' in data:
            report.description = data['description']
        if 'report_type' in data:
            report.report_type = data['report_type']
        if 'format' in data:
            report.format = data['format']
        if 'recipients' in data:
            report.recipients = data['recipients']
        if 'frequency' in data:
            report.frequency = data['frequency']
        if 'day_of_week' in data:
            report.day_of_week = data['day_of_week']
        if 'day_of_month' in data:
            report.day_of_month = data['day_of_month']
        if 'time_of_day' in data:
            report.time_of_day = data['time_of_day']
        if 'timezone' in data:
            report.timezone = data['timezone']
        if 'filters' in data:
            report.filters = data['filters']
        if 'date_range_days' in data:
            report.date_range_days = data['date_range_days']
        if 'is_active' in data:
            report.is_active = data['is_active']
        
        # Recalculate next run if schedule changed
        if any(k in data for k in ['frequency', 'day_of_week', 'day_of_month', 'time_of_day', 'timezone']):
            report.calculate_next_run()
        
        report.save()
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'scheduled_report_updated',
            details={
                'report_id': report.id,
                'report_name': report.name,
                'updated_fields': list(data.keys())
            },
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Scheduled report updated successfully',
            'next_run': report.next_run.isoformat() if report.next_run else None
        })
    except ScheduledReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["DELETE"])
def admin_scheduled_report_delete(request, report_id):
    """
    Delete a scheduled report
    DELETE /api/v1/admin/scheduled-reports/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        report = ScheduledReport.objects.get(id=report_id)
        report_name = report.name
        partner_name = report.partner.name
        
        report.delete()
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'scheduled_report_deleted',
            details={
                'report_id': report_id,
                'report_name': report_name,
                'partner': partner_name
            },
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Scheduled report deleted successfully'
        })
    except ScheduledReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["POST"])
def admin_scheduled_report_run_now(request, report_id):
    """
    Execute a scheduled report immediately
    POST /api/v1/admin/scheduled-reports/<id>/run
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        report = ScheduledReport.objects.get(id=report_id)
        
        # Execute report
        result = ReportScheduler.execute_report(report.id, send_email=True)
        
        # Log activity
        ActivityLogger.log_admin(
            request.user,
            'scheduled_report_run_manually',
            details={
                'report_id': report.id,
                'report_name': report.name,
                'success': result.get('success')
            },
            request=request
        )
        
        return JsonResponse(result)
    except ScheduledReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def admin_scheduled_report_preview(request, report_id):
    """
    Preview a scheduled report (generate but don't email)
    POST /api/v1/admin/scheduled-reports/<id>/preview
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        report = ScheduledReport.objects.get(id=report_id)
        
        # Execute report without sending email
        result = ReportScheduler.execute_report(report.id, send_email=False)
        
        return JsonResponse(result)
    except ScheduledReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========================================
# Routes Management
# ========================================

@require_http_methods(["GET"])
def admin_routes_list(request):
    """
    List all routes with search and filtering
    GET /api/v1/admin/routes?search=&idroute=&fromchannel=&tochannel=&active=&page=1
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel
        
        # Get query parameters
        search = request.GET.get('search', '').strip()
        idroute = request.GET.get('idroute', '').strip()
        fromchannel = request.GET.get('fromchannel', '').strip()
        tochannel = request.GET.get('tochannel', '').strip()
        active = request.GET.get('active', '').strip()
        fromeditype = request.GET.get('fromeditype', '').strip()
        toeditype = request.GET.get('toeditype', '').strip()
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 50))
        
        # Build query
        routes_qs = RoutesModel.objects.select_related(
            'fromchannel', 'tochannel', 'frompartner', 'topartner',
            'frompartner_tochannel', 'topartner_tochannel'
        ).all()
        
        # Apply filters
        if search:
            routes_qs = routes_qs.filter(
                Q(idroute__icontains=search) |
                Q(fromeditype__icontains=search) |
                Q(toeditype__icontains=search) |
                Q(desc__icontains=search)
            )
        
        if idroute:
            routes_qs = routes_qs.filter(idroute=idroute)
        
        if fromchannel:
            routes_qs = routes_qs.filter(fromchannel__idchannel=fromchannel)
        
        if tochannel:
            routes_qs = routes_qs.filter(tochannel__idchannel=tochannel)
        
        if active:
            routes_qs = routes_qs.filter(active=(active.lower() == 'true'))
        
        if fromeditype:
            routes_qs = routes_qs.filter(fromeditype=fromeditype)
        
        if toeditype:
            routes_qs = routes_qs.filter(toeditype=toeditype)
        
        # Order by idroute and sequence
        routes_qs = routes_qs.order_by('idroute', 'seq')
        
        # Paginate
        paginator = Paginator(routes_qs, per_page)
        page_obj = paginator.get_page(page)
        
        # Serialize routes
        routes_data = []
        for route in page_obj:
            routes_data.append({
                'id': route.id,
                'idroute': route.idroute,
                'seq': route.seq,
                'active': route.active,
                'notindefaultrun': route.notindefaultrun,
                'fromchannel': {
                    'id': route.fromchannel.id if route.fromchannel else None,
                    'idchannel': route.fromchannel.idchannel if route.fromchannel else None,
                    'type': route.fromchannel.type if route.fromchannel else None,
                } if route.fromchannel else None,
                'fromeditype': route.fromeditype,
                'frommessagetype': route.frommessagetype,
                'translateind': route.translateind,
                'alt': route.alt,
                'tochannel': {
                    'id': route.tochannel.id if route.tochannel else None,
                    'idchannel': route.tochannel.idchannel if route.tochannel else None,
                    'type': route.tochannel.type if route.tochannel else None,
                } if route.tochannel else None,
                'toeditype': route.toeditype,
                'tomessagetype': route.tomessagetype,
                'frompartner': {
                    'id': str(route.frompartner.id) if route.frompartner and hasattr(route.frompartner, 'id') else None,
                    'idpartner': route.frompartner.idpartner if route.frompartner else None,
                } if route.frompartner else None,
                'topartner': {
                    'id': str(route.topartner.id) if route.topartner and hasattr(route.topartner, 'id') else None,
                    'idpartner': route.topartner.idpartner if route.topartner else None,
                } if route.topartner else None,
                'frompartner_tochannel': {
                    'id': str(route.frompartner_tochannel.id) if route.frompartner_tochannel and hasattr(route.frompartner_tochannel, 'id') else None,
                    'idpartner': route.frompartner_tochannel.idpartner if route.frompartner_tochannel else None,
                } if route.frompartner_tochannel else None,
                'topartner_tochannel': {
                    'id': str(route.topartner_tochannel.id) if route.topartner_tochannel and hasattr(route.topartner_tochannel, 'id') else None,
                    'idpartner': route.topartner_tochannel.idpartner if route.topartner_tochannel else None,
                } if route.topartner_tochannel else None,
                'testindicator': route.testindicator,
                'dirmonitor': route.dirmonitor,
                'defer': route.defer,
                'zip_incoming': route.zip_incoming,
                'zip_outgoing': route.zip_outgoing,
                'desc': route.desc,
                'routescript': getattr(route, 'routescript', None),
            })
        
        return JsonResponse({
            'success': True,
            'routes': routes_data,
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
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@require_http_methods(["POST"])
def admin_route_create(request):
    """
    Create a new route
    POST /api/v1/admin/routes
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel, channel, partner as PartnerModel
        
        data = json.loads(request.body)
        
        # Create route
        route = RoutesModel()
        route.idroute = data.get('idroute')
        route.seq = data.get('seq', 1)
        route.active = data.get('active', False)
        route.notindefaultrun = data.get('notindefaultrun', False)
        
        # Channels
        if data.get('fromchannel_id'):
            route.fromchannel = channel.objects.get(id=data['fromchannel_id'])
        if data.get('tochannel_id'):
            route.tochannel = channel.objects.get(id=data['tochannel_id'])
        
        # EDI types
        route.fromeditype = data.get('fromeditype', '')
        route.frommessagetype = data.get('frommessagetype', '')
        route.toeditype = data.get('toeditype', '')
        route.tomessagetype = data.get('tomessagetype', '')
        
        # Translation
        route.translateind = data.get('translateind', 1)
        route.alt = data.get('alt', '')
        
        # Partners
        if data.get('frompartner_id'):
            route.frompartner = PartnerModel.objects.get(idpartner=data['frompartner_id'])
        if data.get('topartner_id'):
            route.topartner = PartnerModel.objects.get(idpartner=data['topartner_id'])
        if data.get('frompartner_tochannel_id'):
            route.frompartner_tochannel = PartnerModel.objects.get(idpartner=data['frompartner_tochannel_id'])
        if data.get('topartner_tochannel_id'):
            route.topartner_tochannel = PartnerModel.objects.get(idpartner=data['topartner_tochannel_id'])
        
        # Other fields
        route.testindicator = data.get('testindicator', '')
        route.dirmonitor = data.get('dirmonitor', False)
        route.defer = data.get('defer', False)
        route.zip_incoming = data.get('zip_incoming')
        route.zip_outgoing = data.get('zip_outgoing')
        route.desc = data.get('desc', '')
        
        route.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Route created successfully',
            'route_id': route.id
        })
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["GET"])
def admin_route_detail(request, route_id):
    """
    Get route details
    GET /api/v1/admin/routes/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel
        
        route = RoutesModel.objects.select_related(
            'fromchannel', 'tochannel', 'frompartner', 'topartner',
            'frompartner_tochannel', 'topartner_tochannel'
        ).get(id=route_id)
        
        route_data = {
            'id': route.id,
            'idroute': route.idroute,
            'seq': route.seq,
            'active': route.active,
            'notindefaultrun': route.notindefaultrun,
            'fromchannel': {
                'id': route.fromchannel.id,
                'idchannel': route.fromchannel.idchannel,
                'type': route.fromchannel.type,
                'inorout': route.fromchannel.inorout,
            } if route.fromchannel else None,
            'fromeditype': route.fromeditype,
            'frommessagetype': route.frommessagetype,
            'translateind': route.translateind,
            'alt': route.alt,
            'tochannel': {
                'id': route.tochannel.id,
                'idchannel': route.tochannel.idchannel,
                'type': route.tochannel.type,
                'inorout': route.tochannel.inorout,
            } if route.tochannel else None,
            'toeditype': route.toeditype,
            'tomessagetype': route.tomessagetype,
            'frompartner': {
                'id': str(route.frompartner.id) if hasattr(route.frompartner, 'id') else None,
                'idpartner': route.frompartner.idpartner,
                'name': route.frompartner.name,
            } if route.frompartner else None,
            'topartner': {
                'id': str(route.topartner.id) if hasattr(route.topartner, 'id') else None,
                'idpartner': route.topartner.idpartner,
                'name': route.topartner.name,
            } if route.topartner else None,
            'frompartner_tochannel': {
                'id': str(route.frompartner_tochannel.id) if hasattr(route.frompartner_tochannel, 'id') else None,
                'idpartner': route.frompartner_tochannel.idpartner,
                'name': route.frompartner_tochannel.name,
            } if route.frompartner_tochannel else None,
            'topartner_tochannel': {
                'id': str(route.topartner_tochannel.id) if hasattr(route.topartner_tochannel, 'id') else None,
                'idpartner': route.topartner_tochannel.idpartner,
                'name': route.topartner_tochannel.name,
            } if route.topartner_tochannel else None,
            'testindicator': route.testindicator,
            'dirmonitor': route.dirmonitor,
            'defer': route.defer,
            'zip_incoming': route.zip_incoming,
            'zip_outgoing': route.zip_outgoing,
            'desc': route.desc,
            'routescript': getattr(route, 'routescript', None),
            'rsrv1': route.rsrv1,
            'rsrv2': route.rsrv2,
        }
        
        return JsonResponse({
            'success': True,
            'route': route_data
        })
    except RoutesModel.DoesNotExist:
        return JsonResponse({'error': 'Route not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@require_http_methods(["PUT"])
def admin_route_update(request, route_id):
    """
    Update a route
    PUT /api/v1/admin/routes/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel, channel, partner as PartnerModel
        
        route = RoutesModel.objects.get(id=route_id)
        data = json.loads(request.body)
        
        # Update fields
        if 'idroute' in data:
            route.idroute = data['idroute']
        if 'seq' in data:
            route.seq = data['seq']
        if 'active' in data:
            route.active = data['active']
        if 'notindefaultrun' in data:
            route.notindefaultrun = data['notindefaultrun']
        
        # Channels
        if 'fromchannel_id' in data:
            route.fromchannel = channel.objects.get(id=data['fromchannel_id']) if data['fromchannel_id'] else None
        if 'tochannel_id' in data:
            route.tochannel = channel.objects.get(id=data['tochannel_id']) if data['tochannel_id'] else None
        
        # EDI types
        if 'fromeditype' in data:
            route.fromeditype = data['fromeditype']
        if 'frommessagetype' in data:
            route.frommessagetype = data['frommessagetype']
        if 'toeditype' in data:
            route.toeditype = data['toeditype']
        if 'tomessagetype' in data:
            route.tomessagetype = data['tomessagetype']
        
        # Translation
        if 'translateind' in data:
            route.translateind = data['translateind']
        if 'alt' in data:
            route.alt = data['alt']
        
        # Partners
        if 'frompartner_id' in data:
            route.frompartner = PartnerModel.objects.get(idpartner=data['frompartner_id']) if data['frompartner_id'] else None
        if 'topartner_id' in data:
            route.topartner = PartnerModel.objects.get(idpartner=data['topartner_id']) if data['topartner_id'] else None
        if 'frompartner_tochannel_id' in data:
            route.frompartner_tochannel = PartnerModel.objects.get(idpartner=data['frompartner_tochannel_id']) if data['frompartner_tochannel_id'] else None
        if 'topartner_tochannel_id' in data:
            route.topartner_tochannel = PartnerModel.objects.get(idpartner=data['topartner_tochannel_id']) if data['topartner_tochannel_id'] else None
        
        # Other fields
        if 'testindicator' in data:
            route.testindicator = data['testindicator']
        if 'dirmonitor' in data:
            route.dirmonitor = data['dirmonitor']
        if 'defer' in data:
            route.defer = data['defer']
        if 'zip_incoming' in data:
            route.zip_incoming = data['zip_incoming']
        if 'zip_outgoing' in data:
            route.zip_outgoing = data['zip_outgoing']
        if 'desc' in data:
            route.desc = data['desc']
        
        route.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Route updated successfully'
        })
    except RoutesModel.DoesNotExist:
        return JsonResponse({'error': 'Route not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["DELETE"])
def admin_route_delete(request, route_id):
    """
    Delete a route
    DELETE /api/v1/admin/routes/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel
        
        route = RoutesModel.objects.get(id=route_id)
        route_idroute = route.idroute
        route_seq = route.seq
        
        route.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Route {route_idroute} seq {route_seq} deleted successfully'
        })
    except RoutesModel.DoesNotExist:
        return JsonResponse({'error': 'Route not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["POST"])
def admin_route_toggle_active(request, route_id):
    """
    Toggle route active status
    POST /api/v1/admin/routes/<id>/activate
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel
        
        route = RoutesModel.objects.get(id=route_id)
        route.active = not route.active
        route.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Route {"activated" if route.active else "deactivated"} successfully',
            'active': route.active
        })
    except RoutesModel.DoesNotExist:
        return JsonResponse({'error': 'Route not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["POST"])
def admin_route_clone(request, route_id):
    """
    Clone a route
    POST /api/v1/admin/routes/<id>/clone
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel
        
        route = RoutesModel.objects.get(id=route_id)
        data = json.loads(request.body) if request.body else {}
        
        # Create a copy
        new_route = RoutesModel()
        new_route.idroute = data.get('new_idroute', f"{route.idroute}_copy")
        new_route.seq = data.get('new_seq', route.seq)
        new_route.active = False  # Cloned routes start as inactive
        new_route.notindefaultrun = route.notindefaultrun
        new_route.fromchannel = route.fromchannel
        new_route.fromeditype = route.fromeditype
        new_route.frommessagetype = route.frommessagetype
        new_route.translateind = route.translateind
        new_route.alt = route.alt
        new_route.tochannel = route.tochannel
        new_route.toeditype = route.toeditype
        new_route.tomessagetype = route.tomessagetype
        new_route.frompartner = route.frompartner
        new_route.topartner = route.topartner
        new_route.frompartner_tochannel = route.frompartner_tochannel
        new_route.topartner_tochannel = route.topartner_tochannel
        new_route.testindicator = route.testindicator
        new_route.dirmonitor = False  # Don't clone dirmonitor setting
        new_route.defer = route.defer
        new_route.zip_incoming = route.zip_incoming
        new_route.zip_outgoing = route.zip_outgoing
        new_route.desc = route.desc
        new_route.rsrv1 = route.rsrv1
        new_route.rsrv2 = route.rsrv2
        
        new_route.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Route cloned successfully',
            'route_id': new_route.id,
            'idroute': new_route.idroute
        })
    except RoutesModel.DoesNotExist:
        return JsonResponse({'error': 'Route not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["POST"])
def admin_routes_export(request):
    """
    Export selected routes as a plugin
    POST /api/v1/admin/routes/export
    Body: {"route_ids": [1, 2, 3], "include_translations": true}
    """
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({'error': 'Superuser access required'}, status=403)
    
    try:
        from bots.models import routes as RoutesModel
        from bots import pluglib
        import tempfile
        import os
        
        data = json.loads(request.body)
        route_ids = data.get('route_ids', [])
        include_translations = data.get('include_translations', True)
        
        if not route_ids:
            return JsonResponse({'error': 'No routes selected'}, status=400)
        
        # Get routes queryset
        routes_qs = RoutesModel.objects.filter(id__in=route_ids)
        
        if not routes_qs.exists():
            return JsonResponse({'error': 'No routes found'}, status=404)
        
        # Create plugin
        plugin_data = {'queryset': routes_qs}
        if not include_translations:
            plugin_data['notranslate'] = True
        
        # Generate filename
        import time
        filename = f"routes_plugin_{time.strftime('%Y%m%d%H%M%S')}.zip"
        
        # Create plugin using bots pluglib
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp:
            pluglib.make_plugin(plugin_data, tmp.name)
            
            # Read file content
            with open(tmp.name, 'rb') as f:
                file_content = f.read()
            
            # Clean up temp file
            os.unlink(tmp.name)
        
        # Return as download
        response = HttpResponse(file_content, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


# ========================================
# Channels Management
# ========================================

def admin_channels_list_or_create(request):
    """
    List channels (GET) or create channel (POST)
    """
    if request.method == 'GET':
        return admin_channels_list(request)
    elif request.method == 'POST':
        return admin_channel_create(request)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def admin_channel_detail_update_delete(request, channel_id):
    """
    Get channel detail (GET), update channel (PUT), or delete channel (DELETE)
    """
    if request.method == 'GET':
        return admin_channel_detail(request, channel_id)
    elif request.method == 'PUT':
        return admin_channel_update(request, channel_id)
    elif request.method == 'DELETE':
        return admin_channel_delete(request, channel_id)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@require_http_methods(["GET"])
def admin_channels_list(request):
    """
    List all channels with search and filtering
    GET /api/v1/admin/channels?search=&inorout=&type=&page=1
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import channel
        
        # Get query parameters
        search = request.GET.get('search', '').strip()
        inorout = request.GET.get('inorout', '').strip()  # in, out
        channel_type = request.GET.get('type', '').strip()
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 50))
        
        # Build query
        channels_qs = channel.objects.all()
        
        # Apply filters
        if search:
            channels_qs = channels_qs.filter(
                Q(idchannel__icontains=search) |
                Q(type__icontains=search) |
                Q(host__icontains=search) |
                Q(path__icontains=search) |
                Q(desc__icontains=search)
            )
        
        if inorout:
            channels_qs = channels_qs.filter(inorout=inorout)
        
        if channel_type:
            channels_qs = channels_qs.filter(type=channel_type)
        
        # Order by idchannel
        channels_qs = channels_qs.order_by('idchannel')
        
        # Paginate
        paginator = Paginator(channels_qs, per_page)
        page_obj = paginator.get_page(page)
        
        # Serialize channels
        channels_data = []
        for ch in page_obj:
            channels_data.append({
                'id': ch.idchannel,
                'idchannel': ch.idchannel,
                'inorout': ch.inorout,
                'type': ch.type,
                'host': ch.host,
                'port': ch.port,
                'username': ch.username,
                'path': ch.path,
                'filename': ch.filename,
                'remove': ch.remove,
                'archivepath': ch.archivepath,
                'desc': ch.desc,
                'charset': ch.charset,
                'lockname': ch.lockname,
                'syslock': ch.syslock,
                'parameters': ch.parameters,
                'ftpaccount': ch.ftpaccount,
                'ftpactive': ch.ftpactive,
                'ftpbinary': ch.ftpbinary,
                'starttls': ch.starttls,
                'apop': ch.apop,
                'askmdn': ch.askmdn,
                'sendmdn': ch.sendmdn,
                'mdnchannel': ch.mdnchannel,
                'keyfile': ch.keyfile,
                'certfile': ch.certfile,
                'testpath': ch.testpath,
                'debug': ch.debug,
                'rsrv1': ch.rsrv1,
                'rsrv2': ch.rsrv2,
                'rsrv3': ch.rsrv3,
            })
        
        return JsonResponse({
            'success': True,
            'channels': channels_data,
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
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@require_http_methods(["POST"])
def admin_channel_create(request):
    """
    Create a new channel
    POST /api/v1/admin/channels
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import channel
        
        data = json.loads(request.body)
        
        # Check if channel already exists
        if channel.objects.filter(idchannel=data.get('idchannel')).exists():
            return JsonResponse({'error': 'Channel with this ID already exists'}, status=400)
        
        # Create channel
        ch = channel()
        ch.idchannel = data.get('idchannel')
        ch.inorout = data.get('inorout', 'in')
        ch.type = data.get('type', 'file')
        ch.host = data.get('host', '')
        ch.port = data.get('port')
        ch.username = data.get('username', '')
        ch.secret = data.get('secret', '')
        ch.path = data.get('path', '')
        ch.filename = data.get('filename', '')
        ch.remove = data.get('remove', False)
        ch.archivepath = data.get('archivepath', '')
        ch.desc = data.get('desc', '')
        ch.charset = data.get('charset', 'us-ascii')
        ch.lockname = data.get('lockname', '')
        ch.syslock = data.get('syslock', False)
        ch.parameters = data.get('parameters', '')
        ch.ftpaccount = data.get('ftpaccount', '')
        ch.ftpactive = data.get('ftpactive', False)
        ch.ftpbinary = data.get('ftpbinary', False)
        ch.starttls = data.get('starttls', False)
        ch.apop = data.get('apop', False)
        ch.askmdn = data.get('askmdn', '')
        ch.sendmdn = data.get('sendmdn', '')
        ch.mdnchannel = data.get('mdnchannel', '')
        ch.keyfile = data.get('keyfile', '')
        ch.certfile = data.get('certfile', '')
        ch.testpath = data.get('testpath', '')
        ch.debug = data.get('debug')
        ch.rsrv1 = data.get('rsrv1')
        ch.rsrv2 = data.get('rsrv2')
        ch.rsrv3 = data.get('rsrv3')
        
        ch.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Channel created successfully',
            'channel_id': ch.idchannel
        })
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["GET"])
def admin_channel_detail(request, channel_id):
    """
    Get channel details
    GET /api/v1/admin/channels/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import channel
        
        ch = channel.objects.get(idchannel=channel_id)
        
        channel_data = {
            'id': ch.idchannel,
            'idchannel': ch.idchannel,
            'inorout': ch.inorout,
            'type': ch.type,
            'host': ch.host,
            'port': ch.port,
            'username': ch.username,
            'has_secret': bool(ch.secret),  # Don't send actual password
            'path': ch.path,
            'filename': ch.filename,
            'remove': ch.remove,
            'archivepath': ch.archivepath,
            'desc': ch.desc,
            'charset': ch.charset,
            'lockname': ch.lockname,
            'syslock': ch.syslock,
            'parameters': ch.parameters,
            'ftpaccount': ch.ftpaccount,
            'ftpactive': ch.ftpactive,
            'ftpbinary': ch.ftpbinary,
            'starttls': ch.starttls,
            'apop': ch.apop,
            'askmdn': ch.askmdn,
            'sendmdn': ch.sendmdn,
            'mdnchannel': ch.mdnchannel,
            'keyfile': ch.keyfile,
            'certfile': ch.certfile,
            'testpath': ch.testpath,
            'debug': ch.debug,
            'rsrv1': ch.rsrv1,
            'rsrv2': ch.rsrv2,
            'rsrv3': ch.rsrv3,
        }
        
        return JsonResponse({
            'success': True,
            'channel': channel_data
        })
    except channel.DoesNotExist:
        return JsonResponse({'error': 'Channel not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@require_http_methods(["PUT"])
def admin_channel_update(request, channel_id):
    """
    Update a channel
    PUT /api/v1/admin/channels/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import channel
        
        ch = channel.objects.get(idchannel=channel_id)
        data = json.loads(request.body)
        
        # Update fields (can't change idchannel as it's the primary key)
        if 'inorout' in data:
            ch.inorout = data['inorout']
        if 'type' in data:
            ch.type = data['type']
        if 'host' in data:
            ch.host = data['host']
        if 'port' in data:
            ch.port = data['port']
        if 'username' in data:
            ch.username = data['username']
        if 'secret' in data and data['secret']:  # Only update if provided
            ch.secret = data['secret']
        if 'path' in data:
            ch.path = data['path']
        if 'filename' in data:
            ch.filename = data['filename']
        if 'remove' in data:
            ch.remove = data['remove']
        if 'archivepath' in data:
            ch.archivepath = data['archivepath']
        if 'desc' in data:
            ch.desc = data['desc']
        if 'charset' in data:
            ch.charset = data['charset']
        if 'lockname' in data:
            ch.lockname = data['lockname']
        if 'syslock' in data:
            ch.syslock = data['syslock']
        if 'parameters' in data:
            ch.parameters = data['parameters']
        if 'ftpaccount' in data:
            ch.ftpaccount = data['ftpaccount']
        if 'ftpactive' in data:
            ch.ftpactive = data['ftpactive']
        if 'ftpbinary' in data:
            ch.ftpbinary = data['ftpbinary']
        if 'starttls' in data:
            ch.starttls = data['starttls']
        if 'apop' in data:
            ch.apop = data['apop']
        if 'askmdn' in data:
            ch.askmdn = data['askmdn']
        if 'sendmdn' in data:
            ch.sendmdn = data['sendmdn']
        if 'mdnchannel' in data:
            ch.mdnchannel = data['mdnchannel']
        if 'keyfile' in data:
            ch.keyfile = data['keyfile']
        if 'certfile' in data:
            ch.certfile = data['certfile']
        if 'testpath' in data:
            ch.testpath = data['testpath']
        if 'debug' in data:
            ch.debug = data['debug']
        if 'rsrv1' in data:
            ch.rsrv1 = data['rsrv1']
        if 'rsrv2' in data:
            ch.rsrv2 = data['rsrv2']
        if 'rsrv3' in data:
            ch.rsrv3 = data['rsrv3']
        
        ch.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Channel updated successfully'
        })
    except channel.DoesNotExist:
        return JsonResponse({'error': 'Channel not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["DELETE"])
def admin_channel_delete(request, channel_id):
    """
    Delete a channel
    DELETE /api/v1/admin/channels/<id>
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import channel
        
        ch = channel.objects.get(idchannel=channel_id)
        
        # Check if channel is used in routes
        from bots.models import routes
        in_routes = routes.objects.filter(Q(fromchannel=ch) | Q(tochannel=ch)).count()
        if in_routes > 0:
            return JsonResponse({
                'error': f'Cannot delete channel. It is used in {in_routes} route(s). '
                        'Please remove the routes first or change their channels.'
            }, status=400)
        
        ch.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Channel {channel_id} deleted successfully'
        })
    except channel.DoesNotExist:
        return JsonResponse({'error': 'Channel not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["POST"])
def admin_channel_test(request, channel_id):
    """
    Test channel connection
    POST /api/v1/admin/channels/<id>/test
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import channel
        
        ch = channel.objects.get(idchannel=channel_id)
        
        # TODO: Implement actual connection testing based on channel type
        # For now, return a placeholder response
        return JsonResponse({
            'success': True,
            'message': f'Channel test for {channel_id} - Test functionality coming soon',
            'details': {
                'type': ch.type,
                'host': ch.host,
                'port': ch.port,
                'note': 'Full connection testing will be implemented in the next iteration'
            }
        })
    except channel.DoesNotExist:
        return JsonResponse({'error': 'Channel not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


# ========================================
# Translations Management
# ========================================

def admin_translations_list_or_create(request):
    if request.method == 'GET':
        return admin_translations_list(request)
    elif request.method == 'POST':
        return admin_translation_create(request)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def admin_translation_detail_update_delete(request, translation_id):
    if request.method == 'GET':
        return admin_translation_detail(request, translation_id)
    elif request.method == 'PUT':
        return admin_translation_update(request, translation_id)
    elif request.method == 'DELETE':
        return admin_translation_delete(request, translation_id)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@require_http_methods(["GET"])
def admin_translations_list(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import translate
        
        search = request.GET.get('search', '').strip()
        fromeditype = request.GET.get('fromeditype', '').strip()
        toeditype = request.GET.get('toeditype', '').strip()
        active = request.GET.get('active', '').strip()
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 50))
        
        translations_qs = translate.objects.select_related('frompartner', 'topartner').all()
        
        if search:
            translations_qs = translations_qs.filter(
                Q(fromeditype__icontains=search) |
                Q(toeditype__icontains=search) |
                Q(tscript__icontains=search) |
                Q(desc__icontains=search)
            )
        
        if fromeditype:
            translations_qs = translations_qs.filter(fromeditype=fromeditype)
        
        if toeditype:
            translations_qs = translations_qs.filter(toeditype=toeditype)
        
        if active:
            translations_qs = translations_qs.filter(active=(active.lower() == 'true'))
        
        translations_qs = translations_qs.order_by('fromeditype', 'frommessagetype', 'alt')
        
        paginator = Paginator(translations_qs, per_page)
        page_obj = paginator.get_page(page)
        
        translations_data = []
        for t in page_obj:
            translations_data.append({
                'id': t.id,
                'active': t.active,
                'fromeditype': t.fromeditype,
                'frommessagetype': t.frommessagetype,
                'toeditype': t.toeditype,
                'tomessagetype': t.tomessagetype,
                'tscript': t.tscript,
                'alt': t.alt,
                'frompartner': {
                    'id': str(t.frompartner.id) if t.frompartner and hasattr(t.frompartner, 'id') else None,
                    'idpartner': t.frompartner.idpartner if t.frompartner else None,
                } if t.frompartner else None,
                'topartner': {
                    'id': str(t.topartner.id) if t.topartner and hasattr(t.topartner, 'id') else None,
                    'idpartner': t.topartner.idpartner if t.topartner else None,
                } if t.topartner else None,
                'desc': t.desc,
            })
        
        return JsonResponse({
            'success': True,
            'translations': translations_data,
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
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@require_http_methods(["POST"])
def admin_translation_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import translate, partner as PartnerModel
        
        data = json.loads(request.body)
        
        t = translate()
        t.active = data.get('active', False)
        t.fromeditype = data.get('fromeditype')
        t.frommessagetype = data.get('frommessagetype')
        t.toeditype = data.get('toeditype')
        t.tomessagetype = data.get('tomessagetype')
        t.tscript = data.get('tscript')
        t.alt = data.get('alt', '')
        t.desc = data.get('desc', '')
        
        if data.get('frompartner_id'):
            t.frompartner = PartnerModel.objects.get(idpartner=data['frompartner_id'])
        if data.get('topartner_id'):
            t.topartner = PartnerModel.objects.get(idpartner=data['topartner_id'])
        
        t.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Translation created successfully',
            'translation_id': t.id
        })
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["GET"])
def admin_translation_detail(request, translation_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import translate
        
        t = translate.objects.select_related('frompartner', 'topartner').get(id=translation_id)
        
        return JsonResponse({
            'success': True,
            'translation': {
                'id': t.id,
                'active': t.active,
                'fromeditype': t.fromeditype,
                'frommessagetype': t.frommessagetype,
                'toeditype': t.toeditype,
                'tomessagetype': t.tomessagetype,
                'tscript': t.tscript,
                'alt': t.alt,
                'frompartner': {
                    'id': str(t.frompartner.id) if hasattr(t.frompartner, 'id') else None,
                    'idpartner': t.frompartner.idpartner,
                    'name': t.frompartner.name,
                } if t.frompartner else None,
                'topartner': {
                    'id': str(t.topartner.id) if hasattr(t.topartner, 'id') else None,
                    'idpartner': t.topartner.idpartner,
                    'name': t.topartner.name,
                } if t.topartner else None,
                'desc': t.desc,
            }
        })
    except translate.DoesNotExist:
        return JsonResponse({'error': 'Translation not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@require_http_methods(["PUT"])
def admin_translation_update(request, translation_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import translate, partner as PartnerModel
        
        t = translate.objects.get(id=translation_id)
        data = json.loads(request.body)
        
        if 'active' in data:
            t.active = data['active']
        if 'fromeditype' in data:
            t.fromeditype = data['fromeditype']
        if 'frommessagetype' in data:
            t.frommessagetype = data['frommessagetype']
        if 'toeditype' in data:
            t.toeditype = data['toeditype']
        if 'tomessagetype' in data:
            t.tomessagetype = data['tomessagetype']
        if 'tscript' in data:
            t.tscript = data['tscript']
        if 'alt' in data:
            t.alt = data['alt']
        if 'desc' in data:
            t.desc = data['desc']
        
        if 'frompartner_id' in data:
            t.frompartner = PartnerModel.objects.get(idpartner=data['frompartner_id']) if data['frompartner_id'] else None
        if 'topartner_id' in data:
            t.topartner = PartnerModel.objects.get(idpartner=data['topartner_id']) if data['topartner_id'] else None
        
        t.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Translation updated successfully'
        })
    except translate.DoesNotExist:
        return JsonResponse({'error': 'Translation not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["DELETE"])
def admin_translation_delete(request, translation_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import translate
        
        t = translate.objects.get(id=translation_id)
        t.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Translation deleted successfully'
        })
    except translate.DoesNotExist:
        return JsonResponse({'error': 'Translation not found'}, status=404)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=400)


@require_http_methods(["GET"])
def admin_channel_types(request):
    """
    Get available channel types
    GET /api/v1/admin/channels/types
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        from bots.models import CHANNELTYPE
        
        # Convert choices to list of dicts
        types = [{'value': choice[0], 'label': choice[1]} for choice in CHANNELTYPE]
        
        return JsonResponse({
            'success': True,
            'types': types
        })
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)
