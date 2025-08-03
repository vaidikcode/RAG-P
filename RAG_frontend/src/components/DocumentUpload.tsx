import React, { useState, useRef } from 'react';
import { Upload, X, AlertCircle } from 'lucide-react';
import { documentApi } from '../api';
import { Document } from '../types';

interface DocumentUploadProps {
  onUploadSuccess: (document: Document) => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = async (files: FileList) => {
    if (files.length === 0) return;

    const file = files[0];
    const allowedTypes = ['.txt', '.pdf'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();

    if (!allowedTypes.includes(fileExtension)) {
      setError('Only PDF and TXT files are supported');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const response = await documentApi.upload(file);
      onUploadSuccess(response.document);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full">
      <div
        className={`relative border-2 border-dashed rounded-lg p-6 text-center hover:bg-gray-50 cursor-pointer transition-colors ${
          dragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300'
        } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={!uploading ? handleClick : undefined}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt"
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
          className="hidden"
          disabled={uploading}
        />

        <div className="space-y-4">
          <div className="mx-auto h-12 w-12 text-gray-400">
            {uploading ? (
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            ) : (
              <Upload className="h-12 w-12" />
            )}
          </div>
          
          <div>
            <p className="text-lg font-medium text-gray-900">
              {uploading ? 'Uploading...' : 'Upload documents'}
            </p>
            <p className="text-sm text-gray-500">
              Drag & drop or click to browse
            </p>
          </div>
        </div>
      </div>

      {error && (
        <div className="mt-4 flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-md">
          <AlertCircle className="h-5 w-5" />
          <span className="text-sm">{error}</span>
          <button onClick={() => setError(null)} className="ml-auto">
            <X className="h-4 w-4" />
          </button>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
