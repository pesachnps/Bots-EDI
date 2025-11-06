import { Link } from 'react-router-dom';
import { Inbox, CheckCircle, Send, Archive, Trash2, Loader2 } from 'lucide-react';
import { useFolders } from '../hooks/useTransactions';

const folderIcons = {
  inbox: Inbox,
  received: CheckCircle,
  outbox: Send,
  sent: Archive,
  deleted: Trash2,
};

const folderColors = {
  inbox: 'bg-blue-500',
  received: 'bg-green-500',
  outbox: 'bg-yellow-500',
  sent: 'bg-purple-500',
  deleted: 'bg-red-500',
};

function Dashboard() {
  const { data: folders, isLoading, error } = useFolders();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Failed to load folders: {error.message}</p>
      </div>
    );
  }

  return (
    <div>
      {/* Page Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <p className="mt-2 text-gray-600">
          Manage your EDI transactions across all folders
        </p>
      </div>

      {/* Folder Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {folders?.map((folder) => {
          const Icon = folderIcons[folder.name] || Inbox;
          const colorClass = folderColors[folder.name] || 'bg-gray-500';

          return (
            <Link
              key={folder.name}
              to={`/folder/${folder.name}`}
              className="block"
            >
              <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6 border border-gray-200 hover:border-primary-300">
                {/* Icon and Title */}
                <div className="flex items-center space-x-4 mb-4">
                  <div className={`${colorClass} p-3 rounded-lg`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {folder.display_name}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {folder.name}
                    </p>
                  </div>
                </div>

                {/* Transaction Count */}
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Transactions</span>
                    <span className="text-2xl font-bold text-gray-900">
                      {folder.count}
                    </span>
                  </div>
                </div>

                {/* View Link */}
                <div className="mt-4">
                  <span className="text-sm text-primary-600 font-medium hover:text-primary-700">
                    View transactions →
                  </span>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Quick Stats */}
      <div className="mt-8 bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {folders?.map((folder) => (
            <div key={folder.name} className="text-center">
              <p className="text-sm text-gray-600 capitalize">{folder.name}</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{folder.count}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
