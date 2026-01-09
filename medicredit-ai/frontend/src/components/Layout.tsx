import { Link, useLocation } from 'react-router-dom'
import { Activity, Users } from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const isPatient = location.pathname.startsWith('/patient')
  const isProvider = location.pathname.startsWith('/provider')

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">MediCredit AI</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/patient"
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  isPatient
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Users className="h-4 w-4 mr-2" />
                Patient Portal
              </Link>
              <Link
                to="/provider"
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  isProvider
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Activity className="h-4 w-4 mr-2" />
                Provider Dashboard
              </Link>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}

