import { useState, useEffect, useCallback } from 'react'
import VideoPlayer from '../components/VideoPlayer'
import StatusBadge from '../components/StatusBadge'
import { useVideosPending, useApproveVideo, useRejectVideo } from '../api/hooks'

export default function QueueReview() {
  const { data: videos = [], isLoading } = useVideosPending()
  const approve = useApproveVideo()
  const reject = useRejectVideo()
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [rejectReason, setRejectReason] = useState('')
  const [showRejectDialog, setShowRejectDialog] = useState(false)
  const [reviewed, setReviewed] = useState(0)

  const selected = videos.find((v: any) => v.id === selectedId)

  useEffect(() => {
    if (videos.length > 0 && selectedId === null) {
      setSelectedId(videos[0].id)
    }
  }, [videos, selectedId])

  const selectNext = useCallback(() => {
    const idx = videos.findIndex((v: any) => v.id === selectedId)
    if (idx < videos.length - 1) {
      setSelectedId(videos[idx + 1].id)
    }
  }, [videos, selectedId])

  const handleApprove = () => {
    if (selectedId) {
      approve.mutate(selectedId)
      setReviewed((r) => r + 1)
      selectNext()
    }
  }

  const handleReject = () => {
    if (selectedId && rejectReason) {
      reject.mutate({ id: selectedId, reason: rejectReason })
      setReviewed((r) => r + 1)
      setShowRejectDialog(false)
      setRejectReason('')
      selectNext()
    }
  }

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (showRejectDialog) return
      if (e.key === 'a') handleApprove()
      if (e.key === 'r') setShowRejectDialog(true)
      if (e.key === 'ArrowRight') selectNext()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })

  if (isLoading) return <p className="text-gray-500">Loading...</p>
  if (videos.length === 0) {
    return (
      <div className="text-center py-20">
        <p className="text-lg font-semibold">All done!</p>
        <p className="text-gray-500">No videos pending review</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">QC Review</h1>
        <p className="text-sm text-gray-500">{reviewed} / {videos.length + reviewed} reviewed</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Video list */}
        <div className="space-y-2 max-h-[80vh] overflow-y-auto">
          {videos.map((v: any) => (
            <div
              key={v.id}
              onClick={() => setSelectedId(v.id)}
              className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                v.id === selectedId
                  ? 'border-blue-500 bg-gray-900'
                  : 'border-gray-800 bg-gray-900/50 hover:bg-gray-900'
              }`}
            >
              <p className="text-sm font-medium">Video #{v.id}</p>
              <p className="text-xs text-gray-500">{v.duration_sec?.toFixed(1)}s</p>
              <StatusBadge status={v.status} />
            </div>
          ))}
        </div>

        {/* Player + actions */}
        <div className="md:col-span-2 space-y-4">
          {selected && (
            <>
              <VideoPlayer videoId={selected.id} />

              <div className="flex gap-3">
                <button
                  onClick={handleApprove}
                  disabled={approve.isPending}
                  className="flex-1 py-2 bg-green-600 hover:bg-green-500 rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                  Approve (A)
                </button>
                <button
                  onClick={() => setShowRejectDialog(true)}
                  className="flex-1 py-2 bg-red-600 hover:bg-red-500 rounded-lg font-medium transition-colors"
                >
                  Reject (R)
                </button>
              </div>
            </>
          )}

          {/* Reject dialog */}
          {showRejectDialog && (
            <div className="bg-gray-900 border border-gray-700 rounded-lg p-4 space-y-3">
              <p className="font-medium">Rejection Reason</p>
              <textarea
                value={rejectReason}
                onChange={(e) => setRejectReason(e.target.value)}
                className="w-full bg-gray-800 border border-gray-700 rounded p-2 text-sm"
                rows={3}
                placeholder="Why is this video being rejected?"
                autoFocus
              />
              <div className="flex gap-2">
                <button
                  onClick={handleReject}
                  disabled={!rejectReason}
                  className="px-4 py-1.5 bg-red-600 hover:bg-red-500 rounded text-sm disabled:opacity-50"
                >
                  Confirm Reject
                </button>
                <button
                  onClick={() => { setShowRejectDialog(false); setRejectReason('') }}
                  className="px-4 py-1.5 bg-gray-700 hover:bg-gray-600 rounded text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
