import api from './api';

// Login service
export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login', null, {
      params: { username, password },
    });
    return response.data;
  } catch (error) {
    console.error('Login failed:', error.response?.data || error.message);
    throw error;
  }
};
