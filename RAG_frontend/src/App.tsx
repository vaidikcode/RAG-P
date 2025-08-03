import React, { useState, useEffect } from 'react';
import { FileText, Upload, Shield, Trash2, Eye } from 'lucide-react';
import DocumentUpload from './components/DocumentUpload';
import ChatInterface from './components/ChatInterface';
import ChatHistory from './components/ChatHistory';
import { documentApi } from './api';
import { Document, QueryResponse } from './types';

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [chats, setChats] = useState<Array<{ query: string; response: QueryResponse; timestamp: Date }>>([]);
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);
  const [showUpload, setShowUpload] = useState(false);

  const loadDocuments = async () => {
    try {
      const docs = await documentApi.getAll();
      setDocuments(docs);
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleUploadSuccess = (document: Document) => {
    setDocuments((prev) => [document, ...prev]);
  };

  const handleDeleteDocument = async (id: number) => {
    try {
      await documentApi.delete(id);
      setDocuments((prev) => prev.filter((doc) => doc.id !== id));
    } catch (error) {
      console.error('Failed to delete document:', error);
    }
  };

  const handleNewChat = (query: string, response: QueryResponse) => {
    console.log('Adding new chat:', { query, response });
    setChats((prev) => [
      { query, response, timestamp: new Date() },
      ...prev,
    ]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Shield className="h-10 w-10 text-blue-600 mr-4" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Bajaj Finserv</h1>
                <p className="text-sm text-gray-500">AI-Powered Policy Assistant</p>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              {documents.length} Document{documents.length !== 1 ? 's' : ''} Loaded
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Sidebar - Document Management */}
          <div className="lg:col-span-1 space-y-6">
            {/* Upload Section */}
            <div className="bg-white rounded-lg border border-gray-200">
              <div className="px-4 py-3 border-b border-gray-100">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-medium text-gray-900">Documents</h3>
                  <button
                    onClick={() => setShowUpload(!showUpload)}
                    className="flex items-center px-3 py-1.5 text-xs font-medium text-blue-600 bg-blue-50 rounded-md hover:bg-blue-100 transition-colors"
                  >
                    <Upload className="h-3 w-3 mr-1" />
                    Upload
                  </button>
                </div>
              </div>
              
              {showUpload && (
                <div className="p-4 border-b border-gray-200">
                  <DocumentUpload 
                    onUploadSuccess={(doc) => {
                      handleUploadSuccess(doc);
                      setShowUpload(false);
                    }} 
                  />
                </div>
              )}

              {/* Document List */}
              <div className="max-h-96 overflow-y-auto">
                {documents.length > 0 ? (
                  <div className="divide-y divide-gray-200">
                    {documents.map((doc) => (
                      <div key={doc.id} className="p-3 hover:bg-gray-50 transition-colors">
                        <div className="flex items-start justify-between">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center">
                              <FileText className="h-4 w-4 text-gray-400 mr-2 flex-shrink-0" />
                              <h4 className="text-sm font-medium text-gray-900 truncate">
                                {doc.title}
                              </h4>
                            </div>
                            <p className="text-xs text-gray-500 mt-1">
                              {doc.file_name} • {(doc.file_size / 1024).toFixed(1)} KB
                            </p>
                          </div>
                          <div className="flex items-center space-x-1 ml-2">
                            <button
                              onClick={() => setSelectedDocument(doc)}
                              className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                              title="View"
                            >
                              <Eye className="h-3 w-3" />
                            </button>
                            <button
                              onClick={() => handleDeleteDocument(doc.id)}
                              className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                              title="Delete"
                            >
                              <Trash2 className="h-3 w-3" />
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-6 text-center text-gray-500">
                    <FileText className="h-6 w-6 mx-auto mb-2 text-gray-300" />
                    <p className="text-xs">No documents uploaded</p>
                  </div>
                )}
              </div>
            </div>

            {/* Document Viewer */}
            {selectedDocument && (
              <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
                <div className="px-4 py-3 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-medium text-gray-900">Preview</h3>
                    <button
                      onClick={() => setSelectedDocument(null)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ×
                    </button>
                  </div>
                </div>
                <div className="p-4">
                  <h4 className="font-medium text-gray-900 mb-2 text-sm">{selectedDocument.title}</h4>
                  <div className="text-xs text-gray-600 max-h-40 overflow-y-auto">
                    {selectedDocument.content.substring(0, 500)}...
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Main Chat Area - ChatGPT Style */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg border border-gray-200 h-[calc(100vh-200px)] flex flex-col">
              
              {/* Chat History Area */}
              <div className="flex-1 overflow-y-auto p-4">
                {chats.length === 0 ? (
                  <div className="h-full flex items-center justify-center">
                    <div className="text-center">
                      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-full w-20 h-20 mx-auto mb-6 flex items-center justify-center">
                        <Shield className="h-10 w-10 text-blue-500" />
                      </div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome to Bajaj Finserv</h2>
                      <p className="text-gray-600 mb-4">Your AI-powered policy and insurance assistant</p>
                      {documents.length === 0 && (
                        <div className="inline-flex items-center px-4 py-2 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
                          <Upload className="h-4 w-4 mr-2" />
                          Upload documents to start asking questions
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <ChatHistory chats={chats} loading={false} />
                )}
              </div>

              {/* Chat Input Area - Fixed at bottom */}
              <div className="border-t border-gray-200 p-4 bg-gray-50">
                <ChatInterface onNewChat={handleNewChat} />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
