"""
Partner Portal URL Configuration
Routes for partner portal API endpoints
"""

from django.urls import path
from . import partner_auth_views, partner_portal_views

urlpatterns = [
    # Authentication
    path('auth/login', partner_auth_views.partner_login, name='partner_login'),
    path('auth/logout', partner_auth_views.partner_logout, name='partner_logout'),
    path('auth/me', partner_auth_views.partner_me, name='partner_me'),
    path('auth/forgot-password', partner_auth_views.partner_forgot_password, name='partner_forgot_password'),
    path('auth/reset-password', partner_auth_views.partner_reset_password, name='partner_reset_password'),
    path('auth/change-password', partner_auth_views.partner_change_password, name='partner_change_password'),
    
    # Dashboard
    path('dashboard/metrics', partner_portal_views.partner_dashboard_metrics, name='partner_dashboard_metrics'),
    
    # Transactions
    path('transactions', partner_portal_views.partner_transactions_list, name='partner_transactions_list'),
    path('transactions/<uuid:transaction_id>', partner_portal_views.partner_transaction_detail, name='partner_transaction_detail'),
    
    # File operations
    path('files/upload', partner_portal_views.partner_file_upload, name='partner_file_upload'),
    path('files/download', partner_portal_views.partner_files_list, name='partner_files_list'),
    path('files/download/<uuid:transaction_id>', partner_portal_views.partner_file_download, name='partner_file_download'),
    path('files/download/bulk', partner_portal_views.partner_files_bulk_download, name='partner_files_bulk_download'),
    
    # Settings
    path('settings', partner_portal_views.partner_settings_get, name='partner_settings_get'),
    path('settings/contact', partner_portal_views.partner_settings_update_contact, name='partner_settings_update_contact'),
    path('settings/test-connection', partner_portal_views.partner_settings_test_connection, name='partner_settings_test_connection'),
]
