import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';

export default function ActivityLog() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [userTypeFilter, setUserTypeFilter] = useState('all');
  const [actionFilter, setActionFilter] = useState('all');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchLogs();
  }, [search, userTypeFilter, actionFilter, dateFrom, dateTo, page]);

  const fetchLogs = async () => {
    try {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (userTypeFilter !== 'all') params.append('user_type', userTypeFilter);
      if (actionFilter !== 'all') params.append('action', actionFilter);
      if (dateFrom) params.append('date_from', dateFrom);
      if (dateTo) params.append('date_to', dateTo);
      params.append('page', page);

      const response = await fetch(`/modern-edi/api/v1/admin/activity-logs?${params}`);
      const data = await response.json();
      setLogs(data.results || []);
      setTotalPages(Math.ceil(data.count / 50));
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch logs:', error);
      setLoading(false);
    }
  };

  const exportLogs = () => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (userTypeFilter !== 'all') params.append('user_type', userTypeFilter);
    if (actionFilter !== 'all') params.append('action', actionFilter);
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);
    
    window.location.href = `/modern-edi/api/v1/admin/activity-logs/export?${params}`;
  };

  const getActionBadge = (action) => {
    const colors = {
      login: 'bg-green-100 text-green-800',
      logout: 'bg-gray-100 text-gray-800',
      upload: 'bg-blue-100 text-blue-800',
      download: 'bg-indigo-100 text-indigo-800',
      delete: 'bg-red-100 text-red-800',
      edit: 'bg-yellow-100 text-yellow-800',
    };
    return colors[action] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Activity Logs</h1>
        <button
          onClick={exportLogs}
          className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
        >
          <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
          Export CSV
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 space-y-4">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute w-5 h-5 text-gray-400 left-3 top-3" />
          <input
            type="text"
            placeholder="Search by user name or action..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full py-2 pl-10 pr-4 border border-gray-300 rounded-md"
          />
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">User Type</label>
            <select
              value={userTypeFilter}
              onChange={(e) => setUserTypeFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="all">All Types</option>
              <option value="admin">Admin</option>
              <option value="partner">Partner</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Action</label>
            <select
              value={actionFilter}
              onChange={(e) => setActionFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="all">All Actions</option>
              <option value="login">Login</option>
              <option value="logout">Logout</option>
              <option value="upload">Upload</option>
              <option value="download">Download</option>
              <option value="edit">Edit</option>
              <option value="delete">Delete</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">From Date</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">To Date</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-500">Loading logs...</div>
        ) : logs.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No logs found</div>
        ) : (
          <>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Resource</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">IP Address</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Details</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{log.user_name}</div>
                      <div className="text-sm text-gray-500">{log.user_type}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getActionBadge(log.action)}`}>
                        {log.action}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {log.resource_type && (
                        <div>
                          <div>{log.resource_type}</div>
                          <div className="text-xs text-gray-400">{log.resource_id}</div>
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {log.ip_address}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {log.details && Object.keys(log.details).length > 0 && (
                        <pre className="text-xs">{JSON.stringify(log.details, null, 2)}</pre>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination */}
            <div className="px-6 py-4 border-t flex items-center justify-between">
              <div className="text-sm text-gray-500">
                Page {page} of {totalPages}
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-3 py-1 text-sm border rounded disabled:opacity-50"
                >
                  Previous
                </button>
                <button
                  onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-3 py-1 text-sm border rounded disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
