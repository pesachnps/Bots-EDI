import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { transactionApi, folderApi, partnerApi, documentTypeApi } from '../services/api';

// Query keys
export const queryKeys = {
  transactions: (params) => ['transactions', params],
  transaction: (id) => ['transaction', id],
  transactionHistory: (id) => ['transaction', id, 'history'],
  transactionRaw: (id) => ['transaction', id, 'raw'],
  folders: ['folders'],
  folderStats: (folder) => ['folder', folder, 'stats'],
  partners: ['partners'],
  documentTypes: ['documentTypes'],
};

// Transactions hooks
export function useTransactions(params = {}) {
  return useQuery({
    queryKey: queryKeys.transactions(params),
    queryFn: () => transactionApi.list(params).then(res => res.data),
  });
}

export function useTransactionsByFolder(folder, params = {}) {
  return useQuery({
    queryKey: queryKeys.transactions({ folder, ...params }),
    queryFn: () => transactionApi.listByFolder(folder, params).then(res => res.data),
  });
}

export function useTransaction(id) {
  return useQuery({
    queryKey: queryKeys.transaction(id),
    queryFn: () => transactionApi.get(id).then(res => res.data.transaction),
    enabled: !!id,
  });
}

export function useTransactionHistory(id) {
  return useQuery({
    queryKey: queryKeys.transactionHistory(id),
    queryFn: () => transactionApi.history(id).then(res => res.data.history),
    enabled: !!id,
  });
}

export function useTransactionRaw(id) {
  return useQuery({
    queryKey: queryKeys.transactionRaw(id),
    queryFn: () => transactionApi.raw(id).then(res => res.data),
    enabled: !!id,
  });
}

// Mutation hooks
export function useCreateTransaction() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data) => transactionApi.create(data).then(res => res.data),
    onSuccess: () => {
      // Invalidate all transaction queries
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['folders'] });
    },
  });
}

export function useUpdateTransaction() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }) => transactionApi.update(id, data).then(res => res.data),
    onSuccess: (data, variables) => {
      // Invalidate specific transaction and list queries
      queryClient.invalidateQueries({ queryKey: queryKeys.transaction(variables.id) });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
    },
  });
}

export function useMoveTransaction() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, targetFolder }) => transactionApi.move(id, targetFolder).then(res => res.data),
    onSuccess: () => {
      // Invalidate all transaction and folder queries
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['folders'] });
    },
  });
}

export function useSendTransaction() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id) => transactionApi.send(id).then(res => res.data),
    onSuccess: () => {
      // Invalidate all transaction and folder queries
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['folders'] });
    },
  });
}

export function useProcessTransaction() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id) => transactionApi.process(id).then(res => res.data),
    onSuccess: () => {
      // Invalidate all transaction and folder queries
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['folders'] });
    },
  });
}

export function useValidateTransaction(id) {
  return useQuery({
    queryKey: ['transaction', id, 'validation'],
    queryFn: () => transactionApi.validate(id).then(res => res.data),
    enabled: !!id,
  });
}

export function useDeleteTransaction() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id) => transactionApi.delete(id).then(res => res.data),
    onSuccess: () => {
      // Invalidate all transaction and folder queries
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['folders'] });
    },
  });
}

export function usePermanentDeleteTransaction() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id) => transactionApi.permanentDelete(id).then(res => res.data),
    onSuccess: () => {
      // Invalidate all transaction and folder queries
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['folders'] });
    },
  });
}

// Folder hooks
export function useFolders() {
  return useQuery({
    queryKey: queryKeys.folders,
    queryFn: () => folderApi.list().then(res => res.data.folders),
  });
}

export function useFolderStats(folder) {
  return useQuery({
    queryKey: queryKeys.folderStats(folder),
    queryFn: () => folderApi.stats(folder).then(res => res.data),
    enabled: !!folder,
  });
}

// Partner hooks
export function usePartners() {
  return useQuery({
    queryKey: queryKeys.partners,
    queryFn: () => partnerApi.list().then(res => res.data.partners),
  });
}

// Document type hooks
export function useDocumentTypes() {
  return useQuery({
    queryKey: queryKeys.documentTypes,
    queryFn: () => documentTypeApi.list().then(res => res.data.document_types),
  });
}
