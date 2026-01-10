import { useEffect, useState } from 'react';
import { lessonsAPI } from '../services/api';
import { Play, Mic, CheckCircle } from 'lucide-react';

export default function TodayLesson() {
  const [lesson, setLesson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  useEffect(() => {
    loadTodayLesson();
  }, []);

  const loadTodayLesson = async () => {
    try {
      const response = await lessonsAPI.getTodayLesson();
      setLesson(response.data);
    } catch (error) {
      console.error('Failed to load lesson:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const audioChunks = [];

      recorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        await lessonsAPI.submitRecording(lesson.id, audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('Could not access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No lesson for today</h2>
        <p className="text-gray-600">Check back tomorrow for new content!</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24 md:pb-8">
      <div className="card">
        {/* Lesson Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-display font-bold text-gray-900 mb-2">
            {lesson.title}
          </h1>
          <p className="text-lg text-gray-600">{lesson.description}</p>
        </div>

        {/* Phoneme Display */}
        <div className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl p-8 mb-8 text-center">
          <p className="text-sm text-purple-600 font-semibold mb-2">Today's Sound</p>
          <div className="text-8xl font-bold text-gradient mb-4">
            {lesson.phoneme}
          </div>
          <p className="text-xl text-gray-700">{lesson.exampleWord}</p>
        </div>

        {/* Audio Playback */}
        {lesson.audioUrl && (
          <div className="mb-8">
            <button
              onClick={() => new Audio(lesson.audioUrl).play()}
              className="btn-primary w-full flex items-center justify-center space-x-2"
            >
              <Play className="w-5 h-5" />
              <span>Listen to Example</span>
            </button>
          </div>
        )}

        {/* Recording Section */}
        <div className="mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Your Turn!</h3>
          <p className="text-gray-600 mb-4">
            Record yourself saying the sound. Your teacher will review it!
          </p>
          
          <button
            onClick={isRecording ? stopRecording : startRecording}
            className={`w-full py-4 rounded-2xl font-semibold flex items-center justify-center space-x-2 transition-all ${
              isRecording
                ? 'bg-red-500 text-white hover:bg-red-600 animate-pulse'
                : 'bg-gradient-to-r from-pink-500 to-purple-500 text-white hover:shadow-lg'
            }`}
          >
            <Mic className="w-6 h-6" />
            <span>{isRecording ? 'Stop Recording' : 'Start Recording'}</span>
          </button>
        </div>

        {/* Practice Words */}
        {lesson.practiceWords && lesson.practiceWords.length > 0 && (
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Practice Words</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {lesson.practiceWords.map((word, index) => (
                <div
                  key={index}
                  className="bg-gradient-to-br from-blue-100 to-purple-100 rounded-xl p-4 text-center"
                >
                  <span className="text-2xl font-bold text-gray-900">{word}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
