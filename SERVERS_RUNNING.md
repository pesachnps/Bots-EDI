# Server Configuration

## Port Configuration (Fixed)

The application uses these ports consistently across all environments:

### Backend Server
- **Port**: 8080 (configured in `env/default/config/bots.ini`)
- **URL**: http://localhost:8080
- **Start Command**: 
  - Windows: `start_backend.bat`
  - Linux/Mac: `./start_backend.sh`
  - Manual: `cd env/default && python start_server.py`
- **Directory**: `env/default`

### Frontend Server  
- **Port**: 3000 (configured in `env/default/usersys/static/modern-edi/vite.config.js`)
- **URL**: http://localhost:3000/static/modern-edi/
- **Start Command**:
  - Windows: `start_frontend.bat`
  - Linux/Mac: `./start_frontend.sh`
  - Manual: `cd env/default/usersys/static/modern-edi && npm run dev`
- **Directory**: `env/default/usersys/static/modern-edi`

## Current Status

Check if servers are running:

**Windows:**
```powershell
Get-NetTCPConnection -LocalPort 8080,3000 -ErrorAction SilentlyContinue
```

**Linux/Mac:**
```bash
lsof -i :8080,3000
```

## URL Routing Fix Applied

The custom URLs have been registered:
- ✅ Modern EDI Interface: `/modern-edi/api/v1/`
- ✅ Admin Dashboard: `/modern-edi/api/v1/admin/`
- ✅ Partner Portal: `/api/v1/partner/`

## Testing

### Test the folders endpoint (requires login):
```bash
curl http://localhost:8080/modern-edi/api/v1/folders/
```

### Access the frontend:
Open your browser to: http://localhost:3000/static/modern-edi/

### Access Django admin:
http://localhost:8080/admin/

## Next Steps

1. Open the frontend in your browser
2. Log in with your admin credentials
3. Test the folders view - the "Failed to load folders" error should now be resolved
4. Test the admin dashboard links - they should now work correctly

## Stopping the Servers

To stop the servers, use:
```bash
# Stop backend
Stop-Process -Id 18 -Force

# Stop frontend  
Stop-Process -Id 19 -Force
```

Or use Ctrl+C in the terminal where they're running.
