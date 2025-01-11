import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // Adding a custom CSS file for styling

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add your authentication logic here
    console.log('Logging in with', username, password);
    navigate('/home');
  };

  return (
<div className="login-container">
  {/* Phần ảnh bên trái */}
  <div className="login-left">
    <img src="/vct.jpg" alt="Login" className="login-image" />
  </div>

  {/* Phần form bên phải */}
  <div className="login-right">
    <h1>Login</h1>
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
        />
      </div>

      <button type="submit" className="btn-login">Continue</button>
    </form>
  </div>
</div>

  );
};

export default LoginPage;
