import React, { useState } from 'react'
import FileUploadArea from '../components/FileUploadArea'
import ActionButtons from '../components/ActionButtons'
import ResultView from '../components/ResultView'
import ExportButtons from '../components/ExportButtons'
import { PlotCardSkeleton, TextAreaSkeleton } from '../components/LoadingSkeleton'

function ResearchMode() {
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [results, setResults] = useState(null)
  const [isExporting, setIsExporting] = useState(false)

  const handleFilesUpload = (files) => {
    setUploadedFiles(files)
  }

  const handleFileRemove = (fileId) => {
    setUploadedFiles(uploadedFiles.filter(f => f.id !== fileId))
  }

  const handleGenerateReport = async () => {
    if (uploadedFiles.length === 0) return
    
    setIsGenerating(true)
    // Simulate API call
    setTimeout(() => {
      setResults({
        plots: [
          { id: 1, title: 'Volcano Plot', image: null },
          { id: 2, title: 'PCA Plot', image: null },
          { id: 3, title: 'Heatmap', image: null },
          { id: 4, title: 'GSEA Enrichment', image: null },
        ],
        results: 'Based on the differential gene expression analysis, we identified 1,234 significantly differentially expressed genes (DEGs) with adjusted p-value < 0.05 and |log2FC| > 1. The volcano plot reveals distinct clusters of upregulated and downregulated genes, suggesting a robust transcriptional response to the experimental condition.',
        discussion: 'The enrichment analysis indicates significant overrepresentation of pathways related to immune response and metabolic processes. These findings align with previous studies and suggest potential mechanisms underlying the observed phenotype. Further validation through functional assays would strengthen these conclusions.'
      })
      setIsGenerating(false)
    }, 2000)
  }

  const handleExport = async (format) => {
    if (!results) return
    
    setIsExporting(true)
    // Simulate export
    setTimeout(() => {
      setIsExporting(false)
      alert(`${format} export completed!`)
    }, 1500)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Phase 2: File Upload Area */}
          <FileUploadArea 
            uploadedFiles={uploadedFiles}
            onFilesUpload={handleFilesUpload}
            onFileRemove={handleFileRemove}
          />

          {/* Phase 3: Action Buttons */}
          <ActionButtons 
            hasFiles={uploadedFiles.length > 0}
            isGenerating={isGenerating}
            onGenerate={handleGenerateReport}
          />

          {/* Loading State - Show skeletons while generating */}
          {isGenerating && (
            <div className="space-y-8">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4">Charts</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <PlotCardSkeleton />
                  <PlotCardSkeleton />
                  <PlotCardSkeleton />
                  <PlotCardSkeleton />
                </div>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <TextAreaSkeleton />
                <TextAreaSkeleton />
              </div>
            </div>
          )}

          {/* Phase 4: Result View */}
          {results && !isGenerating && (
            <>
              <ResultView results={results} />
              
              {/* Phase 5: Export Buttons */}
              <ExportButtons 
                isExporting={isExporting}
                onExport={handleExport}
              />
            </>
          )}

          {/* Empty State */}
          {!results && !isGenerating && uploadedFiles.length === 0 && (
            <div className="text-center py-16">
              <div className="inline-block p-6 bg-white rounded-lg shadow-sm border border-gray-200">
                <p className="text-gray-500 text-lg">Please upload data to start analysis</p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default ResearchMode

