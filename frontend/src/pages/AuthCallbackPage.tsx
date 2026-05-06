import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { authApi } from '@/lib/api'
import { useQuery } from '@tanstack/react-query'
import LoadingSpinner from '@/components/LoadingSpinner'
import toast from 'react-hot-toast'

export default function AuthCallbackPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { setAuth } = useAuthStore()

  const token = searchParams.get('token')

  const { isLoading, isError } = useQuery({
    queryKey: ['authCallback', token],
    queryFn: async () => {
      if (!token) {
        throw new Error('No token provided')
      }

      // Set the token first
      const user = await authApi.getCurrentUser()
      setAuth(token, user)
      return user
    },
    enabled: !!token,
    retry: false,
    onSuccess: () => {
      toast.success('Logged in successfully!')
      navigate('/dashboard', { replace: true })
    },
    onError: (error: any) => {
      toast.error(error.message || 'Authentication failed')
      navigate('/login', { replace: true })
    },
  })

  useEffect(() => {
    if (!token) {
      toast.error('Invalid authentication callback')
      navigate('/login', { replace: true })
    }
  }, [token, navigate])

  if (isError) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Authentication Failed</h2>
          <p className="text-gray-600 mb-6">Something went wrong. Please try again.</p>
          <button
            onClick={() => navigate('/login')}
            className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
          >
            Back to Login
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <LoadingSpinner size="lg" className="mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          {isLoading ? 'Completing sign in...' : 'Redirecting...'}
        </h2>
        <p className="text-gray-600">Please wait while we set up your account</p>
      </div>
    </div>
  )
}
