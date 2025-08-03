import React, { useState, useEffect } from 'react';
import { Send, Loader, HelpCircle } from 'lucide-react';
import { chatApi } from '../api';
import { QueryResponse } from '../types';

interface ChatInterfaceProps {
  onNewChat: (query: string, response: QueryResponse) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onNewChat }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [timer, setTimer] = useState(0);

  // Timer effect
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (loading) {
      interval = setInterval(() => {
        setTimer((prev) => prev + 1);
      }, 1000);
    } else {
      setTimer(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const sampleQuestions = [
    "What are the key benefits of my life insurance policy?",
    "What documents are required for claim processing?"
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    console.log('Submitting query:', query.trim());
    setLoading(true);
    try {
      const response = await chatApi.query({ query: query.trim() });
      console.log('API response:', response);
      onNewChat(query.trim(), response);
      setQuery('');
    } catch (error) {
      console.error('Query failed:', error);
      // Show error to user with professional message
      alert(`Unable to process your query at the moment. Please try again or contact support.`);
    } finally {
      setLoading(false);
    }
  };

  const handleSampleQuestion = (question: string) => {
    setQuery(question);
  };

  return (
    <div className="space-y-4">
      {/* Loading indicator with timer */}
      {loading && (
        <div className="flex items-center justify-center py-4 bg-blue-50 rounded-lg border border-blue-200">
          <Loader className="h-4 w-4 animate-spin text-blue-600 mr-2" />
          <span className="text-sm text-blue-800">Processing your query...</span>
          <span className="ml-2 text-xs text-blue-600 font-mono">{formatTime(timer)}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about your policies, coverage, premiums, claims..."
            className="w-full p-4 pr-12 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            rows={3}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!query.trim() || loading}
            className="absolute bottom-3 right-3 p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <Loader className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </div>
      </form>

      {/* Sample Questions */}
      <div className="mt-4">
        <div className="flex items-center mb-3">
          <HelpCircle className="h-4 w-4 text-gray-500 mr-2" />
          <p className="text-xs font-medium text-gray-600">Quick Questions:</p>
        </div>
        <div className="grid grid-cols-1 gap-2">
          {sampleQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => handleSampleQuestion(question)}
              disabled={loading}
              className="text-left p-2 text-xs text-gray-600 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 hover:border-gray-300 disabled:opacity-50"
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
