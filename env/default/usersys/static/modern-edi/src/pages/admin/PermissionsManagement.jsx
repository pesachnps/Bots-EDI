import { useState, useEffect } from 'react';
import { CheckIcon, XMarkIcon } from '@heroicons/react/24/outline';
import adminApi from '../../services/adminApi';

export default function PermissionsManagement() {
  const [partners, setPartners] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedPartner, setSelectedPartner] = useState('');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const permissions = [
    { key: 'can_view_transactions', label: 'View Transactions' },
    { key: 'can_upload_files', label: 'Upload Files' },
    { key: 'can_download_files', label: 'Download Files' },
    { key: 'can_view_reports', label: 'View Reports' },
    { key: 'can_manage_settings', label: 'Manage Settings' },
  ];

  useEffect(() => {
    loadPartners();
  }, []);

  useEffect(() => {
    if (selectedPartner) {
      loadUsers();
    }
  }, [selectedPartner]);

  const loadPartners = async () => {
    try {
      const data = await adminApi.getPartners();
      setPartners(data.results || []);
      if (data.results?.length > 0) {
        setSelectedPartner(data.results[0].id);
      }
    } catch (err) {
      console.error('Failed to load partners:', err);
    }
  };

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await adminApi.getPartnerUsers(selectedPartner);
      setUsers(data.results || []);
    } catch (err) {
      console.error('Failed to load users:', err);
    } finally {
      setLoading(false);
    }
  };

  const togglePermission = async (userId, permissionKey, currentValue) => {
    try {
      setSaving(true);
      const user = users.find(u => u.id === userId);
      const updatedPermissions = {
        ...user.permissions,
        [permissionKey]: !currentValue,
      };
      
      await adminApi.updateUserPermissions(userId, updatedPermissions);
      
      // Update local state
      setUsers(users.map(u => 
        u.id === userId 
          ? { ...u, permissions: updatedPermissions }
          : u
      ));
    } catch (err) {
      alert(`Failed to update permission: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Permissions Management</h1>
      </div>

      {/* Partner Select */}
      <div className="bg-white rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Select Partner</label>
        <select
          value={selectedPartner}
          onChange={(e) => setSelectedPartner(e.target.value)}
          className="w-full max-w-md px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option value="">Select a partner...</option>
          {partners.map((partner) => (
            <option key={partner.id} value={partner.id}>
              {partner.name}
            </option>
          ))}
        </select>
      </div>

      {/* Permission Matrix */}
      {loading ? (
        <div className="flex items-center justify-center h-64 bg-white rounded-lg shadow">
          <div className="text-gray-500">Loading permissions...</div>
        </div>
      ) : !selectedPartner ? (
        <div className="flex items-center justify-center h-64 bg-white rounded-lg shadow">
          <div className="text-gray-500">Please select a partner</div>
        </div>
      ) : users.length === 0 ? (
        <div className="flex items-center justify-center h-64 bg-white rounded-lg shadow">
          <div className="text-gray-500">No users found for this partner</div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Role
                </th>
                {permissions.map((perm) => (
                  <th key={perm.key} className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {perm.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap sticky left-0 bg-white">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {user.first_name} {user.last_name}
                      </div>
                      <div className="text-sm text-gray-500">{user.username}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                      {user.role === 'partner_admin' ? 'Admin' : 
                       user.role === 'partner_user' ? 'User' : 'Read-Only'}
                    </span>
                  </td>
                  {permissions.map((perm) => {
                    const hasPermission = user.permissions?.[perm.key] || false;
                    return (
                      <td key={perm.key} className="px-6 py-4 whitespace-nowrap text-center">
                        <button
                          onClick={() => togglePermission(user.id, perm.key, hasPermission)}
                          disabled={saving}
                          className={`inline-flex items-center justify-center w-8 h-8 rounded-full transition-colors ${
                            hasPermission
                              ? 'bg-green-100 text-green-600 hover:bg-green-200'
                              : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                          } ${saving ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                          title={hasPermission ? 'Click to revoke' : 'Click to grant'}
                        >
                          {hasPermission ? (
                            <CheckIcon className="h-5 w-5" />
                          ) : (
                            <XMarkIcon className="h-5 w-5" />
                          )}
                        </button>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        </div>
      )}

      {/* Legend */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-medium text-blue-900 mb-2">Permission Descriptions</h3>
        <ul className="space-y-1 text-sm text-blue-800">
          <li><strong>View Transactions:</strong> Access to transaction list and details</li>
          <li><strong>Upload Files:</strong> Ability to upload EDI files</li>
          <li><strong>Download Files:</strong> Ability to download EDI files</li>
          <li><strong>View Reports:</strong> Access to analytics and reports</li>
          <li><strong>Manage Settings:</strong> Ability to modify partner settings</li>
        </ul>
      </div>
    </div>
  );
}
