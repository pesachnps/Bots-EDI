# Starting the Servers

This project uses two servers that must be running simultaneously:

## Port Configuration

- **Backend (Django/Bots)**: Port 8080
- **Frontend (React/Vite)**: Port 3000

These ports are configured in:
- Backend: `env/default/config/bots.ini` (webserver port = 8080)
- Frontend: `env/default/usersys/static/modern-edi/vite.config.js` (server port = 3000)

## Quick Start

### Windows

1. **Start Backend** (in one terminal):
   ```bash
   start_backend.bat
   ```
   Or manually:
   ```bash
   cd env\default
   python start_server.py
   ```

2. **Start Frontend** (in another terminal):
   ```bash
   start_frontend.bat
   ```
   Or manually:
   ```bash
   cd env\default\usersys\static\modern-edi
   npm run dev
   ```

### Linux/Mac

1. **Start Backend** (in one terminal):
   ```bash
   ./start_backend.sh
   ```
   Or manually:
   ```bash
   cd env/default
   python start_server.py
   ```

2. **Start Frontend** (in another terminal):
   ```bash
   ./start_frontend.sh
   ```
   Or manually:
   ```bash
   cd env/default/usersys/static/modern-edi
   npm run dev
   ```

## Access URLs

Once both servers are running:

- **Frontend Application**: http://localhost:3000/static/modern-edi/
- **Backend API**: http://localhost:8080/modern-edi/api/v1/
- **Admin Dashboard API**: http://localhost:8080/modern-edi/api/v1/admin/
- **Partner Portal API**: http://localhost:8080/api/v1/partner/
- **Django Admin**: http://localhost:8080/admin/

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

**Windows:**
```powershell
# Find process using port 8080
Get-NetTCPConnection -LocalPort 8080 | Select-Object OwningProcess

# Kill the process
Stop-Process -Id <ProcessId> -Force

# Or for port 3000
Get-NetTCPConnection -LocalPort 3000 | Select-Object OwningProcess
Stop-Process -Id <ProcessId> -Force
```

**Linux/Mac:**
```bash
# Find and kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Or for port 3000
lsof -ti:3000 | xargs kill -9
```

### Backend Won't Start

If the backend fails with a config directory error, ensure:
1. The `BOTS_CONFIG_DIR` environment variable is set correctly
2. The `start_server.py` script is being used (it sets this automatically)

### Frontend Can't Connect to Backend

1. Verify backend is running on port 8080
2. Check the proxy configuration in `vite.config.js`
3. Ensure CORS is properly configured in Django settings

## Development vs Production

### Development (Current Setup)
- Frontend runs on Vite dev server (port 3000)
- Hot module replacement enabled
- Proxies API requests to backend

### Production
- Frontend is built and served as static files from Django (port 8080)
- Single server serves both frontend and backend
- Build frontend with: `npm run build`
- Static files served from: `/static/modern-edi/`

## Stopping the Servers

Press `Ctrl+C` in each terminal window to stop the servers gracefully.

Or force kill:
```bash
# Windows
Stop-Process -Name python -Force
Stop-Process -Name node -Force

# Linux/Mac
pkill -f "python start_server.py"
pkill -f "npm run dev"
```
