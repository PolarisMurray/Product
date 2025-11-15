import React from 'react';
import type { Plot } from '../api/types';

interface PlotCardProps {
  plot: Plot;
}

function PlotCard({ plot }: PlotCardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 shadow-sm hover:shadow-md transition-shadow">
      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {plot.name}
      </h3>
      
      {/* Description */}
      {plot.description && (
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
          {plot.description}
        </p>
      )}
      
      {/* Image */}
      {plot.image_base64 && (
        <div className="w-full bg-gray-100 dark:bg-gray-700 rounded-md overflow-hidden min-h-[200px] flex items-center justify-center">
          <img
            src={`data:image/png;base64,${plot.image_base64}`}
            alt={plot.name}
            className="w-full h-auto"
            loading="lazy"
            onError={(e) => {
              // If image loading fails, show placeholder
              const target = e.target as HTMLImageElement;
              target.style.display = 'none';
              const parent = target.parentElement;
              if (parent && !parent.querySelector('.placeholder-text')) {
                const placeholder = document.createElement('div');
                placeholder.className = 'placeholder-text text-gray-400 text-center p-8';
                placeholder.textContent = `${plot.name} - Loading image...`;
                parent.appendChild(placeholder);
              }
            }}
          />
        </div>
      )}
    </div>
  );
}

export default PlotCard;

