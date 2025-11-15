import React, { useState } from 'react'
import ResearchModePage from './pages/ResearchModePage'
import PersonalModePage from './pages/PersonalModePage'
import { FlaskConical, User } from 'lucide-react'

function App() {
  const [mode, setMode] = useState('research') // 'research' | 'personal'

  return (
    <div className="min-h-screen bg-gray-50">
      {/* App Header with Mode Switch */}
      <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            {/* App Title */}
            <div className="flex items-center space-x-3">
              <FlaskConical className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">BioReport Copilot</h1>
            </div>

            {/* Mode Switch */}
            <div className="flex items-center space-x-2 bg-gray-100 p-1 rounded-lg">
              <button
                onClick={() => setMode('research')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all ${
                  mode === 'research'
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <FlaskConical className="w-5 h-5" />
                <span className="font-medium">Research Mode</span>
              </button>
              <button
                onClick={() => setMode('personal')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-all ${
                  mode === 'personal'
                    ? 'bg-white text-purple-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <User className="w-5 h-5" />
                <span className="font-medium">Personal Genomics Mode</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Render Current Mode Page */}
      {mode === 'research' ? <ResearchModePage /> : <PersonalModePage />}
    </div>
  )
}

export default App


