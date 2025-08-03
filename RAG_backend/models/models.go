package models

import (
	"time"
)

type Document struct {
	ID         uint      `json:"id" gorm:"primaryKey"`
	Title      string    `json:"title" gorm:"not null"`
	Content    string    `json:"content" gorm:"type:longtext"`
	FileType   string    `json:"file_type"`
	FileName   string    `json:"file_name"`
	FileSize   int64     `json:"file_size"`
	UploadedAt time.Time `json:"uploaded_at" gorm:"autoCreateTime"`
	UpdatedAt  time.Time `json:"updated_at" gorm:"autoUpdateTime"`
}

type Chat struct {
	ID        uint      `json:"id" gorm:"primaryKey"`
	Query     string    `json:"query" gorm:"not null"`
	Response  string    `json:"response" gorm:"type:longtext"`
	CreatedAt time.Time `json:"created_at" gorm:"autoCreateTime"`
}

type DocumentChunk struct {
	ID         uint     `json:"id" gorm:"primaryKey"`
	DocumentID uint     `json:"document_id"`
	Content    string   `json:"content" gorm:"type:text"`
	ChunkIndex int      `json:"chunk_index"`
	Document   Document `json:"document" gorm:"foreignKey:DocumentID"`
}
