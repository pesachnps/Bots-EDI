# Performance Optimization Guide

## Overview

This guide covers performance optimizations for the EDI system, including database, caching, frontend, and infrastructure optimizations.

## Already Implemented ✅

### Database Optimizations
- ✅ Indexes on frequently queried fields (partner_id, username, email, timestamp, action)
- ✅ select_related() and prefetch_related() in queries
- ✅ Pagination (50 items per page)
- ✅ Efficient query patterns in analytics service

### Caching
- ✅ Dashboard metrics cached (60-second TTL)
- ✅ Chart data cached (5-minute TTL)
- ✅ Cache invalidation on data changes

### Frontend
- ✅ Code splitting in Vite configuration
- ✅ Lazy loading for routes
- ✅ Optimized bundle size with manual chunks

## Additional Optimizations

### 1. Database Performance

#### Connection Pooling

For production with PostgreSQL:

```bash
pip install django-db-connection-pool
```

Update `settings.py`:
```python
DATABASES['default']['ENGINE'] = 'dj_db_conn_pool.backends.postgresql'
DATABASES['default']['POOL_OPTIONS'] = {
    'POOL_SIZE': 10,
    'MAX_OVERFLOW': 10,
    'RECYCLE': 3600,
}
```

#### Query Optimization

```python
# Use select_related for foreign keys (already implemented)
users = PartnerUser.objects.select_related('partner', 'permissions').all()

# Use prefetch_related for reverse foreign keys
partners = Partner.objects.prefetch_related('users').all()

# Use only() to fetch specific fields
users = PartnerUser.objects.only('username', 'email', 'is_active')

# Use values() for dictionaries instead of model instances
user_data = PartnerUser.objects.values('id', 'username', 'email')

# Use iterator() for large querysets
for user in PartnerUser.objects.iterator(chunk_size=100):
    process_user(user)
```

#### Database Indexes

Already implemented in models, but verify with:

```sql
-- PostgreSQL
SELECT * FROM pg_indexes WHERE tablename = 'usersys_partneruser';

-- MySQL
SHOW INDEX FROM usersys_partneruser;
```

### 2. Caching Strategy

#### Redis Cache (Recommended for Production)

```bash
pip install django-redis
```

Update `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        },
        'KEY_PREFIX': 'bots',
        'TIMEOUT': 300,
    }
}
```

#### Cache Usage Patterns

```python
from django.core.cache import cache

# Cache with timeout
cache.set('key', value, timeout=300)  # 5 minutes

# Get from cache
value = cache.get('key')

# Get or set
value = cache.get_or_set('key', lambda: expensive_operation(), timeout=300)

# Delete from cache
cache.delete('key')

# Cache multiple keys
cache.set_many({'key1': 'value1', 'key2': 'value2'}, timeout=300)
values = cache.get_many(['key1', 'key2'])
```

#### View Caching

```python
from django.views.decorators.cache import cache_page

@cache_page(60)  # Cache for 60 seconds
def my_view(request):
    return JsonResponse(data)
```

### 3. Frontend Performance

#### Code Splitting

Already configured in `vite.config.js`, but can be enhanced:

```javascript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom', 'react-router-dom'],
          'charts': ['recharts', 'chart.js', 'react-chartjs-2'],
          'icons': ['@heroicons/react'],
          'admin': [
            './src/pages/admin/AdminDashboard',
            './src/pages/admin/PartnerManagement',
            './src/pages/admin/UserManagement',
          ],
          'partner': [
            './src/pages/partner/PartnerDashboard',
            './src/pages/partner/PartnerTransactions',
          ],
        },
      },
    },
  },
});
```

#### Lazy Loading

```javascript
import { lazy, Suspense } from 'react';

const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard'));
const PartnerDashboard = lazy(() => import('./pages/partner/PartnerDashboard'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/partner-portal" element={<PartnerDashboard />} />
      </Routes>
    </Suspense>
  );
}
```

#### Image Optimization

```bash
npm install -D vite-plugin-imagemin
```

```javascript
import viteImagemin from 'vite-plugin-imagemin';

export default defineConfig({
  plugins: [
    react(),
    viteImagemin({
      gifsicle: { optimizationLevel: 7 },
      optipng: { optimizationLevel: 7 },
      mozjpeg: { quality: 80 },
      svgo: {
        plugins: [{ removeViewBox: false }],
      },
    }),
  ],
});
```

### 4. API Performance

#### Response Compression

Enable gzip compression in Django:

```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # Add at the top
    # ... other middleware
]
```

#### Pagination

Already implemented, but ensure consistent usage:

```python
from django.core.paginator import Paginator

def list_view(request):
    items = Model.objects.all()
    paginator = Paginator(items, 50)  # 50 items per page
    page = paginator.get_page(request.GET.get('page', 1))
    return JsonResponse({
        'results': [item.to_dict() for item in page],
        'count': paginator.count,
        'pages': paginator.num_pages,
    })
```

#### API Response Caching

```python
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

@cache_page(60)
@vary_on_headers('Authorization')
def api_view(request):
    return JsonResponse(data)
```

### 5. Static Files

#### CDN Configuration

For production, serve static files from CDN:

```python
# settings.py
STATIC_URL = 'https://cdn.yourdomain.com/static/'
AWS_S3_CUSTOM_DOMAIN = 'cdn.yourdomain.com'
```

#### Static File Compression

```bash
pip install django-compressor
```

```python
INSTALLED_APPS += ['compressor']
STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
```

### 6. Web Server Configuration

#### Nginx Optimization

```nginx
# Enable gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;

# Enable caching
location /static/ {
    alias /path/to/staticfiles/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location /media/ {
    alias /path/to/media/;
    expires 30d;
    add_header Cache-Control "public";
}

# Enable HTTP/2
listen 443 ssl http2;

# Connection pooling
upstream django {
    server 127.0.0.1:8080;
    keepalive 32;
}

# Buffer sizes
client_body_buffer_size 10K;
client_header_buffer_size 1k;
client_max_body_size 10m;
large_client_header_buffers 2 1k;
```

### 7. Database Tuning

#### PostgreSQL

```sql
-- Increase shared buffers (25% of RAM)
shared_buffers = 2GB

-- Increase work memory
work_mem = 50MB

-- Increase maintenance work memory
maintenance_work_mem = 512MB

-- Increase effective cache size (50-75% of RAM)
effective_cache_size = 6GB

-- Enable query planning
random_page_cost = 1.1

-- Connection pooling
max_connections = 100
```

#### MySQL

```ini
[mysqld]
innodb_buffer_pool_size = 2G
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
max_connections = 100
query_cache_size = 64M
query_cache_type = 1
```

### 8. Monitoring and Profiling

#### Django Debug Toolbar (Development Only)

```bash
pip install django-debug-toolbar
```

```python
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

#### Query Monitoring

```python
from django.db import connection
from django.db import reset_queries

# Enable query logging
settings.DEBUG = True

# After operations
print(f"Number of queries: {len(connection.queries)}")
for query in connection.queries:
    print(f"{query['time']}: {query['sql']}")
```

#### Application Performance Monitoring

Consider using:
- **New Relic**: Full APM solution
- **Sentry**: Error tracking and performance
- **Datadog**: Infrastructure and application monitoring

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
)
```

### 9. Background Tasks

For long-running operations, use background tasks:

```bash
pip install celery redis
```

```python
# celery.py
from celery import Celery

app = Celery('bots')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# tasks.py
from celery import shared_task

@shared_task
def process_large_file(file_id):
    # Long-running operation
    pass
```

### 10. Load Balancing

For high availability:

```nginx
upstream django_cluster {
    least_conn;
    server 127.0.0.1:8080 weight=1;
    server 127.0.0.1:8081 weight=1;
    server 127.0.0.1:8082 weight=1;
}

server {
    location / {
        proxy_pass http://django_cluster;
    }
}
```

## Performance Benchmarks

### Target Metrics

- **API Response Time**: < 200ms (p95)
- **Page Load Time**: < 2s (p95)
- **Database Query Time**: < 50ms (p95)
- **Cache Hit Rate**: > 80%
- **Concurrent Users**: 100+
- **Requests per Second**: 1000+

### Testing Tools

```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:8080/api/v1/endpoint

# Load testing with wrk
wrk -t12 -c400 -d30s http://localhost:8080/api/v1/endpoint

# Database query analysis
python manage.py shell
from django.db import connection
from django.test.utils import override_settings
```

## Performance Checklist

### Database
- [ ] Indexes on all foreign keys
- [ ] Indexes on frequently queried fields
- [ ] Connection pooling configured
- [ ] Query optimization (select_related, prefetch_related)
- [ ] Pagination implemented
- [ ] Database tuning parameters set

### Caching
- [ ] Redis/Memcached configured
- [ ] Dashboard metrics cached
- [ ] API responses cached where appropriate
- [ ] Cache invalidation strategy implemented
- [ ] Cache hit rate monitored

### Frontend
- [ ] Code splitting enabled
- [ ] Lazy loading for routes
- [ ] Images optimized
- [ ] Bundle size optimized
- [ ] CDN configured for static files

### Infrastructure
- [ ] Gzip compression enabled
- [ ] HTTP/2 enabled
- [ ] Static file caching configured
- [ ] Load balancing configured (if needed)
- [ ] Monitoring and alerting set up

### Application
- [ ] Background tasks for long operations
- [ ] API response compression
- [ ] Efficient serialization
- [ ] Proper error handling
- [ ] Logging optimized

## Monitoring

### Key Metrics to Monitor

1. **Response Times**: API and page load times
2. **Error Rates**: 4xx and 5xx errors
3. **Database Performance**: Query times, connection pool usage
4. **Cache Performance**: Hit rate, memory usage
5. **System Resources**: CPU, memory, disk I/O
6. **User Metrics**: Active users, session duration

### Alerting Thresholds

- Response time > 1s (p95)
- Error rate > 1%
- Database connections > 80% of pool
- Cache hit rate < 70%
- CPU usage > 80%
- Memory usage > 85%

## Conclusion

Performance optimization is an ongoing process. Regularly monitor metrics, identify bottlenecks, and apply appropriate optimizations. Start with the most impactful changes (database indexes, caching) before moving to more complex optimizations.
