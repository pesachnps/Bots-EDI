# Port Configuration - Fixed Setup

## Overview

The application now uses fixed ports for consistency across all environments and deployments.

## Port Assignments

| Service | Port | URL | Configuration File |
|---------|------|-----|-------------------|
| Backend (Django/Bots) | **8080** | http://localhost:8080 | `env/default/config/bots.ini` |
| Frontend (React/Vite) | **3000** | http://localhost:3000/static/modern-edi/ | `env/default/usersys/static/modern-edi/vite.config.js` |

## Backend Endpoints (Port 8080)

- **Main Application**: http://localhost:8080
- **Django Admin**: http://localhost:8080/admin
- **Modern EDI API**: http://localhost:8080/modern-edi/api/v1/
  - Folders: `/modern-edi/api/v1/folders/`
  - Transactions: `/modern-edi/api/v1/transactions/`
  - Partners: `/modern-edi/api/v1/partners/`
- **Admin Dashboard API**: http://localhost:8080/modern-edi/api/v1/admin/
  - Metrics: `/modern-edi/api/v1/admin/dashboard/metrics`
  - Partners: `/modern-edi/api/v1/admin/partners`
  - Analytics: `/modern-edi/api/v1/admin/analytics/`
- **Partner Portal API**: http://localhost:8080/api/v1/partner/
  - Auth: `/api/v1/partner/auth/login`
  - Dashboard: `/api/v1/partner/dashboard/metrics`
  - Files: `/api/v1/partner/files/`

## Frontend (Port 3000)

- **Development Server**: http://localhost:3000/static/modern-edi/
- **Features**:
  - Hot module replacement (HMR)
  - Proxies API requests to backend (port 8080)
  - React DevTools support

## Configuration Files

### Backend Port (8080)

**File**: `env/default/config/bots.ini`

```ini
[webserver]
port = 8080
```

### Frontend Port (3000)

**File**: `env/default/usersys/static/modern-edi/vite.config.js`

```javascript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/modern-edi/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      }
    }
  }
})
```

## Startup Scripts

### Windows

- **Backend**: `start_backend.bat`
  - Checks if port 8080 is available
  - Starts backend using `python start_server.py`
  
- **Frontend**: `start_frontend.bat`
  - Checks if port 3000 is available
  - Starts frontend using `npm run dev`

### Linux/Mac

- **Backend**: `start_backend.sh`
  - Checks if port 8080 is available
  - Starts backend using `python start_server.py`
  
- **Frontend**: `start_frontend.sh`
  - Checks if port 3000 is available
  - Starts frontend using `npm run dev`

## URL Routing Fix

The following files ensure custom URLs are properly registered:

1. **`env/default/usersys/url_extensions.py`**
   - Registers custom URL patterns with Django
   - Called automatically when Django app initializes

2. **`env/default/usersys/apps.py`**
   - Updated to call `url_extensions.register_urls()` in `ready()` method

3. **`env/default/start_server.py`**
   - Sets `BOTS_CONFIG_DIR` environment variable
   - Ensures correct config directory is used

## Troubleshooting

### Port Already in Use

**Windows:**
```powershell
# Check what's using the port
Get-NetTCPConnection -LocalPort 8080 | Select-Object OwningProcess
Get-NetTCPConnection -LocalPort 3000 | Select-Object OwningProcess

# Kill the process
Stop-Process -Id <ProcessId> -Force
```

**Linux/Mac:**
```bash
# Check and kill port 8080
lsof -ti:8080 | xargs kill -9

# Check and kill port 3000
lsof -ti:3000 | xargs kill -9
```

### Backend Config Error

If you see: `PanicError: settings file imported ... not in BOTS_CONFIG_DIR`

**Solution**: Use `start_server.py` instead of direct `bots-webserver` command:
```bash
cd env/default
python start_server.py
```

This script sets the correct `BOTS_CONFIG_DIR` environment variable.

### Frontend Can't Connect to Backend

1. Verify backend is running: http://localhost:8080
2. Check proxy configuration in `vite.config.js`
3. Verify CORS settings in Django `settings.py`

## Production Deployment

In production, the frontend is built and served as static files from Django:

```bash
# Build frontend
cd env/default/usersys/static/modern-edi
npm run build

# Start backend only (serves both frontend and API)
cd env/default
python start_server.py
```

Access everything at: http://localhost:8080

## Files Modified

- ✅ `env/default/config/bots.ini` - Backend port (already set to 8080)
- ✅ `env/default/usersys/static/modern-edi/vite.config.js` - Frontend port (already set to 3000)
- ✅ `start_backend.bat` - Updated to use `start_server.py`
- ✅ `start_backend.sh` - Created for Linux/Mac
- ✅ `start_frontend.bat` - Created for Windows
- ✅ `start_frontend.sh` - Created for Linux/Mac
- ✅ `env/default/start_server.py` - Created to set correct config path
- ✅ `env/default/usersys/url_extensions.py` - Created for URL registration
- ✅ `env/default/usersys/apps.py` - Updated to register URLs
- ✅ `README.md` - Added port configuration section
- ✅ `START_SERVERS.md` - Complete startup guide
- ✅ `SERVERS_RUNNING.md` - Updated with fixed port info

## Files Copied to .bots Directory

The following files have been copied to `C:\Users\PGelfand\.bots\env\default\` to ensure they're used:

- `start_server.py`
- `usersys/url_extensions.py`
- `usersys/apps.py`
- `usersys/modern_edi_urls.py`
- `usersys/admin_urls.py`
- `usersys/partner_portal_urls.py`
- All view files and supporting modules

## Verification

Test that everything is working:

```bash
# Test backend
curl http://localhost:8080/modern-edi/api/v1/folders/

# Test frontend
curl http://localhost:3000/static/modern-edi/
```

Both should return valid responses (login page or data).
