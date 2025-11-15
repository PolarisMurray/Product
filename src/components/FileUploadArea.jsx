import React, { useCallback, useState } from 'react'
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react'

function FileUploadArea({ uploadedFiles, onFilesUpload, onFileRemove }) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadStatus, setUploadStatus] = useState({})

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const getFileType = (fileName) => {
    const ext = fileName.split('.').pop().toLowerCase()
    if (['csv', 'tsv'].includes(ext)) return ext.toUpperCase()
    if (ext === 'xlsx') return 'XLSX'
    return ext.toUpperCase()
  }

  const validateFile = (file) => {
    const validTypes = ['text/csv', 'text/tab-separated-values', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    const validExtensions = ['csv', 'tsv', 'xlsx']
    const ext = file.name.split('.').pop().toLowerCase()
    
    return validExtensions.includes(ext) || validTypes.includes(file.type)
  }

  const handleFiles = useCallback((files) => {
    const fileArray = Array.from(files)
    const validFiles = []
    const invalidFiles = []

    fileArray.forEach(file => {
      if (validateFile(file)) {
        const fileObj = {
          id: Date.now() + Math.random(),
          file: file,
          name: file.name,
          size: file.size,
          type: getFileType(file.name),
        }
        validFiles.push(fileObj)
        setUploadStatus(prev => ({
          ...prev,
          [fileObj.id]: 'success'
        }))
      } else {
        invalidFiles.push(file.name)
        setUploadStatus(prev => ({
          ...prev,
          [file.name]: 'error'
        }))
      }
    })

    if (validFiles.length > 0) {
      onFilesUpload([...uploadedFiles, ...validFiles])
    }

    if (invalidFiles.length > 0) {
      alert(`Unsupported file formats: ${invalidFiles.join(', ')}\nSupported formats: CSV, TSV, XLSX`)
    }
  }, [uploadedFiles, onFilesUpload])

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFiles(files)
    }
  }

  const handleFileInput = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      handleFiles(files)
    }
  }

  return (
    <div className="space-y-4">
      {/* Drag & Drop Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-12 text-center transition-all
          ${isDragging 
            ? 'border-research-blue-500 bg-research-blue-50' 
            : 'border-gray-300 bg-white hover:border-research-blue-400 hover:bg-gray-50'
          }
        `}
      >
        <input
          type="file"
          multiple
          accept=".csv,.tsv,.xlsx"
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        <div className="flex flex-col items-center space-y-4">
          <div className={`p-4 rounded-full ${isDragging ? 'bg-research-blue-100' : 'bg-gray-100'}`}>
            <Upload className={`w-12 h-12 ${isDragging ? 'text-research-blue-600' : 'text-gray-400'}`} />
          </div>
          <div>
            <p className="text-lg font-medium text-gray-700">
              Drag files here or click to upload
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Supports CSV / TSV / XLSX
            </p>
          </div>
        </div>
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Uploaded Files</h3>
          <div className="space-y-2">
            {uploadedFiles.map((fileObj) => (
              <div
                key={fileObj.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center space-x-3 flex-1 min-w-0">
                  <File className="w-5 h-5 text-research-blue-600 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {fileObj.name}
                      </p>
                      {uploadStatus[fileObj.id] === 'success' && (
                        <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                      )}
                      {uploadStatus[fileObj.id] === 'error' && (
                        <AlertCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                      )}
                    </div>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-xs text-gray-500">{fileObj.type}</span>
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-500">{formatFileSize(fileObj.size)}</span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => onFileRemove(fileObj.id)}
                  className="ml-4 p-1 text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
                  aria-label="Remove file"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default FileUploadArea

