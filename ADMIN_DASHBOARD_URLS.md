# Admin Dashboard Access URLs - Reference Guide

## ✅ Correct Access URLs

### Production (After `npm run build`)
- **Admin Dashboard**: http://localhost:8080/modern-edi/admin/
- **Partner Portal**: http://localhost:8080/modern-edi/partner-portal/
- **Modern EDI Interface**: http://localhost:8080/modern-edi/

### Development (`npm run dev`)
- **Admin Dashboard**: http://localhost:3000/admin/
- **Partner Portal**: http://localhost:3000/partner-portal/
- **Modern EDI Interface**: http://localhost:3000/

## ⚠️ Common Mistake

**DO NOT use**: `http://localhost:8080/static/modern-edi/`

The `/static/` prefix is only used internally by Vite for build configuration (`base: '/static/modern-edi/'` in `vite.config.js`). It's NOT part of the actual URL path for accessing the application.

## 📐 Technical Explanation

### Vite Configuration
```javascript
// vite.config.js
export default defineConfig({
  base: '/static/modern-edi/',  // ⚠️ This is for ASSET PATHS, not URLs
  // ...
})
```

This `base` setting tells Vite where to look for JavaScript/CSS assets in production builds. It does NOT determine the URL where the app is served.

### React Router Configuration
```javascript
// main.jsx
<BrowserRouter basename="/modern-edi">  // ✅ This is the actual URL path
  <App />
</BrowserRouter>
```

The `basename` prop tells React Router what the base URL path is for the application.

## 🔗 Complete URL Structure

### Admin Dashboard Pages
- Dashboard: `/modern-edi/admin/`
- Partners: `/modern-edi/admin/partners`
- Users: `/modern-edi/admin/users`
- Permissions: `/modern-edi/admin/permissions`
- Analytics: `/modern-edi/admin/analytics`
- Activity Logs: `/modern-edi/admin/activity-logs`

### API Endpoints
- Admin API: `/modern-edi/api/v1/admin/`
- Partner API: `/api/v1/partner/`
- Modern EDI API: `/modern-edi/api/v1/`

## 🚀 Quick Start Commands

### Build and Access (Production)
```bash
cd env/default/usersys/static/modern-edi
npm run build
cd ../../..
bots-webserver

# Then open: http://localhost:8080/modern-edi/admin/
```

### Development Mode
```bash
# Terminal 1: Backend
cd env/default
bots-webserver

# Terminal 2: Frontend
cd env/default/usersys/static/modern-edi
npm run dev

# Then open: http://localhost:3000/admin/
```

## 📝 Summary

- **Production URL**: Use `/modern-edi/` prefix (port 8080)
- **Development URL**: No prefix needed (port 3000)
- **Never use**: `/static/modern-edi/` as a URL path

---

**Last Updated**: November 7, 2025  
**Issue Fixed**: Sidebar visibility - BrowserRouter basename mismatch
