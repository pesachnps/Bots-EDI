# Frontend Implementation Guide - Admin Dashboard & Partner Portal

## Overview

This guide provides the complete plan for implementing the React frontend for the Admin Dashboard and Partner Portal. The backend is complete and ready to serve data.

## Architecture

The frontend will be integrated into the existing Modern EDI React application at:
```
env/default/usersys/static/modern-edi/
```

## Tasks Remaining

### Task 8: Admin Dashboard Pages (6 pages)
### Task 9: Admin Dashboard Components  
### Task 10: Partner Portal Pages (6 pages)
### Task 11: Partner Portal Components
### Task 12: Integrate Routes into React App

## Directory Structure

```
env/default/usersys/static/modern-edi/src/
├── pages/
│   ├── Dashboard.jsx                    # Existing
│   ├── FolderView.jsx                   # Existing
│   ├── admin/                           # NEW
│   │   ├── AdminDashboard.jsx
│   │   ├── PartnerManagement.jsx
│   │   ├── UserManagement.jsx
│   │   ├── PermissionsManagement.jsx
│   │   ├── Analytics.jsx
│   │   └── ActivityLog.jsx
│   └── partner-portal/                  # NEW
│       ├── PartnerLogin.jsx
│       ├── PartnerDashboard.jsx
│       ├── PartnerTransactions.jsx
│       ├── PartnerUpload.jsx
│       ├── PartnerDownload.jsx
│       └── PartnerSettings.jsx
├── components/
│   ├── Layout.jsx                       # Existing
│   ├── AdminLayout.jsx                  # NEW
│   ├── PartnerPortalLayout.jsx          # NEW
│   ├── admin/                           # NEW
│   │   ├── MetricCard.jsx
│   │   ├── ChartWidget.jsx
│   │   ├── PartnerTable.jsx
│   │   ├── UserTable.jsx
│   │   ├── PermissionMatrix.jsx
│   │   ├── PartnerForm.jsx
│   │   ├── UserForm.jsx
│   │   └── ActivityLogTable.jsx
│   └── partner/                         # NEW
│       ├── FileUploader.jsx
│       ├── FileList.jsx
│       ├── TransactionTable.jsx
│       ├── LoginForm.jsx
│       └── ContactInfoForm.jsx
├── hooks/
│   ├── useTransactions.js               # Existing
│   ├── useAdmin.js                      # NEW
│   └── usePartnerPortal.js              # NEW
├── services/
│   └── api.js                           # Update with new endpoints
└── App.jsx                              # Update with new routes
```

## Implementation Priority

### Phase 1: Core Infrastructure (High Priority)
1. Update `api.js` with admin and partner portal endpoints
2. Create `AdminLayout.jsx` and `PartnerPortalLayout.jsx`
3. Create authentication hooks
4. Update `App.jsx` with route guards

### Phase 2: Admin Dashboard (High Priority)
1. `AdminDashboard.jsx` - Overview with metrics
2. `PartnerManagement.jsx` - Partner CRUD
3. `UserManagement.jsx` - User CRUD
4. Supporting components (MetricCard, tables, forms)

### Phase 3: Partner Portal (Medium Priority)
1. `PartnerLogin.jsx` - Authentication
2. `PartnerDashboard.jsx` - Overview
3. `PartnerTransactions.jsx` - Transaction list
4. `PartnerUpload.jsx` - File upload
5. Supporting components

### Phase 4: Advanced Features (Lower Priority)
1. `Analytics.jsx` - Charts and reports
2. `ActivityLog.jsx` - Log viewing
3. `PermissionsManagement.jsx` - Permission matrix
4. Advanced analytics components

## API Integration

### Update services/api.js

Add these endpoint groups:

```javascript
// Admin Dashboard Endpoints
export const adminAPI = {
  getDashboardMetrics: (days = 30) => 
    axios.get(`/modern-edi/api/v1/admin/dashboard/metrics?days=${days}`),
  
  getDashboardCharts: (days = 30) => 
    axios.get(`/modern-edi/api/v1/admin/dashboard/charts?days=${days}`),
  
  getPartners: (params) => 
    axios.get('/modern-edi/api/v1/admin/partners', { params }),
  
  getPartnerUsers: (partnerId) => 
    axios.get(`/modern-edi/api/v1/admin/partners/${partnerId}/users`),
  
  createPartnerUser: (partnerId, data) => 
    axios.post(`/modern-edi/api/v1/admin/partners/${partnerId}/users`, data),
  
  updateUser: (userId, data) => 
    axios.put(`/modern-edi/api/v1/admin/users/${userId}`, data),
  
  resetPassword: (userId, newPassword) => 
    axios.post(`/modern-edi/api/v1/admin/users/${userId}/reset-password`, { new_password: newPassword }),
  
  updatePermissions: (userId, permissions) => 
    axios.put(`/modern-edi/api/v1/admin/users/${userId}/permissions`, permissions),
  
  getActivityLogs: (params) => 
    axios.get('/modern-edi/api/v1/admin/activity-logs', { params }),
  
  exportActivityLogs: () => 
    axios.get('/modern-edi/api/v1/admin/activity-logs/export', { responseType: 'blob' }),
};

// Partner Portal Endpoints
export const partnerPortalAPI = {
  login: (username, password) => 
    axios.post('/modern-edi/api/v1/partner-portal/auth/login', { username, password }),
  
  logout: () => 
    axios.post('/modern-edi/api/v1/partner-portal/auth/logout'),
  
  getMe: () => 
    axios.get('/modern-edi/api/v1/partner-portal/auth/me'),
  
  changePassword: (currentPassword, newPassword) => 
    axios.post('/modern-edi/api/v1/partner-portal/auth/change-password', { 
      current_password: currentPassword, 
      new_password: newPassword 
    }),
  
  getDashboardMetrics: (days = 30) => 
    axios.get(`/modern-edi/api/v1/partner-portal/dashboard/metrics?days=${days}`),
  
  getTransactions: (params) => 
    axios.get('/modern-edi/api/v1/partner-portal/transactions', { params }),
  
  getTransaction: (id) => 
    axios.get(`/modern-edi/api/v1/partner-portal/transactions/${id}`),
  
  uploadFile: (formData) => 
    axios.post('/modern-edi/api/v1/partner-portal/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  
  getFiles: () => 
    axios.get('/modern-edi/api/v1/partner-portal/files/download'),
  
  downloadFile: (id) => 
    axios.get(`/modern-edi/api/v1/partner-portal/files/download/${id}`, { responseType: 'blob' }),
  
  bulkDownload: (transactionIds) => 
    axios.post('/modern-edi/api/v1/partner-portal/files/download/bulk', 
      { transaction_ids: transactionIds }, 
      { responseType: 'blob' }
    ),
  
  getSettings: () => 
    axios.get('/modern-edi/api/v1/partner-portal/settings'),
  
  updateContact: (data) => 
    axios.put('/modern-edi/api/v1/partner-portal/settings/contact', data),
};
```

## Route Configuration

### Update App.jsx

```javascript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Existing imports
import Dashboard from './pages/Dashboard';
import FolderView from './pages/FolderView';

// NEW: Admin imports
import AdminLayout from './components/AdminLayout';
import AdminDashboard from './pages/admin/AdminDashboard';
import PartnerManagement from './pages/admin/PartnerManagement';
import UserManagement from './pages/admin/UserManagement';
import Analytics from './pages/admin/Analytics';
import ActivityLog from './pages/admin/ActivityLog';

// NEW: Partner Portal imports
import PartnerPortalLayout from './components/PartnerPortalLayout';
import PartnerLogin from './pages/partner-portal/PartnerLogin';
import PartnerDashboard from './pages/partner-portal/PartnerDashboard';
import PartnerTransactions from './pages/partner-portal/PartnerTransactions';
import PartnerUpload from './pages/partner-portal/PartnerUpload';
import PartnerDownload from './pages/partner-portal/PartnerDownload';
import PartnerSettings from './pages/partner-portal/PartnerSettings';

function App() {
  return (
    <BrowserRouter basename="/modern-edi">
      <Routes>
        {/* Existing Modern EDI routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="folder/:name" element={<FolderView />} />
        </Route>

        {/* NEW: Admin Dashboard routes */}
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<AdminDashboard />} />
          <Route path="partners" element={<PartnerManagement />} />
          <Route path="users" element={<UserManagement />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="activity" element={<ActivityLog />} />
        </Route>

        {/* NEW: Partner Portal routes */}
        <Route path="/partner-portal/login" element={<PartnerLogin />} />
        <Route path="/partner-portal" element={<PartnerPortalLayout />}>
          <Route index element={<PartnerDashboard />} />
          <Route path="transactions" element={<PartnerTransactions />} />
          <Route path="upload" element={<PartnerUpload />} />
          <Route path="download" element={<PartnerDownload />} />
          <Route path="settings" element={<PartnerSettings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

## Component Templates

### Example: AdminDashboard.jsx

```javascript
import { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import MetricCard from '../../components/admin/MetricCard';
import ChartWidget from '../../components/admin/ChartWidget';

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [charts, setCharts] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [metricsRes, chartsRes] = await Promise.all([
        adminAPI.getDashboardMetrics(30),
        adminAPI.getDashboardCharts(30)
      ]);
      setMetrics(metricsRes.data.metrics);
      setCharts(chartsRes.data.charts);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
      
      {/* Metrics Cards */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <MetricCard 
          title="Total Partners" 
          value={metrics.total_partners} 
          icon="users"
        />
        <MetricCard 
          title="Total Transactions" 
          value={metrics.total_transactions} 
          icon="file"
        />
        <MetricCard 
          title="Success Rate" 
          value={`${metrics.success_rate}%`} 
          icon="check"
        />
        <MetricCard 
          title="Error Rate" 
          value={`${metrics.error_rate}%`} 
          icon="alert"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-2 gap-6">
        <ChartWidget 
          title="Transaction Volume" 
          data={charts.transaction_volume} 
          type="line"
        />
        <ChartWidget 
          title="Top Partners" 
          data={charts.top_partners} 
          type="bar"
        />
      </div>
    </div>
  );
}
```

### Example: PartnerLogin.jsx

```javascript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { partnerPortalAPI } from '../../services/api';

export default function PartnerLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await partnerPortalAPI.login(username, password);
      if (response.data.success) {
        navigate('/partner-portal');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">Partner Portal Login</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="mt-4 text-center">
          <a href="#" className="text-blue-600 hover:underline text-sm">
            Forgot Password?
          </a>
        </div>
      </div>
    </div>
  );
}
```

## Next Steps

1. **Start with API Integration** - Update `services/api.js` first
2. **Create Layouts** - Build AdminLayout and PartnerPortalLayout
3. **Implement Authentication** - PartnerLogin and auth hooks
4. **Build Core Pages** - Start with dashboards, then add features
5. **Add Components** - Create reusable components as needed
6. **Test Integration** - Verify all API calls work with backend

## Notes

- Reuse existing components from Modern EDI where possible
- Follow the same Tailwind CSS styling patterns
- Use React Query or similar for data fetching
- Implement proper error handling and loading states
- Add route guards to protect authenticated routes
- Consider responsive design for mobile devices

## Estimated Effort

- **API Integration:** 2-4 hours
- **Layouts & Auth:** 4-6 hours
- **Admin Dashboard:** 8-12 hours
- **Partner Portal:** 8-12 hours
- **Components:** 6-8 hours
- **Testing & Polish:** 4-6 hours

**Total:** 32-48 hours of development time

The backend is ready and waiting. Frontend implementation can proceed independently!
