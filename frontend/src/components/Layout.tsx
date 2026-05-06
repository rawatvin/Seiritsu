import { Outlet, NavLink } from 'react-router-dom'
import { LayoutDashboard, ListTodo, BarChart3, Settings, LogOut, Loader2 } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { authApi, syncApi } from '@/lib/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { cn } from '@/lib/utils'

export default function Layout() {
  const { user, logout } = useAuthStore()

  const { mutate: handleLogout, isLoading: isLoggingOut } = useMutation({
    mutationFn: authApi.logout,
    onSuccess: () => {
      logout()
      toast.success('Logged out successfully')
    },
  })

  const { data: syncStatus } = useQuery({
    queryKey: ['syncStatus'],
    queryFn: syncApi.getStatus,
    refetchInterval: 60000, // Refetch every minute
  })

  const { mutate: triggerSync, isLoading: isSyncing } = useMutation({
    mutationFn: () => syncApi.trigger(),
    onSuccess: () => {
      toast.success('Sync triggered successfully')
    },
  })

  const navigation = [
    { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
    { name: 'Tasks', to: '/tasks', icon: ListTodo },
    { name: 'Analytics', to: '/analytics', icon: BarChart3 },
    { name: 'Settings', to: '/settings', icon: Settings },
  ]

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
        {/* Logo */}
        <div className="h-16 flex items-center px-6 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-900">Task Intelligence</h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                )
              }
            >
              <item.icon className="w-5 h-5" />
              {item.name}
            </NavLink>
          ))}
        </nav>

        {/* Sync Status */}
        {syncStatus && syncStatus.length > 0 && (
          <div className="px-4 py-3 border-t border-gray-200">
            <button
              onClick={() => triggerSync()}
              disabled={isSyncing}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
            >
              {isSyncing ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Syncing...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Sync Now
                </>
              )}
            </button>
            <div className="mt-2 text-xs text-gray-500 text-center">
              {syncStatus.filter(s => s.is_enabled).length} sources enabled
            </div>
          </div>
        )}

        {/* User Profile */}
        <div className="px-4 py-4 border-t border-gray-200">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-semibold">
              {user?.display_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user?.display_name || user?.email}
              </p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
          </div>

          <button
            onClick={() => handleLogout()}
            disabled={isLoggingOut}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors disabled:opacity-50"
          >
            {isLoggingOut ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Logging out...
              </>
            ) : (
              <>
                <LogOut className="w-4 h-4" />
                Logout
              </>
            )}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
