package models

import (
	"time"
)

type Newprompt struct {
	ID        uint      `json:"id" gorm:"primaryKey"`
	Useremail string    `json:"useremail"`
	Prompt    string    `json:"prompt"`
	PostedOn  time.Time `json:"posted_on"`
}

