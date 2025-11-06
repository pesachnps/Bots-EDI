import { useState } from 'react';
import { usePartners, useDocumentTypes } from '../hooks/useTransactions';

function SearchFilter({ onFilterChange }) {
  const [filters, setFilters] = useState({
    partner: '',
    document_type: '',
    status: '',
    date_from: '',
    date_to: '',
  });

  const { data: partners } = usePartners();
  const { data: documentTypes } = useDocumentTypes();

  const handleChange = (field, value) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
    
    // Remove empty filters
    const activeFilters = Object.entries(newFilters).reduce((acc, [key, val]) => {
      if (val) acc[key] = val;
      return acc;
    }, {});
    
    onFilterChange(activeFilters);
  };

  const handleClear = () => {
    setFilters({
      partner: '',
      document_type: '',
      status: '',
      date_from: '',
      date_to: '',
    });
    onFilterChange({});
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Partner Filter */}
        <div>
          <label className="label">Partner</label>
          <select
            value={filters.partner}
            onChange={(e) => handleChange('partner', e.target.value)}
            className="input"
          >
            <option value="">All Partners</option>
            {partners?.map((partner) => (
              <option key={partner.name} value={partner.name}>
                {partner.name}
              </option>
            ))}
          </select>
        </div>

        {/* Document Type Filter */}
        <div>
          <label className="label">Document Type</label>
          <select
            value={filters.document_type}
            onChange={(e) => handleChange('document_type', e.target.value)}
            className="input"
          >
            <option value="">All Types</option>
            {documentTypes?.map((type) => (
              <option key={type.code} value={type.code}>
                {type.code} - {type.name}
              </option>
            ))}
          </select>
        </div>

        {/* Status Filter */}
        <div>
          <label className="label">Status</label>
          <select
            value={filters.status}
            onChange={(e) => handleChange('status', e.target.value)}
            className="input"
          >
            <option value="">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="ready">Ready</option>
            <option value="processing">Processing</option>
            <option value="sent">Sent</option>
            <option value="acknowledged">Acknowledged</option>
            <option value="failed">Failed</option>
          </select>
        </div>

        {/* Date From */}
        <div>
          <label className="label">Date From</label>
          <input
            type="date"
            value={filters.date_from}
            onChange={(e) => handleChange('date_from', e.target.value)}
            className="input"
          />
        </div>

        {/* Date To */}
        <div>
          <label className="label">Date To</label>
          <input
            type="date"
            value={filters.date_to}
            onChange={(e) => handleChange('date_to', e.target.value)}
            className="input"
          />
        </div>
      </div>

      {/* Clear Filters Button */}
      <div className="flex justify-end">
        <button
          onClick={handleClear}
          className="btn btn-secondary text-sm"
        >
          Clear Filters
        </button>
      </div>
    </div>
  );
}

export default SearchFilter;
