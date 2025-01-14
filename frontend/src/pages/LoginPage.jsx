import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css"; // Adding a custom CSS file for styling
import { authen } from "../services/authService"; // Import the authen function from the API file
import { Box, Typography, TextField, Button, Paper } from "@mui/material";
import { AuthContext } from "../App";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { login } = React.useContext(AuthContext);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Add your authentication logic here
    console.log("Logging in with", username, password);
    if (!username || !password) {
      setError("Username and password are required");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await authen(username, password);
      console.log("Login successful:", data);
      // Handle successful login (e.g., redirect, save token)
      login(data.data.access_token);
      navigate("/home");
    } catch (err) {
      setError(
        err.response?.data?.message || "Login failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {/* Phần ảnh bên trái */}
      <div className="login-left">
        <img src="/vct.jpg" alt="Login" className="login-image" />
      </div>

      {/* Phần form bên phải */}
      <div className="login-right">
        <h1>Đăng nhập</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Tên đăng nhập</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Nhập tên đăng nhập"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Mật khẩu</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Nhập mật khẩu"
              required
            />
          </div>
          {error && (
            <Typography color="error" sx={{ mb: 2 }}>
              {error}
            </Typography>
          )}
          <button type="submit" className="btn-login">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
