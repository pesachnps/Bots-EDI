# Complete Implementation Guide - Phases 4-12

## Current Status: 25% Complete (Phases 1-3 Done)

This guide provides step-by-step implementation details for the remaining 9 phases.

---

## Phase 4: Confirm Rules & Code Lists (HIGH Priority)

### Backend Implementation

#### Step 1: Add URL routes to `admin_urls.py`
```python
# Confirm Rules
path('confirmrules', admin_views.admin_confirmrules_list_or_create),
path('confirmrules/<int:rule_id>', admin_views.admin_confirmrule_detail_update_delete),

# Code Lists
path('codelists', admin_views.admin_codelists_list),
path('codelists/<str:ccodeid>', admin_views.admin_codelist_codes_list_or_create),
path('codelists/<str:ccodeid>/<int:code_id>', admin_views.admin_codelist_code_update_delete),

# Counters
path('counters', admin_views.admin_counters_list),
path('counters/<str:domein>', admin_views.admin_counter_update),
```

#### Step 2: Add views to `admin_views.py`
Follow the same pattern as Routes/Channels/Translations:
- Import models: `from bots.models import confirmrule, ccode, ccodetrigger, uniek`
- Create list/create/detail/update/delete functions
- Add pagination, filtering, search
- Return JsonResponse with success/error

#### Step 3: Key Model Fields
- **confirmrule**: confirmtype, ruletype, idroute, idchannel, frompartner, topartner, editype, messagetype, rsrv1, rsrv2
- **ccode**: ccodeid, leftcode, rightcode, attr1-attr8, desc
- **uniek**: domein, nummer (counter value)

### Frontend Implementation

#### Files to Create:
```
src/hooks/useConfirmRules.js
src/hooks/useCodeLists.js  
src/hooks/useCounters.js
src/pages/admin/ConfirmRules.jsx
src/pages/admin/CodeLists.jsx
src/pages/admin/Counters.jsx
```

#### Pattern:
Use same structure as Translations (minimal but functional):
- List view with search/filter
- Card/table display
- CRUD actions
- Pagination

#### Add to App.jsx and AdminLayout.jsx
```jsx
<Route path="confirmrules" element={<ConfirmRules />} />
<Route path="codelists" element={<CodeLists />} />
<Route path="counters" element={<Counters />} />
```

---

## Phase 5: Transactions - Incoming & Outgoing (HIGH Priority)

### Backend Implementation

#### Models to Use:
- `from bots.models import ta` (transaction model)
- Fields: idta, statust, status, fromchannel, tochannel, editype, messagetype, filename, ts, filesize, frompartner, topartner, errortext

#### API Endpoints:
```python
path('transactions/incoming', admin_views.admin_transactions_incoming),
path('transactions/outgoing', admin_views.admin_transactions_outgoing),
path('transactions/<int:ta_id>', admin_views.admin_transaction_detail),
path('transactions/<int:ta_id>/resend', admin_views.admin_transaction_resend),
path('transactions/<int:ta_id>/content', admin_views.admin_transaction_content),
path('transactions/bulk-delete', admin_views.admin_transactions_bulk_delete),
```

#### Key Features:
- Filter by statust (100=incoming, 200-900=outgoing stages)
- Date range filtering
- Status filtering (OK, ERROR, DONE, etc.)
- Partner/channel filtering
- Bulk operations

### Frontend Implementation

#### Files:
```
src/hooks/useTransactions.js (extend existing)
src/pages/admin/Incoming.jsx
src/pages/admin/Outgoing.jsx
```

#### Features:
- Table view with sortable columns
- Status badges (color-coded)
- Date/time display
- Bulk select checkboxes
- Action buttons (view, resend, delete)
- Advanced filters panel

---

## Phase 6: Transaction Detail & Reports (HIGH Priority)

### Backend Implementation

#### API Endpoints:
```python
path('transactions/<int:ta_id>/lineage', admin_views.admin_transaction_lineage),
path('transactions/<int:ta_id>/raw', admin_views.admin_transaction_raw),
path('processes', admin_views.admin_processes_list),
path('reports/query', admin_views.admin_reports_query),
```

#### Lineage Query:
```python
def get_lineage(ta_id):
    # Get parent transactions
    parents = ta.objects.filter(child=ta_id)
    # Get child transactions  
    children = ta.objects.filter(parent=ta_id)
    # Return tree structure
```

### Frontend Implementation

#### Files:
```
src/pages/admin/TransactionDetail.jsx
src/pages/admin/Reports.jsx
src/components/admin/LineageTree.jsx
```

#### Features:
- Full transaction details
- Parent/child lineage visualization (tree/graph)
- View raw message content
- Error details with formatting
- Download message
- Resend/confirm actions

---

## Phase 7: File Management (MEDIUM Priority)

### Backend Implementation

#### API Endpoints:
```python
path('files/browse', admin_views.admin_files_browse),
path('files/download', admin_views.admin_files_download),
path('files/delete', admin_views.admin_files_delete),
path('logs', admin_views.admin_logs_list),
path('logs/<str:filename>', admin_views.admin_log_view),
```

#### Implementation:
```python
import os
import botsglobal

def admin_files_browse(request):
    path = request.GET.get('path', 'data')
    base_dir = botsglobal.ini.get('directories', 'botssysabs')
    full_path = os.path.join(base_dir, path)
    # List files with os.listdir()
    # Return file info (name, size, modified date)
```

### Frontend Implementation

#### Files:
```
src/pages/admin/FileBrowser.jsx
src/pages/admin/LogViewer.jsx
```

#### Features:
- Directory tree navigation
- File list with details
- Download/delete actions
- Log viewer with pagination
- Search logs
- Real-time tail option

---

## Phase 8: Operations (MEDIUM Priority)

### Backend Implementation

#### API Endpoints:
```python
path('engine/status', admin_views.admin_engine_status),
path('engine/run', admin_views.admin_engine_run),
path('cleanup/preview', admin_views.admin_cleanup_preview),
path('cleanup/execute', admin_views.admin_cleanup_execute),
```

#### Engine Control:
```python
import subprocess

def admin_engine_run(request):
    # Run bots-engine command
    result = subprocess.run(['bots-engine'], capture_output=True)
    return JsonResponse({'success': True, 'output': result.stdout})
```

#### Cleanup:
```python
from datetime import datetime, timedelta

def admin_cleanup_preview(request):
    days = int(request.GET.get('days', 30))
    cutoff = datetime.now() - timedelta(days=days)
    count = ta.objects.filter(ts__lt=cutoff).count()
    return JsonResponse({'count': count})
```

### Frontend Implementation

#### Files:
```
src/pages/admin/EngineControl.jsx
src/pages/admin/DataCleanup.jsx
```

#### Features:
- Engine status indicator
- Run engine button
- Real-time output display
- Cleanup preview
- Date range selector
- Execute with confirmation

---

## Phase 9: Plugins & Backup (MEDIUM Priority)

### Backend Implementation

#### API Endpoints:
```python
path('plugins', admin_views.admin_plugins_list),
path('plugins/upload', admin_views.admin_plugin_upload),
path('backup/create', admin_views.admin_backup_create),
path('backup/list', admin_views.admin_backup_list),
```

#### Implementation:
```python
from bots import pluglib

def admin_plugin_upload(request):
    file = request.FILES['plugin']
    # Save to temp location
    # Use pluglib to install
    pluglib.load_plugin(file.path)
```

### Frontend Implementation

#### Files:
```
src/pages/admin/Plugins.jsx
src/pages/admin/BackupRestore.jsx
```

#### Features:
- Plugin list
- Drag-drop upload
- Backup creation
- Backup list with download
- Restore wizard

---

## Phase 10: System Utilities (LOW Priority)

### Backend Implementation

#### API Endpoints:
```python
path('system/info', admin_views.admin_system_info),
path('system/health', admin_views.admin_system_health),
path('system/test-email', admin_views.admin_test_email),
```

#### Implementation:
```python
import platform
import sys

def admin_system_info(request):
    return JsonResponse({
        'python_version': sys.version,
        'bots_version': botsglobal.version,
        'platform': platform.platform(),
        'database': settings.DATABASES['default']['ENGINE'],
    })
```

### Frontend Implementation

#### Files:
```
src/pages/admin/SystemInfo.jsx
src/pages/admin/SystemHealth.jsx
```

---

## Phase 11: Navigation & Permissions (HIGH Priority)

### Implementation Steps

#### Step 1: Update AdminLayout.jsx
Create collapsible navigation sections:

```jsx
const navigationSections = [
  {
    name: 'Configuration',
    items: [
      { name: 'Routes', href: '/admin/routes', icon: MapIcon },
      { name: 'Channels', href: '/admin/channels', icon: ServerIcon },
      { name: 'Translations', href: '/admin/translations', icon: LanguageIcon },
      { name: 'Confirm Rules', href: '/admin/confirmrules', icon: CheckIcon },
      { name: 'Code Lists', href: '/admin/codelists', icon: TableIcon },
    ]
  },
  {
    name: 'Transactions',
    items: [
      { name: 'Incoming', href: '/admin/incoming', icon: InboxIcon },
      { name: 'Outgoing', href: '/admin/outgoing', icon: PaperAirplaneIcon },
    ]
  },
  // ... more sections
];
```

#### Step 2: Add Collapsible Component
```jsx
const [openSections, setOpenSections] = useState(['Configuration']);

const toggleSection = (name) => {
  setOpenSections(prev => 
    prev.includes(name) ? prev.filter(s => s !== name) : [...prev, name]
  );
};
```

#### Step 3: Create usePermissions Hook
```jsx
// src/hooks/usePermissions.js
export const usePermissions = () => {
  const user = useContext(UserContext);
  
  const hasPermission = (permission) => {
    return user?.permissions?.includes(permission) || user?.is_superuser;
  };
  
  return { hasPermission };
};
```

---

## Phase 12: Testing & Documentation (CRITICAL)

### Testing Implementation

#### Backend Tests
Create `tests/test_admin_api.py`:
```python
from django.test import TestCase, Client
from django.contrib.auth.models import User

class AdminAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('admin', password='test')
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='admin', password='test')
    
    def test_routes_list(self):
        response = self.client.get('/api/v1/admin/routes')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
    
    # Add tests for all endpoints
```

#### Frontend Tests
Create `src/pages/admin/__tests__/Routes.test.jsx`:
```jsx
import { render, screen, waitFor } from '@testing-library/react';
import Routes from '../Routes';

test('renders routes page', async () => {
  render(<Routes />);
  await waitFor(() => {
    expect(screen.getByText('Routes')).toBeInTheDocument();
  });
});
```

### Documentation

#### Create User Guide
`docs/USER_GUIDE.md`:
- Getting Started
- Routes Management
- Channels Configuration
- Translations Setup
- Transaction Monitoring
- Operations & Maintenance

#### Create API Documentation
`docs/API.md`:
- Authentication
- Endpoints list
- Request/response examples
- Error codes

#### Create Migration Guide
`docs/MIGRATION.md`:
- Differences from old interface
- Feature mapping
- Step-by-step migration process

---

## Build & Deploy Commands

### Development Build
```bash
cd env/default/usersys/static/modern-edi
npm run build
```

### Copy to Production
```bash
xcopy /Y /S usersys\* botssys\
```

### Run Tests
```bash
python manage.py test tests.test_admin_api
cd static/modern-edi && npm test
```

### Commit Pattern
```bash
git add -A
git commit -m "feat: add [Feature] - Phase X complete"
git push
```

---

## Estimated Effort

| Phase | Backend | Frontend | Total Hours |
|-------|---------|----------|-------------|
| Phase 4 | 4h | 3h | 7h |
| Phase 5 | 6h | 4h | 10h |
| Phase 6 | 5h | 4h | 9h |
| Phase 7 | 4h | 3h | 7h |
| Phase 8 | 3h | 2h | 5h |
| Phase 9 | 4h | 3h | 7h |
| Phase 10 | 2h | 2h | 4h |
| Phase 11 | 2h | 4h | 6h |
| Phase 12 | 8h | 4h | 12h |
| **Total** | **38h** | **29h** | **67h** |

---

## Quick Start for Each Phase

1. **Read models** in `bots/models.py`
2. **Add URLs** to `admin_urls.py`
3. **Create views** in `admin_views.py` (follow existing patterns)
4. **Test backend** with curl or Postman
5. **Create hook** in `src/hooks/`
6. **Create page** in `src/pages/admin/`
7. **Add to routing** in `App.jsx` and `AdminLayout.jsx`
8. **Build** with `npm run build`
9. **Copy to botssys**
10. **Test in browser**
11. **Commit to git**

---

## Key Files Reference

### Backend
- `env/default/usersys/admin_views.py` - All API logic
- `env/default/usersys/admin_urls.py` - URL routing
- `bots/models.py` - Django models (READ ONLY)

### Frontend
- `src/pages/admin/*.jsx` - Page components
- `src/components/admin/*.jsx` - Reusable components
- `src/hooks/*.js` - Custom hooks
- `src/App.jsx` - Main routing
- `src/pages/admin/AdminLayout.jsx` - Sidebar navigation

### Build
- `package.json` - Dependencies
- `vite.config.js` - Build configuration
- `dist/` - Built output (copy to botssys)

---

## Success Criteria

✅ All 24 features implemented  
✅ 100% feature parity with old interface  
✅ All tests passing  
✅ Documentation complete  
✅ Performance < 100ms API response  
✅ No critical bugs  
✅ User acceptance testing passed  

---

**Current Progress: 3/12 phases (25%)**  
**Remaining: 9 phases (75%)**

Follow this guide to complete the migration systematically!
