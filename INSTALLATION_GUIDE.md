# Bots EDI - Complete Installation Guide

This guide walks you through a fresh installation of Bots EDI with all required setup steps.

## Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning)
- Windows, macOS, or Linux

## Installation Steps

### 1. Install Bots EDI Package

```bash
pip install bots
```

Or install from source if you have the package locally.

### 2. Clone or Download the Project

```bash
git clone https://github.com/YOUR_USERNAME/Bots-EDI.git
cd Bots-EDI
```

### 3. Initialize Database Tables

Bots EDI requires several core tables that must be created before first use:

```bash
python create_missing_tables.py
```

This script creates:
- **`ta`** - Main transaction table (stores all EDI transactions)
- **`uniek`** - Unique counter values (for generating sequential numbers)
- **`persist`** - Persistent data storage
- **`mutex`** - Locking mechanism (prevents concurrent execution conflicts)

**Output:**
```
✅ Created all missing Bots EDI tables successfully

✅ Verified tables:
  ✓ ta
  ✓ persist
  ✓ mutex
  ✓ uniek
```

### 4. Create Admin Users

Create the default admin accounts:

```bash
python create_admin.py
```

This creates two superuser accounts:
- **Primary Account**
  - Username: `edi_admin`
  - Password: `Bots@2025!EDI`
  
- **Development Account**
  - Username: `bots`
  - Password: `bots`

**Output:**
```
Creating users from README...

✅ Superuser 'edi_admin' created successfully!
   Username: edi_admin
   Password: Bots@2025!EDI
   Login at: http://localhost:8080/admin

✅ Superuser 'bots' created successfully!
   Username: bots
   Password: bots
   Login at: http://localhost:8080/admin
```

### 5. Configure PATH (Windows Only)

Add the bots-engine executable to your PATH so the web interface can run it:

**PowerShell:**
```powershell
# Replace YOUR_USERNAME with your actual Windows username
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\YOUR_USERNAME\AppData\Roaming\Python\Python313\Scripts", "User")
```

**To find your username:**
```powershell
echo $env:USERNAME
```

**Verify bots-engine is accessible:**
```powershell
where.exe bots-engine
# Should show: C:\Users\YOUR_USERNAME\AppData\Roaming\Python\Python313\Scripts\bots-engine.exe
```

### 6. Start the Backend Server

#### Option A: Using the provided script (Windows)
```powershell
.\start_backend.ps1
```

#### Option B: Manual start
```bash
cd env/default
python -m bots.webserver -cC:\Users\YOUR_USERNAME\Projects\bots\env\default\config
```

**Expected output:**
```
Starting backend server...
Backend will be available at: http://localhost:8080
Django Admin: http://localhost:8080/admin

2025.11.07 10:57:36 STARTINFO [__main__] Starting ...
2025.11.07 10:58:20 STARTINFO [__main__] Serving at port: "8080".
```

### 7. Access the Web Interface

Open your browser and navigate to:
- **Main Interface:** http://localhost:8080
- **Django Admin:** http://localhost:8080/admin

Login with:
- Username: `edi_admin`
- Password: `Bots@2025!EDI`

## Verification Checklist

After installation, verify everything works:

- [ ] Database tables created (run `python list_tables.py` to verify)
- [ ] Admin users can login at http://localhost:8080/admin
- [ ] No 500 errors on these pages:
  - [ ] http://localhost:8080/admin/bots/uniek/
  - [ ] http://localhost:8080/bots/document/?allstatus=True
  - [ ] http://localhost:8080/run/
- [ ] Backend server starts without errors
- [ ] Can access configuration pages

## Troubleshooting

### Database Tables Missing

**Symptom:** Error 500 with "no such table: ta" or "no such table: uniek"

**Solution:**
```bash
python create_missing_tables.py
```

### Cannot Login

**Symptom:** "Please enter a correct username and password"

**Solution:**
```bash
# Recreate admin users
python create_admin.py
```

**Note:** If users already exist, delete them first:
```python
python -c "import sqlite3; conn = sqlite3.connect(r'env\botssys\sqlitedb\botsdb'); cursor = conn.cursor(); cursor.execute('DELETE FROM auth_user'); conn.commit(); conn.close()"
```

Then run `create_admin.py` again.

### Bots-Engine Not Found

**Symptom:** "Errors while trying to run bots-engine: [WinError 2] The system cannot find the file specified"

**Solution (Windows):**
```powershell
# Add to PATH
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\YOUR_USERNAME\AppData\Roaming\Python\Python313\Scripts", "User")

# Restart PowerShell or terminal
# Restart the backend server
```

**Verify:**
```powershell
where.exe bots-engine
```

### Port 8080 Already in Use

**Check what's using the port:**
```powershell
# Windows
Get-NetTCPConnection -LocalPort 8080

# Linux/Mac
lsof -i :8080
```

**Solution:** Either:
1. Stop the process using port 8080
2. Or change the port in `env/default/config/bots.ini`:
   ```ini
   [webserver]
   port = 8081
   ```

## Post-Installation Steps

### 1. Change Default Passwords

For security, change the default passwords immediately:

```bash
cd env/default
python manage_users.py reset edi_admin YourNewSecurePassword123!
```

### 2. Configure Environment

Edit configuration files as needed:
- `env/default/config/settings.py` - Django settings
- `env/default/config/bots.ini` - Bots configuration

### 3. Set Up Your First Route

1. Create grammars in `env/default/usersys/grammars/`
2. Create mappings in `env/default/usersys/mappings/`
3. Configure partners and routes in the web interface

## Quick Reference

### Important Files

```
bots/
├── create_admin.py              # Creates admin users
├── create_missing_tables.py     # Creates database tables
├── create_uniek_table.py        # Creates uniek table (if needed separately)
├── list_tables.py               # Lists all database tables
├── start_backend.ps1            # Windows backend startup script
└── env/
    └── default/
        ├── config/
        │   ├── bots.ini         # Bots configuration
        │   └── settings.py      # Django settings
        └── botssys/
            └── sqlitedb/
                └── botsdb       # SQLite database file
```

### Important Commands

```bash
# List database tables
python list_tables.py

# Create missing tables
python create_missing_tables.py

# Create admin users
python create_admin.py

# Start backend (Windows)
.\start_backend.ps1

# Start backend (Linux/Mac)
cd env/default
python -m bots.webserver
```

## Support

- **Documentation:** See `docs/` folder
- **README:** See `README.md` for features and capabilities
- **Getting Started:** See `docs/GETTING_STARTED.md`
- **Issues:** Check existing issues or create new ones on GitHub

## Next Steps

After successful installation:

1. Read the [Getting Started Guide](docs/GETTING_STARTED.md)
2. Review the [Quick Reference](docs/QUICK_REFERENCE.md)
3. Explore the [API Documentation](docs/API_DOCUMENTATION.md)
4. Set up your first EDI translation route

---

**Installation Complete!** 🎉

You now have a fully functional Bots EDI system ready for EDI message translation and processing.
