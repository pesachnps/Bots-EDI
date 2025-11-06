"""
Modern EDI Interface URL Configuration
"""

from django.urls import path
from . import modern_edi_views

app_name = 'modern_edi'

urlpatterns = [
    # Transaction CRUD endpoints
    path('api/v1/transactions/', modern_edi_views.list_transactions, name='list_transactions'),
    path('api/v1/transactions/<str:folder>/', modern_edi_views.list_transactions_by_folder, name='list_transactions_by_folder'),
    path('api/v1/transaction/<uuid:transaction_id>/', modern_edi_views.get_transaction, name='get_transaction'),
    path('api/v1/transaction/create/', modern_edi_views.create_transaction, name='create_transaction'),
    path('api/v1/transaction/<uuid:transaction_id>/update/', modern_edi_views.update_transaction, name='update_transaction'),
    path('api/v1/transaction/<uuid:transaction_id>/delete/', modern_edi_views.delete_transaction, name='delete_transaction'),
    
    # Transaction action endpoints
    path('api/v1/transaction/<uuid:transaction_id>/move/', modern_edi_views.move_transaction, name='move_transaction'),
    path('api/v1/transaction/<uuid:transaction_id>/send/', modern_edi_views.send_transaction, name='send_transaction'),
    path('api/v1/transaction/<uuid:transaction_id>/process/', modern_edi_views.process_transaction, name='process_transaction'),
    path('api/v1/transaction/<uuid:transaction_id>/validate/', modern_edi_views.validate_transaction, name='validate_transaction'),
    path('api/v1/transaction/<uuid:transaction_id>/permanent-delete/', modern_edi_views.permanent_delete_transaction, name='permanent_delete_transaction'),
    path('api/v1/transaction/<uuid:transaction_id>/history/', modern_edi_views.get_transaction_history, name='get_transaction_history'),
    path('api/v1/transaction/<uuid:transaction_id>/raw/', modern_edi_views.get_transaction_raw, name='get_transaction_raw'),
    
    # Folder endpoints
    path('api/v1/folders/', modern_edi_views.get_folders, name='get_folders'),
    path('api/v1/folders/<str:folder>/stats/', modern_edi_views.get_folder_stats, name='get_folder_stats'),
    
    # Metadata endpoints
    path('api/v1/partners/', modern_edi_views.get_partners, name='get_partners'),
    path('api/v1/document-types/', modern_edi_views.get_document_types, name='get_document_types'),
    
    # Search endpoint
    path('api/v1/search/', modern_edi_views.search_transactions, name='search_transactions'),
]
