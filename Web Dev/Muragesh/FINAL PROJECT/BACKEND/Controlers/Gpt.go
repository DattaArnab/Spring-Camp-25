package Controlers

import (
	"intellbot/database"
	"intellbot/models"
	"net/http"
	

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func GetPromptsByEmail(db *gorm.DB, email string) ([]models.Newprompt, error) {
	var prompts []models.Newprompt
	if err := db.Where("useremail = ?", email).Find(&prompts).Error; err != nil {
		return nil, err
	}
	return prompts, nil
}

func Newprompt(c *gin.Context) {
	var promp models.Newprompt
	gmail := c.GetHeader("email")

	if err := c.ShouldBindJSON(&promp); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	db, err := database.Connection()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Database connection failed"})
		return
	}

	if err := database.Saveprompt(db, promp); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save prompt"})
		return
	}


	prompts, err := GetPromptsByEmail(db, gmail)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch user-specific prompts"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message":     "Prompt saved successfully",
		"all_prompts": prompts,
	})
}


func GetAllPrompts(c *gin.Context) {
	email := c.GetHeader("email")

	db, err := database.Connection()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Database connection failed"})
		return
	}

	// Fetch prompts
	prompts, err := GetPromptsByEmail(db, email)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch prompts"})
		return
	}

	// Send successful response
	c.JSON(http.StatusOK, gin.H{"all_prompts": prompts})
}


type Savedpromts struct {
	ID        uint   `json:"id" gorm:"primaryKey"`
	Useremail string `json:"useremail"`
	Prompt    string `json:"msgai"`
}


func Saveprompt(c*gin.Context)  {
	var NewSave database.Savedpromts
	c.ShouldBindJSON(&NewSave)

	db, err := database.Connection()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Database connection failed"})
		return
	}
	if err := database.SaveNew(db, NewSave); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save prompt"})
		return
	}

}

func GetAllsaved(c*gin.Context)  {
	user:=c.GetHeader("email")
	db, err := database.Connection()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Database connection failed"})
		return
	}
	allSaved,err:=database.GetAllsaved(db,user)
	if err!=nil {
		
	}
	c.JSON(http.StatusOK, gin.H{"all_prompts": allSaved})

	
}