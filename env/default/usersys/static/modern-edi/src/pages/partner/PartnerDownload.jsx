import { useState, useEffect } from 'react';
import { ArrowDownTrayIcon, CheckIcon } from '@heroicons/react/24/outline';

export default function PartnerDownload() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFiles, setSelectedFiles] = useState(new Set());

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await fetch('/modern-edi/api/v1/partner-portal/files/download');
      const data = await response.json();
      setFiles(data.files || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch files:', error);
      setLoading(false);
    }
  };

  const handleDownload = async (fileId, filename) => {
    try {
      const response = await fetch(`/modern-edi/api/v1/partner-portal/files/download/${fileId}`);
      const blob = await response.blob();
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      // Refresh file list
      fetchFiles();
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  const handleBulkDownload = async () => {
    if (selectedFiles.size === 0) return;

    try {
      const response = await fetch('/modern-edi/api/v1/partner-portal/files/download/bulk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transaction_ids: Array.from(selectedFiles) }),
      });
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'edi_files.zip';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      setSelectedFiles(new Set());
      fetchFiles();
    } catch (error) {
      console.error('Bulk download failed:', error);
    }
  };

  const toggleFileSelection = (fileId) => {
    const newSelection = new Set(selectedFiles);
    if (newSelection.has(fileId)) {
      newSelection.delete(fileId);
    } else {
      newSelection.add(fileId);
    }
    setSelectedFiles(newSelection);
  };

  const toggleSelectAll = () => {
    if (selectedFiles.size === files.length) {
      setSelectedFiles(new Set());
    } else {
      setSelectedFiles(new Set(files.map(f => f.id)));
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Download Files</h1>
        {selectedFiles.size > 0 && (
          <button
            onClick={handleBulkDownload}
            className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
          >
            <ArrowDownTrayIcon className="w-5 h-5 mr-2" />
            Download Selected ({selectedFiles.size})
          </button>
        )}
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading files...</div>
        ) : files.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No files available for download</div>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    checked={selectedFiles.size === files.length}
                    onChange={toggleSelectAll}
                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded"
                  />
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">File Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Document Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Size</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {files.map((file) => (
                <tr key={file.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <input
                      type="checkbox"
                      checked={selectedFiles.has(file.id)}
                      onChange={() => toggleFileSelection(file.id)}
                      className="w-4 h-4 text-indigo-600 border-gray-300 rounded"
                    />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {file.filename}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {file.document_type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(file.date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatFileSize(file.size)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {file.downloaded ? (
                      <span className="flex items-center text-sm text-green-600">
                        <CheckIcon className="w-4 h-4 mr-1" />
                        Downloaded
                      </span>
                    ) : (
                      <span className="px-2 py-1 text-xs font-medium text-blue-800 bg-blue-100 rounded-full">
                        New
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleDownload(file.id, file.filename)}
                      className="text-indigo-600 hover:text-indigo-900"
                    >
                      Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Download Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-blue-900 mb-2">Download Information</h3>
        <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
          <li>Files can be downloaded multiple times</li>
          <li>Select multiple files to download as a ZIP archive</li>
          <li>Downloaded files are marked with a checkmark</li>
          <li>Files are retained according to your retention policy</li>
        </ul>
      </div>
    </div>
  );
}
