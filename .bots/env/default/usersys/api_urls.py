"""
Bots EDI API URL Configuration
"""

from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    # File operations
    path('v1/files/upload', api_views.upload_file, name='upload_file'),
    path('v1/files/download/<path:file_id>', api_views.download_file, name='download_file'),
    path('v1/files/list', api_views.list_files, name='list_files'),
    
    # Route operations
    path('v1/routes/execute', api_views.execute_route, name='execute_route'),
    
    # Reports
    path('v1/reports', api_views.get_reports, name='get_reports'),
    
    # Status
    path('v1/status', api_views.api_status, name='status'),
]
