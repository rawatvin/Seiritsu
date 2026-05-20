import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/store/authStore'
import { Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function LoginPage() {
  const navigate = useNavigate()
  const { isAuthenticated, setAuth } = useAuthStore()
  const [demoEmail, setDemoEmail] = useState('')
  const [demoName, setDemoName] = useState('')
  const [showDemoForm, setShowDemoForm] = useState(false)

  const { mutate: handleLogin, isLoading } = useMutation({
    mutationFn: authApi.getLoginUrl,
    onSuccess: (data) => {
      window.location.href = data.auth_url
    },
    onError: () => {
      toast.error('Failed to initiate login')
    },
  })

  const { mutate: handleDemoLogin, isLoading: isDemoLoading } = useMutation({
    mutationFn: async (data: { email: string; name: string }) => {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/auth/demo-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      if (!response.ok) throw new Error('Demo login failed')
      return response.json()
    },
    onSuccess: (data) => {
      setAuth(data.access_token, data.user)
      toast.success('Welcome to Task Intelligence!')
      navigate('/dashboard')
    },
    onError: () => {
      toast.error('Demo login failed')
    },
  })

  // Redirect if already authenticated
  if (isAuthenticated) {
    navigate('/dashboard')
    return null
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Logo/Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Task Intelligence
            </h1>
            <p className="text-gray-600">
              AI-powered task management for your workflow
            </p>
          </div>

          {/* Features */}
          <div className="space-y-3 mb-8">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Auto-extract tasks</p>
                <p className="text-xs text-gray-500">From emails, Teams, and meetings</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Smart prioritization</p>
                <p className="text-xs text-gray-500">AI learns from your behavior</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Actionable insights</p>
                <p className="text-xs text-gray-500">Find time-saving opportunities</p>
              </div>
            </div>
          </div>

          {/* Login Buttons */}
          {!showDemoForm ? (
            <>
              <button
                onClick={() => handleLogin()}
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-3 px-6 py-3 bg-white border-2 border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Connecting...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" viewBox="0 0 21 21" fill="none">
                      <rect x="1" y="1" width="9" height="9" fill="#F25022"/>
                      <rect x="11" y="1" width="9" height="9" fill="#7FBA00"/>
                      <rect x="1" y="11" width="9" height="9" fill="#00A4EF"/>
                      <rect x="11" y="11" width="9" height="9" fill="#FFB900"/>
                    </svg>
                    Sign in with Microsoft
                  </>
                )}
              </button>

              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">or</span>
                </div>
              </div>

              <button
                onClick={() => setShowDemoForm(true)}
                className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Try Demo Mode (No Azure Required)
              </button>

              <p className="mt-6 text-xs text-center text-gray-500">
                Demo mode: Full features without Microsoft login
              </p>
            </>
          ) : (
            <>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Your Email
                  </label>
                  <input
                    type="email"
                    value={demoEmail}
                    onChange={(e) => setDemoEmail(e.target.value)}
                    placeholder="demo@example.com"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Your Name
                  </label>
                  <input
                    type="text"
                    value={demoName}
                    onChange={(e) => setDemoName(e.target.value)}
                    placeholder="Demo User"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  />
                </div>

                <button
                  onClick={() => handleDemoLogin({ email: demoEmail, name: demoName || 'Demo User' })}
                  disabled={isDemoLoading || !demoEmail}
                  className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isDemoLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Starting Demo...
                    </>
                  ) : (
                    <>
                      Start Demo
                    </>
                  )}
                </button>

                <button
                  onClick={() => setShowDemoForm(false)}
                  className="w-full px-6 py-2 text-sm text-gray-600 hover:text-gray-900"
                >
                  ← Back to login options
                </button>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <p className="mt-8 text-center text-sm text-gray-600">
          Powered by Claude AI • Built with React & FastAPI
        </p>
      </div>
    </div>
  )
}
