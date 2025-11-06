# Admin Dashboard Quick Start Guide

## Prerequisites

1. **Backend Setup Complete**
   - Database migrations run
   - Django admin user created
   - Bots server running

2. **Node.js Installed**
   - Node.js 18+ required
   - npm included

## Step 1: Install Dependencies

```bash
cd env/default/usersys/static/modern-edi
npm install
```

## Step 2: Build the Frontend

### For Development (with hot reload):
```bash
npm run dev
```
This starts the development server at `http://localhost:3000`

### For Production:
```bash
npm run build
```
This creates optimized files in the `dist/` directory

## Step 3: Start the Backend

In a separate terminal:

```bash
cd env/default
bots-webserver
```

The server runs at `http://localhost:8080`

## Step 4: Access the Admin Dashboard

### Option 1: Development Mode
If running `npm run dev`:
- Open `http://localhost:3000/admin`
- The Vite dev server will proxy API calls to Django

### Option 2: Production Mode
If you built with `npm run build`:
1. Collect static files:
   ```bash
   cd env/default
   python manage.py collectstatic --noinput
   ```

2. Access at `http://localhost:8080/modern-edi/admin/`

## Step 5: Login

1. First, login to Django Admin:
   - Go to `http://localhost:8080/admin`
   - Username: `edi_admin`
   - Password: `Bots@2025!EDI`

2. Then access Admin Dashboard:
   - Go to `http://localhost:8080/modern-edi/admin/`
   - Your Django session will authenticate you

## Current Status

### ✅ Completed Components
- **AdminLayout** - Sidebar navigation
- **AdminDashboard** - Main dashboard with metrics
- **API Service** - Complete API integration (`adminApi.js`)

### 📋 Components with Placeholders
These pages exist but need full implementation:
- **PartnerManagement** - Partner list and management
- **UserManagement** - User administration
- **PermissionsManagement** - Permission matrix
- **Analytics** - Charts and reports
- **ActivityLog** - Activity log viewer

## Quick Test

Test the backend API directly:

```bash
# Login to Django admin first, then:
curl http://localhost:8080/modern-edi/api/v1/admin/dashboard/metrics \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  --cookie-jar cookies.txt
```

## Troubleshooting

### "Cannot GET /admin"
- Make sure you're accessing `/modern-edi/admin/` (with the prefix)
- Or use the dev server at `http://localhost:3000/admin`

### API Calls Failing
- Ensure you're logged into Django admin first
- Check that bots-webserver is running
- Verify the session cookie is being sent

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors in Development
The vite.config.js should have proxy configured:
```javascript
server: {
  proxy: {
    '/modern-edi/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
    },
  },
}
```

## Next Steps

1. **Test the Dashboard**
   - View metrics
   - Check system status
   - Navigate between pages

2. **Implement Remaining Pages**
   - Partner Management (full CRUD)
   - User Management (create/edit users)
   - Analytics (charts with Recharts)
   - Activity Logs (search and export)

3. **Build Partner Portal**
   - Similar process for partner-facing pages
   - Separate authentication flow

## Development Workflow

```bash
# Terminal 1: Backend
cd env/default
bots-webserver

# Terminal 2: Frontend
cd env/default/usersys/static/modern-edi
npm run dev

# Access at http://localhost:3000/admin
```

## Production Deployment

```bash
# 1. Build frontend
cd env/default/usersys/static/modern-edi
npm run build

# 2. Collect static files
cd env/default
python manage.py collectstatic --noinput

# 3. Start server
bots-webserver

# Access at http://localhost:8080/modern-edi/admin/
```

## Files Created

- `src/services/adminApi.js` - Admin API service
- `src/pages/admin/AdminDashboard.jsx` - Updated with real API calls
- `src/pages/admin/AdminLayout.jsx` - Sidebar navigation
- `src/pages/admin/*.jsx` - Other admin pages (placeholders)

## API Endpoints Available

- `GET /modern-edi/api/v1/admin/dashboard/metrics` - Dashboard metrics
- `GET /modern-edi/api/v1/admin/dashboard/charts` - Chart data
- `GET /modern-edi/api/v1/admin/partners/` - List partners
- `GET /modern-edi/api/v1/admin/partners/<id>/analytics` - Partner analytics
- `GET /modern-edi/api/v1/admin/activity-logs` - Activity logs
- And 20+ more endpoints...

See `docs/ADMIN_PARTNER_API_DOCUMENTATION.md` for complete API reference.

## Support

- **Backend Issues**: Check `docs/BACKEND_OPERATIONS_GUIDE.md`
- **Frontend Issues**: Check `docs/FRONTEND_BUILD_GUIDE.md`
- **API Reference**: Check `docs/ADMIN_PARTNER_API_DOCUMENTATION.md`

---

**Status**: Admin Dashboard frontend is functional with real API integration. Additional pages can be implemented as needed.
