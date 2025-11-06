import { useState } from 'react';
import { MoreVertical, Edit, Trash2, Send, FolderInput, CheckCircle, XCircle, Clock, AlertCircle, ArrowRight } from 'lucide-react';
import { format } from 'date-fns';
import { useMoveTransaction, useDeleteTransaction, useSendTransaction, useProcessTransaction, useValidateTransaction } from '../hooks/useTransactions';
import MoveDialog from './MoveDialog';

function TransactionCard({ transaction, folderType, onClick }) {
  const [showMenu, setShowMenu] = useState(false);
  const [showMoveDialog, setShowMoveDialog] = useState(false);
  
  const moveTransaction = useMoveTransaction();
  const deleteTransaction = useDeleteTransaction();
  const sendTransaction = useSendTransaction();
  const processTransaction = useProcessTransaction();
  const { data: validation } = useValidateTransaction(transaction.id);

  const handleMove = (targetFolder) => {
    moveTransaction.mutate(
      { id: transaction.id, targetFolder },
      {
        onSuccess: () => {
          setShowMoveDialog(false);
        },
      }
    );
  };

  const handleDelete = () => {
    if (confirm('Move this transaction to deleted folder?')) {
      deleteTransaction.mutate(transaction.id);
    }
    setShowMenu(false);
  };

  const handleSend = () => {
    if (confirm('Send this transaction?')) {
      sendTransaction.mutate(transaction.id);
    }
    setShowMenu(false);
  };

  const handleProcess = () => {
    const action = folderType === 'inbox' ? 'process to Received' : 'send to Sent';
    if (confirm(`Ready to ${action}?`)) {
      processTransaction.mutate(transaction.id);
    }
  };

  const hasValidationErrors = validation?.has_errors || false;
  const canProcess = (folderType === 'inbox' || folderType === 'outbox') && !hasValidationErrors;

  const getStatusBadge = () => {
    if (folderType === 'sent') {
      if (transaction.acknowledgment_status === 'accepted') {
        return (
          <span className="inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
            <CheckCircle className="h-3 w-3" />
            <span>Acknowledged</span>
          </span>
        );
      } else if (transaction.acknowledgment_status === 'rejected') {
        return (
          <span className="inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
            <XCircle className="h-3 w-3" />
            <span>Rejected</span>
          </span>
        );
      } else {
        return (
          <span className="inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            <Clock className="h-3 w-3" />
            <span>Pending</span>
          </span>
        );
      }
    }
    return null;
  };

  const getDisplayDate = () => {
    if (transaction.sent_at) {
      return format(new Date(transaction.sent_at), 'MMM d, yyyy HH:mm');
    } else if (transaction.received_at) {
      return format(new Date(transaction.received_at), 'MMM d, yyyy HH:mm');
    } else {
      return format(new Date(transaction.created_at), 'MMM d, yyyy HH:mm');
    }
  };

  return (
    <>
      <div className={`bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 p-4 border-2 relative ${
        hasValidationErrors ? 'border-red-300' : 'border-gray-200'
      }`}>
        {/* Validation Error Indicator */}
        {hasValidationErrors && (
          <div className="absolute top-2 left-2">
            <AlertCircle className="h-5 w-5 text-red-500" />
          </div>
        )}

        {/* Action Menu */}
        <div className="absolute top-4 right-4">
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowMenu(!showMenu);
            }}
            className="p-1 rounded-lg hover:bg-gray-100"
          >
            <MoreVertical className="h-5 w-5 text-gray-500" />
          </button>

          {showMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setShowMoveDialog(true);
                  setShowMenu(false);
                }}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
              >
                <FolderInput className="h-4 w-4" />
                <span>Move</span>
              </button>

              {transaction.is_editable && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onClick();
                    setShowMenu(false);
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                >
                  <Edit className="h-4 w-4" />
                  <span>Edit</span>
                </button>
              )}

              {transaction.is_sendable && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSend();
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                >
                  <Send className="h-4 w-4" />
                  <span>Send</span>
                </button>
              )}

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete();
                }}
                className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2"
              >
                <Trash2 className="h-4 w-4" />
                <span>Delete</span>
              </button>
            </div>
          )}
        </div>

        {/* Card Content */}
        <div onClick={onClick} className="cursor-pointer">
          {/* Partner Name */}
          <h3 className={`text-lg font-semibold mb-2 pr-8 ${hasValidationErrors ? 'pl-6' : ''} ${
            hasValidationErrors ? 'text-red-700' : 'text-gray-900'
          }`}>
            {transaction.partner_name}
          </h3>

          {/* Document Type */}
          <p className="text-sm text-gray-600 mb-1">
            <span className="font-medium">Type:</span> {transaction.document_type}
          </p>

          {/* PO Number */}
          {transaction.po_number && (
            <p className="text-sm text-gray-600 mb-1">
              <span className="font-medium">PO:</span> {transaction.po_number}
            </p>
          )}

          {/* Date */}
          <p className="text-sm text-gray-500 mb-3">
            {getDisplayDate()}
          </p>

          {/* Status Badge */}
          {getStatusBadge()}

          {/* File Info */}
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs text-gray-500">
              {transaction.filename} • {(transaction.file_size / 1024).toFixed(1)} KB
            </p>
          </div>
        </div>

        {/* Process Button */}
        {(folderType === 'inbox' || folderType === 'outbox') && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleProcess();
              }}
              disabled={hasValidationErrors}
              className={`w-full flex items-center justify-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                hasValidationErrors
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-600 text-white hover:bg-primary-700'
              }`}
            >
              <span>{folderType === 'inbox' ? 'Process to Received' : 'Send to Sent'}</span>
              <ArrowRight className="h-4 w-4" />
            </button>
            {hasValidationErrors && (
              <p className="text-xs text-red-600 mt-1 text-center">
                Fix validation errors first
              </p>
            )}
          </div>
        )}
      </div>

      {/* Move Dialog */}
      {showMoveDialog && (
        <MoveDialog
          currentFolder={folderType}
          onMove={handleMove}
          onCancel={() => setShowMoveDialog(false)}
        />
      )}
    </>
  );
}

export default TransactionCard;
