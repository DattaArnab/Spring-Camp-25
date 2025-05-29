package database

import (
	"log"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"intellbot/models"
)


func Connection() (*gorm.DB, error) {
	dsn := "host=localhost user=postgres password=Namos@302 dbname=intellbot port=5857 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
		return nil, err
	}
	log.Println("Database connection successful")
	err = db.AutoMigrate(&models.User{})
	if err != nil {
		log.Fatal("Migration failed:", err)
	}
	return db, nil
}
