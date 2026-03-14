import { useNavigate } from 'react-router-dom'
import MetricCard from '../components/MetricCard'
import JobTimeline from '../components/JobTimeline'
import { useVideosPending, useTodaySchedule, useRunJob, useWeeklyAnalytics } from '../api/hooks'
import { useWebSocket } from '../hooks/useWebSocket'

export default function Dashboard() {
  useWebSocket()
  const { data: pending = [] } = useVideosPending()
  const { data: schedule = [] } = useTodaySchedule()
  const { data: weekly } = useWeeklyAnalytics()
  const runJob = useRunJob()
  const navigate = useNavigate()

  const approvedToday = 0 // Would come from a dedicated endpoint
  const publishedToday = 0
  const gmvToday = weekly?.total_gmv ?? 0

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Metric cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard label="In Queue" value={pending.length} sub="pending QC" />
        <MetricCard label="Approved Today" value={approvedToday} />
        <MetricCard label="Published Today" value={publishedToday} />
        <MetricCard label="Est. GMV" value={`฿${gmvToday.toLocaleString()}`} />
      </div>

      {/* Next action card */}
      {pending.length > 0 && (
        <div
          onClick={() => navigate('/review')}
          className="bg-blue-900/30 border border-blue-800 rounded-lg p-4 cursor-pointer hover:bg-blue-900/50 transition-colors"
        >
          <p className="font-semibold">QC Review Ready</p>
          <p className="text-sm text-gray-400">{pending.length} videos waiting for review</p>
        </div>
      )}

      {/* Pipeline timeline */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Today's Pipeline</h2>
        <JobTimeline
          jobs={schedule}
          onRetry={(name) => runJob.mutate(name)}
        />
      </div>
    </div>
  )
}
