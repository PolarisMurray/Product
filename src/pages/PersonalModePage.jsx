import React from 'react'
import { User } from 'lucide-react'

function PersonalModePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Page Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <User className="w-8 h-8 text-purple-600" />
            <h1 className="text-2xl font-bold text-gray-900">Personal Genomics Mode</h1>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-16">
          <div className="inline-block p-6 bg-white rounded-lg shadow-sm border border-gray-200">
            <p className="text-gray-500 text-lg">
              Personal Genomics Mode - Coming Soon
            </p>
            <p className="text-gray-400 text-sm mt-2">
              This page will allow you to input SNP genotypes and lifestyle factors
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}

export default PersonalModePage

