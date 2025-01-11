import React from 'react';
import ReactDOM from 'react-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme';
import App from './App';
// import './styles.css';

ReactDOM.render(
  <ThemeProvider theme={theme}>
  <React.StrictMode>
    <App />
  </React.StrictMode></ThemeProvider>,
  document.getElementById('root')
);
