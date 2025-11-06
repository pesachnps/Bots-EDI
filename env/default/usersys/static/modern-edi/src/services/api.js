import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: '/modern-edi/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Include cookies for Django session auth
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add CSRF token if available
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors
    if (error.response) {
      const { status, data } = error.response;
      
      if (status === 401) {
        // Unauthorized - redirect to login
        window.location.href = '/login/';
      } else if (status === 403) {
        console.error('Permission denied:', data.error);
      } else if (status === 429) {
        console.error('Rate limit exceeded:', data.error);
      }
    }
    
    return Promise.reject(error);
  }
);

// Helper function to get cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Transaction API methods
export const transactionApi = {
  // List transactions
  list: (params = {}) => api.get('/transactions/', { params }),
  
  // List transactions by folder
  listByFolder: (folder, params = {}) => api.get(`/transactions/${folder}/`, { params }),
  
  // Get transaction details
  get: (id) => api.get(`/transaction/${id}/`),
  
  // Create transaction
  create: (data) => api.post('/transaction/create/', data),
  
  // Update transaction
  update: (id, data) => api.put(`/transaction/${id}/update/`, data),
  
  // Delete transaction (soft delete)
  delete: (id) => api.delete(`/transaction/${id}/delete/`),
  
  // Move transaction
  move: (id, targetFolder) => api.post(`/transaction/${id}/move/`, { target_folder: targetFolder }),
  
  // Send transaction
  send: (id) => api.post(`/transaction/${id}/send/`),
  
  // Process transaction (Inbox->Received, Outbox->Sent)
  process: (id) => api.post(`/transaction/${id}/process/`),
  
  // Validate transaction
  validate: (id) => api.get(`/transaction/${id}/validate/`),
  
  // Permanent delete
  permanentDelete: (id) => api.post(`/transaction/${id}/permanent-delete/`),
  
  // Get transaction history
  history: (id) => api.get(`/transaction/${id}/history/`),
  
  // Get raw EDI content
  raw: (id) => api.get(`/transaction/${id}/raw/`),
};

// Folder API methods
export const folderApi = {
  // List all folders with counts
  list: () => api.get('/folders/'),
  
  // Get folder statistics
  stats: (folder) => api.get(`/folders/${folder}/stats/`),
};

// Partner API methods
export const partnerApi = {
  // List all partners
  list: () => api.get('/partners/'),
};

// Document type API methods
export const documentTypeApi = {
  // List all document types
  list: () => api.get('/document-types/'),
};

// Search API methods
export const searchApi = {
  // Search transactions
  search: (params) => api.get('/search/', { params }),
};

export default api;
