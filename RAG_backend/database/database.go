package database

import (
	"fmt"
	"log"
	"rag-backend/models"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDatabase(dsn string) error {
	var err error
	DB, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		return fmt.Errorf("failed to connect to database: %v", err)
	}

	err = DB.AutoMigrate(&models.Document{}, &models.Chat{}, &models.DocumentChunk{})
	if err != nil {
		return fmt.Errorf("failed to migrate database: %v", err)
	}

	log.Println("Database connected and migrated successfully")
	return nil
}

func GetDB() *gorm.DB {
	return DB
}
