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
]
