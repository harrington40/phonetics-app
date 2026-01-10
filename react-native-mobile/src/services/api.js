import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Update this to your backend URL
const API_BASE_URL = __DEV__ 
  ? 'http://10.0.2.2:8000'  // Android emulator
  : 'https://your-production-api.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    try {
      const authData = await AsyncStorage.getItem('auth-storage');
      if (authData) {
        const parsed = JSON.parse(authData);
        if (parsed.state?.token) {
          config.headers.Authorization = `Bearer ${parsed.state.token}`;
        }
      }
    } catch (error) {
      console.error('Error reading auth token:', error);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await AsyncStorage.removeItem('auth-storage');
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  logout: () => api.post('/api/auth/logout'),
  getProfile: () => api.get('/api/auth/profile'),
};

export const lessonsAPI = {
  getTodayLesson: () => api.get('/api/lessons/today'),
  getAllLessons: () => api.get('/api/lessons'),
  getLessonById: (id) => api.get(`/api/lessons/${id}`),
  submitRecording: (lessonId, audioUri) => {
    const formData = new FormData();
    formData.append('audio', {
      uri: audioUri,
      type: 'audio/m4a',
      name: 'recording.m4a',
    });
    formData.append('lesson_id', lessonId);
    return api.post('/api/lessons/submit-recording', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const progressAPI = {
  getUserProgress: () => api.get('/api/progress'),
  getLessonProgress: (lessonId) => api.get(`/api/progress/lesson/${lessonId}`),
  updateProgress: (lessonId, data) => api.post(`/api/progress/lesson/${lessonId}`, data),
  getStats: () => api.get('/api/progress/stats'),
};

export default api;
