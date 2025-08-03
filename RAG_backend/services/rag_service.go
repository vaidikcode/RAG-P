package services

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

type RAGService struct {
	PythonServiceURL string
}

type RAGRequest struct {
	Query     string           `json:"query"`
	Documents []DocumentForRAG `json:"documents"`
}

type DocumentForRAG struct {
	Content  string `json:"content"`
	Title    string `json:"title"`
	FileType string `json:"file_type"`
}

type RAGResponse struct {
	Answer          string   `json:"answer"`
	SourceDocuments []string `json:"source_documents"`
	Error           string   `json:"error,omitempty"`
}

func NewRAGService(pythonURL string) *RAGService {
	return &RAGService{
		PythonServiceURL: pythonURL,
	}
}

func (r *RAGService) ProcessQuery(query string, documents []DocumentForRAG) (*RAGResponse, error) {
	reqData := RAGRequest{
		Query:     query,
		Documents: documents,
	}

	jsonData, err := json.Marshal(reqData)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %v", err)
	}

	resp, err := http.Post(r.PythonServiceURL+"/rag/query", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("failed to call Python service: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %v", err)
	}

	var ragResp RAGResponse
	if err := json.Unmarshal(body, &ragResp); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	return &ragResp, nil
}

func (r *RAGService) ChunkText(text string) []string {
	const chunkSize = 1000
	const overlap = 200

	var chunks []string
	words := strings.Fields(text)

	if len(words) <= chunkSize {
		return []string{text}
	}

	for i := 0; i < len(words); i += chunkSize - overlap {
		end := i + chunkSize
		if end > len(words) {
			end = len(words)
		}

		chunk := strings.Join(words[i:end], " ")
		chunks = append(chunks, chunk)

		if end == len(words) {
			break
		}
	}

	return chunks
}
