import React from 'react';
import { User, Bot, FileText, Shield } from 'lucide-react';
import { QueryResponse } from '../types';

interface ChatHistoryProps {
  chats: Array<{ query: string; response: QueryResponse; timestamp: Date }>;
  loading: boolean;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ chats, loading }) => {
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // Function to clean and limit response text
  const cleanResponse = (text: string): string => {
    // Remove <think>...</think> blocks
    const cleaned = text.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
    
    // Split into paragraphs and limit to 5-6
    const paragraphs = cleaned.split('\n\n').filter(p => p.trim().length > 0);
    return paragraphs.slice(0, 6).join('\n\n');
  };

  if (loading) {
    return (
      <div className="space-y-6">
        {[1, 2].map((i) => (
          <div key={i} className="animate-pulse space-y-4">
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gray-200 rounded-full"></div>
              <div className="flex-1">
                <div className="bg-gray-200 h-4 rounded w-3/4 mb-2"></div>
                <div className="bg-gray-200 h-16 rounded-lg"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (chats.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
          <Shield className="h-8 w-8 text-blue-500" />
        </div>
        <p className="font-medium text-gray-700 text-lg mb-2">Welcome to Bajaj Finserv</p>
        <p className="text-sm text-gray-500">Ask me about your policies, insurance, or loans</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {chats.map((chat, index) => (
        <div key={index} className="space-y-2">
          {/* User Question */}
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 mt-1">
              <div className="w-6 h-6 bg-gradient-to-br from-gray-600 to-gray-700 rounded-full flex items-center justify-center shadow-sm">
                <User className="h-3 w-3 text-white" />
              </div>
            </div>
            <div className="flex-1">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 border-l-3 border-gray-400 rounded-lg p-3 shadow-sm">
                <p className="text-sm text-gray-900 font-medium leading-relaxed">{chat.query}</p>
              </div>
              <div className="text-xs text-gray-400 mt-1 ml-1">
                {formatTime(chat.timestamp)}
              </div>
            </div>
          </div>

          {/* AI Response */}
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 mt-1">
              <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-sm">
                <Bot className="h-3 w-3 text-white" />
              </div>
            </div>
            <div className="flex-1">
              <div className="bg-gradient-to-br from-blue-50 via-indigo-50 to-blue-100 border-l-3 border-blue-400 rounded-lg p-4 shadow-sm">
                <div className="prose prose-sm max-w-none">
                  <div className="text-xs font-medium text-blue-900 mb-2 flex items-center">
                    <Shield className="h-3 w-3 mr-1 text-blue-600" />
                    Bajaj Finserv Assistant
                  </div>
                  <div className="text-sm text-gray-900 leading-relaxed space-y-2">
                    {cleanResponse(chat.response.answer).split('\n\n').map((paragraph, idx) => (
                      <p key={idx} className="mb-2 last:mb-0 text-gray-800 leading-6">
                        {paragraph}
                      </p>
                    ))}
                  </div>
                </div>
                
                {chat.response.source_documents && chat.response.source_documents.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-blue-200">
                    <p className="text-xs font-medium text-blue-700 mb-2 flex items-center">
                      <FileText className="h-3 w-3 mr-1" />
                      Sources:
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {chat.response.source_documents.slice(0, 3).map((source, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-700 border border-blue-200"
                        >
                          <FileText className="h-2 w-2 mr-1" />
                          {source}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              <div className="text-xs text-gray-400 mt-1 ml-1">
                AI Assistant • {formatTime(chat.timestamp)}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatHistory;
