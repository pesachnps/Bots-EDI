# Modern EDI Interface - Frontend

React-based frontend for the Modern EDI Interface.

## Setup

### Install Dependencies

```bash
cd env/default/usersys/static/modern-edi
npm install
```

### Development

```bash
npm run dev
```

The development server will start at `http://localhost:3000` with proxy to the Django backend at `http://localhost:8080`.

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Project Structure

```
src/
├── components/          # Reusable React components
│   ├── Layout.jsx       # Main layout with header/footer
│   ├── TransactionCard.jsx
│   ├── TransactionDetail.jsx
│   ├── TransactionForm.jsx
│   ├── MoveDialog.jsx
│   └── SearchFilter.jsx
├── pages/              # Page components
│   ├── Dashboard.jsx   # Main dashboard with folder cards
│   └── FolderView.jsx  # Transaction list view
├── hooks/              # Custom React hooks
│   └── useTransactions.js  # React Query hooks for API
├── services/           # API services
│   └── api.js          # Axios instance and API methods
├── App.jsx             # Main app component with routing
├── main.jsx            # Entry point
└── index.css           # Global styles with Tailwind

## Features

### Dashboard
- View all 5 folders (Inbox, Received, Outbox, Sent, Deleted)
- See transaction counts for each folder
- Quick navigation to folder views

### Folder View
- List all transactions in a folder
- Search transactions by partner, PO, or filename
- Filter by partner, document type, status, and date range
- Create new transactions (Inbox/Outbox only)
- Pagination support

### Transaction Card
- Display key transaction information
- Action menu (Move, Edit, Delete, Send)
- Status indicators for sent transactions
- Click to view full details

### Transaction Detail Modal
- Tabbed interface (Overview, Raw Data, History, Acknowledgment)
- View all transaction metadata
- See raw EDI content
- Review transaction history
- Check acknowledgment status (for sent transactions)

### Transaction Form
- Create new transactions
- Edit existing transactions (Inbox/Outbox only)
- Partner and document type selection
- Form validation

### Move Dialog
- Move transactions between folders
- Visual folder selection
- Folder icons and colors

## API Integration

The frontend communicates with the Django backend API at `/modern-edi/api/v1/`.

All API calls use:
- Django session authentication (cookies)
- CSRF token protection
- Automatic error handling
- Request/response interceptors

## Technologies

- **React 18** - UI framework
- **React Router 6** - Client-side routing
- **TanStack Query** - Data fetching and caching
- **React Hook Form** - Form management
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **date-fns** - Date formatting
- **Vite** - Build tool

## Development Tips

### Hot Reload
Vite provides instant hot module replacement (HMR) during development.

### API Proxy
The dev server proxies `/modern-edi/api` requests to `http://localhost:8080`.

### React Query DevTools
Add React Query DevTools for debugging:

```jsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

// In App.jsx
<ReactQueryDevtools initialIsOpen={false} />
```

### Debugging
- Use browser DevTools React extension
- Check Network tab for API calls
- Review Console for errors

## Deployment

### Build
```bash
npm run build
```

### Serve with Django
The built files should be served by Django's static file system.

Update Django settings to collect static files:
```bash
python manage.py collectstatic
```

### Environment Variables
Create `.env` file for environment-specific config:
```
VITE_API_BASE_URL=/modern-edi/api/v1
```

## Troubleshooting

### CORS Issues
Ensure Django CORS settings allow the frontend origin.

### Authentication Issues
Check that Django session cookies are being sent with requests.

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Contributing

1. Follow React best practices
2. Use functional components with hooks
3. Keep components small and focused
4. Add PropTypes or TypeScript for type safety
5. Write meaningful commit messages

## License

Same as parent project.
