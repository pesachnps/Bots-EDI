import { Outlet, Link } from 'react-router-dom';
import { FileText, Home, LogOut } from 'lucide-react';

function Layout() {
  const handleLogout = () => {
    window.location.href = '/logout/';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Title */}
            <div className="flex items-center space-x-3">
              <FileText className="h-8 w-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">Modern EDI Interface</h1>
                <p className="text-xs text-gray-500">Transaction Management</p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center space-x-4">
              <Link
                to="/"
                className="flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              >
                <Home className="h-5 w-5" />
                <span>Dashboard</span>
              </Link>
              
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            © 2025 Modern EDI Interface. Built on Bots EDI Framework.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default Layout;
