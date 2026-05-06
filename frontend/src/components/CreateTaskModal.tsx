import { useState } from 'react'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { taskApi, learningApi } from '@/lib/api'
import { X, Loader2, Sparkles } from 'lucide-react'
import type { TaskCreate, TaskPriority, TaskStatus } from '@/types'
import toast from 'react-hot-toast'
import { cn } from '@/lib/utils'

interface CreateTaskModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function CreateTaskModal({ isOpen, onClose }: CreateTaskModalProps) {
  const queryClient = useQueryClient()
  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: '',
    status: 'todo',
    priority: 'medium',
    source: 'manual',
  })

  const [showSuggestions, setShowSuggestions] = useState(false)

  // Get AI suggestions when title changes
  const { data: suggestions, isLoading: loadingSuggestions } = useQuery({
    queryKey: ['suggestions', formData.title],
    queryFn: () =>
      learningApi.getSuggestions(formData.title, formData.description),
    enabled: formData.title.length > 10 && showSuggestions,
    retry: false,
  })

  // Get categories
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: taskApi.getCategories,
  })

  const { mutate: createTask, isLoading: isCreating } = useMutation({
    mutationFn: taskApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries(['tasks'])
      queryClient.invalidateQueries(['dashboardSummary'])
      toast.success('Task created successfully!')
      onClose()
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.title.trim()) {
      toast.error('Please enter a task title')
      return
    }

    createTask(formData)
  }

  const handleChange = (
    field: keyof TaskCreate,
    value: string | string[] | number | undefined
  ) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const applySuggestion = () => {
    if (suggestions) {
      if (suggestions.category_suggestion) {
        handleChange('category', suggestions.category_suggestion)
      }
      if (suggestions.estimated_hours) {
        handleChange('estimated_hours', suggestions.estimated_hours)
      }
      toast.success('Applied AI suggestions!')
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900">Create New Task</h2>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="Enter task title..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              autoFocus
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              placeholder="Add details about this task..."
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
            />
          </div>

          {/* AI Suggestions */}
          {formData.title.length > 10 && (
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-purple-600" />
                  <span className="text-sm font-medium text-purple-900">
                    AI Suggestions
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setShowSuggestions(!showSuggestions)}
                  className="text-xs text-purple-600 hover:text-purple-700 font-medium"
                >
                  {showSuggestions ? 'Hide' : 'Show'}
                </button>
              </div>

              {showSuggestions && (
                <>
                  {loadingSuggestions ? (
                    <div className="flex items-center justify-center py-4">
                      <Loader2 className="w-5 h-5 animate-spin text-purple-600" />
                    </div>
                  ) : suggestions ? (
                    <div className="space-y-2">
                      {suggestions.category_suggestion && (
                        <div className="text-sm">
                          <span className="text-gray-600">Category: </span>
                          <span className="font-medium text-gray-900">
                            {suggestions.category_suggestion}
                          </span>
                          <span className="text-xs text-gray-500 ml-2">
                            ({suggestions.category_confidence}% confident)
                          </span>
                        </div>
                      )}
                      {suggestions.estimated_hours && (
                        <div className="text-sm">
                          <span className="text-gray-600">Estimated time: </span>
                          <span className="font-medium text-gray-900">
                            {suggestions.estimated_hours} hours
                          </span>
                        </div>
                      )}
                      {suggestions.similar_tasks.length > 0 && (
                        <div className="text-sm">
                          <span className="text-gray-600">
                            {suggestions.similar_tasks.length} similar task(s) found
                          </span>
                        </div>
                      )}
                      <button
                        type="button"
                        onClick={applySuggestion}
                        className="mt-2 px-3 py-1 bg-purple-600 text-white text-xs rounded-lg hover:bg-purple-700 transition-colors"
                      >
                        Apply Suggestions
                      </button>
                    </div>
                  ) : (
                    <p className="text-sm text-gray-600">No suggestions available</p>
                  )}
                </>
              )}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            {/* Status */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={formData.status}
                onChange={(e) => handleChange('status', e.target.value as TaskStatus)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="backlog">Backlog</option>
                <option value="todo">To Do</option>
                <option value="in_progress">In Progress</option>
                <option value="review">Review</option>
              </select>
            </div>

            {/* Priority */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Priority
              </label>
              <select
                value={formData.priority}
                onChange={(e) => handleChange('priority', e.target.value as TaskPriority)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Category
              </label>
              <input
                type="text"
                value={formData.category || ''}
                onChange={(e) => handleChange('category', e.target.value)}
                placeholder="e.g., Development, Design"
                list="categories"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              />
              {categories && categories.length > 0 && (
                <datalist id="categories">
                  {categories.map((cat) => (
                    <option key={cat} value={cat} />
                  ))}
                </datalist>
              )}
            </div>

            {/* Estimated Hours */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Estimated Hours
              </label>
              <input
                type="number"
                value={formData.estimated_hours || ''}
                onChange={(e) =>
                  handleChange('estimated_hours', e.target.value ? parseInt(e.target.value) : undefined)
                }
                placeholder="Hours"
                min="1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
          </div>

          {/* Deadline */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Deadline
            </label>
            <input
              type="datetime-local"
              value={formData.deadline || ''}
              onChange={(e) => handleChange('deadline', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tags
            </label>
            <input
              type="text"
              value={formData.tags?.join(', ') || ''}
              onChange={(e) =>
                handleChange(
                  'tags',
                  e.target.value.split(',').map((t) => t.trim()).filter(Boolean)
                )
              }
              placeholder="Enter tags separated by commas"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
            <p className="mt-1 text-xs text-gray-500">
              Separate multiple tags with commas
            </p>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isCreating || !formData.title.trim()}
              className={cn(
                'px-6 py-2 bg-primary text-white rounded-lg transition-colors',
                isCreating || !formData.title.trim()
                  ? 'opacity-50 cursor-not-allowed'
                  : 'hover:bg-primary/90'
              )}
            >
              {isCreating ? (
                <>
                  <Loader2 className="inline w-4 h-4 animate-spin mr-2" />
                  Creating...
                </>
              ) : (
                'Create Task'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
