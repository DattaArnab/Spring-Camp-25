package main

import (
	"intellbot/Controlers"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)



func main(){
    r := gin.Default()
    r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"}, 
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Content-Type", "Authorization", "email"}, 
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))
    r.POST("/register", Controlers.RegisterUser)
    r.POST("/login",Controlers.Login)
   r.GET("/api/isauthorized",Controlers.Validate)
    r.POST("/newprompt",Controlers.Newprompt)
    r.POST("/all",Controlers.GetAllPrompts)
	r.POST("/api/askai",Controlers.GetResponse)
	r.POST("/saveprompt",Controlers.Saveprompt)
	r.POST("./allSaved",Controlers.GetAllsaved)
    
    // r.POST("/identify",Controlers.GetEmailFromToken)
    r.Run(":8080")

}