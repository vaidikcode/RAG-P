package handlers

import (
	"net/http"
	"rag-backend/database"
	"rag-backend/models"
	"rag-backend/services"
	"strconv"

	"github.com/gin-gonic/gin"
)

type ChatHandler struct {
	ragService *services.RAGService
}

func NewChatHandler(ragService *services.RAGService) *ChatHandler {
	return &ChatHandler{
		ragService: ragService,
	}
}

func (h *ChatHandler) ProcessQuery(c *gin.Context) {
	var request struct {
		Query string `json:"query" binding:"required"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var documents []models.Document
	if err := database.GetDB().Find(&documents).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch documents"})
		return
	}

	var docsForRAG []services.DocumentForRAG
	for _, doc := range documents {
		docsForRAG = append(docsForRAG, services.DocumentForRAG{
			Content:  doc.Content,
			Title:    doc.Title,
			FileType: doc.FileType,
		})
	}

	response, err := h.ragService.ProcessQuery(request.Query, docsForRAG)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	chat := models.Chat{
		Query:    request.Query,
		Response: response.Answer,
	}
	database.GetDB().Create(&chat)

	c.JSON(http.StatusOK, gin.H{
		"answer":           response.Answer,
		"source_documents": response.SourceDocuments,
	})
}

func (h *ChatHandler) GetChatHistory(c *gin.Context) {
	limit := 50
	if l := c.Query("limit"); l != "" {
		if parsed, err := strconv.Atoi(l); err == nil {
			limit = parsed
		}
	}

	var chats []models.Chat
	if err := database.GetDB().Order("created_at desc").Limit(limit).Find(&chats).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch chat history"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"chats": chats})
}
