import { Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import QueueReview from './pages/QueueReview'
import ContentBrief from './pages/ContentBrief'
import Analytics from './pages/Analytics'
import Products from './pages/Products'
import Schedule from './pages/Schedule'

const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/review', label: 'QC Review' },
  { path: '/brief', label: 'Content Brief' },
  { path: '/analytics', label: 'Analytics' },
  { path: '/products', label: 'Products' },
  { path: '/schedule', label: 'Schedule' },
]

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <nav className="bg-gray-900 border-b border-gray-800 px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center gap-1 overflow-x-auto">
          <span className="font-bold text-lg mr-4 shrink-0">TikTok Auto</span>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `px-3 py-1.5 rounded-md text-sm whitespace-nowrap transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
                }`
              }
              end={item.path === '/'}
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </nav>

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/review" element={<QueueReview />} />
          <Route path="/brief" element={<ContentBrief />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/products" element={<Products />} />
          <Route path="/schedule" element={<Schedule />} />
        </Routes>
      </main>
    </div>
  )
}
