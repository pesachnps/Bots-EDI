import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { useCreateTransaction, useUpdateTransaction, usePartners, useDocumentTypes } from '../hooks/useTransactions';

function TransactionForm({ mode = 'create', folderType, transactionId, onSave, onCancel }) {
  const { register, handleSubmit, formState: { errors }, setValue } = useForm();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const createTransaction = useCreateTransaction();
  const updateTransaction = useUpdateTransaction();
  const { data: partners } = usePartners();
  const { data: documentTypes } = useDocumentTypes();

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    
    try {
      const payload = {
        folder: folderType,
        partner_name: data.partner_name,
        partner_id: data.partner_id,
        document_type: data.document_type,
        po_number: data.po_number,
        metadata: {
          buyer_name: data.buyer_name,
          seller_name: data.seller_name,
        },
      };

      if (mode === 'create') {
        await createTransaction.mutateAsync(payload);
      } else {
        await updateTransaction.mutateAsync({ id: transactionId, data: payload });
      }
      
      onSave();
    } catch (error) {
      console.error('Form submission error:', error);
      alert('Failed to save transaction: ' + (error.response?.data?.error || error.message));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">
            {mode === 'create' ? 'Create Transaction' : 'Edit Transaction'}
          </h2>
          <button
            onClick={onCancel}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="h-6 w-6 text-gray-500" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="flex-1 overflow-y-auto p-6">
          <div className="space-y-4">
            {/* Partner Name */}
            <div>
              <label className="label">
                Partner Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                {...register('partner_name', { required: 'Partner name is required' })}
                className="input"
                placeholder="Enter partner name"
              />
              {errors.partner_name && (
                <p className="text-sm text-red-600 mt-1">{errors.partner_name.message}</p>
              )}
            </div>

            {/* Partner ID */}
            <div>
              <label className="label">Partner ID</label>
              <input
                type="text"
                {...register('partner_id')}
                className="input"
                placeholder="Enter partner ID (optional)"
              />
            </div>

            {/* Document Type */}
            <div>
              <label className="label">
                Document Type <span className="text-red-500">*</span>
              </label>
              <select
                {...register('document_type', { required: 'Document type is required' })}
                className="input"
              >
                <option value="">Select document type</option>
                {documentTypes?.map((type) => (
                  <option key={type.code} value={type.code}>
                    {type.code} - {type.name}
                  </option>
                ))}
              </select>
              {errors.document_type && (
                <p className="text-sm text-red-600 mt-1">{errors.document_type.message}</p>
              )}
            </div>

            {/* PO Number */}
            <div>
              <label className="label">PO Number</label>
              <input
                type="text"
                {...register('po_number')}
                className="input"
                placeholder="Enter PO number (optional)"
              />
            </div>

            {/* Buyer Name */}
            <div>
              <label className="label">Buyer Name</label>
              <input
                type="text"
                {...register('buyer_name')}
                className="input"
                placeholder="Enter buyer name (optional)"
              />
            </div>

            {/* Seller Name */}
            <div>
              <label className="label">Seller Name</label>
              <input
                type="text"
                {...register('seller_name')}
                className="input"
                placeholder="Enter seller name (optional)"
              />
            </div>
          </div>
        </form>

        {/* Footer */}
        <div className="flex justify-end space-x-3 p-6 border-t border-gray-200">
          <button
            type="button"
            onClick={onCancel}
            className="btn btn-secondary"
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            type="submit"
            onClick={handleSubmit(onSubmit)}
            className="btn btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Saving...' : mode === 'create' ? 'Create' : 'Update'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default TransactionForm;
