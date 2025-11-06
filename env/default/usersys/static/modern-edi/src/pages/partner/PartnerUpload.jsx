import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowUpTrayIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

export default function PartnerUpload() {
  const [file, setFile] = useState(null);
  const [documentType, setDocumentType] = useState('850');
  const [poNumber, setPoNumber] = useState('');
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const navigate = useNavigate();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError('');
    setSuccess(false);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);
    if (poNumber) formData.append('po_number', poNumber);

    try {
      const response = await fetch('/modern-edi/api/v1/partner-portal/files/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        setFile(null);
        setPoNumber('');
        setTimeout(() => {
          navigate('/modern-edi/partner-portal/transactions');
        }, 2000);
      } else {
        setError(data.error || 'Upload failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Upload EDI File</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Document Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Document Type *
            </label>
            <select
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              required
            >
              <option value="850">850 - Purchase Order</option>
              <option value="810">810 - Invoice</option>
              <option value="856">856 - Advance Ship Notice</option>
              <option value="997">997 - Functional Acknowledgment</option>
              <option value="855">855 - Purchase Order Acknowledgment</option>
              <option value="860">860 - Purchase Order Change</option>
            </select>
          </div>

          {/* PO Number */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              PO Number (Optional)
            </label>
            <input
              type="text"
              value={poNumber}
              onChange={(e) => setPoNumber(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              placeholder="Enter PO number for reference"
            />
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              EDI File *
            </label>
            <div
              className={`relative border-2 border-dashed rounded-lg p-8 text-center ${
                dragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                onChange={handleFileChange}
                accept=".edi,.x12,.txt,.xml"
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <ArrowUpTrayIcon className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2 text-sm text-gray-600">
                {file ? (
                  <span className="font-medium text-indigo-600">{file.name}</span>
                ) : (
                  <>
                    Drag and drop your file here, or <span className="text-indigo-600">browse</span>
                  </>
                )}
              </p>
              <p className="mt-1 text-xs text-gray-500">
                Supported formats: .edi, .x12, .txt, .xml (Max 10 MB)
              </p>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 text-sm text-red-700 bg-red-100 rounded-md">
              {error}
            </div>
          )}

          {/* Success Message */}
          {success && (
            <div className="flex items-center p-3 text-sm text-green-700 bg-green-100 rounded-md">
              <CheckCircleIcon className="w-5 h-5 mr-2" />
              File uploaded successfully! Redirecting...
            </div>
          )}

          {/* Buttons */}
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => navigate('/modern-edi/partner-portal/dashboard')}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!file || uploading}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : 'Upload File'}
            </button>
          </div>
        </form>
      </div>

      {/* Upload Guidelines */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-blue-900 mb-2">Upload Guidelines</h3>
        <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
          <li>Maximum file size: 10 MB</li>
          <li>Supported formats: .edi, .x12, .txt, .xml</li>
          <li>Files are processed automatically after upload</li>
          <li>You'll receive a confirmation once processing is complete</li>
        </ul>
      </div>
    </div>
  );
}
