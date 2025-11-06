import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Plus, RefreshCw, Search, Filter, Loader2 } from 'lucide-react';
import { useTransactionsByFolder } from '../hooks/useTransactions';
import TransactionCard from '../components/TransactionCard';
import TransactionDetail from '../components/TransactionDetail';
import TransactionForm from '../components/TransactionForm';
import SearchFilter from '../components/SearchFilter';

function FolderView() {
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

  const handleSearch = (query) => {
    setSearchQuery(query);
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
    <div>
      {/* Header */}
      <div className="mb-6">
        <Link
          to="/"
          className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Dashboard</span>
        </Link>

        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 capitalize">{folderName}</h2>
            <p className="mt-1 text-gray-600">
              {data?.pagination?.total_count || 0} transactions
            </p>
          </div>

          <div className="flex items-center space-x-3">
            {canCreate && (
              <button
                onClick={handleCreateClick}
                className="btn btn-primary flex items-center space-x-2"
              >
                <Plus className="h-5 w-5" />
                <span>Create</span>
              </button>
            )}
            
            <button
              onClick={handleRefresh}
              className="btn btn-secondary flex items-center space-x-2"
            >
              <RefreshCw className="h-5 w-5" />
              <span>Refresh</span>
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filter Bar */}
      <div className="mb-6 bg-white rounded-lg shadow-sm p-4 border border-gray-200">
        <div className="flex items-center space-x-4">
          {/* Search Input */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by partner, PO number, or filename..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Filter Button */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`btn ${showFilters ? 'btn-primary' : 'btn-secondary'} flex items-center space-x-2`}
          >
            <Filter className="h-5 w-5" />
            <span>Filters</span>
          </button>
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <SearchFilter onFilterChange={handleFilter} />
          </div>
        )}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Failed to load transactions: {error.message}</p>
        </div>
      )}

      {/* Transaction Grid */}
      {!isLoading && !error && (
        <>
          {data?.transactions?.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm p-12 text-center border border-gray-200">
              <p className="text-gray-500 text-lg">No transactions found</p>
              {canCreate && (
                <button
                  onClick={handleCreateClick}
                  className="mt-4 btn btn-primary"
                >
                  Create your first transaction
                </button>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {data?.transactions?.map((transaction) => (
                <TransactionCard
                  key={transaction.id}
                  transaction={transaction}
                  folderType={folderName}
                  onClick={() => handleTransactionClick(transaction.id)}
                />
              ))}
            </div>
          )}

          {/* Pagination */}
          {data?.pagination && data.pagination.total_pages > 1 && (
            <div className="mt-6 flex items-center justify-center space-x-2">
              <button
                disabled={!data.pagination.has_previous}
                className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span className="text-gray-600">
                Page {data.pagination.page} of {data.pagination.total_pages}
              </span>
              <button
                disabled={!data.pagination.has_next}
                className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}

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

export default FolderView;
