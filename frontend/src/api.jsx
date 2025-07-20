import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const registerUser = (user) => axios.post(`${API_BASE}/register`, user);

export const loginUser = (user) => axios.post(`${API_BASE}/login`, user);

export const generateID = (formData) =>
  axios.post(`${API_BASE}/generate-id`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
