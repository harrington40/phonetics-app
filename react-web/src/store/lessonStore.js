import { create } from 'zustand';

export const useLessonStore = create((set) => ({
  currentLesson: null,
  lessons: [],
  progress: {},
  isLoading: false,
  error: null,

  setCurrentLesson: (lesson) => set({ currentLesson: lesson }),
  
  setLessons: (lessons) => set({ lessons }),
  
  setProgress: (progress) => set({ progress }),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  setError: (error) => set({ error }),
  
  clearError: () => set({ error: null }),
  
  updateLessonProgress: (lessonId, progressData) =>
    set((state) => ({
      progress: {
        ...state.progress,
        [lessonId]: progressData,
      },
    })),
}));
