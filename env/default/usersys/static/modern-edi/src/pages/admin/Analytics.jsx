import { useState, useEffect } from 'react';
import { ArrowDownTrayIcon } from '@heroicons/react/24/outline';

export default function Analytics() {
  const [period, setPeriod] = useState('month');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, [period, dateFrom, dateTo]);

  const fetchAnalytics = async () => {
    try {
      const params = new URLSearchParams();
      if (dateFrom) params.append('date_from', dateFrom);
      if (dateTo) params.append('date_to', dateTo);
      params.append('period', period);

      const response = await fetch(`/modern-edi/api/v1/admin/analytics/transactions?${params}`);
      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    }
  };

  const exportData = (format) => {
    const params = new URLSearchParams();
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);
    params.append('export', format);
    
    window.location.href = `/modern-edi/api/v1/admin/analytics/transactions?${params}`;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics & Reporting</h1>
        <div className="flex space-x-2">
          <button
            onClick={() => exportData('csv')}
            className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
            Export CSV
          </button>
          <button
            onClick={() => exportData('pdf')}
            className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
            Export PDF
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Period</label>
            <select
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="day">Daily</option>
              <option value="week">Weekly</option>
              <option value="month">Monthly</option>
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
          <div className="flex items-end">
            <button
              onClick={() => { setDateFrom(''); setDateTo(''); }}
              className="w-full px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Transaction Volume Chart */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">Transaction Volume</h2>
        </div>
        <div className="p-6">
          <div className="h-64 flex items-center justify-center text-gray-500">
            Chart placeholder - Integrate Chart.js or Recharts for line chart
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Document Type Breakdown */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium text-gray-900">Document Type Breakdown</h2>
          </div>
          <div className="p-6">
            <div className="h-64 flex items-center justify-center text-gray-500">
              Pie chart placeholder
            </div>
          </div>
        </div>

        {/* Success/Failure Rates */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium text-gray-900">Success/Failure Rates by Partner</h2>
          </div>
          <div className="p-6">
            <div className="h-64 flex items-center justify-center text-gray-500">
              Bar chart placeholder
            </div>
          </div>
        </div>
      </div>

      {/* Partner Activity Heatmap */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">Partner Activity Heatmap</h2>
        </div>
        <div className="p-6">
          <div className="h-64 flex items-center justify-center text-gray-500">
            Heatmap placeholder - Shows activity by hour and day
          </div>
        </div>
      </div>
    </div>
  );
}
