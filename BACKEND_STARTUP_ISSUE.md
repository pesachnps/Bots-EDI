# Backend Startup Issue

## Problem
The backend server fails to start with the error:
```
PanicError: Initilisation: settings file imported "C:\Users\PGelfand\Projects\bots\env\default\config\settings.py" 
not in BOTS_CONFIG_DIR: "C:\Users\PGelfand\.bots\env\default\config"
```

## Root Cause
The bots EDI system has a dual-directory structure:
- **Project directory**: `C:\Users\PGelfand\Projects\bots\env\default\`
- **Config directory**: `C:\Users\PGelfand\.bots\env\default\`

The bots initialization expects the settings.py to be imported from the BOTS_CONFIG_DIR (`.bots`), but Python is importing it from the project directory.

## Immediate Workaround

### Option 1: Start from .bots directory
```bash
cd C:\Users\PGelfand\.bots\env\default
python -c "import sys; sys.path.insert(0, '.'); import bots.botsinit; bots.botsinit.generalinit(); from bots import webserver; webserver.run()"
```

### Option 2: Copy all files to .bots
```bash
# Copy all usersys files
xcopy /E /Y "C:\Users\PGelfand\Projects\bots\env\default\usersys\*" "C:\Users\PGelfand\.bots\env\default\usersys\"

# Copy config files
copy /Y "C:\Users\PGelfand\Projects\bots\env\default\config\*" "C:\Users\PGelfand\.bots\env\default\config\"
```

### Option 3: Set PYTHONPATH
```bash
set PYTHONPATH=C:\Users\PGelfand\.bots\env\default
cd C:\Users\PGelfand\Projects\bots\env\default
python -c "import sys; sys.path.insert(0, '.'); import bots.botsinit; bots.botsinit.generalinit(); from bots import webserver; webserver.run()"
```

## URL Routing Fix Applied
The following files have been created/updated to register custom URLs:
- `env/default/usersys/url_extensions.py` - URL registration function
- `env/default/usersys/apps.py` - Calls URL registration on app ready
- `env/default/usersys/modern_edi_urls.py` - Modern EDI endpoints
- `env/default/usersys/admin_urls.py` - Admin dashboard endpoints  
- `env/default/usersys/partner_portal_urls.py` - Partner portal endpoints

These files have been copied to `C:\Users\PGelfand\.bots\env\default\usersys\`.

## Testing After Fix
Once the backend starts successfully, test the endpoints:

```bash
# Test folders endpoint
curl http://localhost:8080/modern-edi/api/v1/folders/

# Test admin dashboard
curl http://localhost:8080/modern-edi/api/v1/admin/dashboard/metrics

# Test partner portal
curl http://localhost:8080/api/v1/partner/auth/me
```

## Next Steps
1. Try starting the backend from the `.bots` directory
2. If successful, test the frontend to confirm the "Failed to load folders" error is resolved
3. If the issue persists, we may need to modify the bots initialization to handle the dual-directory structure
