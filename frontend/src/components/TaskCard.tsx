import { Clock, Calendar, AlertCircle, Tag, Sparkles } from 'lucide-react'
import type { Task } from '@/types'
import { cn, formatDate, getPriorityColor, isOverdue, getDaysUntil, truncate } from '@/lib/utils'

interface TaskCardProps {
  task: Task
  onDragStart: (e: React.DragEvent) => void
  onClick: () => void
}

export default function TaskCard({ task, onDragStart, onClick }: TaskCardProps) {
  const daysUntil = getDaysUntil(task.deadline)
  const overdue = isOverdue(task.deadline)

  return (
    <div
      draggable
      onDragStart={onDragStart}
      onClick={onClick}
      className={cn(
        'bg-white rounded-lg border-2 p-4 cursor-pointer transition-all hover:shadow-md',
        getPriorityColor(task.priority),
        'hover:scale-[1.02] active:scale-[0.98]'
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2 mb-2">
        <h4 className="font-medium text-gray-900 text-sm leading-tight flex-1">
          {task.title}
        </h4>
        {task.ai_extracted && (
          <div className="flex-shrink-0" title="AI Extracted">
            <Sparkles className="w-4 h-4 text-purple-500" />
          </div>
        )}
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-xs text-gray-600 mb-3 line-clamp-2">
          {truncate(task.description, 100)}
        </p>
      )}

      {/* Metadata */}
      <div className="space-y-2">
        {/* Deadline */}
        {task.deadline && (
          <div className="flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5 text-gray-400" />
            <span
              className={cn(
                'text-xs',
                overdue ? 'text-red-600 font-medium' : 'text-gray-600'
              )}
            >
              {overdue ? (
                <>
                  <AlertCircle className="inline w-3 h-3 mr-1" />
                  Overdue: {formatDate(task.deadline)}
                </>
              ) : daysUntil !== null && daysUntil <= 3 ? (
                <>
                  {daysUntil === 0
                    ? 'Due today'
                    : daysUntil === 1
                    ? 'Due tomorrow'
                    : `Due in ${daysUntil} days`}
                </>
              ) : (
                formatDate(task.deadline)
              )}
            </span>
          </div>
        )}

        {/* Estimated Hours */}
        {task.estimated_hours && (
          <div className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-gray-400" />
            <span className="text-xs text-gray-600">
              {task.estimated_hours}h estimated
            </span>
          </div>
        )}

        {/* Category */}
        {task.category && (
          <div className="flex items-center gap-1.5">
            <Tag className="w-3.5 h-3.5 text-gray-400" />
            <span className="text-xs text-gray-600">{task.category}</span>
          </div>
        )}

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {task.tags.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className="px-2 py-0.5 bg-gray-100 text-gray-700 text-xs rounded-full"
              >
                {tag}
              </span>
            ))}
            {task.tags.length > 3 && (
              <span className="px-2 py-0.5 bg-gray-100 text-gray-500 text-xs rounded-full">
                +{task.tags.length - 3}
              </span>
            )}
          </div>
        )}

        {/* Priority Badge */}
        <div className="flex items-center justify-between mt-2 pt-2 border-t border-gray-100">
          <span
            className={cn(
              'px-2 py-0.5 text-xs font-medium rounded-full',
              getPriorityColor(task.priority)
            )}
          >
            {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
          </span>

          {/* Urgency Score */}
          {task.urgency_score > 70 && (
            <span className="text-xs text-red-600 font-medium">
              🔥 High urgency
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
