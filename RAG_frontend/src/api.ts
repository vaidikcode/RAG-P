import axios from 'axios';
import { Document, Chat, QueryRequest, QueryResponse, UploadResponse } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes - increased for RAG processing
});

// Add request/response interceptors for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url, config.data);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url, response.data);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const documentApi = {
  upload: async (file: File, title?: string): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    if (title) {
      formData.append('title', title);
    }
    
    const response = await api.post<UploadResponse>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getAll: async (): Promise<Document[]> => {
    const response = await api.get<{ documents: Document[] }>('/documents');
    return response.data.documents;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/documents/${id}`);
  },
};

export const chatApi = {
  query: async (request: QueryRequest): Promise<QueryResponse> => {
    const response = await api.post<QueryResponse>('/chat/query', request);
    return response.data;
  },

  getHistory: async (limit?: number): Promise<Chat[]> => {
    const response = await api.get<{ chats: Chat[] }>('/chat/history', {
      params: { limit },
    });
    return response.data.chats;
  },
};

export default api;
