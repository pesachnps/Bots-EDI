# 🚀 Start Admin Dashboard - Step by Step

## Quick Start (2 Terminals)

### Terminal 1: Start Backend

```powershell
# Open PowerShell or Command Prompt
cd C:\Users\USER\Projects\bots\env\default

# Start the Bots webserver
python -c "import sys; sys.path.insert(0, '.'); import bots.botsinit; bots.botsinit.generalinit(); from bots import webserver; webserver.run()"
```

**Backend will run on:** `http://localhost:8080`

### Terminal 2: Start Frontend

```powershell
# Open a NEW PowerShell or Command Prompt
cd C:\Users\USER\Projects\bots\env\default\usersys\static\modern-edi

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Frontend will run on:** `http://localhost:3000`

---

## 🔐 How to Access

### Step 1: Login to Django Admin
1. Open browser: `http://localhost:8080/admin`
2. **Username:** `edi_admin`
3. **Password:** `Bots@2025!EDI`
4. Click "Log in"

### Step 2: Access Admin Dashboard
Once logged in to Django admin, open a new tab:
- **Admin Dashboard:** `http://localhost:3000/admin`

You'll be automatically authenticated!

---

## 📊 Available Pages

Once you're at `http://localhost:3000/admin`, you can access:

1. **Dashboard** - `/admin` - Overview and metrics
2. **Partners** - `/admin/partners` - Manage trading partners
3. **Users** - `/admin/users` - Create and manage users
4. **Permissions** - `/admin/permissions` - Permission matrix
5. **Analytics** - `/admin/analytics` - Reports and charts
6. **Activity Logs** - `/admin/activity-logs` - Audit trail

---

## 🛠️ Troubleshooting

### Backend Won't Start
If you get path errors, try:
```powershell
cd C:\Users\USER\Projects\bots\env\default
python -c "import bots.botsinit; bots.botsinit.generalinit(); from bots import webserver; webserver.run()"
```

### Frontend Won't Start
```powershell
# Clear and reinstall
cd C:\Users\USER\Projects\bots\env\default\usersys\static\modern-edi
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
npm run dev
```

### Can't Login
- Make sure backend is running on port 8080
- Try: `http://localhost:8080/admin` first
- Default credentials: `edi_admin` / `Bots@2025!EDI`

### Port Already in Use
If port 3000 is busy, edit `vite.config.js`:
```javascript
server: {
  port: 3001,  // Change to any available port
  // ...
}
```

---

## ✅ Quick Test

1. **Backend running?** Visit `http://localhost:8080/admin`
2. **Frontend running?** Visit `http://localhost:3000`
3. **Can login?** Use `edi_admin` / `Bots@2025!EDI`
4. **Dashboard loads?** Visit `http://localhost:3000/admin`

---

## 🎯 What You Can Do

### Dashboard
- View system metrics
- Monitor transaction success rates
- See top partners
- Track recent errors

### Partner Management
- Search and filter partners
- View partner analytics
- Access partner users

### User Management
- ✅ Create new users
- ✅ Edit user information
- ✅ Reset passwords
- ✅ Delete users
- ✅ Activate/deactivate accounts

### Permissions
- View permission matrix
- Toggle permissions with one click
- Manage access control

### Activity Logs
- Search all system activity
- Filter by user type and action
- Export logs to CSV

### Analytics
- View transaction trends
- Compare partner performance
- Analyze document types

---

## 📱 Mobile Testing

The dashboard is fully responsive! Test on:
- Mobile: Resize browser to 375px width
- Tablet: Resize to 768px width
- Desktop: Full width

All tables scroll, modals fit, buttons are touch-friendly!

---

## 🆘 Need Help?

- **Backend Issues:** Check `docs/BACKEND_OPERATIONS_GUIDE.md`
- **Frontend Issues:** Check `docs/FRONTEND_BUILD_GUIDE.md`
- **API Reference:** Check `docs/ADMIN_PARTNER_API_DOCUMENTATION.md`

---

**Ready to go!** Open two terminals and follow the steps above. 🚀
