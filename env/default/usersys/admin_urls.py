"""
Admin Dashboard URL Configuration
Routes for admin dashboard API endpoints
"""

from django.urls import path
from . import admin_views

urlpatterns = [
    # Dashboard overview
    path('dashboard/metrics', admin_views.admin_dashboard_metrics, name='admin_dashboard_metrics'),
    path('dashboard/charts', admin_views.admin_dashboard_charts, name='admin_dashboard_charts'),
    
    # Partner management
    path('partners', admin_views.admin_partners_list, name='admin_partners_list'),
    path('partners/<uuid:partner_id>/analytics', admin_views.admin_partner_analytics, name='admin_partner_analytics'),
    path('partners/<uuid:partner_id>/users', admin_views.admin_partner_users, name='admin_partner_users'),
    path('partners/<uuid:partner_id>/users', admin_views.admin_create_partner_user, name='admin_create_partner_user'),
    
    # User management
    path('users/<int:user_id>', admin_views.admin_update_user, name='admin_update_user'),
    path('users/<int:user_id>', admin_views.admin_delete_user, name='admin_delete_user'),
    path('users/<int:user_id>/reset-password', admin_views.admin_reset_user_password, name='admin_reset_user_password'),
    path('users/<int:user_id>/permissions', admin_views.admin_update_user_permissions, name='admin_update_user_permissions'),
    
    # Analytics
    path('analytics/transactions', admin_views.admin_analytics_transactions, name='admin_analytics_transactions'),
    path('analytics/partners', admin_views.admin_analytics_partners, name='admin_analytics_partners'),
    path('analytics/documents', admin_views.admin_analytics_documents, name='admin_analytics_documents'),
    
    # Activity logs
    path('activity-logs', admin_views.admin_activity_logs, name='admin_activity_logs'),
    path('activity-logs/export', admin_views.admin_activity_logs_export, name='admin_activity_logs_export'),
    
    # SFTP Configuration Management
    path('partners/<uuid:partner_id>/sftp-config', admin_views.admin_partner_sftp_config, name='admin_partner_sftp_config'),
    path('partners/<uuid:partner_id>/sftp-config', admin_views.admin_partner_sftp_config_create, name='admin_partner_sftp_config_create'),
    path('partners/<uuid:partner_id>/sftp-config', admin_views.admin_partner_sftp_config_update, name='admin_partner_sftp_config_update'),
    path('partners/<uuid:partner_id>/sftp-config', admin_views.admin_partner_sftp_config_delete, name='admin_partner_sftp_config_delete'),
    path('partners/<uuid:partner_id>/sftp-config/test', admin_views.admin_partner_sftp_test_connection, name='admin_partner_sftp_test_connection'),
    path('sftp/generate-credentials', admin_views.admin_generate_sftp_credentials, name='admin_generate_sftp_credentials'),
    
    # Scheduled Reports Management
    path('scheduled-reports', admin_views.admin_scheduled_reports_list, name='admin_scheduled_reports_list'),
    path('scheduled-reports', admin_views.admin_scheduled_report_create, name='admin_scheduled_report_create'),
    path('scheduled-reports/<int:report_id>', admin_views.admin_scheduled_report_update, name='admin_scheduled_report_update'),
    path('scheduled-reports/<int:report_id>', admin_views.admin_scheduled_report_delete, name='admin_scheduled_report_delete'),
    path('scheduled-reports/<int:report_id>/run', admin_views.admin_scheduled_report_run_now, name='admin_scheduled_report_run_now'),
    path('scheduled-reports/<int:report_id>/preview', admin_views.admin_scheduled_report_preview, name='admin_scheduled_report_preview'),
]
