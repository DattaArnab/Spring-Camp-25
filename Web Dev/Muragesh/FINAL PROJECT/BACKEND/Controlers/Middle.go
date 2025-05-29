package Controlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)


func Validate(c *gin.Context) {

	tokenString, err := c.Cookie("token")
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{
			"isAuthenticated": false,
			"message":         "No token found",
		})
		return
	}


	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return []byte(secretKey), nil
	})
	if err != nil || !token.Valid {
		c.JSON(http.StatusUnauthorized, gin.H{
			"isAuthenticated": false,
			"message":         "Invalid token",
		})
		return
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{
			"isAuthenticated": false,
			"message":         "Invalid token format",
		})
		return
	}


	c.JSON(http.StatusOK, gin.H{
		"isAuthenticated": true,
		"payload":         claims,
	})
}
