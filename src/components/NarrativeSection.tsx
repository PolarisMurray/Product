import React from 'react';
import type { NarrativeSection as NarrativeSectionType } from '../api/types';

interface NarrativeSectionProps {
  section: NarrativeSectionType;
}

function NarrativeSection({ section }: NarrativeSectionProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      {/* Title */}
      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
        {section.title}
      </h2>
      
      {/* Content */}
      <div className="prose max-w-none dark:prose-invert">
        <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed">
          {section.content}
        </p>
      </div>
    </div>
  );
}

export default NarrativeSection;

