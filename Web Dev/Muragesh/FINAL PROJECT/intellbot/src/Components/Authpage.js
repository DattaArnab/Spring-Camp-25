import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import "./Auth.css";

const AuthPage = () => {
  const navigate = useNavigate();
  const [isRegister, setIsRegister] = useState(false);
  const [formdata, setFormdata] = useState({
    name: "",
    email: "",
    password: "",
    country: "",
    interests: "",
  });

 
  const handleChange = (e) => {
    setFormdata({ ...formdata, [e.target.name]: e.target.value });
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = isRegister ? "http://localhost:8080/register" : "http://localhost:8080/login";
  
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formdata),
        credentials: "include", // 🔹 Allows cookies to be stored
      });
  
      if (response.ok) {
        setFormdata({ name: "", email: "", password: "", country: "", interests: "" });
        navigate("/mainpage");
      } else {
        const data = await response.json();
        alert(data.error);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong");
    }
  };
  

  return (
    <div className="mainauth">
  <div className="leftauth">
  <h1 className="title">Welcome to IntellBot</h1>
  <img src="/logo.png" alt="IntellBot Logo" className="logo" />
  <p className="descriptionn">
    IntellBot is your smart AI-powered chatbot, designed to assist, engage, 
    and solve queries with ease. Experience seamless communication now!
  </p>
  <br></br>  <br></br>   <br></br>
  <p className="description">
    <span className="animated-text">
      <span> Your AI-powered assistant.</span>
      <span> Solving queries in seconds.</span>
      <span> Experience seamless communication.</span>
      <span> Smart. Fast. Reliable.</span>
    </span>
  </p>
</div>

    <div className="auth-container">
      {/* <div className="auth-quote">
        <h2>“Innovation distinguishes between a leader and a follower.”</h2>
        <p>Welcome to IntellBot – your gateway to a smarter future.</p>
      </div> */}

      <div className="auth-form-container">
        <div className="auth-card">
          <h2>{isRegister ? "Create Your Account" : "Welcome Back"}</h2>
          <p>
            {isRegister
              ? "Join us and explore a world of AI-powered insights."
              : "Sign in to unlock the future of smart collaboration."}
          </p>

          <form onSubmit={handleSubmit}>
            {isRegister && (
              <>
                <input
                  type="text"
                  name="name"
                  placeholder="Full Name"
                  value={formdata.name}
                  onChange={handleChange}
                  required
                />
                <input
                  type="text"
                  name="country"
                  placeholder="Country"
                  value={formdata.country}
                  onChange={handleChange}
                  required
                />
                <input
                  type="text"
                  name="interests"
                  placeholder="Interests"
                  value={formdata.interests}
                  onChange={handleChange}
                />
              </>
            )}
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formdata.email}
              onChange={handleChange}
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formdata.password}
              onChange={handleChange}
              required
            />
            <button type="submit">
              {isRegister ? "Register" : "Log In"}
            </button>
          </form>
          <p className="toggle-text" onClick={() => setIsRegister(!isRegister)}>
            {isRegister
              ? "Already have an account? Log In"
              : "Don't have an account? Register Now"}
          </p>
        </div>
      </div>
    </div>
    </div>
  );
};

export default AuthPage;
