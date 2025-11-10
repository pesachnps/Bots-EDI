import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import FolderView from './pages/FolderView';

// Admin Authentication
import { AdminAuthProvider } from './context/AdminAuthContext';
import ProtectedAdminRoute from './components/ProtectedAdminRoute';
import AdminLogin from './pages/admin/AdminLogin';
import AdminSignup from './pages/admin/AdminSignup';
import AdminForgotPassword from './pages/admin/AdminForgotPassword';
import AdminResetPassword from './pages/admin/AdminResetPassword';

// Admin Dashboard
import AdminLayout from './pages/admin/AdminLayout';
import AdminDashboard from './pages/admin/AdminDashboard';
import PartnerManagement from './pages/admin/PartnerManagement';
import UserManagement from './pages/admin/UserManagement';
import PermissionsManagement from './pages/admin/PermissionsManagement';
import Analytics from './pages/admin/Analytics';
import ActivityLog from './pages/admin/ActivityLog';
import MailboxFolderView from './pages/admin/MailboxFolderView';
import RoutesPage from './pages/admin/Routes';
import Channels from './pages/admin/Channels';
import Translations from './pages/admin/Translations';
import ConfirmRules from './pages/admin/ConfirmRules';
import CodeLists from './pages/admin/CodeLists';
import Counters from './pages/admin/Counters';
import Incoming from './pages/admin/Incoming';
import Outgoing from './pages/admin/Outgoing';
import System from './pages/admin/System';
import Engine from './pages/admin/Engine';
import Files from './pages/admin/Files';
import Logs from './pages/admin/Logs';
import Cleanup from './pages/admin/Cleanup';

// Partner Portal
import PartnerPortalLayout from './pages/partner/PartnerPortalLayout';
import PartnerLogin from './pages/partner/PartnerLogin';
import PartnerDashboard from './pages/partner/PartnerDashboard';
import PartnerTransactions from './pages/partner/PartnerTransactions';
import PartnerUpload from './pages/partner/PartnerUpload';
import PartnerDownload from './pages/partner/PartnerDownload';
import PartnerSettings from './pages/partner/PartnerSettings';

import './App.css';

function App() {
  return (
    <AdminAuthProvider>
      <Routes>
        {/* Modern EDI Interface - Redirect to Admin */}
        <Route path="/" element={<Navigate to="/admin" replace />} />
        <Route path="/old-dashboard" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="folder/:folderName" element={<FolderView />} />
        </Route>

        {/* Admin Auth Routes (Public) */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/signup" element={<AdminSignup />} />
        <Route path="/admin/forgot-password" element={<AdminForgotPassword />} />
        <Route path="/admin/reset-password" element={<AdminResetPassword />} />

        {/* Admin Dashboard (Protected) */}
        <Route path="/admin" element={
          <ProtectedAdminRoute>
            <AdminLayout />
          </ProtectedAdminRoute>
        }>
        <Route index element={<AdminDashboard />} />
        <Route path="partners" element={<PartnerManagement />} />
        <Route path="routes" element={<RoutesPage />} />
        <Route path="channels" element={<Channels />} />
        <Route path="translations" element={<Translations />} />
        <Route path="confirmrules" element={<ConfirmRules />} />
        <Route path="codelists" element={<CodeLists />} />
        <Route path="counters" element={<Counters />} />
        <Route path="incoming" element={<Incoming />} />
        <Route path="outgoing" element={<Outgoing />} />
        <Route path="system" element={<System />} />
        <Route path="engine" element={<Engine />} />
        <Route path="files" element={<Files />} />
        <Route path="logs" element={<Logs />} />
        <Route path="cleanup" element={<Cleanup />} />
        <Route path="users" element={<UserManagement />} />
        <Route path="permissions" element={<PermissionsManagement />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="activity-logs" element={<ActivityLog />} />
        <Route path="mailbox/:folderName" element={<MailboxFolderView />} />
      </Route>

      {/* Partner Portal */}
      <Route path="/partner-portal/login" element={<PartnerLogin />} />
      <Route path="/partner-portal" element={<PartnerPortalLayout />}>
        <Route index element={<Navigate to="/partner-portal/dashboard" replace />} />
        <Route path="dashboard" element={<PartnerDashboard />} />
        <Route path="transactions" element={<PartnerTransactions />} />
        <Route path="upload" element={<PartnerUpload />} />
        <Route path="download" element={<PartnerDownload />} />
        <Route path="settings" element={<PartnerSettings />} />
      </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AdminAuthProvider>
  );
}

export default App;
