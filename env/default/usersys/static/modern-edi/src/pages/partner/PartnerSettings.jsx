import { useState, useEffect } from 'react';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

export default function PartnerSettings() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [testingConnection, setTestingConnection] = useState(false);
  const [connectionResult, setConnectionResult] = useState(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await fetch('/modern-edi/api/v1/partner-portal/settings');
      const data = await response.json();
      setSettings(data.settings);
      setFormData({
        contact_name: data.settings.partner.contact_name,
        contact_email: data.settings.partner.contact_email,
        contact_phone: data.settings.partner.contact_phone,
      });
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch settings:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/modern-edi/api/v1/partner-portal/settings/contact', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setEditing(false);
        fetchSettings();
      }
    } catch (error) {
      console.error('Failed to update settings:', error);
    }
  };

  const handleTestConnection = async () => {
    setTestingConnection(true);
    setConnectionResult(null);

    try {
      const response = await fetch('/modern-edi/api/v1/partner-portal/settings/test-connection', {
        method: 'POST',
      });
      const data = await response.json();
      setConnectionResult(data);
    } catch (error) {
      setConnectionResult({ success: false, message: 'Connection test failed' });
    } finally {
      setTestingConnection(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading settings...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Settings</h1>

      {/* Partner Information */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">Partner Information</h2>
        </div>
        <div className="p-6">
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <dt className="text-sm font-medium text-gray-500">Partner ID</dt>
              <dd className="mt-1 text-sm text-gray-900">{settings?.partner.partner_id}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Company Name</dt>
              <dd className="mt-1 text-sm text-gray-900">{settings?.partner.name}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Communication Method</dt>
              <dd className="mt-1 text-sm text-gray-900 capitalize">{settings?.partner.communication_method}</dd>
            </div>
          </dl>
        </div>
      </div>

      {/* Contact Information */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b flex items-center justify-between">
          <h2 className="text-lg font-medium text-gray-900">Contact Information</h2>
          {!editing && (
            <button
              onClick={() => setEditing(true)}
              className="px-3 py-1 text-sm font-medium text-indigo-600 hover:text-indigo-700"
            >
              Edit
            </button>
          )}
        </div>
        <div className="p-6">
          {editing ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Contact Name</label>
                <input
                  type="text"
                  value={formData.contact_name}
                  onChange={(e) => setFormData({ ...formData, contact_name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.contact_email}
                  onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input
                  type="tel"
                  value={formData.contact_phone}
                  onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setEditing(false)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
                >
                  Save Changes
                </button>
              </div>
            </form>
          ) : (
            <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <dt className="text-sm font-medium text-gray-500">Contact Name</dt>
                <dd className="mt-1 text-sm text-gray-900">{settings?.partner.contact_name || '-'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Email</dt>
                <dd className="mt-1 text-sm text-gray-900">{settings?.partner.contact_email || '-'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Phone</dt>
                <dd className="mt-1 text-sm text-gray-900">{settings?.partner.contact_phone || '-'}</dd>
              </div>
            </dl>
          )}
        </div>
      </div>

      {/* Connection Settings */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">Connection Settings</h2>
        </div>
        <div className="p-6 space-y-4">
          {settings?.sftp_config && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">SFTP Configuration</h3>
              <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Host</dt>
                  <dd className="mt-1 text-sm text-gray-900">{settings.sftp_config.host}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Port</dt>
                  <dd className="mt-1 text-sm text-gray-900">{settings.sftp_config.port}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Status</dt>
                  <dd className="mt-1 text-sm text-gray-900">{settings.sftp_config.status}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Last Test</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {settings.sftp_config.last_test ? new Date(settings.sftp_config.last_test).toLocaleString() : 'Never'}
                  </dd>
                </div>
              </dl>
            </div>
          )}

          {settings?.api_config && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">API Configuration</h3>
              <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Base URL</dt>
                  <dd className="mt-1 text-sm text-gray-900">{settings.api_config.base_url}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Status</dt>
                  <dd className="mt-1 text-sm text-gray-900">{settings.api_config.status}</dd>
                </div>
              </dl>
            </div>
          )}

          <div className="pt-4">
            <button
              onClick={handleTestConnection}
              disabled={testingConnection}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {testingConnection ? 'Testing...' : 'Test Connection'}
            </button>
          </div>

          {connectionResult && (
            <div className={`flex items-center p-3 rounded-md ${
              connectionResult.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {connectionResult.success ? (
                <CheckCircleIcon className="w-5 h-5 mr-2" />
              ) : (
                <XCircleIcon className="w-5 h-5 mr-2" />
              )}
              <span className="text-sm">{connectionResult.message || connectionResult.results?.sftp?.message}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
