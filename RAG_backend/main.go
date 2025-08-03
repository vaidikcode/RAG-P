package main

import (
	"log"
	"os"
	"rag-backend/database"
	"rag-backend/handlers"
	"rag-backend/services"
	"strings"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func init() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found, using environment variables")
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func main() {
	dbHost := getEnv("DB_HOST", "localhost")
	dbPort := getEnv("DB_PORT", "3306")
	dbUser := getEnv("DB_USER", "root")
	dbPassword := getEnv("DB_PASSWORD", "Vaidik@2005")
	dbName := getEnv("DB_NAME", "rag_db")

	dsn := dbUser + ":" + dbPassword + "@tcp(" + dbHost + ":" + dbPort + ")/" + dbName + "?charset=utf8mb4&parseTime=True&loc=Local"

	if err := database.InitDatabase(dsn); err != nil {
		log.Fatal("Failed to initialize database:", err)
	}

	pythonRagURL := getEnv("PYTHON_RAG_URL", "http://localhost:8080")
	ragService := services.NewRAGService(pythonRagURL)

	documentHandler := handlers.NewDocumentHandler(ragService)
	chatHandler := handlers.NewChatHandler(ragService)

	if getEnv("NODE_ENV", "development") == "production" {
		gin.SetMode(gin.ReleaseMode)
	}

	r := gin.Default()

	corsOrigins := strings.Split(getEnv("CORS_ORIGINS", "http://localhost:3000"), ",")
	r.Use(cors.New(cors.Config{
		AllowOrigins:     corsOrigins,
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization"},
		AllowCredentials: true,
	}))

	api := r.Group("/api")
	{
		documents := api.Group("/documents")
		{
			documents.POST("/upload", documentHandler.UploadDocument)
			documents.GET("", documentHandler.GetDocuments)
			documents.DELETE("/:id", documentHandler.DeleteDocument)
		}

		chat := api.Group("/chat")
		{
			chat.POST("/query", chatHandler.ProcessQuery)
			chat.GET("/history", chatHandler.GetChatHistory)
		}
	}

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})

	serverPort := getEnv("SERVER_PORT", "8090")
	log.Printf("Server starting on :%s", serverPort)
	r.Run(":" + serverPort)
}
