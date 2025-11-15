import React from 'react';
import type { GeneticBioCard as GeneticBioCardType } from '../api/types';
import { Copy, Download, Sparkles } from 'lucide-react';

interface GeneticBioCardProps {
  card: GeneticBioCardType;
}

function GeneticBioCard({ card }: GeneticBioCardProps) {
  const handleCopySummary = () => {
    // TODO: Implement copy to clipboard functionality
    // Create a formatted text summary of the card
    const summary = `${card.title}\n${card.subtitle}\n\n${card.badges.join(', ')}\n\n${card.highlights.join('\n')}`;
    navigator.clipboard.writeText(summary).then(() => {
      // Could add a toast notification here
      alert('Summary copied to clipboard!');
    }).catch(() => {
      alert('Failed to copy to clipboard');
    });
  };

  const handleDownloadImage = () => {
    // TODO: Implement image download functionality
    // This would require:
    // 1. Convert the card component to an image (using html2canvas or similar)
    // 2. Trigger download of the image file
    alert('Image download feature coming soon!');
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 md:p-8 max-w-2xl mx-auto">
      {/* Header with action buttons */}
      <div className="flex items-start justify-between mb-6">
        <div className="flex-1">
          {/* Title */}
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
            {card.title}
          </h2>
          
          {/* Subtitle */}
          <p className="text-sm md:text-base text-gray-600 dark:text-gray-400">
            {card.subtitle}
          </p>
        </div>
        
        {/* Action buttons */}
        <div className="flex items-center space-x-2 ml-4">
          <button
            onClick={handleCopySummary}
            className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            title="Copy summary"
          >
            <Copy className="w-5 h-5" />
          </button>
          <button
            onClick={handleDownloadImage}
            className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            title="Download as image (TODO)"
          >
            <Download className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Badges */}
      {card.badges && card.badges.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-6">
          {card.badges.map((badge, index) => (
            <span
              key={index}
              className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200 border border-purple-200 dark:border-purple-700"
            >
              <Sparkles className="w-3 h-3 mr-1.5" />
              {badge}
            </span>
          ))}
        </div>
      )}

      {/* Highlights */}
      {card.highlights && card.highlights.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wide mb-3">
            Key Highlights
          </h3>
          <ul className="space-y-2">
            {card.highlights.map((highlight, index) => (
              <li
                key={index}
                className="flex items-start space-x-3 text-gray-700 dark:text-gray-300"
              >
                <span className="flex-shrink-0 w-2 h-2 rounded-full bg-purple-500 dark:bg-purple-400 mt-2" />
                <span className="text-sm md:text-base leading-relaxed">
                  {highlight}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default GeneticBioCard;

