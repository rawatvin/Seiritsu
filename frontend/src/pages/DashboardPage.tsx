import { useQuery } from '@tanstack/react-query'
import { analyticsApi, taskApi } from '@/lib/api'
import LoadingSpinner from '@/components/LoadingSpinner'
import { AlertCircle, CheckCircle2, Clock, TrendingUp, Calendar } from 'lucide-react'
import { formatDate, getStatusColor, getPriorityColor, getStatusLabel, getPriorityLabel } from '@/lib/utils'
import { Link } from 'react-router-dom'

export default function DashboardPage() {
  const { data: summary, isLoading } = useQuery({
    queryKey: ['dashboardSummary'],
    queryFn: analyticsApi.getSummary,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!summary) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-500">No data available</p>
      </div>
    )
  }

  const stats = [
    {
      label: 'Active Tasks',
      value: summary.active_tasks,
      icon: Clock,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Completed This Week',
      value: summary.completed_this_week,
      icon: CheckCircle2,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      label: 'Overdue',
      value: summary.overdue_tasks,
      icon: AlertCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
    },
    {
      label: 'Total Tasks',
      value: summary.total_tasks,
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
  ]

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Overview of your tasks and productivity</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
              <span className={`text-3xl font-bold ${stat.color}`}>{stat.value}</span>
            </div>
            <p className="text-sm font-medium text-gray-600">{stat.label}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Tasks by Status */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Tasks by Status</h2>
          <div className="space-y-3">
            {Object.entries(summary.tasks_by_status).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(status)}`}>
                    {getStatusLabel(status)}
                  </span>
                </div>
                <span className="text-lg font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Tasks by Priority */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Tasks by Priority</h2>
          <div className="space-y-3">
            {Object.entries(summary.tasks_by_priority).map(([priority, count]) => (
              <div key={priority} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(priority)}`}>
                    {getPriorityLabel(priority)}
                  </span>
                </div>
                <span className="text-lg font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Tasks by Source */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Tasks by Source</h2>
          <div className="space-y-3">
            {Object.entries(summary.tasks_by_source).map(([source, count]) => (
              <div key={source} className="flex items-center justify-between">
                <span className="text-sm text-gray-700 capitalize">{source.replace('_', ' ')}</span>
                <span className="text-lg font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Upcoming Deadlines */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Upcoming Deadlines</h2>
            <Calendar className="w-5 h-5 text-gray-400" />
          </div>
          <div className="space-y-3">
            {summary.upcoming_deadlines.length === 0 ? (
              <p className="text-sm text-gray-500">No upcoming deadlines</p>
            ) : (
              summary.upcoming_deadlines.map((task) => (
                <div key={task.id} className="flex items-start justify-between gap-2 pb-3 border-b border-gray-100 last:border-0">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{task.title}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full border ${getPriorityColor(task.priority)}`}>
                        {getPriorityLabel(task.priority)}
                      </span>
                      <span className="text-xs text-gray-500">
                        {formatDate(task.deadline)}
                      </span>
                    </div>
                  </div>
                  <span className="text-xs font-medium text-gray-600 whitespace-nowrap">
                    {task.days_until === 0 ? 'Today' : `${task.days_until}d`}
                  </span>
                </div>
              ))
            )}
          </div>
          {summary.upcoming_deadlines.length > 0 && (
            <Link
              to="/tasks"
              className="mt-4 block text-center text-sm font-medium text-primary hover:text-primary/80"
            >
              View all tasks →
            </Link>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl shadow-lg p-6 text-white">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to="/tasks"
            className="flex items-center gap-3 p-4 bg-white/10 backdrop-blur-sm rounded-lg hover:bg-white/20 transition-colors"
          >
            <div className="p-2 bg-white/20 rounded-lg">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </div>
            <div>
              <p className="font-medium">Create Task</p>
              <p className="text-xs text-white/80">Add a new task manually</p>
            </div>
          </Link>

          <Link
            to="/analytics"
            className="flex items-center gap-3 p-4 bg-white/10 backdrop-blur-sm rounded-lg hover:bg-white/20 transition-colors"
          >
            <div className="p-2 bg-white/20 rounded-lg">
              <TrendingUp className="w-5 h-5" />
            </div>
            <div>
              <p className="font-medium">View Analytics</p>
              <p className="text-xs text-white/80">See insights and trends</p>
            </div>
          </Link>

          <Link
            to="/settings"
            className="flex items-center gap-3 p-4 bg-white/10 backdrop-blur-sm rounded-lg hover:bg-white/20 transition-colors"
          >
            <div className="p-2 bg-white/20 rounded-lg">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </div>
            <div>
              <p className="font-medium">Configure Sync</p>
              <p className="text-xs text-white/80">Manage data sources</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
}
