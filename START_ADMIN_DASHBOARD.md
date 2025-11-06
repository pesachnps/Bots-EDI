# Start Admin Dashboard - Simple Guide

## Quick Start (2 Steps)

### Step 1: Start Backend
```bash
cd env/default
bots-webserver
```
Leave this running in Terminal 1.

### Step 2: Start Frontend
Open a new terminal:
```bash
cd env/default/usersys/static/modern-edi
npm install
npm run dev
```

**Access at: http://localhost:3000/admin**

## Login

1. **First**: Login to Django Admin
   - Go to: `http://localhost:8080/admin`
   - Username: `edi_admin`
   - Password: `Bots@2025!EDI`

2. **Then**: Open Admin Dashboard
   - Go to: `http://localhost:3000/admin`
   - You'll be automatically authenticated

## What You'll See

✅ **Dashboard with real data:**
- Total partners count
- Total transactions count
- Success/error rates
- System health status
- Top 10 partners
- Recent errors
- Auto-refresh every 60 seconds

## Ports

- **Backend (Django)**: Port 8080
- **Frontend (Vite Dev Server)**: Port 3000
- **Production**: Port 8080 (after building)

## If Port 3000 is Also Busy

Edit `env/default/usersys/static/modern-edi/vite.config.js`:

```javascript
server: {
  port: 3001,  // Change to any available port
  proxy: {
    '/modern-edi/api': {
      target: 'http://localhost:8080',
      changeOrigin: true,
    }
  }
}
```

Then access at `http://localhost:3001/admin`

## Troubleshooting

### "Loading..." Forever
- Make sure bots-webserver is running (Terminal 1)
- Make sure you logged into Django admin first
- Check browser console for errors

### "npm: command not found"
- Install Node.js from https://nodejs.org/
- Restart your terminal after installation

### Port Already in Use
- Change the port in vite.config.js (see above)
- Or stop the other process using that port

## Production Build (Optional)

If you want to build for production instead:

```bash
# Windows
scripts\build_admin_dashboard.bat

# Linux/Mac
chmod +x scripts/build_admin_dashboard.sh
./scripts/build_admin_dashboard.sh
```

Then access at: `http://localhost:8080/modern-edi/admin/`

---

**That's it!** You should now see your Admin Dashboard with live data. 🎉
