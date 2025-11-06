import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, PlusIcon } from '@heroicons/react/24/outline';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [partners, setPartners] = useState([]);
  const [selectedPartner, setSelectedPartner] = useState('all');
  const [loading, setLoading] = useState(true);

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
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch partners:', error);
      setLoading(false);
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

  const getRoleBadge = (role) => {
    const colors = {
      partner_admin: 'bg-purple-100 text-purple-800',
      partner_user: 'bg-blue-100 text-blue-800',
      partner_readonly: 'bg-gray-100 text-gray-800',
    };
    return colors[role] || colors.partner_user;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">User Management</h1>
        {selectedPartner && selectedPartner !== 'all' && (
          <button className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700">
            <PlusIcon className="w-5 h-5 mr-2" />
            Create User
          </button>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Select Partner</label>
        <select
          value={selectedPartner}
          onChange={(e) => setSelectedPartner(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option value="all">Select a partner...</option>
          {partners.map((partner) => (
            <option key={partner.id} value={partner.id}>
              {partner.name}
            </option>
          ))}
        </select>
      </div>

      {selectedPartner && selectedPartner !== 'all' && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {users.length === 0 ? (
            <div className="p-8 text-center text-gray-500">No users found for this partner</div>
          ) : (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Login</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{user.full_name}</div>
                      <div className="text-sm text-gray-500">{user.email}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getRoleBadge(user.role)}`}>
                        {user.role.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}
                    </td>
                    <td className="px-6 py-4 text-right text-sm font-medium space-x-2">
                      <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
                      <button className="text-red-600 hover:text-red-900">Reset Password</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
