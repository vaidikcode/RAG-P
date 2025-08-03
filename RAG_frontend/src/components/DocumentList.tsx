import React from 'react';
import { FileText, Trash2, Clock } from 'lucide-react';
import { Document } from '../types';

interface DocumentListProps {
  documents: Document[];
  onDelete: (id: number) => void;
  loading: boolean;
}

const DocumentList: React.FC<DocumentListProps> = ({ documents, onDelete, loading }) => {
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="animate-pulse bg-gray-200 h-20 rounded-lg"></div>
        ))}
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <FileText className="mx-auto h-12 w-12 mb-4 text-gray-300" />
        <p>No documents uploaded yet</p>
        <p className="text-sm">Upload some documents to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {documents.map((doc) => (
        <div
          key={doc.id}
          className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1">
              <div className="flex-shrink-0">
                <FileText className="h-8 w-8 text-primary-500" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium text-gray-900 truncate">
                  {doc.title}
                </h3>
                <p className="text-xs text-gray-500 mt-1">
                  {doc.file_name} • {formatFileSize(doc.file_size)}
                </p>
                <div className="flex items-center mt-2 text-xs text-gray-400">
                  <Clock className="h-3 w-3 mr-1" />
                  {formatDate(doc.uploaded_at)}
                </div>
              </div>
            </div>
            <button
              onClick={() => onDelete(doc.id)}
              className="flex-shrink-0 p-1 text-gray-400 hover:text-red-500 transition-colors"
              title="Delete document"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DocumentList;
