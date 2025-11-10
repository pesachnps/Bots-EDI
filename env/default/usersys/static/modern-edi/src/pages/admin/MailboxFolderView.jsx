import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { PlusIcon, ArrowPathIcon, MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';
import { useTransactionsByFolder } from '../../hooks/useTransactions';
import TransactionCard from '../../components/TransactionCard';
import TransactionDetail from '../../components/TransactionDetail';
import TransactionForm from '../../components/TransactionForm';
import SearchFilter from '../../components/SearchFilter';

export default function MailboxFolderView() {
  const { folderName } = useParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({});
  const [selectedTransactionId, setSelectedTransactionId] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  // Build query params
  const queryParams = {
    search: searchQuery || undefined,
    ...filters,
  };

  const { data, isLoading, error, refetch } = useTransactionsByFolder(folderName, queryParams);

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleFilter = (newFilters) => {
    setFilters(newFilters);
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleCreateClick = () => {
    setShowCreateForm(true);
  };

  const handleTransactionClick = (id) => {
    setSelectedTransactionId(id);
  };

  const canCreate = folderName === 'inbox' || folderName === 'outbox';

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 capitalize">{folderName}</h1>
        <p className="mt-1 text-sm text-gray-600">
          {data?.pagination?.total_count || 0} transactions
        </p>
      </div>

      <div className="bg-white rounded-lg shadow">
        {/* Action Bar */}
        <div className="p-4 border-b border-gray-200">
        <div className="flex flex-wrap items-center gap-2">
          {/* Search Input */}
          <div className="flex-1 min-w-[200px] relative">
            <MagnifyingGlassIcon className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search transactions..."
              value={searchQuery}
              onChange={handleSearch}
              className="w-full pl-8 pr-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`px-2 py-1.5 text-xs font-medium rounded-md flex items-center gap-1 ${
                showFilters
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <FunnelIcon className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">Filters</span>
            </button>

            {canCreate && (
              <button
                onClick={handleCreateClick}
                className="px-2 py-1.5 text-xs font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 flex items-center gap-1"
              >
                <PlusIcon className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Create</span>
              </button>
            )}

            <button
              onClick={handleRefresh}
              className="px-2 py-1.5 text-xs font-medium bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 flex items-center gap-1"
            >
              <ArrowPathIcon className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">Refresh</span>
            </button>
          </div>
        </div>

          {/* Filter Panel */}
          {showFilters && (
            <div className="mt-3 pt-3 border-t border-gray-200">
              <SearchFilter onFilterChange={handleFilter} />
            </div>
          )}
        </div>

        {/* Content Area */}
        <div className="p-4">
          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center justify-center py-12">
              <div className="text-sm text-gray-500">Loading transactions...</div>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">Failed to load transactions: {error.message}</p>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && !error && data?.transactions?.length === 0 && (
            <div className="text-center py-12">
              <p className="text-sm text-gray-500 mb-3">No transactions found</p>
              {canCreate && (
                <button
                  onClick={handleCreateClick}
                  className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
                >
                  Create your first transaction
                </button>
              )}
            </div>
          )}

          {/* Transaction Grid */}
          {!isLoading && !error && data?.transactions?.length > 0 && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {data.transactions.map((transaction) => (
                  <TransactionCard
                    key={transaction.id}
                    transaction={transaction}
                    folderType={folderName}
                    onClick={() => handleTransactionClick(transaction.id)}
                  />
                ))}
              </div>

              {/* Pagination */}
              {data?.pagination && data.pagination.total_pages > 1 && (
                <div className="mt-6 pt-4 border-t border-gray-200 flex items-center justify-between text-sm">
                  <button
                    disabled={!data.pagination.has_previous}
                    className="px-4 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                  >
                    Previous
                  </button>
                  <span className="text-gray-600">
                    Page {data.pagination.page} of {data.pagination.total_pages}
                  </span>
                  <button
                    disabled={!data.pagination.has_next}
                    className="px-4 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* Transaction Detail Modal */}
      {selectedTransactionId && (
        <TransactionDetail
          transactionId={selectedTransactionId}
          onClose={() => setSelectedTransactionId(null)}
        />
      )}

      {/* Create Transaction Form Modal */}
      {showCreateForm && (
        <TransactionForm
          mode="create"
          folderType={folderName}
          onSave={() => {
            setShowCreateForm(false);
            refetch();
          }}
          onCancel={() => setShowCreateForm(false)}
        />
      )}
    </div>
  );
}
