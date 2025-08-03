package handlers

import (
	"fmt"
	"net/http"
	"path/filepath"
	"rag-backend/database"
	"rag-backend/models"
	"rag-backend/services"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
)

type DocumentHandler struct {
	docService *services.DocumentService
	ragService *services.RAGService
}

func NewDocumentHandler(ragService *services.RAGService) *DocumentHandler {
	return &DocumentHandler{
		docService: services.NewDocumentService(),
		ragService: ragService,
	}
}

func (h *DocumentHandler) UploadDocument(c *gin.Context) {
	file, header, err := c.Request.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "No file uploaded"})
		return
	}
	defer file.Close()

	title := c.PostForm("title")
	if title == "" {
		title = strings.TrimSuffix(header.Filename, filepath.Ext(header.Filename))
	}

	content, err := h.docService.ExtractTextFromFile(file, header)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": fmt.Sprintf("Failed to extract text: %v", err)})
		return
	}

	document := models.Document{
		Title:    title,
		Content:  content,
		FileType: filepath.Ext(header.Filename),
		FileName: header.Filename,
		FileSize: header.Size,
	}

	if err := database.GetDB().Create(&document).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save document"})
		return
	}

	chunks := h.ragService.ChunkText(content)
	for i, chunk := range chunks {
		documentChunk := models.DocumentChunk{
			DocumentID: document.ID,
			Content:    chunk,
			ChunkIndex: i,
		}
		database.GetDB().Create(&documentChunk)
	}

	c.JSON(http.StatusOK, gin.H{
		"message":  "Document uploaded successfully",
		"document": document,
	})
}

func (h *DocumentHandler) GetDocuments(c *gin.Context) {
	var documents []models.Document

	if err := database.GetDB().Find(&documents).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch documents"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"documents": documents})
}

func (h *DocumentHandler) DeleteDocument(c *gin.Context) {
	id := c.Param("id")
	docID, err := strconv.Atoi(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid document ID"})
		return
	}

	if err := database.GetDB().Delete(&models.DocumentChunk{}, "document_id = ?", docID).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete document chunks"})
		return
	}

	if err := database.GetDB().Delete(&models.Document{}, docID).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete document"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Document deleted successfully"})
}
