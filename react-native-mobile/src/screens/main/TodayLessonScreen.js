import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import { lessonsAPI } from '../../services/api';
import AudioRecorderPlayer from 'react-native-audio-recorder-player';

const audioRecorderPlayer = new AudioRecorderPlayer();

export default function TodayLessonScreen() {
  const [lesson, setLesson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [recordPath, setRecordPath] = useState(null);

  useEffect(() => {
    loadLesson();
    return () => {
      audioRecorderPlayer.stopRecorder();
    };
  }, []);

  const loadLesson = async () => {
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
      const path = await audioRecorderPlayer.startRecorder();
      setRecordPath(path);
      setIsRecording(true);
    } catch (error) {
      Alert.alert('Error', 'Failed to start recording');
    }
  };

  const stopRecording = async () => {
    try {
      await audioRecorderPlayer.stopRecorder();
      setIsRecording(false);
      
      if (recordPath && lesson) {
        await lessonsAPI.submitRecording(lesson.id, recordPath);
        Alert.alert('Success', 'Recording submitted!');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to submit recording');
    }
  };

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <Text>Loading...</Text>
      </View>
    );
  }

  if (!lesson) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.centered}>
          <Icon name="book-outline" size={64} color="#9CA3AF" />
          <Text style={styles.emptyText}>No lesson for today</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{lesson.title}</Text>
        <Text style={styles.subtitle}>{lesson.description}</Text>
      </View>

      <View style={styles.phonemeCard}>
        <Text style={styles.phonemeLabel}>Today's Sound</Text>
        <Text style={styles.phoneme}>{lesson.phoneme}</Text>
        <Text style={styles.example}>{lesson.exampleWord}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Your Turn!</Text>
        <Text style={styles.sectionText}>
          Record yourself saying the sound
        </Text>
        
        <TouchableOpacity
          style={[styles.recordButton, isRecording && styles.recordingButton]}
          onPress={isRecording ? stopRecording : startRecording}>
          <Icon
            name={isRecording ? 'stop-circle' : 'mic'}
            size={32}
            color="#FFFFFF"
          />
          <Text style={styles.recordButtonText}>
            {isRecording ? 'Stop Recording' : 'Start Recording'}
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6B7280',
  },
  phonemeCard: {
    margin: 20,
    padding: 40,
    backgroundColor: '#FFFFFF',
    borderRadius: 24,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  phonemeLabel: {
    fontSize: 14,
    color: '#9333EA',
    fontWeight: '600',
    marginBottom: 16,
  },
  phoneme: {
    fontSize: 96,
    fontWeight: 'bold',
    color: '#9333EA',
    marginBottom: 16,
  },
  example: {
    fontSize: 24,
    color: '#6B7280',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 8,
  },
  sectionText: {
    fontSize: 16,
    color: '#6B7280',
    marginBottom: 24,
  },
  recordButton: {
    backgroundColor: '#9333EA',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 20,
    borderRadius: 16,
    gap: 12,
  },
  recordingButton: {
    backgroundColor: '#DC2626',
  },
  recordButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  emptyText: {
    fontSize: 18,
    color: '#6B7280',
    marginTop: 16,
  },
});
