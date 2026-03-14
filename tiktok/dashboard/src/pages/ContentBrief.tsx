import { useState } from 'react'
import StatusBadge from '../components/StatusBadge'
import { useTodayBrief, useApproveBrief, useProducts, useUpdateProduct } from '../api/hooks'

export default function ContentBrief() {
  const { data: brief, isLoading, error } = useTodayBrief()
  const { data: products = [] } = useProducts()
  const approveBrief = useApproveBrief()
  const updateProduct = useUpdateProduct()
  const [selectedIdeas, setSelectedIdeas] = useState<Set<number>>(new Set())

  const toggleIdea = (idx: number) => {
    const next = new Set(selectedIdeas)
    next.has(idx) ? next.delete(idx) : next.add(idx)
    setSelectedIdeas(next)
  }

  const handleConfirm = () => {
    approveBrief.mutate(Array.from(selectedIdeas))
  }

  if (isLoading) return <p className="text-gray-500">Loading brief...</p>
  if (error) return <p className="text-gray-500">No brief available for today</p>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Content Brief</h1>
        <p className="text-sm text-gray-500">{brief?.date}</p>
      </div>

      {brief?.human_approved && (
        <div className="bg-green-900/30 border border-green-800 rounded-lg p-3 text-sm">
          Brief approved at {brief.approved_at}
        </div>
      )}

      {/* Ideas */}
      <div className="space-y-3">
        {brief?.ideas?.map((idea: any, idx: number) => (
          <div
            key={idx}
            className={`bg-gray-900 border rounded-lg p-4 cursor-pointer transition-colors ${
              selectedIdeas.has(idx) ? 'border-blue-500' : 'border-gray-800'
            }`}
            onClick={() => toggleIdea(idx)}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-bold text-blue-400">#{idea.rank}</span>
                  <span className="font-medium">{idea.product_name}</span>
                  <StatusBadge status={idea.estimated_difficulty || 'medium'} />
                </div>
                <p className="text-sm text-gray-300">{idea.angle}</p>
                <p className="text-sm text-gray-500 mt-1">Hook: {idea.hook_idea}</p>
                <div className="flex gap-1 mt-2 flex-wrap">
                  {idea.hashtags?.map((h: string) => (
                    <span key={h} className="text-xs bg-gray-800 px-2 py-0.5 rounded">#{h}</span>
                  ))}
                </div>
              </div>
              <div className={`w-5 h-5 rounded border-2 flex items-center justify-center shrink-0 ${
                selectedIdeas.has(idx) ? 'bg-blue-600 border-blue-600' : 'border-gray-600'
              }`}>
                {selectedIdeas.has(idx) && <span className="text-xs">✓</span>}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Product approval table */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Products</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500 border-b border-gray-800">
                <th className="pb-2">Name</th>
                <th className="pb-2">Commission</th>
                <th className="pb-2">Affiliate Link</th>
                <th className="pb-2">Approved</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p: any) => (
                <tr key={p.id} className="border-b border-gray-800/50">
                  <td className="py-2">{p.name || '—'}</td>
                  <td className="py-2">
                    <span className={
                      p.commission_rate >= 15 ? 'text-green-400' :
                      p.commission_rate >= 10 ? 'text-yellow-400' : 'text-red-400'
                    }>
                      {p.commission_rate}%
                    </span>
                  </td>
                  <td className="py-2 max-w-xs truncate text-gray-500">{p.affiliate_link || '—'}</td>
                  <td className="py-2">
                    <button
                      onClick={() => updateProduct.mutate({ id: p.id, approved: !p.approved })}
                      className={`px-2 py-0.5 rounded text-xs ${
                        p.approved ? 'bg-green-900 text-green-300' : 'bg-gray-800 text-gray-500'
                      }`}
                    >
                      {p.approved ? 'Yes' : 'No'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Confirm button */}
      <button
        onClick={handleConfirm}
        disabled={selectedIdeas.size === 0 || approveBrief.isPending}
        className="w-full py-3 bg-blue-600 hover:bg-blue-500 rounded-lg font-medium transition-colors disabled:opacity-50"
      >
        Confirm Brief ({selectedIdeas.size} ideas selected)
      </button>
    </div>
  )
}
