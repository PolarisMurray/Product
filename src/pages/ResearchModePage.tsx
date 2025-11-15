import React, { useState, FormEvent, ChangeEvent } from 'react';
import { analyzeResearch, exportReport } from '../api/client';
import type { ResearchAnalyzeResponse } from '../api/types';
import { Loader2, AlertCircle, CheckCircle2, FileDown } from 'lucide-react';
import PlotCard from '../components/PlotCard';
import NarrativeSection from '../components/NarrativeSection';
import Toast from '../components/Toast';

function ResearchModePage() {
  // Form state
  const [projectName, setProjectName] = useState('');
  const [species, setSpecies] = useState('');
  const [contrastLabel, setContrastLabel] = useState('');
  const [degFile, setDegFile] = useState<File | null>(null);
  const [enrichmentFile, setEnrichmentFile] = useState<File | null>(null);

  // API state
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<ResearchAnalyzeResponse | null>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const handleDegFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setDegFile(file);
  };

  const handleEnrichmentFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setEnrichmentFile(file);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!degFile) {
      setError('Please select a DEG file');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Construct FormData
      const formData = new FormData();
      formData.append('deg_file', degFile);
      
      if (enrichmentFile) {
        formData.append('enrichment_file', enrichmentFile);
      }

      // Add metadata as JSON string
      const meta = {
        project_name: projectName || null,
        species: species || null,
        contrast_label: contrastLabel || null,
      };
      formData.append('meta', JSON.stringify(meta));

      // Call API
      const result = await analyzeResearch(formData);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred while analyzing the data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportReport = async () => {
    if (!response) {
      setToast({ message: 'No analysis results to export', type: 'error' });
      return;
    }

    setIsExporting(true);
    setError(null);

    try {
      const exportRequest = {
        mode: 'research' as const,
        format: 'pdf' as const,
        payload: response,
      };

      const exportResult = await exportReport(exportRequest);
      
      if (exportResult.download_url) {
        // For now, just show the URL since backend returns a stub
        console.log('Report download URL:', exportResult.download_url);
        setToast({
          message: `Report generated: ${exportResult.download_url}`,
          type: 'success',
        });
        
        // In production, you would open the URL:
        // window.open(exportResult.download_url, '_blank');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to export report';
      setError(errorMessage);
      setToast({ message: errorMessage, type: 'error' });
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Form Section */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Upload Analysis Data</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Project Name */}
              <div>
                <label htmlFor="project_name" className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name
                </label>
                <input
                  type="text"
                  id="project_name"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter project name (optional)"
                />
              </div>

              {/* Species */}
              <div>
                <label htmlFor="species" className="block text-sm font-medium text-gray-700 mb-2">
                  Species
                </label>
                <input
                  type="text"
                  id="species"
                  value={species}
                  onChange={(e) => setSpecies(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., Homo sapiens (optional)"
                />
              </div>

              {/* Contrast Label */}
              <div>
                <label htmlFor="contrast_label" className="block text-sm font-medium text-gray-700 mb-2">
                  Contrast Label
                </label>
                <input
                  type="text"
                  id="contrast_label"
                  value={contrastLabel}
                  onChange={(e) => setContrastLabel(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., Treatment vs Control (optional)"
                />
              </div>

              {/* DEG File */}
              <div>
                <label htmlFor="deg_file" className="block text-sm font-medium text-gray-700 mb-2">
                  DEG File <span className="text-red-500">*</span>
                </label>
                <input
                  type="file"
                  id="deg_file"
                  accept=".csv,.tsv,.xlsx"
                  onChange={handleDegFileChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
                {degFile && (
                  <p className="mt-2 text-sm text-gray-600">
                    Selected: {degFile.name}
                  </p>
                )}
              </div>

              {/* Enrichment File */}
              <div>
                <label htmlFor="enrichment_file" className="block text-sm font-medium text-gray-700 mb-2">
                  Enrichment File (Optional)
                </label>
                <input
                  type="file"
                  id="enrichment_file"
                  accept=".csv,.tsv,.xlsx"
                  onChange={handleEnrichmentFileChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                {enrichmentFile && (
                  <p className="mt-2 text-sm text-gray-600">
                    Selected: {enrichmentFile.name}
                  </p>
                )}
              </div>

              {/* Submit Button */}
              <div>
                <button
                  type="submit"
                  disabled={isLoading || !degFile}
                  className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <span>Generate Report</span>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Results Section */}
          {response && (
            <div className="space-y-8">
              {/* Success Message */}
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start space-x-3">
                <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-sm font-medium text-green-800">Analysis Complete</h3>
                  <p className="text-sm text-green-700 mt-1">Report generated successfully</p>
                </div>
              </div>

              {/* Plots Section */}
              {response.plots && response.plots.length > 0 && (
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Visualizations</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
                    {response.plots.map((plot, index) => (
                      <PlotCard key={index} plot={plot} />
                    ))}
                  </div>
                </div>
              )}

              {/* Narrative Section */}
              {response.narrative && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Results */}
                  {response.narrative.results && (
                    <NarrativeSection section={response.narrative.results} />
                  )}

                  {/* Discussion */}
                  {response.narrative.discussion && (
                    <NarrativeSection section={response.narrative.discussion} />
                  )}
                </div>
              )}

              {/* Summary Stats */}
              {response.summary_stats && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">Summary Statistics</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(response.summary_stats).map(([key, value]) => (
                      <div key={key} className="border border-gray-200 rounded-lg p-4">
                        <p className="text-sm font-medium text-gray-600 mb-1">
                          {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </p>
                        <p className="text-2xl font-bold text-gray-900">
                          {typeof value === 'number' ? value.toLocaleString() : String(value)}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Export Button */}
              <div className="flex justify-center">
                <button
                  onClick={handleExportReport}
                  disabled={isExporting}
                  className="flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isExporting ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Exporting...</span>
                    </>
                  ) : (
                    <>
                      <FileDown className="w-5 h-5" />
                      <span>Export Scientific Report (PDF)</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Toast Notification */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}

export default ResearchModePage;

