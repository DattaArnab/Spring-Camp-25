package database

import (
	"intellbot/models"


	"gorm.io/gorm"
)


func RegisterUser(db *gorm.DB, user models.User) error {
	result := db.Create(&user)
	return result.Error
}
func Saveprompt(db *gorm.DB, newPrompt models.Newprompt) error {
	
	db.AutoMigrate(&models.Newprompt{})


	result := db.Create(&newPrompt)
	return result.Error
}

type Savedpromts struct {
	ID        uint   `json:"id" gorm:"primaryKey"`
	Useremail string `json:"useremail"`
	Prompt    string `json:"msgai"`
}

func SaveNew(db *gorm.DB ,newSave Savedpromts)  error{
	db.AutoMigrate(&Savedpromts{})
	results:=db.Create(&newSave)
	return results.Error
}

func GetAllPrompts(db *gorm.DB) ([]models.Newprompt, error) {
	var prompts []models.Newprompt
	result := db.Find(&prompts)
	return prompts, result.Error
}
func GetAllsaved(db *gorm.DB,email string) ([]Savedpromts,error)  {

	var prompts []Savedpromts
	if err:=db.Where("useremail=?",email).Find(&prompts).Error;err!=nil{
		return nil,err
	}
	return prompts,nil}
	




