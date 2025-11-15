import React from 'react'
import { FileText, File, Loader2 } from 'lucide-react'

function ExportButtons({ isExporting, onExport }) {
  return (
    <div className="flex justify-center space-x-4">
      <button
        onClick={() => onExport('PDF')}
        disabled={isExporting}
        className={`
          flex items-center space-x-3 px-6 py-3 rounded-lg font-semibold
          transition-all duration-200 transform
          ${isExporting
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-red-600 text-white hover:bg-red-700 hover:shadow-lg active:scale-95'
          }
        `}
      >
        {isExporting ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>生成中...</span>
          </>
        ) : (
          <>
            <FileText className="w-5 h-5" />
            <span>Export PDF</span>
          </>
        )}
      </button>

      <button
        onClick={() => onExport('DOCX')}
        disabled={isExporting}
        className={`
          flex items-center space-x-3 px-6 py-3 rounded-lg font-semibold
          transition-all duration-200 transform
          ${isExporting
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-lg active:scale-95'
          }
        `}
      >
        {isExporting ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>生成中...</span>
          </>
        ) : (
          <>
            <File className="w-5 h-5" />
            <span>Export DOCX</span>
          </>
        )}
      </button>
    </div>
  )
}

export default ExportButtons


