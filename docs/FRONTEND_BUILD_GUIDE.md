# Frontend Build and Deployment Guide

## Overview

This guide covers building and deploying the React frontend for the Modern EDI Interface, Admin Dashboard, and Partner Portal.

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend)
- All backend components installed and configured

## Installation

### 1. Install Frontend Dependencies

```bash
cd env/default/usersys/static/modern-edi
npm install
```

This will install:
- React 18.2
- React Router DOM 6.20
- Heroicons (for icons)
- Recharts & Chart.js (for charts)
- Tailwind CSS (for styling)
- Vite (build tool)
- And other dependencies

### 2. Verify Installation

```bash
npm list
```

Check that all packages installed successfully.

## Development

### Start Development Server

```bash
cd env/default/usersys/static/modern-edi
npm run dev
```

This starts the Vite development server at `http://localhost:5173`

**Note:** In development, you'll need the Django backend running simultaneously:

```bash
# In another terminal
cd env/default
bots-webserver
```

### Development Features

- Hot Module Replacement (HMR) - changes reflect instantly
- Fast refresh for React components
- Source maps for debugging
- Proxy to backend API (configured in vite.config.js)

## Building for Production

### 1. Build the Frontend

```bash
cd env/default/usersys/static/modern-edi
npm run build
```

This creates optimized production files in the `dist/` directory:
- Minified JavaScript bundles
- Optimized CSS
- Compressed assets
- Source maps (optional)

### 2. Preview Production Build

```bash
npm run preview
```

This serves the production build locally for testing.

## Deployment

### Option 1: Django Static Files (Recommended)

#### Step 1: Configure Django Static Files

Ensure `env/default/config/settings.py` has:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'usersys', 'static', 'modern-edi', 'dist'),
]
```

#### Step 2: Build Frontend

```bash
cd env/default/usersys/static/modern-edi
npm run build
```

#### Step 3: Collect Static Files

```bash
cd env/default
python manage.py collectstatic --noinput
```

#### Step 4: Configure URL Routing

The Django URLs should already be configured to serve the React app:

```python
# In urls.py
from django.views.generic import TemplateView

urlpatterns = [
    # ... other patterns ...
    re_path(r'^modern-edi/.*', TemplateView.as_view(template_name='modern-edi/index.html')),
]
```

#### Step 5: Start Server

```bash
cd env/default
bots-webserver
```

Access the applications:
- Modern EDI: `http://localhost:8080/modern-edi/`
- Admin Dashboard: `http://localhost:8080/modern-edi/admin/`
- Partner Portal: `http://localhost:8080/modern-edi/partner-portal/`

### Option 2: Separate Web Server (Advanced)

For high-traffic deployments, serve the React app from a separate web server (Nginx, Apache).

#### Step 1: Build Frontend

```bash
cd env/default/usersys/static/modern-edi
npm run build
```

#### Step 2: Copy Build to Web Server

```bash
cp -r dist/* /var/www/edi-frontend/
```

#### Step 3: Configure Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Serve React app
    location / {
        root /var/www/edi-frontend;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to Django
    location /modern-edi/api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /admin/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Environment Configuration

### Vite Configuration

The `vite.config.js` should be configured for your environment:

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/modern-edi/',  // Base path for assets
  server: {
    proxy: {
      '/modern-edi/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
      '/admin': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,  // Set to true for debugging
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts', 'chart.js', 'react-chartjs-2'],
        },
      },
    },
  },
});
```

## Troubleshooting

### Build Errors

**Error: Module not found**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: Out of memory**
```bash
# Increase Node memory
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### Runtime Errors

**404 on page refresh**
- Ensure Django catch-all route is configured
- Check that `index.html` is being served for all routes

**API calls failing**
- Verify backend is running
- Check CORS settings in Django
- Verify API endpoints are correct

**Blank page after deployment**
- Check browser console for errors
- Verify `base` path in vite.config.js matches deployment path
- Check that static files were collected correctly

### Performance Issues

**Slow initial load**
- Enable code splitting in vite.config.js
- Use lazy loading for routes
- Optimize images and assets

**Large bundle size**
- Analyze bundle with `npm run build -- --analyze`
- Remove unused dependencies
- Use dynamic imports for large libraries

## Optimization

### Code Splitting

Implement lazy loading for routes:

```javascript
import { lazy, Suspense } from 'react';

const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Suspense>
  );
}
```

### Asset Optimization

```bash
# Optimize images before building
npm install -D vite-plugin-imagemin
```

### Caching Strategy

Configure cache headers in your web server:

```nginx
location /modern-edi/assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Testing

### Unit Tests

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
npm run test
```

### E2E Tests

```bash
npm install -D playwright
npx playwright test
```

### Build Verification

After building, verify:

1. All routes load correctly
2. API calls work
3. Authentication flows work
4. File uploads/downloads work
5. Charts render correctly
6. Mobile responsiveness

## Continuous Integration

### GitHub Actions Example

```yaml
name: Build Frontend

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd env/default/usersys/static/modern-edi && npm ci
      - run: cd env/default/usersys/static/modern-edi && npm run build
      - run: cd env/default && python manage.py collectstatic --noinput
```

## Monitoring

### Performance Monitoring

Add performance monitoring:

```javascript
// In main.jsx
import { reportWebVitals } from './reportWebVitals';

reportWebVitals(console.log);
```

### Error Tracking

Integrate error tracking (e.g., Sentry):

```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-dsn",
  environment: "production",
});
```

## Maintenance

### Updating Dependencies

```bash
# Check for updates
npm outdated

# Update all dependencies
npm update

# Update specific package
npm install react@latest
```

### Security Audits

```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix
```

## Checklist

### Pre-Deployment

- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Backend API running and accessible
- [ ] Build completes without errors
- [ ] All routes tested
- [ ] Authentication flows tested
- [ ] API integration tested
- [ ] Mobile responsiveness verified
- [ ] Browser compatibility checked
- [ ] Performance optimized

### Post-Deployment

- [ ] All routes accessible
- [ ] Static files serving correctly
- [ ] API calls working
- [ ] Authentication working
- [ ] File uploads/downloads working
- [ ] Charts rendering
- [ ] No console errors
- [ ] Performance acceptable
- [ ] Monitoring configured
- [ ] Backups configured

## Support

For issues:
- Check browser console for errors
- Review Django logs
- Check network tab for failed requests
- Verify static files are collected
- Test API endpoints directly

## Additional Resources

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Recharts Documentation](https://recharts.org/)
- [Django Static Files](https://docs.djangoproject.com/en/stable/howto/static-files/)
