package services

import (
	"fmt"
	"io"
	"mime/multipart"
	"path/filepath"
	"strings"

	"github.com/ledongthuc/pdf"
)

type DocumentService struct{}

func NewDocumentService() *DocumentService {
	return &DocumentService{}
}

func (d *DocumentService) ExtractTextFromFile(file multipart.File, header *multipart.FileHeader) (string, error) {
	ext := strings.ToLower(filepath.Ext(header.Filename))

	switch ext {
	case ".txt":
		return d.extractTextFromTXT(file)
	case ".pdf":
		return d.extractTextFromPDF(file)
	default:
		return "", fmt.Errorf("unsupported file type: %s", ext)
	}
}

func (d *DocumentService) extractTextFromTXT(file multipart.File) (string, error) {
	content, err := io.ReadAll(file)
	if err != nil {
		return "", fmt.Errorf("failed to read text file: %v", err)
	}
	return string(content), nil
}

func (d *DocumentService) extractTextFromPDF(file multipart.File) (string, error) {
	content, err := io.ReadAll(file)
	if err != nil {
		return "", fmt.Errorf("failed to read PDF file: %v", err)
	}

	reader, err := pdf.NewReader(strings.NewReader(string(content)), int64(len(content)))
	if err != nil {
		return "", fmt.Errorf("failed to create PDF reader: %v", err)
	}

	fonts := make(map[string]*pdf.Font)

	var textContent strings.Builder
	for i := 1; i <= reader.NumPage(); i++ {
		page := reader.Page(i)
		if page.V.IsNull() {
			continue
		}

		text, err := page.GetPlainText(fonts)
		if err != nil {
			continue
		}
		textContent.WriteString(text)
		textContent.WriteString("\n")
	}

	return textContent.String(), nil
}
