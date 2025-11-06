import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowUpTrayIcon,
  ArrowDownTrayIcon,
  DocumentTextIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';

export default function PartnerDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/modern-edi/api/v1/partner-portal/dashboard/metrics');
      const data = await response.json();
      setMetrics(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading...</div>;
  }

  const metricCards = [
    {
      name: 'Sent Transactions',
      value: metrics?.metrics?.sent_count || 0,
      icon: ArrowUpTrayIcon,
      color: 'bg-blue-500',
      link: '/modern-edi/partner-portal/transactions?direction=sent',
    },
    {
      name: 'Received Transactions',
      value: metrics?.metrics?.received_count || 0,
      icon: ArrowDownTrayIcon,
      color: 'bg-green-500',
      link: '/modern-edi/partner-portal/transactions?direction=received',
    },
    {
      name: 'Pending',
      value: metrics?.metrics?.pending_count || 0,
      icon: DocumentTextIcon,
      color: 'bg-yellow-500',
      link: '/modern-edi/partner-portal/transactions?status=pending',
    },
    {
      name: 'Errors',
      value: metrics?.metrics?.error_count || 0,
      icon: ExclamationCircleIcon,
      color: 'bg-red-500',
      link: '/modern-edi/partner-portal/transactions?status=error',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back, {metrics?.partner?.name}</p>
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
            <div className="px-5 py-3 bg-gray-50">
              <Link to={card.link} className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                View details →
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Link
            to="/modern-edi/partner-portal/upload"
            className="flex items-center justify-center px-4 py-3 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
          >
            <ArrowUpTrayIcon className="w-5 h-5 mr-2" />
            Upload File
          </Link>
          <Link
            to="/modern-edi/partner-portal/download"
            className="flex items-center justify-center px-4 py-3 text-sm font-medium text-indigo-600 bg-indigo-100 rounded-md hover:bg-indigo-200"
          >
            <ArrowDownTrayIcon className="w-5 h-5 mr-2" />
            Download Files
          </Link>
          <Link
            to="/modern-edi/partner-portal/transactions"
            className="flex items-center justify-center px-4 py-3 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
          >
            <DocumentTextIcon className="w-5 h-5 mr-2" />
            View Transactions
          </Link>
        </div>
      </div>

      {/* Recent Transactions */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">Recent Transactions</h2>
        </div>
        <div className="p-6">
          {metrics?.recent_transactions?.length > 0 ? (
            <div className="space-y-4">
              {metrics.recent_transactions.map((txn) => (
                <div key={txn.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{txn.type} - {txn.po_number}</p>
                    <p className="text-sm text-gray-500">{new Date(txn.date).toLocaleString()}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    txn.status === 'sent' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {txn.status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500">No recent transactions</div>
          )}
        </div>
      </div>

      {/* Partner Information */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Partner Information</h2>
        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Partner ID</dt>
            <dd className="mt-1 text-sm text-gray-900">{metrics?.partner?.partner_id}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Company Name</dt>
            <dd className="mt-1 text-sm text-gray-900">{metrics?.partner?.name}</dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
