import React from 'react'
import { FlaskConical, Loader2 } from 'lucide-react'

function ActionButtons({ hasFiles, isGenerating, onGenerate }) {
  return (
    <div className="flex justify-center">
      <button
        onClick={onGenerate}
        disabled={!hasFiles || isGenerating}
        className={`
          flex items-center space-x-3 px-8 py-4 rounded-lg font-semibold text-lg
          transition-all duration-200 transform
          ${hasFiles && !isGenerating
            ? 'bg-research-blue-600 text-white hover:bg-research-blue-700 hover:shadow-lg active:scale-95'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }
        `}
      >
        {isGenerating ? (
          <>
            <Loader2 className="w-6 h-6 animate-spin" />
            <span>Generating report...</span>
          </>
        ) : (
          <>
            <FlaskConical className="w-6 h-6" />
            <span>Generate Report</span>
          </>
        )}
      </button>
    </div>
  )
}

export default ActionButtons


