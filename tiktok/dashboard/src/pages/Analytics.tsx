import { useState } from 'react'
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import MetricCard from '../components/MetricCard'
import { useWeeklyAnalytics } from '../api/hooks'

export default function Analytics() {
  const [week, setWeek] = useState('current')
  const { data: report, isLoading } = useWeeklyAnalytics(week)

  if (isLoading) return <p className="text-gray-500">Loading analytics...</p>
  if (!report) return <p className="text-gray-500">No analytics data available</p>

  // Mock chart data from report
  const viewsData = [
    { day: 'Mon', tiktok: 1200, reels: 400, shorts: 300 },
    { day: 'Tue', tiktok: 1800, reels: 600, shorts: 450 },
    { day: 'Wed', tiktok: 2200, reels: 800, shorts: 500 },
    { day: 'Thu', tiktok: 1600, reels: 500, shorts: 400 },
    { day: 'Fri', tiktok: 2500, reels: 900, shorts: 600 },
  ]

  const gmvData = report.top_3_videos?.map((v: any, i: number) => ({
    name: `Video ${v.published_video_id}`,
    gmv: v.gmv,
  })) || []

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Analytics</h1>
        <p className="text-sm text-gray-500">{report.period}</p>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <MetricCard label="Total Views" value={report.total_views?.toLocaleString()} />
        <MetricCard label="Total GMV" value={`฿${report.total_gmv?.toLocaleString()}`} />
        <MetricCard label="Avg CTR" value={`${(report.avg_ctr * 100).toFixed(1)}%`} />
        <MetricCard label="Videos Published" value={report.videos_published} />
        <MetricCard label="Total Likes" value={report.total_likes?.toLocaleString()} />
      </div>

      {/* Views chart */}
      <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
        <h3 className="font-semibold mb-4">Views Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={viewsData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="day" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }} />
            <Area type="monotone" dataKey="tiktok" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.2} />
            <Area type="monotone" dataKey="reels" stroke="#EC4899" fill="#EC4899" fillOpacity={0.2} />
            <Area type="monotone" dataKey="shorts" stroke="#EF4444" fill="#EF4444" fillOpacity={0.2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* GMV per video */}
      {gmvData.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
          <h3 className="font-semibold mb-4">GMV per Video</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={gmvData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }} />
              <Bar dataKey="gmv" fill="#10B981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Top videos table */}
      <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
        <h3 className="font-semibold mb-3">Top Videos</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-gray-800">
              <th className="pb-2">Video</th>
              <th className="pb-2">Views</th>
              <th className="pb-2">CTR</th>
              <th className="pb-2">GMV</th>
              <th className="pb-2">Winner</th>
            </tr>
          </thead>
          <tbody>
            {report.top_3_videos?.map((v: any, i: number) => (
              <tr key={i} className={`border-b border-gray-800/50 ${v.winner ? 'bg-green-900/10' : ''}`}>
                <td className="py-2">Video {v.published_video_id}</td>
                <td className="py-2">{v.views?.toLocaleString()}</td>
                <td className="py-2">{(v.ctr * 100).toFixed(1)}%</td>
                <td className="py-2">฿{v.gmv?.toLocaleString()}</td>
                <td className="py-2">{v.winner ? '★' : ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
