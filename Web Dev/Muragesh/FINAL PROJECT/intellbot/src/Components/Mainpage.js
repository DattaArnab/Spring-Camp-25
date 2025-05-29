import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";
import Historypromp from "./Historypromp";
import moment from "moment";
import useStore from "./store";
import Tesseract from "tesseract.js";
import { data } from "react-router-dom";
import("./Mainpage.css");

function Mainpage() {
  const [promp, setPromp] = useState({ text: "" });
  const [aians, setAians] = useState("");
  const [sessionarry, setSessionary] = useState([]);
  const [allprompt, setAll] = useState([]);
  const [Islisten, setIslisten] = useState(false);
  const [main, Setmail] = useState("");
  const [displ, setDispl] = useState("none");
  const [saves, setSaved] = useState([]);
  const [text, setText] = useState("");
  const [listtext,setList]=useState("")
  const [dis, setDis] = useState("none");
  const { ema } = useStore();
  const [isAIReady, setIsAIReady] = useState(false);
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const speak = () => {
  setList(aians)
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(listtext);
      speechSynthesis.speak(utterance);
    } else {
      alert("Your browser does not support speech synthesis.");
    }
  };

 
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file)); // Preview image
      extractText(file); // Process OCR
    }
  };

  // Extract text from image using OCR
  const extractText = async (file) => {
    setLoading(true);
    try {
      const { data: { text } } = await Tesseract.recognize(file, "eng", {
        logger: (m) => console.log(m) 
      });

      setText(text);
      setSessionary([...sessionarry, text]); 
      setPromp({ text });

    } catch (error) {
      console.error("OCR Error:", error);
    }
    setLoading(false);
  };

  const handleChange = (e) => {
    setPromp({ ...promp, [e.target.name]: e.target.value });
  };

  const sendpromp = async () => {
    setIsAIReady(true);
    setDispl("");
    setDis("");

    try {
      const updatedText = [...sessionarry, text || promp.text]; 
      const sessionString = updatedText.join(" ");

      const response = await fetch("http://localhost:8080/api/askai", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: sessionString }),
      });

      const data = await response.json();
      setSessionary(updatedText);
      setAians(data.response);
      setIsAIReady(false);
      setPromp({ text: "" });
      setText(""); 
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const funNew = async () => {
    if (sessionarry.length === 0) {
      alert("YOU ARE ALREADY IN NEW CHAT ");
      return;
    } else {
      setDis("none");
      setDispl("none");
      console.log(sessionarry);
      const sessionString = await sessionarry.join(" ");
      setSessionary([]);
      setAians("");
      setPromp({ text: "" });

      const response = await fetch("http://localhost:8080/newprompt", {
        method: "POST",
        headers: { "Content-Type": "application/json", email: ema },
        body: JSON.stringify({
          useremail: ema,
          prompt: sessionString,
          posted_on: new Date().toISOString(),
        }),
      });

      const data = await response.json();
      setAll(data.all_prompts.reverse());
      console.log(data.all_prompts);
    }
  };

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("THIS FEATURE IS NOT SUPPORTED IN YOUR SYSTEM CHANGE BROWSER");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      setIslisten(true);
    };

    recognition.onend = () => {
      setIslisten(false);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setPromp((prev) => ({ text: prev.text + " " + transcript }));
    };

    recognition.start();
  };

  const displayl = async () => {
    const response = await fetch("http://localhost:8080/all", {
      method: "POST",
      headers: { "Content-Type": "application/json", email: ema },
    });
    const data = await response.json();

    setAll(data.all_prompts.reverse());
    console.log(ema);
  };

  useEffect(() => {
    displayl();
  }, []);

  const funsave = async () => {
    const response = await fetch("http://localhost:8080/saveprompt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        useremail: ema,
        msgai: aians,
      }),
    });
    setDispl("none");
  };

  return (
    <div className="mainback">
      <Navbar />
      <div className="lowermain">
        <div className="history">
          <div style={{ display: "flex" }}>
            <h3 style={{ color: "#b5d8f2" }}>
              <b>History</b>
            </h3>
            <button className="newchat" onClick={funNew}>New chat</button>
          </div>
          <h4 style={{ color: "#b5d8f2" }}>Analyze what we are discussed</h4>
          {allprompt.map((pr, index) => (
            <Historypromp key={index} msg={pr.prompt.substring(0, 100)} tim={moment(pr.posted_on).fromNow()} />
          ))}
        </div>

        <div className="realapp">
          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="text"
              className="inputmain"
              value={text || promp.text} 
              onChange={handleChange}
              name="text"
              placeholder="Feel free to ask anything..."
            />

            <button onClick={startListening} style={{
              backgroundColor: Islisten ? "red" : "#4CAF50",
              color: "white",
              border: "none",
              padding: "12px",
              borderRadius: "50%",
              fontSize: "18px",
              marginLeft: "10px",
              cursor: "pointer",
            }}>🎤</button>
          </div>

          <input type="file" accept="image/*" onChange={handleImageChange} className="fileadd" />
          <label for="fileInput" class="file-label">Choose File</label>
          <div class="file-name" id="fileName">No file selected</div>

          <button className="butinput" onClick={sendpromp}>Send</button>

          <button className="butt" onClick={funsave} style={{ display: displ }}>Save This Response</button>

          <button onClick={speak} style={{ marginLeft: "1rem", width: "3rem", height: "2rem", backgroundColor: "#4CAF50", display: dis, marginTop: "1rem" }}>🔊</button>

          <h2 style={{ color: "white", marginTop: "2rem" }}>{aians}</h2>

          {isAIReady && <div className="typing-indicator"><span></span><span></span><span></span></div>}
        </div>
      </div>
    </div>
  );
}

export default Mainpage;
