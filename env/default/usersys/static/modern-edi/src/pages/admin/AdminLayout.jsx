import { useState } from 'react';
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  UsersIcon, 
  ChartBarIcon, 
  ClipboardDocumentListIcon,
  ShieldCheckIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
  MapIcon,
  CheckCircleIcon,
  TableCellsIcon,
  HashtagIcon,
  InboxIcon,
  PaperAirplaneIcon,
  ComputerDesktopIcon,
  PlayIcon,
  FolderIcon,
  DocumentTextIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  Cog6ToothIcon,
  WrenchScrewdriverIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  TrashIcon
} from '@heroicons/react/24/outline';

export default function AdminLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    configuration: true,
    transactions: true,
    operations: true,
    administration: false
  });
  const navigate = useNavigate();
  const location = useLocation();

  const navigationSections = [
    {
      name: 'Dashboard',
      href: '/admin',
      icon: HomeIcon,
      standalone: true
    },
    {
      name: 'Partners',
      href: '/admin/partners',
      icon: UsersIcon,
      standalone: true
    },
    {
      key: 'configuration',
      title: 'Configuration',
      icon: Cog6ToothIcon,
      items: [
        { name: 'Routes', href: '/admin/routes', icon: MapIcon },
        { name: 'Channels', href: '/admin/channels', icon: HomeIcon },
        { name: 'Translations', href: '/admin/translations', icon: DocumentTextIcon },
        { name: 'Confirm Rules', href: '/admin/confirmrules', icon: CheckCircleIcon },
        { name: 'Code Lists', href: '/admin/codelists', icon: TableCellsIcon },
        { name: 'Counters', href: '/admin/counters', icon: HashtagIcon },
      ]
    },
    {
      key: 'transactions',
      title: 'Transactions',
      icon: InboxIcon,
      items: [
        { name: 'Inbox', href: '/admin/mailbox/inbox', icon: InboxIcon },
        { name: 'Received', href: '/admin/mailbox/received', icon: ArrowDownTrayIcon },
        { name: 'Outbox', href: '/admin/mailbox/outbox', icon: ArrowUpTrayIcon },
        { name: 'Sent', href: '/admin/mailbox/sent', icon: CheckCircleIcon },
        { name: 'Deleted', href: '/admin/mailbox/deleted', icon: TrashIcon },
      ]
    },
    {
      key: 'operations',
      title: 'Operations',
      icon: WrenchScrewdriverIcon,
      items: [
        { name: 'Engine', href: '/admin/engine', icon: PlayIcon },
        { name: 'Files', href: '/admin/files', icon: FolderIcon },
        { name: 'Logs', href: '/admin/logs', icon: DocumentTextIcon },
        { name: 'System', href: '/admin/system', icon: ComputerDesktopIcon },
      ]
    },
    {
      key: 'administration',
      title: 'Administration',
      icon: ShieldCheckIcon,
      items: [
        { name: 'Users', href: '/admin/users', icon: UsersIcon },
        { name: 'Permissions', href: '/admin/permissions', icon: ShieldCheckIcon },
        { name: 'Analytics', href: '/admin/analytics', icon: ChartBarIcon },
        { name: 'Activity Logs', href: '/admin/activity-logs', icon: ClipboardDocumentListIcon },
      ]
    }
  ];

  const toggleSection = (key) => {
    setExpandedSections(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleLogout = () => {
    // Logout logic
    window.location.href = '/admin/logout/';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-40 lg:hidden ${sidebarOpen ? '' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 flex w-64 flex-col bg-white">
          <div className="flex items-center justify-between h-16 px-4 border-b">
            <span className="text-xl font-bold text-indigo-600">Admin Dashboard</span>
            <button onClick={() => setSidebarOpen(false)}>
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>
          <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
            {navigationSections.map((section) => {
              if (section.standalone) {
                const isActive = location.pathname === section.href;
                return (
                  <Link
                    key={section.name}
                    to={section.href}
                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-indigo-100 text-indigo-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <section.icon className="mr-3 h-5 w-5" />
                    {section.name}
                  </Link>
                );
              }

              return (
                <div key={section.key} className="space-y-1">
                  <button
                    onClick={() => toggleSection(section.key)}
                    className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-100"
                  >
                    <section.icon className="mr-3 h-5 w-5" />
                    <span className="flex-1 text-left">{section.title}</span>
                    {expandedSections[section.key] ? (
                      <ChevronDownIcon className="h-4 w-4" />
                    ) : (
                      <ChevronRightIcon className="h-4 w-4" />
                    )}
                  </button>
                  {expandedSections[section.key] && (
                    <div className="ml-4 space-y-1">
                      {section.items.map((item) => {
                        const isActive = location.pathname === item.href;
                        return (
                          <Link
                            key={item.name}
                            to={item.href}
                            className={`flex items-center px-3 py-2 text-sm rounded-md ${
                              isActive
                                ? 'bg-indigo-100 text-indigo-700 font-medium'
                                : 'text-gray-600 hover:bg-gray-100'
                            }`}
                            onClick={() => setSidebarOpen(false)}
                          >
                            <item.icon className="mr-3 h-4 w-4" />
                            {item.name}
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-col flex-1 min-h-0 bg-white border-r">
          <div className="flex items-center h-16 px-4 border-b">
            <span className="text-xl font-bold text-indigo-600">Admin Dashboard</span>
          </div>
          <div className="flex-1 flex flex-col overflow-hidden">
            <nav className="px-2 py-4 space-y-1 overflow-y-auto">
              {navigationSections.map((section) => {
                if (section.standalone) {
                  const isActive = location.pathname === section.href;
                  return (
                    <Link
                      key={section.name}
                      to={section.href}
                      className={`flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                        isActive
                          ? 'bg-indigo-100 text-indigo-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <section.icon className="mr-3 h-5 w-5" />
                      {section.name}
                    </Link>
                  );
                }

                return (
                  <div key={section.key} className="space-y-1">
                    <button
                      onClick={() => toggleSection(section.key)}
                      className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-100"
                    >
                      <section.icon className="mr-3 h-5 w-5" />
                      <span className="flex-1 text-left">{section.title}</span>
                      {expandedSections[section.key] ? (
                        <ChevronDownIcon className="h-4 w-4" />
                      ) : (
                        <ChevronRightIcon className="h-4 w-4" />
                      )}
                    </button>
                    {expandedSections[section.key] && (
                      <div className="ml-4 space-y-1">
                        {section.items.map((item) => {
                          const isActive = location.pathname === item.href;
                          return (
                            <Link
                              key={item.name}
                              to={item.href}
                              className={`flex items-center px-3 py-2 text-sm rounded-md ${
                                isActive
                                  ? 'bg-indigo-100 text-indigo-700 font-medium'
                                  : 'text-gray-600 hover:bg-gray-100'
                              }`}
                            >
                              <item.icon className="mr-3 h-4 w-4" />
                              {item.name}
                            </Link>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>
          </div>
          <div className="flex-shrink-0 p-4 border-t">
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-100"
            >
              <ArrowRightOnRectangleIcon className="mr-3 h-5 w-5" />
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-10 flex h-16 bg-white border-b lg:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="px-4 text-gray-500 focus:outline-none"
          >
            <Bars3Icon className="h-6 w-6" />
          </button>
          <div className="flex items-center flex-1 px-4">
            <span className="text-lg font-semibold">Admin Dashboard</span>
          </div>
        </div>

        {/* Page content */}
        <main className="py-6">
          <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
