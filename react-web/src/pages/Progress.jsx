import { useEffect, useState } from 'react';
import { progressAPI } from '../services/api';
import { TrendingUp } from 'lucide-react';

export default function Progress() {
  const [progress, setProgress] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const response = await progressAPI.getUserProgress();
      setProgress(response.data);
    } catch (error) {
      console.error('Failed to load progress:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24 md:pb-8">
      <h1 className="text-3xl font-display font-bold text-gray-900 mb-6">
        Your Progress
      </h1>
      
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-emerald-400 rounded-xl flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Learning Journey</h2>
            <p className="text-gray-600">Track your achievements</p>
          </div>
        </div>

        {/* Progress visualization would go here */}
        <div className="text-center py-12">
          <p className="text-gray-600">
            Progress tracking visualization coming soon!
          </p>
        </div>
      </div>
    </div>
  );
}
