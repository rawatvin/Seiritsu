import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { taskApi } from '@/lib/api'
import { Plus, Search, Filter } from 'lucide-react'
import LoadingSpinner from '@/components/LoadingSpinner'
import TaskCard from '@/components/TaskCard'
import CreateTaskModal from '@/components/CreateTaskModal'
import TaskDetailModal from '@/components/TaskDetailModal'
import type { Task, TaskStatus } from '@/types'
import toast from 'react-hot-toast'
import { cn, debounce } from '@/lib/utils'

const COLUMNS: { id: TaskStatus; label: string; color: string }[] = [
  { id: 'backlog', label: 'Backlog', color: 'bg-gray-100' },
  { id: 'todo', label: 'To Do', color: 'bg-blue-100' },
  { id: 'in_progress', label: 'In Progress', color: 'bg-purple-100' },
  { id: 'review', label: 'Review', color: 'bg-yellow-100' },
  { id: 'completed', label: 'Completed', color: 'bg-green-100' },
]

export default function KanbanPage() {
  const queryClient = useQueryClient()
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [showFilters, setShowFilters] = useState(false)

  const { data: tasksData, isLoading } = useQuery({
    queryKey: ['tasks', { search: searchQuery }],
    queryFn: () =>
      taskApi.list({
        search: searchQuery || undefined,
        page_size: 100,
        sort_by: 'auto_priority_score',
        sort_order: 'desc',
      }),
  })

  const { mutate: updateTaskStatus } = useMutation({
    mutationFn: ({ taskId, status }: { taskId: string; status: TaskStatus }) =>
      taskApi.updateStatus(taskId, status),
    onSuccess: () => {
      queryClient.invalidateQueries(['tasks'])
      queryClient.invalidateQueries(['dashboardSummary'])
      toast.success('Task updated successfully')
    },
  })

  const tasks = tasksData?.tasks || []

  const tasksByStatus = COLUMNS.reduce((acc, column) => {
    acc[column.id] = tasks.filter((task) => task.status === column.id)
    return acc
  }, {} as Record<TaskStatus, Task[]>)

  const handleSearch = debounce((value: string) => {
    setSearchQuery(value)
  }, 300)

  const handleDragStart = (e: React.DragEvent, task: Task) => {
    e.dataTransfer.setData('taskId', task.id)
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
  }

  const handleDrop = (e: React.DragEvent, status: TaskStatus) => {
    e.preventDefault()
    const taskId = e.dataTransfer.getData('taskId')
    const task = tasks.find((t) => t.id === taskId)

    if (task && task.status !== status) {
      updateTaskStatus({ taskId, status })
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-8 py-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
            <p className="text-sm text-gray-600 mt-1">{tasks.length} total tasks</p>
          </div>

          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Task
          </button>
        </div>

        {/* Search and Filters */}
        <div className="flex items-center gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search tasks..."
              onChange={(e) => handleSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className={cn(
              'flex items-center gap-2 px-4 py-2 border rounded-lg transition-colors',
              showFilters
                ? 'bg-primary text-white border-primary'
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            )}
          >
            <Filter className="w-4 h-4" />
            Filters
          </button>
        </div>
      </div>

      {/* Kanban Board */}
      <div className="flex-1 overflow-x-auto overflow-y-hidden">
        <div className="h-full p-6 flex gap-4 min-w-max">
          {COLUMNS.map((column) => {
            const columnTasks = tasksByStatus[column.id] || []

            return (
              <div
                key={column.id}
                className="flex-shrink-0 w-80 flex flex-col bg-white rounded-xl shadow-sm border border-gray-200"
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, column.id)}
              >
                {/* Column Header */}
                <div className="px-4 py-3 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={cn('w-3 h-3 rounded-full', column.color)} />
                      <h3 className="font-semibold text-gray-900">{column.label}</h3>
                    </div>
                    <span className="text-sm font-medium text-gray-500">
                      {columnTasks.length}
                    </span>
                  </div>
                </div>

                {/* Column Tasks */}
                <div className="flex-1 p-3 space-y-3 overflow-y-auto">
                  {columnTasks.length === 0 ? (
                    <div className="flex items-center justify-center h-32 text-sm text-gray-400">
                      No tasks
                    </div>
                  ) : (
                    columnTasks.map((task) => (
                      <TaskCard
                        key={task.id}
                        task={task}
                        onDragStart={(e) => handleDragStart(e, task)}
                        onClick={() => setSelectedTask(task)}
                      />
                    ))
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Modals */}
      {isCreateModalOpen && (
        <CreateTaskModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
        />
      )}

      {selectedTask && (
        <TaskDetailModal
          task={selectedTask}
          isOpen={!!selectedTask}
          onClose={() => setSelectedTask(null)}
        />
      )}
    </div>
  )
}
