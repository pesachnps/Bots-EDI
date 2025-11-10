"""
Admin Dashboard URL Configuration
Routes for admin dashboard API endpoints
"""

from django.urls import path
from . import admin_views
from . import admin_auth_views

urlpatterns = [
    # Admin Authentication
    path('auth/login', admin_auth_views.admin_login, name='admin_login'),
    path('auth/logout', admin_auth_views.admin_logout, name='admin_logout'),
    path('auth/check', admin_auth_views.admin_check_auth, name='admin_check_auth'),
    path('auth/signup', admin_auth_views.admin_signup, name='admin_signup'),
    path('auth/request-reset', admin_auth_views.admin_request_password_reset, name='admin_request_reset'),
    path('auth/reset-password', admin_auth_views.admin_reset_password, name='admin_reset_password'),
    
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
    
    # Routes Management
    path('routes', admin_views.admin_routes_list, name='admin_routes_list'),
    path('routes/<int:route_id>', admin_views.admin_route_detail, name='admin_route_detail'),
    path('routes/<int:route_id>', admin_views.admin_route_update, name='admin_route_update'),
    path('routes/<int:route_id>', admin_views.admin_route_delete, name='admin_route_delete'),
    path('routes/<int:route_id>/activate', admin_views.admin_route_toggle_active, name='admin_route_toggle_active'),
    path('routes/<int:route_id>/clone', admin_views.admin_route_clone, name='admin_route_clone'),
    path('routes/export', admin_views.admin_routes_export, name='admin_routes_export'),
    
    # Channels Management
    path('channels/types', admin_views.admin_channel_types, name='admin_channel_types'),
    path('channels', admin_views.admin_channels_list_or_create, name='admin_channels_list_create'),
    path('channels/<str:channel_id>', admin_views.admin_channel_detail_update_delete, name='admin_channel_detail'),
    path('channels/<str:channel_id>/test', admin_views.admin_channel_test, name='admin_channel_test'),
    
    # Translations Management
    path('translations', admin_views.admin_translations_list_or_create, name='admin_translations_list_create'),
    path('translations/<int:translation_id>', admin_views.admin_translation_detail_update_delete, name='admin_translation_detail'),
    
    # Confirm Rules Management
    path('confirmrules', admin_views.admin_confirmrules_list_or_create, name='admin_confirmrules_list_create'),
    path('confirmrules/<int:rule_id>', admin_views.admin_confirmrule_detail_update_delete, name='admin_confirmrule_detail'),
    
    # Code Lists Management
    path('codelists', admin_views.admin_codelists_list, name='admin_codelists_list'),
    path('codelists/<str:ccodeid>', admin_views.admin_codelist_detail, name='admin_codelist_detail'),
    path('codelists/<str:ccodeid>/codes', admin_views.admin_codelist_codes_list_or_create, name='admin_codelist_codes'),
    path('codelists/<str:ccodeid>/codes/<int:code_id>', admin_views.admin_codelist_code_update_delete, name='admin_codelist_code_detail'),
    
    # Counters Management
    path('counters', admin_views.admin_counters_list, name='admin_counters_list'),
    path('counters/<str:domein>', admin_views.admin_counter_update, name='admin_counter_update'),
    
    # Transaction Management
    path('transactions/incoming', admin_views.admin_transactions_incoming, name='admin_transactions_incoming'),
    path('transactions/outgoing', admin_views.admin_transactions_outgoing, name='admin_transactions_outgoing'),
    path('transactions/<int:ta_id>', admin_views.admin_transaction_detail, name='admin_transaction_detail'),
    path('transactions/<int:ta_id>/resend', admin_views.admin_transaction_resend, name='admin_transaction_resend'),
    path('transactions/<int:ta_id>/lineage', admin_views.admin_transaction_lineage, name='admin_transaction_lineage'),
    
    # File Management
    path('files/browse', admin_views.admin_files_browse, name='admin_files_browse'),
    path('logs', admin_views.admin_logs_list, name='admin_logs_list'),
    path('logs/content', admin_views.admin_log_content, name='admin_log_content'),
    
    # Operations
    path('engine/run', admin_views.admin_engine_run, name='admin_engine_run'),
    path('engine/status', admin_views.admin_engine_status, name='admin_engine_status'),
    path('cleanup/execute', admin_views.admin_cleanup_execute, name='admin_cleanup_execute'),
    
    # System
    path('system/info', admin_views.admin_system_info, name='admin_system_info'),
]
