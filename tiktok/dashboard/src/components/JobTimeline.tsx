import StatusBadge from './StatusBadge'

interface Job {
  name: string
  module: string
  scheduled_time: string
  status: string
  last_run?: string | null
  duration?: number | null
}

interface JobTimelineProps {
  jobs: Job[]
  onRetry?: (jobName: string) => void
}

export default function JobTimeline({ jobs, onRetry }: JobTimelineProps) {
  return (
    <div className="space-y-2">
      {jobs.map((job) => (
        <div
          key={job.name}
          className="flex items-center gap-3 bg-gray-900 border border-gray-800 rounded-lg px-4 py-3"
        >
          <span className="text-sm text-gray-500 w-14 shrink-0">{job.scheduled_time}</span>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{job.name}</p>
            <p className="text-xs text-gray-500">{job.module}</p>
          </div>
          <StatusBadge status={job.status} />
          {job.duration != null && (
            <span className="text-xs text-gray-500">{job.duration.toFixed(1)}s</span>
          )}
          {job.status === 'failed' && onRetry && (
            <button
              onClick={() => onRetry(job.name)}
              className="text-xs px-2 py-1 bg-blue-600 hover:bg-blue-500 rounded transition-colors"
            >
              Retry
            </button>
          )}
        </div>
      ))}
    </div>
  )
}
