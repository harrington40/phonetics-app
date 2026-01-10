import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-storage');
    if (token) {
      try {
        const parsed = JSON.parse(token);
        if (parsed.state?.token) {
          config.headers.Authorization = `Bearer ${parsed.state.token}`;
        }
      } catch (error) {
        console.error('Error parsing token:', error);
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - clear auth and redirect to login
      localStorage.removeItem('auth-storage');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  logout: () => api.post('/api/auth/logout'),
  getProfile: () => api.get('/api/auth/profile'),
  updateProfile: (data) => api.put('/api/auth/profile', data),
};

export const lessonsAPI = {
  getTodayLesson: () => api.get('/api/lessons/today'),
  getAllLessons: () => api.get('/api/lessons'),
  getLessonById: (id) => api.get(`/api/lessons/${id}`),
  submitRecording: (lessonId, audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
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

export const parentAPI = {
  getChildProgress: (childId) => api.get(`/api/parent/child/${childId}/progress`),
  getAllChildren: () => api.get('/api/parent/children'),
  getReports: (childId, dateRange) => 
    api.get(`/api/parent/child/${childId}/reports`, { params: dateRange }),
};

export default api;
