import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/login', credentials),
  loginWithPassword: (userId, password) => api.post('/login-with-password', { user_id: userId, password }),
  logout: () => api.post('/logout'),
  getCurrentUser: () => api.get('/current-user'),
  verifyPassword: (userId, password) => api.post('/verify-password', { user_id: userId, password }),
};

// Users API
export const usersAPI = {
  getAll: () => api.get('/users'),
  getById: (id) => api.get(`/users/${id}`),
  create: (userData) => api.post('/users', userData),
  update: (id, userData) => api.put(`/users/${id}`, userData),
  delete: (id) => api.delete(`/users/${id}`),
};

// Notes API
export const notesAPI = {
  getByUserId: (userId) => api.get(`/users/${userId}/notes`),
  create: (userId, noteData) => api.post(`/users/${userId}/notes`, noteData),
  update: (userId, noteId, noteData) => api.put(`/users/${userId}/notes/${noteId}`, noteData),
  delete: (userId, noteId) => api.delete(`/users/${userId}/notes/${noteId}`),
};

export default api;
