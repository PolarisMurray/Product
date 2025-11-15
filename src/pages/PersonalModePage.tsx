import React, { useState } from 'react';
import { User, FileDown, Loader2 } from 'lucide-react';
import { exportReport } from '../api/client';
import GeneticBioCard from '../components/GeneticBioCard';
import Toast from '../components/Toast';
import type { PersonalAnalyzeResponse } from '../api/types';

function PersonalModePage() {
  // For now, this is a placeholder page
  // TODO: Add form for SNP input and lifestyle factors
  // TODO: Call analyzePersonal API and display results
  
  // This will be set when API response is available
  const [response, setResponse] = useState<PersonalAnalyzeResponse | null>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const handleExportReport = async () => {
    if (!response) {
      setToast({ message: 'No analysis results to export', type: 'error' });
      return;
    }

    setIsExporting(true);

    try {
      const exportRequest = {
        mode: 'personal' as const,
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
      setToast({ message: errorMessage, type: 'error' });
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Page Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center space-x-3">
            <User className="w-8 h-8 text-purple-600 dark:text-purple-400" />
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Personal Genomics Mode</h1>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {response?.genetic_card ? (
          // Display Genetic BioCard when response is available
          <div className="space-y-8">
            <GeneticBioCard card={response.genetic_card} />
            {/* TODO: Add other sections like cards and peer_comparison */}
            
            {/* Export Button */}
            <div className="flex justify-center">
              <button
                onClick={handleExportReport}
                disabled={isExporting}
                className="flex items-center space-x-2 bg-purple-600 text-white px-6 py-3 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isExporting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Exporting...</span>
                  </>
                ) : (
                  <>
                    <FileDown className="w-5 h-5" />
                    <span>Export Personal Genome Report (PDF)</span>
                  </>
                )}
              </button>
            </div>
          </div>
        ) : (
          // Placeholder content
          <div className="text-center py-16">
            <div className="inline-block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <p className="text-gray-500 dark:text-gray-400 text-lg">
                Personal Genomics Mode - Coming Soon
              </p>
              <p className="text-gray-400 dark:text-gray-500 text-sm mt-2">
                This page will allow you to input SNP genotypes and lifestyle factors
              </p>
            </div>
          </div>
        )}
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

export default PersonalModePage;

