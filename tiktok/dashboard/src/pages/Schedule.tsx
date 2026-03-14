import JobTimeline from '../components/JobTimeline'
import { useTodaySchedule, useRunJob } from '../api/hooks'
import { useWebSocket } from '../hooks/useWebSocket'

export default function Schedule() {
  useWebSocket()
  const { data: schedule = [], isLoading } = useTodaySchedule()
  const runJob = useRunJob()

  if (isLoading) return <p className="text-gray-500">Loading schedule...</p>

  const doneCount = schedule.filter((j: any) => j.status === 'done').length
  const failedCount = schedule.filter((j: any) => j.status === 'failed').length
  const runningCount = schedule.filter((j: any) => j.status === 'running').length

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Schedule</h1>

      <div className="flex gap-4 text-sm">
        <span className="text-green-400">{doneCount} done</span>
        <span className="text-blue-400">{runningCount} running</span>
        <span className="text-red-400">{failedCount} failed</span>
        <span className="text-gray-500">{schedule.length - doneCount - failedCount - runningCount} pending</span>
      </div>

      {/* Job table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-gray-800">
              <th className="pb-2">Job</th>
              <th className="pb-2">Module</th>
              <th className="pb-2">Scheduled</th>
              <th className="pb-2">Last Run</th>
              <th className="pb-2">Status</th>
              <th className="pb-2">Duration</th>
              <th className="pb-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map((job: any) => (
              <tr key={job.name} className="border-b border-gray-800/50">
                <td className="py-2 font-medium">{job.name}</td>
                <td className="py-2 text-gray-500">{job.module}</td>
                <td className="py-2">{job.scheduled_time}</td>
                <td className="py-2 text-gray-500 text-xs">{job.last_run || '—'}</td>
                <td className="py-2">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    job.status === 'done' ? 'bg-green-900 text-green-300' :
                    job.status === 'running' ? 'bg-blue-900 text-blue-300 animate-pulse' :
                    job.status === 'failed' ? 'bg-red-900 text-red-300' :
                    'bg-gray-700 text-gray-300'
                  }`}>
                    {job.status}
                  </span>
                </td>
                <td className="py-2 text-gray-500">
                  {job.duration != null ? `${job.duration.toFixed(1)}s` : '—'}
                </td>
                <td className="py-2">
                  <button
                    onClick={() => runJob.mutate(job.name)}
                    disabled={job.status === 'running' || runJob.isPending}
                    className="text-xs px-3 py-1 bg-blue-600 hover:bg-blue-500 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Run Now
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Timeline view */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Timeline</h2>
        <JobTimeline
          jobs={schedule}
          onRetry={(name) => runJob.mutate(name)}
        />
      </div>
    </div>
  )
}
