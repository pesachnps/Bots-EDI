import { useState, useEffect } from 'react';
import {
  ArrowDownTrayIcon,
  ChartBarIcon,
  DocumentTextIcon,
  UsersIcon,
} from '@heroicons/react/24/outline';
import adminApi from '../../services/adminApi';

export default function Analytics() {
  const [loading, setLoading] = useState(true);
  const [transactionData, setTransactionData] = useState(null);
  const [partnerData, setPartnerData] = useState(null);
  const [documentData, setDocumentData] = useState(null);
  const [dateRange, setDateRange] = useState('30');

  useEffect(() => {
    loadAnalytics();
  }, [dateRange]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [transactions, partners, documents] = await Promise.all([
        adminApi.getTransactionAnalytics({ days: dateRange }),
        adminApi.getPartnerAnalyticsList({ days: dateRange }),
        adminApi.getDocumentAnalytics({ days: dateRange }),
      ]);
      
      setTransactionData(transactions);
      setPartnerData(partners);
      setDocumentData(documents);
    } catch (err) {
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    // Export functionality
    alert('Export functionality - integrate with backend export endpoint');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics & Reports</h1>
        <div className="flex items-center space-x-4">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="7">Last 7 Days</option>
            <option value="30">Last 30 Days</option>
            <option value="90">Last 90 Days</option>
          </select>
          <button
            onClick={handleExport}
            className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
          >
            <ArrowDownTrayIcon className="h-5 w-5 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
              <ChartBarIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Total Transactions</dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {transactionData?.data?.reduce((sum, d) => sum + (d.count || 0), 0).toLocaleString() || 0}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
              <UsersIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Active Partners</dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {partnerData?.partners?.length || 0}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
              <DocumentTextIcon className="h-6 w-6 text-white" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Document Types</dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {documentData?.document_types?.length || 0}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* Transaction Volume Chart */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">Transaction Volume Over Time</h2>
        </div>
        <div className="p-6">
          <div className="h-80 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
            <div className="text-center">
              <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Chart Placeholder</h3>
              <p className="mt-1 text-sm text-gray-500">
                Install Recharts or Chart.js to display transaction volume chart
              </p>
              <div className="mt-4 text-xs text-gray-400">
                <code>npm install recharts</code>
              </div>
            </div>
          </div>
          
          {/* Data Table as Fallback */}
          {transactionData?.data && (
            <div className="mt-6">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Transaction Data</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Count</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Success</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Failed</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {transactionData.data.slice(0, 10).map((row, idx) => (
                      <tr key={idx}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{row.date}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">{row.count}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 text-right">{row.success}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 text-right">{row.failed}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Partner Performance */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium text-gray-900">Partner Performance</h2>
          </div>
          <div className="p-6">
            {partnerData?.partners && partnerData.partners.length > 0 ? (
              <div className="space-y-4">
                {partnerData.partners.slice(0, 10).map((partner) => (
                  <div key={partner.id} className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">{partner.name}</p>
                      <p className="text-xs text-gray-500">
                        Success Rate: {partner.success_rate?.toFixed(1)}%
                      </p>
                    </div>
                    <div className="ml-4 flex-shrink-0">
                      <span className="text-sm font-semibold text-gray-900">
                        {partner.transaction_count?.toLocaleString()}
                      </span>
                      <span className="text-xs text-gray-500 ml-1">txns</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">No partner data available</div>
            )}
          </div>
        </div>

        {/* Document Type Breakdown */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium text-gray-900">Document Type Breakdown</h2>
          </div>
          <div className="p-6">
            {documentData?.document_types && documentData.document_types.length > 0 ? (
              <div className="space-y-4">
                {documentData.document_types.map((doc) => (
                  <div key={doc.type} className="flex items-center">
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-900">{doc.type}</span>
                        <span className="text-sm text-gray-500">{doc.percentage?.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-indigo-600 h-2 rounded-full"
                          style={{ width: `${doc.percentage}%` }}
                        />
                      </div>
                    </div>
                    <div className="ml-4 text-sm font-semibold text-gray-900">
                      {doc.count?.toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">No document data available</div>
            )}
          </div>
        </div>
      </div>

      {/* Chart Integration Guide */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-medium text-blue-900 mb-2">📊 Add Charts</h3>
        <p className="text-sm text-blue-800 mb-4">
          To display interactive charts, install a charting library:
        </p>
        <div className="bg-white rounded p-4 font-mono text-sm space-y-2">
          <div className="text-gray-600"># Option 1: Recharts (Recommended)</div>
          <div className="text-gray-900">npm install recharts</div>
          <div className="text-gray-600 mt-4"># Option 2: Chart.js</div>
          <div className="text-gray-900">npm install chart.js react-chartjs-2</div>
        </div>
        <p className="text-sm text-blue-800 mt-4">
          Then import and use the chart components in this file. The data is already loaded and ready to use!
        </p>
      </div>
    </div>
  );
}
