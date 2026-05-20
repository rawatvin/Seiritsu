import { Settings } from 'lucide-react'

export default function SettingsPage() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-gray-600">Configure sync sources and preferences</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-12 border border-gray-200 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
          <Settings className="w-8 h-8 text-gray-600" />
        </div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Settings Coming Soon</h2>
        <p className="text-gray-600 max-w-md mx-auto">
          Sync configuration, user preferences, and integration settings will be available here.
        </p>
      </div>
    </div>
  )
}
