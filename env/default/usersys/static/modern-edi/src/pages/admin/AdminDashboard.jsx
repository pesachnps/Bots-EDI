import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  UsersIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  ArrowTrendingUpIcon,
} from '@heroicons/react/24/outline';

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    fetchMetrics();
    
    if (autoRefresh) {
      const interval = setInterval(fetchMetrics, 60000); // Refresh every 60 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/modern-edi/api/v1/admin/dashboard/metrics');
      const data = await response.json();
      setMetrics(data.metrics);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  const metricCards = [
    {
      name: 'Total Partners',
      value: metrics?.total_partners || 0,
      icon: UsersIcon,
      color: 'bg-blue-500',
      link: '/modern-edi/admin/partners',
    },
    {
      name: 'Total Transactions',
      value: metrics?.total_transactions || 0,
      icon: DocumentTextIcon,
      color: 'bg-green-500',
      link: '/modern-edi/admin/analytics',
    },
    {
      name: 'Success Rate',
      value: `${metrics?.success_rate?.toFixed(1) || 0}%`,
      icon: CheckCircleIcon,
      color: 'bg-emerald-500',
    },
    {
      name: 'Error Rate',
      value: `${metrics?.error_rate?.toFixed(1) || 0}%`,
      icon: ExclamationCircleIcon,
      color: 'bg-red-500',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
        <div className="flex items-center space-x-4">
          <label className="flex items-center text-sm text-gray-600">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="mr-2"
            />
            Auto-refresh (60s)
          </label>
          <button
            onClick={fetchMetrics}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
          >
            Refresh Now
          </button>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {metricCards.map((card) => (
          <div key={card.name} className="overflow-hidden bg-white rounded-lg shadow">
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 p-3 rounded-md ${card.color}`}>
                  <card.icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1 w-0 ml-5">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{card.name}</dt>
                    <dd className="text-2xl font-semibold text-gray-900">{card.value}</dd>
                  </dl>
                </div>
              </div>
            </div>
            {card.link && (
              <div className="px-5 py-3 bg-gray-50">
                <Link to={card.link} className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                  View details →
                </Link>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Transaction Volume Chart */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">Transaction Volume (Last 30 Days)</h2>
        </div>
        <div className="p-6">
          <div className="h-64 flex items-center justify-center text-gray-500">
            Chart placeholder - Integrate Chart.js or Recharts
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Top Partners */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium text-gray-900">Top Partners by Volume</h2>
          </div>
          <div className="p-6">
            {metrics?.top_partners?.length > 0 ? (
              <div className="space-y-4">
                {metrics.top_partners.slice(0, 10).map((partner, index) => (
                  <div key={partner.id} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <span className="flex items-center justify-center w-8 h-8 text-sm font-medium text-white bg-indigo-600 rounded-full">
                        {index + 1}
                      </span>
                      <span className="ml-3 text-sm font-medium text-gray-900">{partner.name}</span>
                    </div>
                    <span className="text-sm text-gray-500">{partner.transaction_count} txns</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500">No data available</div>
            )}
          </div>
        </div>

        {/* Recent Errors */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-lg font-medium text-gray-900">Recent Errors</h2>
          </div>
          <div className="p-6">
            {metrics?.recent_errors?.length > 0 ? (
              <div className="space-y-4">
                {metrics.recent_errors.map((error) => (
                  <div key={error.id} className="flex items-start">
                    <ExclamationCircleIcon className="w-5 h-5 mt-0.5 text-red-500 flex-shrink-0" />
                    <div className="ml-3 flex-1">
                      <p className="text-sm font-medium text-gray-900">{error.partner_name}</p>
                      <p className="text-sm text-gray-500">{error.error_type}</p>
                      <p className="text-xs text-gray-400">{new Date(error.timestamp).toLocaleString()}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500">No recent errors</div>
            )}
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">System Status</h2>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {metrics?.system_status && Object.entries(metrics.system_status).map(([key, status]) => (
              <div key={key} className="flex items-center justify-between p-4 border rounded-lg">
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {key.replace(/_/g, ' ')}
                </span>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                  status === 'healthy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
