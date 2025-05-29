import React ,{useState}from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Authpage from "./Components/Authpage";
import Mainpage from "./Components/Mainpage";
import ProtectedRoute from "./Components/Protectedroute"; // Import Protected Route
import("./App.css");

function App() {
  const [useremail,setEmail]=useState("")
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Authpage />} />
        <Route path="/mainpage" element={<ProtectedRoute element={<Mainpage />} />} />
      </Routes>
    </Router>
  );
}

export default App;
