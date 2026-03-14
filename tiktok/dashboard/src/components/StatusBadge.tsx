const colors: Record<string, string> = {
  pending: 'bg-gray-700 text-gray-300',
  running: 'bg-blue-900 text-blue-300 animate-pulse',
  done: 'bg-green-900 text-green-300',
  failed: 'bg-red-900 text-red-300',
  approved: 'bg-green-900 text-green-300',
  rejected: 'bg-red-900 text-red-300',
  pending_review: 'bg-yellow-900 text-yellow-300',
  published: 'bg-purple-900 text-purple-300',
  low: 'bg-green-900 text-green-300',
  medium: 'bg-yellow-900 text-yellow-300',
  high: 'bg-red-900 text-red-300',
}

interface StatusBadgeProps {
  status: string
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const cls = colors[status] || 'bg-gray-700 text-gray-300'
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${cls}`}>
      {status.replace('_', ' ')}
    </span>
  )
}
