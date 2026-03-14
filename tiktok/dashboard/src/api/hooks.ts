import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import client from './client'

// Videos
export function useVideosPending() {
  return useQuery({
    queryKey: ['videos', 'pending'],
    queryFn: () => client.get('/api/videos/pending').then((r) => r.data),
  })
}

export function useApproveVideo() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => client.post(`/api/videos/${id}/approve`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['videos'] }),
  })
}

export function useRejectVideo() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, reason }: { id: number; reason: string }) =>
      client.post(`/api/videos/${id}/reject`, { reason }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['videos'] }),
  })
}

// Brief
export function useTodayBrief() {
  return useQuery({
    queryKey: ['brief', 'today'],
    queryFn: () => client.get('/api/brief/today').then((r) => r.data),
    retry: false,
  })
}

export function useApproveBrief() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (ideaIds: number[]) =>
      client.post('/api/brief/approve', { idea_ids: ideaIds }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['brief'] }),
  })
}

// Analytics
export function useWeeklyAnalytics(week = 'current') {
  return useQuery({
    queryKey: ['analytics', 'weekly', week],
    queryFn: () => client.get('/api/analytics/weekly', { params: { week } }).then((r) => r.data),
  })
}

export function useVideoMetrics(videoId: number) {
  return useQuery({
    queryKey: ['analytics', 'video', videoId],
    queryFn: () => client.get(`/api/analytics/video/${videoId}`).then((r) => r.data),
    enabled: videoId > 0,
  })
}

// Products
export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => client.get('/api/products').then((r) => r.data),
  })
}

export function useCreateProduct() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: Record<string, unknown>) => client.post('/api/products', data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['products'] }),
  })
}

export function useUpdateProduct() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, ...data }: { id: string } & Record<string, unknown>) =>
      client.put(`/api/products/${id}`, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['products'] }),
  })
}

export function useDeleteProduct() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => client.delete(`/api/products/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['products'] }),
  })
}

// Schedule
export function useTodaySchedule() {
  return useQuery({
    queryKey: ['schedule', 'today'],
    queryFn: () => client.get('/api/schedule/today').then((r) => r.data),
    refetchInterval: 10_000,
  })
}

export function useRunJob() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (jobName: string) => client.post(`/api/schedule/run/${jobName}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['schedule'] }),
  })
}
