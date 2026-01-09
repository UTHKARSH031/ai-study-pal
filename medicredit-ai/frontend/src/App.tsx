import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import PatientPortal from './pages/PatientPortal'
import ProviderDashboard from './pages/ProviderDashboard'
import Layout from './components/Layout'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/patient" replace />} />
          <Route path="/patient/*" element={<PatientPortal />} />
          <Route path="/provider/*" element={<ProviderDashboard />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

