import { useState, useEffect } from 'react';

export default function PermissionsManagement() {
  const [partners, setPartners] = useState([]);
  const [selectedPartner, setSelectedPartner] = useState('all');
  const [users, setUsers] = useState([]);

  const permissions = [
    { key: 'can_view_transactions', label: 'View Transactions' },
    { key: 'can_upload_files', label: 'Upload Files' },
    { key: 'can_download_files', label: 'Download Files' },
    { key: 'can_view_reports', label: 'View Reports' },
    { key: 'can_manage_settings', label: 'Manage Settings' },
  ];

  useEffect(() => {
    fetchPartners();
  }, []);

  useEffect(() => {
    if (selectedPartner && selectedPartner !== 'all') {
      fetchUsers(selectedPartner);
    }
  }, [selectedPartner]);

  const fetchPartners = async () => {
    try {
      const response = await fetch('/modern-edi/api/v1/admin/partners/');
      const data = await response.json();
      setPartners(data.results || []);
    } catch (error) {
      console.error('Failed to fetch partners:', error);
    }
  };

  const fetchUsers = async (partnerId) => {
    try {
      const response = await fetch(`/modern-edi/api/v1/admin/partners/${partnerId}/users`);
      const data = await response.json();
      setUsers(data.users || []);
    } catch (error) {
      console.error('Failed to fetch users:', error);
    }
  };

  const handlePermissionToggle = async (userId, permissionKey, currentValue) => {
    try {
      const response = await fetch(`/modern-edi/api/v1/admin/users/${userId}/permissions`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          [permissionKey]: !currentValue
        })
      });
      
      if (response.ok) {
        // Refresh users
        fetchUsers(selectedPartner);
      }
    } catch (error) {
      console.error('Failed to update permission:', error);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Permissions Management</h1>

      <div className="bg-white rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Select Partner</label>
        <select
          value={selectedPartner}
          onChange={(e) => setSelectedPartner(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option value="all">Select a partner...</option>
          {partners.map((partner) => (
            <option key={partner.id} value={partner.id}>{partner.name}</option>
          ))}
        </select>
      </div>

      {selectedPartner && selectedPartner !== 'all' && users.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase sticky left-0 bg-gray-50">
                  User
                </th>
                {permissions.map((perm) => (
                  <th key={perm.key} className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                    {perm.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap sticky left-0 bg-white">
                    <div className="text-sm font-medium text-gray-900">{user.full_name}</div>
                    <div className="text-sm text-gray-500">{user.role.replace('_', ' ')}</div>
                  </td>
                  {permissions.map((perm) => (
                    <td key={perm.key} className="px-6 py-4 text-center">
                      <input
                        type="checkbox"
                        checked={user.permissions?.[perm.key] || false}
                        onChange={() => handlePermissionToggle(user.id, perm.key, user.permissions?.[perm.key])}
                        className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
