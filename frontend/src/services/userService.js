import api from './api';

// Get all users
export const getAllUsers = async () => {
  try {
    const response = await api.get('/user/users');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch users:', error.response?.data || error.message);
    throw error;
  }
};

// Create a new user
export const createUser = async (userData) => {
  try {
    const response = await api.post('/user/users', userData);
    return response.data;
  } catch (error) {
    console.error('Failed to create user:', error.response?.data || error.message);
    throw error;
  }
};

// Search for a user
export const searchUser = async (username) => {
  try {
    const response = await api.get('/user/users/search', {
      params: { username },
    });
    return response.data;
  } catch (error) {
    console.error('Failed to search user:', error.response?.data || error.message);
    throw error;
  }
};

// Get a user by ID
export const getUserById = async (userId) => {
  try {
    const response = await api.get(`/user/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user by ID:', error.response?.data || error.message);
    throw error;
  }
};

// Update a user
export const updateUser = async (userId, updateData) => {
  try {
    const response = await api.put(`/user/users/${userId}`, updateData);
    return response.data;
  } catch (error) {
    console.error('Failed to update user:', error.response?.data || error.message);
    throw error;
  }
};

// Delete a user
export const deleteUser = async (userId) => {
  try {
    const response = await api.delete(`/user/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to delete user:', error.response?.data || error.message);
    throw error;
  }
};

// Activate a user
export const activateUser = async (userId) => {
  try {
    const response = await api.patch(`/user/users/${userId}/activate`);
    return response.data;
  } catch (error) {
    console.error('Failed to activate user:', error.response?.data || error.message);
    throw error;
  }
};

// Deactivate a user
export const deactivateUser = async (userId) => {
  try {
    const response = await api.patch(`/user/users/${userId}/deactivate`);
    return response.data;
  } catch (error) {
    console.error('Failed to deactivate user:', error.response?.data || error.message);
    throw error;
  }
};
