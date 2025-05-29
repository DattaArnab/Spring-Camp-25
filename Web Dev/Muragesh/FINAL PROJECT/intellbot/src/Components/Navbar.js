import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import useStore from "./store";
import "./Navbar.css";
import "./Saved.css";

function Navbar() {
  
  const { ema } = useStore();
  const [saves, setSaved] = useState([]);
  const [displayy, setDisplayy] = useState("none");
  const navigate = useNavigate(); // Initialize navigate function

  const funlogout = () => {
    localStorage.removeItem("token"); // Remove token
    navigate("/"); // Redirect to login page
  };

  const toggledisplay = () => {
    if (displayy === "none") setDisplayy("");
    else setDisplayy("none");
  };

  const getallsaved = async () => {
    try {
      const response = await fetch("http://localhost:8080/allSaved", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          email: ema,
        },
      });
      const data = await response.json();
      console.log(data.all_prompts)
      setSaved(data.all_prompts);
    } catch (error) {
      console.error("Error fetching saved notes:", error);
    }
  };

  return (
    <div className="nav">
      <h2 className="heading">
        <strong>INTELLBOT</strong>
      </h2>
      <h2>
        <a
          href="#"
          style={{
            color: "#b5d8f2",
            position: "relative",
            right: "-70vw",
            textDecoration: "none",
            cursor: "pointer",
          }}
          onClick={funlogout}
        >
          <b>Logout</b>
        </a>
      </h2>
      <h2>
        <a
          href="#"
          style={{
            color: "#b5d8f2",
            position: "relative",
            right: "-71vw",
            textDecoration: "none",
            cursor: "pointer",
          }}
          onClick={() => {
            toggledisplay();
            getallsaved(); // Fetch saved notes when toggling
          }}
        >
          <b>SavedNotes</b>
        </a>
      </h2>
      <div className="saved" style={{ display: displayy }}>
        <button onClick={toggledisplay} className="Togbut">Back</button>
        <h3>EXPLORE YOUR SAVED NOTES</h3>
        <ul>
          {saves.length > 0 ? (
            saves.map((save, index) => (
              <li className="asave" style={{margin:"auto",marginTop:"1rem",fontSize:"120%"}} key={index}>{save.msgai}</li>
            ))
          ) : (
            <p>No saved notes found.</p>
          )}
        </ul>
      </div>
    </div>
  );
}

export default Navbar;

