import { useState } from 'react'
import { useProducts, useCreateProduct, useUpdateProduct, useDeleteProduct } from '../api/hooks'

export default function Products() {
  const { data: products = [], isLoading } = useProducts()
  const createProduct = useCreateProduct()
  const updateProduct = useUpdateProduct()
  const deleteProduct = useDeleteProduct()
  const [showAdd, setShowAdd] = useState(false)
  const [newProduct, setNewProduct] = useState({
    name: '', tiktok_shop_url: '', commission_rate: 0,
    affiliate_link: '', utm_campaign: '', approved: false,
  })
  const [editingCell, setEditingCell] = useState<{ id: string; field: string } | null>(null)
  const [editValue, setEditValue] = useState('')

  const handleInlineEdit = (id: string, field: string, value: string | number | boolean) => {
    updateProduct.mutate({ id, [field]: value })
    setEditingCell(null)
  }

  const startEdit = (id: string, field: string, currentValue: string) => {
    setEditingCell({ id, field })
    setEditValue(currentValue)
  }

  const handleAdd = () => {
    createProduct.mutate(newProduct)
    setShowAdd(false)
    setNewProduct({ name: '', tiktok_shop_url: '', commission_rate: 0, affiliate_link: '', utm_campaign: '', approved: false })
  }

  if (isLoading) return <p className="text-gray-500">Loading...</p>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Products</h1>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm transition-colors"
        >
          Add Product
        </button>
      </div>

      {/* Add dialog */}
      {showAdd && (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 space-y-3">
          <input
            value={newProduct.name}
            onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
            placeholder="Product name"
            className="w-full bg-gray-800 border border-gray-700 rounded p-2 text-sm"
          />
          <input
            value={newProduct.tiktok_shop_url}
            onChange={(e) => setNewProduct({ ...newProduct, tiktok_shop_url: e.target.value })}
            placeholder="TikTok Shop URL"
            className="w-full bg-gray-800 border border-gray-700 rounded p-2 text-sm"
          />
          <div className="grid grid-cols-2 gap-3">
            <input
              type="number"
              value={newProduct.commission_rate}
              onChange={(e) => setNewProduct({ ...newProduct, commission_rate: parseFloat(e.target.value) || 0 })}
              placeholder="Commission %"
              min={0} max={100}
              className="bg-gray-800 border border-gray-700 rounded p-2 text-sm"
            />
            <input
              value={newProduct.affiliate_link}
              onChange={(e) => setNewProduct({ ...newProduct, affiliate_link: e.target.value })}
              placeholder="Affiliate link"
              className="bg-gray-800 border border-gray-700 rounded p-2 text-sm"
            />
          </div>
          <div className="flex gap-2">
            <button onClick={handleAdd} disabled={!newProduct.name} className="px-4 py-1.5 bg-green-600 hover:bg-green-500 rounded text-sm disabled:opacity-50">
              Save
            </button>
            <button onClick={() => setShowAdd(false)} className="px-4 py-1.5 bg-gray-700 hover:bg-gray-600 rounded text-sm">
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Products table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-gray-800">
              <th className="pb-2">Name</th>
              <th className="pb-2">Shop URL</th>
              <th className="pb-2">Commission</th>
              <th className="pb-2">Affiliate Link</th>
              <th className="pb-2">Campaign</th>
              <th className="pb-2">Approved</th>
              <th className="pb-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p: any) => (
              <tr key={p.id} className="border-b border-gray-800/50">
                <td className="py-2">
                  {editingCell?.id === p.id && editingCell.field === 'name' ? (
                    <input
                      value={editValue}
                      onChange={(e) => setEditValue(e.target.value)}
                      onBlur={() => handleInlineEdit(p.id, 'name', editValue)}
                      onKeyDown={(e) => e.key === 'Enter' && handleInlineEdit(p.id, 'name', editValue)}
                      className="bg-gray-800 border border-gray-700 rounded px-1 text-sm w-full"
                      autoFocus
                    />
                  ) : (
                    <span onClick={() => startEdit(p.id, 'name', p.name)} className="cursor-pointer hover:text-blue-400">
                      {p.name || '—'}
                    </span>
                  )}
                </td>
                <td className="py-2 max-w-[120px] truncate text-gray-500">{p.tiktok_shop_url || '—'}</td>
                <td className="py-2">
                  <span className={
                    p.commission_rate >= 15 ? 'text-green-400' :
                    p.commission_rate >= 10 ? 'text-yellow-400' : 'text-red-400'
                  }>
                    {p.commission_rate}%
                  </span>
                </td>
                <td className="py-2 max-w-[150px] truncate">
                  {editingCell?.id === p.id && editingCell.field === 'affiliate_link' ? (
                    <input
                      value={editValue}
                      onChange={(e) => setEditValue(e.target.value)}
                      onBlur={() => handleInlineEdit(p.id, 'affiliate_link', editValue)}
                      onKeyDown={(e) => e.key === 'Enter' && handleInlineEdit(p.id, 'affiliate_link', editValue)}
                      className="bg-gray-800 border border-gray-700 rounded px-1 text-sm w-full"
                      autoFocus
                    />
                  ) : (
                    <span onClick={() => startEdit(p.id, 'affiliate_link', p.affiliate_link)} className="cursor-pointer hover:text-blue-400 text-gray-500">
                      {p.affiliate_link || '—'}
                    </span>
                  )}
                </td>
                <td className="py-2 text-gray-500">{p.utm_campaign || '—'}</td>
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
                <td className="py-2">
                  <button
                    onClick={() => {
                      if (confirm('Delete this product?')) deleteProduct.mutate(p.id)
                    }}
                    className="text-xs text-red-400 hover:text-red-300"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
