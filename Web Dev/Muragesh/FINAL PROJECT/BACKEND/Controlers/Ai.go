package Controlers

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/gin-gonic/gin"
)


type AIRequest struct {
	Text string `json:"text"`
}


type GroqRequest struct {
	Model    string    `json:"model"`
	Messages []Message `json:"messages"`
}


type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}


func AskAI(input string) (string, error) {
	url := "https://api.groq.com/openai/v1/chat/completions"
	apiKey := "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" //scrt

	requestBody, _ := json.Marshal(GroqRequest{
		Model: "mixtral-8x7b-32768",
		Messages: []Message{
			{Role: "user", Content: input},
		},
	})

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(requestBody))
	if err != nil {
		return "", err
	}


	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()


	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}


	var result map[string]interface{}
	json.Unmarshal(body, &result)

	if choices, ok := result["choices"].([]interface{}); ok {
		if len(choices) > 0 {
			firstChoice := choices[0].(map[string]interface{})
			message := firstChoice["message"].(map[string]interface{})
			return message["content"].(string), nil
		}
	}

	return "", fmt.Errorf("invalid response from AI")
}


func GetResponse(c *gin.Context) {
	var input AIRequest


	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input"})
		return
	}

	response, err := AskAI(input.Text)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get AI response"})
		return
	}


	c.JSON(http.StatusOK, gin.H{"response": response})
}
