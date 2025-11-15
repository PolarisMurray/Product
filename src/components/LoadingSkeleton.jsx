import React from 'react'

export function PlotCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden animate-pulse">
      <div className="p-4 border-b border-gray-200">
        <div className="h-6 bg-gray-200 rounded w-32"></div>
      </div>
      <div className="p-6 bg-gray-50 min-h-[300px]">
        <div className="w-full h-full bg-gray-200 rounded-lg"></div>
      </div>
      <div className="p-4 border-t border-gray-200">
        <div className="h-4 bg-gray-200 rounded w-24"></div>
      </div>
    </div>
  )
}

export function TextAreaSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden animate-pulse">
      <div className="p-4 border-b border-gray-200">
        <div className="h-6 bg-gray-200 rounded w-24"></div>
      </div>
      <div className="p-6">
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-4/5"></div>
        </div>
      </div>
    </div>
  )
}


