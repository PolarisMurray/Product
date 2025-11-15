import React, { useState } from 'react'
import { Download, Copy, Check } from 'lucide-react'

function ResultView({ results }) {
  const [copiedSection, setCopiedSection] = useState(null)

  const handleCopy = (text, section) => {
    navigator.clipboard.writeText(text)
    setCopiedSection(section)
    setTimeout(() => setCopiedSection(null), 2000)
  }

  return (
    <div className="space-y-8">
      {/* Plot Cards Grid */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">图表展示</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {results.plots.map((plot) => (
            <div
              key={plot.id}
              className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden"
            >
              <div className="p-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">{plot.title}</h3>
              </div>
              <div className="p-6 bg-gray-50 min-h-[300px] flex items-center justify-center">
                {plot.image ? (
                  <img src={plot.image} alt={plot.title} className="max-w-full h-auto rounded-lg" />
                ) : (
                  <div className="text-center text-gray-400">
                    <div className="w-32 h-32 mx-auto mb-4 bg-gradient-to-br from-research-blue-100 to-research-blue-200 rounded-lg flex items-center justify-center shadow-inner">
                      <span className="text-5xl">📊</span>
                    </div>
                    <p className="text-sm font-medium">图表占位符</p>
                    <p className="text-xs mt-1 text-gray-400">图表生成后将显示在此处</p>
                  </div>
                )}
              </div>
              <div className="p-4 border-t border-gray-200">
                <button className="flex items-center space-x-2 text-research-blue-600 hover:text-research-blue-700 transition-colors">
                  <Download className="w-4 h-4" />
                  <span className="text-sm font-medium">Download Image</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI Text Areas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Results Section */}
        <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200 flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">Results</h3>
            <button
              onClick={() => handleCopy(results.results, 'results')}
              className="flex items-center space-x-2 text-gray-600 hover:text-research-blue-600 transition-colors"
            >
              {copiedSection === 'results' ? (
                <>
                  <Check className="w-4 h-4" />
                  <span className="text-sm">已复制</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  <span className="text-sm">复制</span>
                </>
              )}
            </button>
          </div>
          <div className="p-6">
            <textarea
              defaultValue={results.results}
              className="w-full h-64 p-4 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-research-blue-500 focus:border-transparent"
              placeholder="自动生成的结果将显示在这里..."
            />
          </div>
        </div>

        {/* Discussion Section */}
        <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200 flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">Discussion</h3>
            <button
              onClick={() => handleCopy(results.discussion, 'discussion')}
              className="flex items-center space-x-2 text-gray-600 hover:text-research-blue-600 transition-colors"
            >
              {copiedSection === 'discussion' ? (
                <>
                  <Check className="w-4 h-4" />
                  <span className="text-sm">已复制</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  <span className="text-sm">复制</span>
                </>
              )}
            </button>
          </div>
          <div className="p-6">
            <textarea
              defaultValue={results.discussion}
              className="w-full h-64 p-4 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-research-blue-500 focus:border-transparent"
              placeholder="自动生成的讨论将显示在这里..."
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultView

