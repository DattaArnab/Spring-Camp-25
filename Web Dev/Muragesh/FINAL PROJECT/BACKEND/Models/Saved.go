package models;


type Savedpromts struct {
	ID        uint   `json:"id" gorm:"primaryKey"`
	Useremail string `json:"useremail"`
	Prompt    string `json:"prompt"`
}
