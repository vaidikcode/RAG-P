export interface Document {
  id: number;
  title: string;
  content: string;
  file_type: string;
  file_name: string;
  file_size: number;
  uploaded_at: string;
}

export interface Chat {
  id: number;
  query: string;
  response: string;
  created_at: string;
}

export interface QueryRequest {
  query: string;
}

export interface QueryResponse {
  answer: string;
  source_documents: string[];
}

export interface UploadResponse {
  message: string;
  document: Document;
}
