import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import FolderView from './pages/FolderView';

// Admin Dashboard
import AdminLayout from './pages/admin/AdminLayout';
import AdminDashboard from './pages/admin/AdminDashboard';
import PartnerManagement from './pages/admin/PartnerManagement';
import UserManagement from './pages/admin/UserManagement';
import PermissionsManagement from './pages/admin/PermissionsManagement';
import Analytics from './pages/admin/Analytics';
import ActivityLog from './pages/admin/ActivityLog';
import MailboxFolderView from './pages/admin/MailboxFolderView';
import RoutesManagement from './pages/admin/Routes';
import Channels from './pages/admin/Channels';

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
    <Routes>
      {/* Modern EDI Interface - Redirect to Admin */}
      <Route path="/" element={<Navigate to="/admin" replace />} />
      <Route path="/old-dashboard" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="folder/:folderName" element={<FolderView />} />
      </Route>

      {/* Admin Dashboard */}
      <Route path="/admin" element={<AdminLayout />}>
        <Route index element={<AdminDashboard />} />
        <Route path="partners" element={<PartnerManagement />} />
        <Route path="routes" element={<RoutesManagement />} />
        <Route path="channels" element={<Channels />} />
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
  );
}

export default App;
