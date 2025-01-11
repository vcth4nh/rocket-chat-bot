import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FormInput from '../components/FormInput';
import { login } from '../services/authService';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (username === '' || password === '') {
      setErrorMessage('All fields are required!');
      return;
    }

    try {
      const isAuthenticated = await login(username, password);
      if (isAuthenticated) {
        navigate('/home'); // Redirect to home page
      } else {
        setErrorMessage('Invalid username or password.');
      }
    } catch (error) {
      console.error('Authentication failed:', error);
      setErrorMessage('Something went wrong. Please try again later.');
    }
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <FormInput
          id="username"
          label="Username:"
          type="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
        />
        <FormInput
          id="password"
          label="Password:"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
