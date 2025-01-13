import api from "./api"; // Ensure this path matches your API instance

export const login = async (username, password) => {
  try {
    const response = await api.post("/auth/login", {
      username,
      password: password,
    });

    return response.data;
  } catch (error) {
    console.error("Login failed:", error.response?.data || error.message);
    throw error;
  }
};
