import React, { useState } from "react";

const SpeechToText = () => {
  const [text, setText] = useState("");
  const [isListening, setIsListening] = useState(false);

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "en-US";

  recognition.onresult = (event) => {
    const transcript = Array.from(event.results)
      .map((result) => result[0].transcript)
      .join("");
    setText(transcript);
  };

  const startListening = () => {
    setIsListening(true);
    recognition.start();
  };

  const stopListening = () => {
    setIsListening(false);
    recognition.stop();
  };

  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Speech to Text</h2>
      
      
      <button
        onClick={toggleListening}
        style={{
          backgroundColor: isListening ? "red" : "#4CAF50",
          color: "white",
          border: "none",
          padding: "15px",
          borderRadius: "50%",
          fontSize: "24px",
          cursor: "pointer",
        }}
      >
        🎤
      </button>
      
      <p style={{ marginTop: "20px", fontSize: "18px" }}>{text}</p>
    </div>
  );
};

export default SpeechToText;
