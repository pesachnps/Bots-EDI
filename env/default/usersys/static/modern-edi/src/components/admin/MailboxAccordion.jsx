import { useState } from 'react';
import { 
  InboxIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  CheckCircleIcon,
  TrashIcon,
  ChevronDownIcon,
  ChevronUpIcon
} from '@heroicons/react/24/outline';
import { useFolders } from '../../hooks/useTransactions';
import MailboxFolderContent from './MailboxFolderContent';

const folderIcons = {
  inbox: InboxIcon,
  received: ArrowDownTrayIcon,
  outbox: ArrowUpTrayIcon,
  sent: CheckCircleIcon,
  deleted: TrashIcon,
};

const folderColors = {
  inbox: 'text-blue-600 bg-blue-50',
  received: 'text-green-600 bg-green-50',
  outbox: 'text-yellow-600 bg-yellow-50',
  sent: 'text-purple-600 bg-purple-50',
  deleted: 'text-red-600 bg-red-50',
};

const folderBadgeColors = {
  inbox: 'bg-blue-500 text-white',
  received: 'bg-green-500 text-white',
  outbox: 'bg-yellow-500 text-white',
  sent: 'bg-purple-500 text-white',
  deleted: 'bg-red-500 text-white',
};

export default function MailboxAccordion() {
  const [expandedFolder, setExpandedFolder] = useState(null);
  const { data: folders, isLoading, error } = useFolders();

  const toggleFolder = (folderName) => {
    setExpandedFolder(expandedFolder === folderName ? null : folderName);
  };

  if (isLoading) {
    return (
      <div className="px-2 py-4">
        <div className="text-xs text-gray-500 text-center">Loading folders...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="px-2 py-4">
        <div className="text-xs text-red-500 text-center">Failed to load folders</div>
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {folders?.map((folder) => {
        const Icon = folderIcons[folder.name] || InboxIcon;
        const colorClass = folderColors[folder.name] || 'text-gray-600 bg-gray-50';
        const badgeColorClass = folderBadgeColors[folder.name] || 'bg-gray-500 text-white';
        const isExpanded = expandedFolder === folder.name;

        return (
          <div key={folder.name} className="border-b border-gray-200 last:border-b-0">
            {/* Accordion Header */}
            <button
              onClick={() => toggleFolder(folder.name)}
              className={`w-full flex items-center justify-between px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                isExpanded
                  ? 'bg-indigo-50 text-indigo-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <div className="flex items-center space-x-2 flex-1 min-w-0">
                <div className={`flex-shrink-0 p-1.5 rounded ${colorClass}`}>
                  <Icon className="h-4 w-4" />
                </div>
                <span className="capitalize truncate">{folder.display_name || folder.name}</span>
                <span className={`flex-shrink-0 px-2 py-0.5 text-xs font-semibold rounded-full ${badgeColorClass}`}>
                  {folder.count}
                </span>
              </div>
              <div className="flex-shrink-0 ml-2">
                {isExpanded ? (
                  <ChevronUpIcon className="h-4 w-4" />
                ) : (
                  <ChevronDownIcon className="h-4 w-4" />
                )}
              </div>
            </button>

            {/* Accordion Content */}
            {isExpanded && (
              <div className="mt-2 px-2 pb-2">
                <MailboxFolderContent folderName={folder.name} />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
