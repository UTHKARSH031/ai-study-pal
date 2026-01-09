import { useState } from 'react'
import DenialRiskScorer from '../components/provider/DenialRiskScorer'
import ClaimQA from '../components/provider/ClaimQA'
import RevenueAnalytics from '../components/provider/RevenueAnalytics'
import CodingRecommendations from '../components/provider/CodingRecommendations'

export default function ProviderDashboard() {
  const [activeTab, setActiveTab] = useState('denial')

  const tabs = [
    { id: 'denial', label: 'Denial Risk Scorer', component: DenialRiskScorer },
    { id: 'qa', label: 'Claim QA', component: ClaimQA },
    { id: 'analytics', label: 'Revenue Analytics', component: RevenueAnalytics },
    { id: 'coding', label: 'Coding Recommendations', component: CodingRecommendations },
  ]

  const ActiveComponent = tabs.find(t => t.id === activeTab)?.component || DenialRiskScorer

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Provider Dashboard</h1>
        <p className="text-gray-600">Optimize billing and reduce claim denials</p>
      </div>

      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <ActiveComponent />
    </div>
  )
}

