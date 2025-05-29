package models;

import "github.com/jinzhu/gorm"

type User struct {
	gorm.Model

	


	Name     string `json:"name" binding:"required"`
	Country     string `json:"country" binding:"required"`
	Email     string `json:"email" binding:"required,email" `
	Interests  string `json:"interests"`  
	Password string `json:"password" binding:"required"` 

}
type Sessions struct{
	gorm.Model
	Prompt[]int
}
type Prompt struct{
	gorm.Model
	// prompt string
}