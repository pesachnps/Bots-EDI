import { useState } from 'react';
import { X, Loader2, FileText, History, CheckCircle, AlertTriangle } from 'lucide-react';
import { format } from 'date-fns';
import { useTransaction, useTransactionHistory, useTransactionRaw, useValidateTransaction } from '../hooks/useTransactions';

function TransactionDetail({ transactionId, onClose }) {
  const [activeTab, setActiveTab] = useState('overview');
  
  const { data: transaction, isLoading } = useTransaction(transactionId);
  const { data: history } = useTransactionHistory(transactionId);
  const { data: rawData } = useTransactionRaw(transactionId);
  const { data: validation } = useValidateTransaction(transactionId);

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
        </div>
      </div>
    );
  }

  if (!transaction) {
    return null;
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: FileText },
    { id: 'raw', label: 'Raw Data', icon: FileText },
    { id: 'history', label: 'History', icon: History },
  ];

  if (transaction.folder === 'sent' || transaction.folder === 'received') {
    tabs.push({ id: 'acknowledgment', label: 'Acknowledgment', icon: CheckCircle });
  }

  if (validation?.has_errors) {
    tabs.unshift({ id: 'errors', label: 'Errors', icon: AlertTriangle });
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{transaction.partner_name}</h2>
            <p className="text-sm text-gray-500 mt-1">
              {transaction.document_type} • {transaction.filename}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="h-6 w-6 text-gray-500" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-200 px-6">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {activeTab === 'errors' && validation?.has_errors && (
            <div>
              <h3 className="text-lg font-semibold text-red-700 mb-4 flex items-center space-x-2">
                <AlertTriangle className="h-5 w-5" />
                <span>Validation Errors</span>
              </h3>
              
              {/* Validation Errors */}
              {validation.validation && !validation.validation.valid && (
                <div className="mb-6">
                  <h4 className="font-medium text-gray-900 mb-3">Missing or Invalid Data:</h4>
                  <div className="space-y-2">
                    {validation.validation.errors.map((error, index) => (
                      <div key={index} className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                        <p className="text-sm font-medium text-red-800">{error.field}</p>
                        <p className="text-sm text-red-700">{error.message}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Acknowledgment Errors */}
              {validation.acknowledgment_errors && validation.acknowledgment_errors.length > 0 && (
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Acknowledgment Issues:</h4>
                  <div className="space-y-2">
                    {validation.acknowledgment_errors.map((error, index) => (
                      <div 
                        key={index} 
                        className={`border-l-4 p-3 rounded ${
                          error.severity === 'error' 
                            ? 'bg-red-50 border-red-500' 
                            : 'bg-yellow-50 border-yellow-500'
                        }`}
                      >
                        <p className={`text-sm font-medium ${
                          error.severity === 'error' ? 'text-red-800' : 'text-yellow-800'
                        }`}>
                          {error.field}
                        </p>
                        <p className={`text-sm ${
                          error.severity === 'error' ? 'text-red-700' : 'text-yellow-700'
                        }`}>
                          {error.message}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  <strong>Note:</strong> Fix these errors before processing or sending this transaction.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Basic Information */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className={validation?.validation?.errors?.some(e => e.field === 'partner_name') ? 'bg-red-50 p-2 rounded border border-red-200' : ''}>
                    <p className="text-sm text-gray-600">Partner Name</p>
                    <p className={`text-base font-medium ${validation?.validation?.errors?.some(e => e.field === 'partner_name') ? 'text-red-700' : 'text-gray-900'}`}>
                      {transaction.partner_name || <span className="text-red-500">Missing</span>}
                    </p>
                    {validation?.validation?.errors?.find(e => e.field === 'partner_name') && (
                      <p className="text-xs text-red-600 mt-1">
                        {validation.validation.errors.find(e => e.field === 'partner_name').message}
                      </p>
                    )}
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Partner ID</p>
                    <p className="text-base font-medium text-gray-900">{transaction.partner_id || 'N/A'}</p>
                  </div>
                  <div className={validation?.validation?.errors?.some(e => e.field === 'document_type') ? 'bg-red-50 p-2 rounded border border-red-200' : ''}>
                    <p className="text-sm text-gray-600">Document Type</p>
                    <p className={`text-base font-medium ${validation?.validation?.errors?.some(e => e.field === 'document_type') ? 'text-red-700' : 'text-gray-900'}`}>
                      {transaction.document_type || <span className="text-red-500">Missing</span>}
                    </p>
                    {validation?.validation?.errors?.find(e => e.field === 'document_type') && (
                      <p className="text-xs text-red-600 mt-1">
                        {validation.validation.errors.find(e => e.field === 'document_type').message}
                      </p>
                    )}
                  </div>
                  <div className={validation?.validation?.errors?.some(e => e.field === 'po_number') ? 'bg-red-50 p-2 rounded border border-red-200' : ''}>
                    <p className="text-sm text-gray-600">PO Number</p>
                    <p className={`text-base font-medium ${validation?.validation?.errors?.some(e => e.field === 'po_number') ? 'text-red-700' : 'text-gray-900'}`}>
                      {transaction.po_number || <span className={validation?.validation?.errors?.some(e => e.field === 'po_number') ? 'text-red-500' : 'text-gray-400'}>N/A</span>}
                    </p>
                    {validation?.validation?.errors?.find(e => e.field === 'po_number') && (
                      <p className="text-xs text-red-600 mt-1">
                        {validation.validation.errors.find(e => e.field === 'po_number').message}
                      </p>
                    )}
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Status</p>
                    <p className="text-base font-medium text-gray-900 capitalize">{transaction.status}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Folder</p>
                    <p className="text-base font-medium text-gray-900 capitalize">{transaction.folder}</p>
                  </div>
                </div>
              </div>

              {/* File Information */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">File Information</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Filename</p>
                    <p className="text-base font-medium text-gray-900">{transaction.filename}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">File Size</p>
                    <p className="text-base font-medium text-gray-900">
                      {(transaction.file_size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                  <div className="col-span-2">
                    <p className="text-sm text-gray-600">File Path</p>
                    <p className="text-sm font-mono text-gray-700 break-all">{transaction.file_path}</p>
                  </div>
                </div>
              </div>

              {/* Timestamps */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Timestamps</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Created</p>
                    <p className="text-base font-medium text-gray-900">
                      {format(new Date(transaction.created_at), 'MMM d, yyyy HH:mm:ss')}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Modified</p>
                    <p className="text-base font-medium text-gray-900">
                      {format(new Date(transaction.modified_at), 'MMM d, yyyy HH:mm:ss')}
                    </p>
                  </div>
                  {transaction.sent_at && (
                    <div>
                      <p className="text-sm text-gray-600">Sent</p>
                      <p className="text-base font-medium text-gray-900">
                        {format(new Date(transaction.sent_at), 'MMM d, yyyy HH:mm:ss')}
                      </p>
                    </div>
                  )}
                  {transaction.received_at && (
                    <div>
                      <p className="text-sm text-gray-600">Received</p>
                      <p className="text-base font-medium text-gray-900">
                        {format(new Date(transaction.received_at), 'MMM d, yyyy HH:mm:ss')}
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Metadata */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Metadata</h3>
                {transaction.metadata && Object.keys(transaction.metadata).length > 0 ? (
                  <div className="space-y-3">
                    <div className={validation?.validation?.errors?.some(e => e.field === 'metadata.buyer_name') ? 'bg-red-50 p-3 rounded border border-red-200' : 'bg-gray-50 p-3 rounded'}>
                      <p className="text-sm text-gray-600">Buyer Name</p>
                      <p className={`text-base font-medium ${validation?.validation?.errors?.some(e => e.field === 'metadata.buyer_name') ? 'text-red-700' : 'text-gray-900'}`}>
                        {transaction.metadata.buyer_name || <span className="text-red-500">Missing</span>}
                      </p>
                      {validation?.validation?.errors?.find(e => e.field === 'metadata.buyer_name') && (
                        <p className="text-xs text-red-600 mt-1">
                          {validation.validation.errors.find(e => e.field === 'metadata.buyer_name').message}
                        </p>
                      )}
                    </div>
                    <div className={validation?.validation?.errors?.some(e => e.field === 'metadata.seller_name') ? 'bg-red-50 p-3 rounded border border-red-200' : 'bg-gray-50 p-3 rounded'}>
                      <p className="text-sm text-gray-600">Seller Name</p>
                      <p className={`text-base font-medium ${validation?.validation?.errors?.some(e => e.field === 'metadata.seller_name') ? 'text-red-700' : 'text-gray-900'}`}>
                        {transaction.metadata.seller_name || <span className="text-red-500">Missing</span>}
                      </p>
                      {validation?.validation?.errors?.find(e => e.field === 'metadata.seller_name') && (
                        <p className="text-xs text-red-600 mt-1">
                          {validation.validation.errors.find(e => e.field === 'metadata.seller_name').message}
                        </p>
                      )}
                    </div>
                    <details className="mt-2">
                      <summary className="text-sm text-primary-600 cursor-pointer">View full metadata JSON</summary>
                      <pre className="mt-2 bg-gray-50 rounded-lg p-4 text-sm overflow-x-auto">
                        {JSON.stringify(transaction.metadata, null, 2)}
                      </pre>
                    </details>
                  </div>
                ) : (
                  <div className={validation?.validation?.errors?.some(e => e.field === 'metadata') ? 'bg-red-50 p-3 rounded border border-red-200' : 'bg-gray-50 p-3 rounded'}>
                    <p className="text-red-500">No metadata available</p>
                    {validation?.validation?.errors?.find(e => e.field === 'metadata') && (
                      <p className="text-xs text-red-600 mt-1">
                        {validation.validation.errors.find(e => e.field === 'metadata').message}
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'raw' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Raw EDI Content</h3>
              <pre className="bg-gray-900 text-green-400 rounded-lg p-4 text-sm overflow-x-auto font-mono">
                {rawData?.content || 'Loading...'}
              </pre>
            </div>
          )}

          {activeTab === 'history' && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Transaction History</h3>
              <div className="space-y-4">
                {history?.map((entry) => (
                  <div key={entry.id} className="border-l-4 border-primary-500 pl-4 py-2">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-gray-900 capitalize">{entry.action}</span>
                      <span className="text-sm text-gray-500">
                        {format(new Date(entry.timestamp), 'MMM d, yyyy HH:mm:ss')}
                      </span>
                    </div>
                    {entry.user && (
                      <p className="text-sm text-gray-600">By: {entry.user}</p>
                    )}
                    {entry.from_folder && entry.to_folder && (
                      <p className="text-sm text-gray-600">
                        From: {entry.from_folder} → To: {entry.to_folder}
                      </p>
                    )}
                    {entry.details && Object.keys(entry.details).length > 0 && (
                      <details className="mt-2">
                        <summary className="text-sm text-primary-600 cursor-pointer">View details</summary>
                        <pre className="mt-2 bg-gray-50 rounded p-2 text-xs overflow-x-auto">
                          {JSON.stringify(entry.details, null, 2)}
                        </pre>
                      </details>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'acknowledgment' && (transaction.folder === 'sent' || transaction.folder === 'received') && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                {transaction.folder === 'sent' ? 'Acknowledgment Status' : 'Processing Status'}
              </h3>
              
              {transaction.folder === 'sent' && (
                <div className="space-y-4">
                  <div className={validation?.acknowledgment_errors?.length > 0 ? 'bg-red-50 p-3 rounded border border-red-200' : ''}>
                    <p className="text-sm text-gray-600">Status</p>
                    <p className={`text-lg font-medium capitalize ${
                      transaction.acknowledgment_status === 'rejected' ? 'text-red-700' :
                      transaction.acknowledgment_status === 'accepted' ? 'text-green-700' :
                      'text-yellow-700'
                    }`}>
                      {transaction.acknowledgment_status || 'Pending'}
                    </p>
                  </div>
                  {transaction.acknowledgment_message && (
                    <div className={transaction.acknowledgment_status === 'rejected' ? 'bg-red-50 p-3 rounded border border-red-200' : ''}>
                      <p className="text-sm text-gray-600">Message</p>
                      <p className={`text-base ${transaction.acknowledgment_status === 'rejected' ? 'text-red-700' : 'text-gray-900'}`}>
                        {transaction.acknowledgment_message}
                      </p>
                    </div>
                  )}
                  {transaction.acknowledged_at && (
                    <div>
                      <p className="text-sm text-gray-600">Acknowledged At</p>
                      <p className="text-base font-medium text-gray-900">
                        {format(new Date(transaction.acknowledged_at), 'MMM d, yyyy HH:mm:ss')}
                      </p>
                    </div>
                  )}
                  
                  {validation?.acknowledgment_errors && validation.acknowledgment_errors.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <h4 className="font-medium text-red-700">Issues:</h4>
                      {validation.acknowledgment_errors.map((error, index) => (
                        <div 
                          key={index}
                          className={`p-3 rounded border-l-4 ${
                            error.severity === 'error' 
                              ? 'bg-red-50 border-red-500' 
                              : 'bg-yellow-50 border-yellow-500'
                          }`}
                        >
                          <p className={`text-sm ${
                            error.severity === 'error' ? 'text-red-700' : 'text-yellow-700'
                          }`}>
                            {error.message}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {transaction.folder === 'received' && (
                <div className="space-y-4">
                  <div className={transaction.status === 'failed' ? 'bg-red-50 p-3 rounded border border-red-200' : ''}>
                    <p className="text-sm text-gray-600">Processing Status</p>
                    <p className={`text-lg font-medium capitalize ${
                      transaction.status === 'failed' ? 'text-red-700' : 'text-green-700'
                    }`}>
                      {transaction.status}
                    </p>
                  </div>

                  {validation?.acknowledgment_errors && validation.acknowledgment_errors.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <h4 className="font-medium text-red-700">Processing Issues:</h4>
                      {validation.acknowledgment_errors.map((error, index) => (
                        <div 
                          key={index}
                          className="bg-red-50 p-3 rounded border-l-4 border-red-500"
                        >
                          <p className="text-sm font-medium text-red-800">{error.field}</p>
                          <p className="text-sm text-red-700">{error.message}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {transaction.received_at && (
                    <div>
                      <p className="text-sm text-gray-600">Received At</p>
                      <p className="text-base font-medium text-gray-900">
                        {format(new Date(transaction.received_at), 'MMM d, yyyy HH:mm:ss')}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200">
          <button onClick={onClose} className="btn btn-secondary">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default TransactionDetail;
