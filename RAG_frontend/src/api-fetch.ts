import { Document, Chat, QueryRequest, QueryResponse, UploadResponse } from './types';

const API_BASE_URL = 'http://localhost:8090/api';

const fetchApi = async (url: string, options: RequestInit = {}): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};

export const documentApi = {
  upload: async (file: File, title?: string): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    if (title) {
      formData.append('title', title);
    }
    
    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.status}`);
    }

    return response.json();
  },

  getAll: async (): Promise<Document[]> => {
    const data = await fetchApi('/documents');
    return data.documents;
  },

  delete: async (id: number): Promise<void> => {
    await fetchApi(`/documents/${id}`, {
      method: 'DELETE',
    });
  },
};

export const chatApi = {
  query: async (request: QueryRequest): Promise<QueryResponse> => {
    return fetchApi('/chat/query', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  getHistory: async (limit?: number): Promise<Chat[]> => {
    const url = limit ? `/chat/history?limit=${limit}` : '/chat/history';
    const data = await fetchApi(url);
    return data.chats;
  },
};

export default { documentApi, chatApi };
