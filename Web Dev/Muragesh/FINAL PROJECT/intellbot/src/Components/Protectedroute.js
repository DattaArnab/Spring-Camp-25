import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import useStore from "./store";

const ProtectedRoute = ({ element }) => {
  const [isAuthorized, setIsAuthorized] = useState(null);
  const { ema, setEm } = useStore();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch("http://localhost:8080/api/isauthorized", {
          method: "GET", 
          credentials: "include", 
        });

        const data = await response.json();
        
        if (data?.payload?.useremail) {
          setEm(data.payload.useremail);
        }

        setIsAuthorized(response.ok && data.isAuthenticated);
      } catch (error) {
        console.error("Error checking authorization:", error);
        setIsAuthorized(false);
      }
    };

    checkAuth();
  }, [setEm]);

  if (isAuthorized === null) {
    return <div>Loading...</div>; 
  }

  return isAuthorized ? element : <Navigate to="/" />;
};

export default ProtectedRoute;
