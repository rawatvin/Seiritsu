import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { taskApi } from '@/lib/api'
import {
  X,
  Loader2,
  Calendar,
  Clock,
  Tag,
  Trash2,
  Edit2,
  Save,
  Sparkles,
  ExternalLink,
  User,
} from 'lucide-react'
import type { Task, TaskUpdate, TaskPriority, TaskStatus } from '@/types'
import toast from 'react-hot-toast'
import {
  cn,
  formatDate,
  formatDateTime,
  formatRelativeTime,
  getPriorityColor,
  getStatusColor,
  getStatusLabel,
  getPriorityLabel,
} from '@/lib/utils'

interface TaskDetailModalProps {
  task: Task
  isOpen: boolean
  onClose: () => void
}

export default function TaskDetailModal({ task, isOpen, onClose }: TaskDetailModalProps) {
  const queryClient = useQueryClient()
  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState<TaskUpdate>({
    title: task.title,
    description: task.description,
    status: task.status,
    priority: task.priority,
    deadline: task.deadline,
    estimated_hours: task.estimated_hours,
    actual_hours: task.actual_hours,
    category: task.category,
    tags: task.tags,
  })

  const { mutate: updateTask, isLoading: isUpdating } = useMutation({
    mutationFn: (updates: TaskUpdate) => taskApi.update(task.id, updates),
    onSuccess: () => {
      queryClient.invalidateQueries(['tasks'])
      queryClient.invalidateQueries(['dashboardSummary'])
      toast.success('Task updated successfully!')
      setIsEditing(false)
    },
  })

  const { mutate: deleteTask, isLoading: isDeleting } = useMutation({
    mutationFn: () => taskApi.delete(task.id),
    onSuccess: () => {
      queryClient.invalidateQueries(['tasks'])
      queryClient.invalidateQueries(['dashboardSummary'])
      toast.success('Task deleted successfully!')
      onClose()
    },
  })

  const handleSave = () => {
    if (!editData.title?.trim()) {
      toast.error('Title cannot be empty')
      return
    }
    updateTask(editData)
  }

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      deleteTask()
    }
  }

  const handleChange = (field: keyof TaskUpdate, value: any) => {
    setEditData((prev) => ({ ...prev, [field]: value }))
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              {isEditing ? (
                <input
                  type="text"
                  value={editData.title}
                  onChange={(e) => handleChange('title', e.target.value)}
                  className="w-full text-xl font-semibold text-gray-900 border-b-2 border-primary focus:outline-none"
                  autoFocus
                />
              ) : (
                <h2 className="text-xl font-semibold text-gray-900">{task.title}</h2>
              )}

              <div className="flex items-center gap-2 mt-2">
                <span className={cn('px-3 py-1 rounded-full text-xs font-medium border', getStatusColor(task.status))}>
                  {getStatusLabel(task.status)}
                </span>
                <span className={cn('px-3 py-1 rounded-full text-xs font-medium border', getPriorityColor(task.priority))}>
                  {getPriorityLabel(task.priority)}
                </span>
                {task.ai_extracted && (
                  <span className="flex items-center gap-1 px-2 py-1 bg-purple-50 text-purple-700 rounded-full text-xs">
                    <Sparkles className="w-3 h-3" />
                    AI Extracted
                  </span>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2">
              {isEditing ? (
                <>
                  <button
                    onClick={() => setIsEditing(false)}
                    className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                  <button
                    onClick={handleSave}
                    disabled={isUpdating}
                    className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors disabled:opacity-50"
                  >
                    {isUpdating ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
                  </button>
                </>
              ) : (
                <>
                  <button
                    onClick={() => setIsEditing(true)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                  >
                    <Edit2 className="w-5 h-5" />
                  </button>
                  <button
                    onClick={handleDelete}
                    disabled={isDeleting}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                  >
                    {isDeleting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Trash2 className="w-5 h-5" />}
                  </button>
                  <button
                    onClick={onClose}
                    className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
            {isEditing ? (
              <textarea
                value={editData.description || ''}
                onChange={(e) => handleChange('description', e.target.value)}
                rows={6}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                placeholder="Add a description..."
              />
            ) : (
              <p className="text-gray-700 whitespace-pre-wrap">
                {task.description || <span className="text-gray-400 italic">No description</span>}
              </p>
            )}
          </div>

          {/* Metadata Grid */}
          <div className="grid grid-cols-2 gap-4">
            {/* Status */}
            {isEditing && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                <select
                  value={editData.status}
                  onChange={(e) => handleChange('status', e.target.value as TaskStatus)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="backlog">Backlog</option>
                  <option value="todo">To Do</option>
                  <option value="in_progress">In Progress</option>
                  <option value="blocked">Blocked</option>
                  <option value="review">Review</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
            )}

            {/* Priority */}
            {isEditing && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select
                  value={editData.priority}
                  onChange={(e) => handleChange('priority', e.target.value as TaskPriority)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
            )}

            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              {isEditing ? (
                <input
                  type="text"
                  value={editData.category || ''}
                  onChange={(e) => handleChange('category', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="e.g., Development"
                />
              ) : (
                <div className="flex items-center gap-2 text-gray-700">
                  <Tag className="w-4 h-4 text-gray-400" />
                  {task.category || <span className="text-gray-400 italic">No category</span>}
                </div>
              )}
            </div>

            {/* Deadline */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Deadline</label>
              {isEditing ? (
                <input
                  type="datetime-local"
                  value={editData.deadline || ''}
                  onChange={(e) => handleChange('deadline', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                />
              ) : (
                <div className="flex items-center gap-2 text-gray-700">
                  <Calendar className="w-4 h-4 text-gray-400" />
                  {task.deadline ? formatDateTime(task.deadline) : <span className="text-gray-400 italic">No deadline</span>}
                </div>
              )}
            </div>

            {/* Estimated Hours */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Estimated Hours</label>
              {isEditing ? (
                <input
                  type="number"
                  value={editData.estimated_hours || ''}
                  onChange={(e) => handleChange('estimated_hours', e.target.value ? parseInt(e.target.value) : undefined)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Hours"
                  min="1"
                />
              ) : (
                <div className="flex items-center gap-2 text-gray-700">
                  <Clock className="w-4 h-4 text-gray-400" />
                  {task.estimated_hours ? `${task.estimated_hours}h` : <span className="text-gray-400 italic">Not set</span>}
                </div>
              )}
            </div>

            {/* Actual Hours */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Actual Hours</label>
              {isEditing ? (
                <input
                  type="number"
                  value={editData.actual_hours || ''}
                  onChange={(e) => handleChange('actual_hours', e.target.value ? parseInt(e.target.value) : undefined)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Hours"
                  min="0"
                />
              ) : (
                <div className="flex items-center gap-2 text-gray-700">
                  <Clock className="w-4 h-4 text-gray-400" />
                  {task.actual_hours ? `${task.actual_hours}h` : <span className="text-gray-400 italic">Not tracked</span>}
                </div>
              )}
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
            {isEditing ? (
              <input
                type="text"
                value={editData.tags?.join(', ') || ''}
                onChange={(e) =>
                  handleChange(
                    'tags',
                    e.target.value.split(',').map((t) => t.trim()).filter(Boolean)
                  )
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Enter tags separated by commas"
              />
            ) : (
              <div className="flex flex-wrap gap-2">
                {task.tags && task.tags.length > 0 ? (
                  task.tags.map((tag) => (
                    <span key={tag} className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">
                      {tag}
                    </span>
                  ))
                ) : (
                  <span className="text-gray-400 italic">No tags</span>
                )}
              </div>
            )}
          </div>

          {/* Source Info */}
          <div className="bg-gray-50 rounded-lg p-4 space-y-2">
            <h3 className="text-sm font-medium text-gray-700">Source Information</h3>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-gray-500">Source:</span>
                <span className="ml-2 font-medium text-gray-900 capitalize">
                  {task.source.replace('_', ' ')}
                </span>
              </div>
              {task.source_url && (
                <div>
                  <a
                    href={task.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline flex items-center gap-1"
                  >
                    View source <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              )}
              <div>
                <span className="text-gray-500">Created:</span>
                <span className="ml-2 text-gray-900">{formatRelativeTime(task.created_at)}</span>
              </div>
              <div>
                <span className="text-gray-500">Updated:</span>
                <span className="ml-2 text-gray-900">{formatRelativeTime(task.updated_at)}</span>
              </div>
              {task.urgency_score > 0 && (
                <div>
                  <span className="text-gray-500">Urgency Score:</span>
                  <span className="ml-2 font-medium text-gray-900">{task.urgency_score}/100</span>
                </div>
              )}
              {task.extraction_confidence && (
                <div>
                  <span className="text-gray-500">AI Confidence:</span>
                  <span className="ml-2 font-medium text-gray-900">{task.extraction_confidence}%</span>
                </div>
              )}
            </div>
          </div>

          {/* Assigned To */}
          {task.assigned_to && task.assigned_to.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Assigned To</label>
              <div className="flex flex-wrap gap-2">
                {task.assigned_to.map((assignee) => (
                  <span key={assignee} className="flex items-center gap-1 px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full">
                    <User className="w-3 h-3" />
                    {assignee}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
