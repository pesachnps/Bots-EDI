import { X, Inbox, CheckCircle, Send, Archive, Trash2 } from 'lucide-react';

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

function MoveDialog({ currentFolder, onMove, onCancel }) {
  const folders = ['inbox', 'received', 'outbox', 'sent', 'deleted'];
  const availableFolders = folders.filter(f => f !== currentFolder);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-gray-900">Move Transaction</h2>
          <button
            onClick={onCancel}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <p className="text-gray-600 mb-4">Select destination folder:</p>
          <div className="space-y-2">
            {availableFolders.map((folder) => {
              const Icon = folderIcons[folder];
              const colorClass = folderColors[folder];

              return (
                <button
                  key={folder}
                  onClick={() => onMove(folder)}
                  className="w-full flex items-center space-x-3 p-4 rounded-lg border-2 border-gray-200 hover:border-primary-500 hover:bg-primary-50 transition-colors"
                >
                  <div className={`${colorClass} p-2 rounded-lg`}>
                    <Icon className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-lg font-medium text-gray-900 capitalize">
                    {folder}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t border-gray-200">
          <button onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default MoveDialog;
