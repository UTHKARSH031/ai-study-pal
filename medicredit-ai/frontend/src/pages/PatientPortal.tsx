import { useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import CostEstimator from '../components/patient/CostEstimator'
import BillAnalysis from '../components/patient/BillAnalysis'
import AssistanceFinder from '../components/patient/AssistanceFinder'
import RiskDashboard from '../components/patient/RiskDashboard'

export default function PatientPortal() {
  const [activeTab, setActiveTab] = useState('estimate')

  const tabs = [
    { id: 'estimate', label: 'Cost Estimator', component: CostEstimator },
    { id: 'bill', label: 'Bill Analysis', component: BillAnalysis },
    { id: 'assistance', label: 'Find Assistance', component: AssistanceFinder },
    { id: 'risk', label: 'Risk Dashboard', component: RiskDashboard },
  ]

  const ActiveComponent = tabs.find(t => t.id === activeTab)?.component || CostEstimator

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Patient Portal</h1>
        <p className="text-gray-600">Navigate healthcare costs with AI-powered insights</p>
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

