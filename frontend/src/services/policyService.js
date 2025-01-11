import api from './api';

// Get all policy rules
export const getAllPolicies = async () => {
  try {
    const response = await api.get('/policy/policies');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch policies:', error.response?.data || error.message);
    throw error;
  }
};

// Create a new policy rule
export const createPolicy = async (policyData) => {
  try {
    const response = await api.post('/policy/policies', policyData);
    return response.data;
  } catch (error) {
    console.error('Failed to create policy:', error.response?.data || error.message);
    throw error;
  }
};

// Get a policy by ID
export const getPolicyById = async (policyId) => {
  try {
    const response = await api.get(`/policy/policies/${policyId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch policy by ID:', error.response?.data || error.message);
    throw error;
  }
};

// Update a policy
export const updatePolicy = async (policyId, updateData) => {
  try {
    const response = await api.put(`/policy/policies/${policyId}`, updateData);
    return response.data;
  } catch (error) {
    console.error('Failed to update policy:', error.response?.data || error.message);
    throw error;
  }
};

// Delete a policy
export const deletePolicy = async (policyId) => {
  try {
    const response = await api.delete(`/policy/policies/${policyId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to delete policy:', error.response?.data || error.message);
    throw error;
  }
};
