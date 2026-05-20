import { Routes, Route, Navigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/store/authStore'
import { authApi } from '@/lib/api'

// Pages
import LoginPage from '@/pages/LoginPage'
import AuthCallbackPage from '@/pages/AuthCallbackPage'
import DashboardPage from '@/pages/DashboardPage'
import KanbanPage from '@/pages/KanbanPage'
import AnalyticsPage from '@/pages/AnalyticsPage'
import SettingsPage from '@/pages/SettingsPage'

// Components
import Layout from '@/components/Layout'
import LoadingSpinner from '@/components/LoadingSpinner'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, setUser } = useAuthStore()

  const { isLoading } = useQuery({
    queryKey: ['currentUser'],
    queryFn: authApi.getCurrentUser,
    enabled: isAuthenticated,
    onSuccess: (user) => {
      setUser(user)
    },
    onError: () => {
      useAuthStore.getState().logout()
    },
    retry: false,
  })

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return <>{children}</>
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/auth/callback" element={<AuthCallbackPage />} />

      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="tasks" element={<KanbanPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
