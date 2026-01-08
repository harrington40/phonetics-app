import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:phonetics_poc/models/lesson.dart';
import 'package:phonetics_poc/services/api_service.dart';
import 'package:phonetics_poc/services/recording_service.dart';
import 'package:phonetics_poc/widgets/cartoon_animal.dart';
import 'package:phonetics_poc/widgets/activity_graphics.dart';

void main() {
  runApp(const PhonicsPoC());
}

class PhonicsPoC extends StatelessWidget {
  const PhonicsPoC({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Phonetics Learning App',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF667eea),
          brightness: Brightness.light,
        ),
      ),
      home: const LessonScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class LessonScreen extends StatefulWidget {
  const LessonScreen({super.key});

  @override
  State<LessonScreen> createState() => _LessonScreenState();
}

class _LessonScreenState extends State<LessonScreen> {
  Lesson? lesson;
  final player = AudioPlayer();
  final apiService = ApiService();
  final recordingService = RecordingService();
  Timer? timer;
  Stopwatch stopwatch = Stopwatch();

  Viseme currentViseme = Viseme.rest;
  bool isLoading = false;
  bool isPlaying = false;
  bool isRecording = false;
  bool showRewardGraphic = false;
  double recordingScore = 0;
  String? recordingPath;
  String? errorMessage;

  @override
  void dispose() {
    timer?.cancel();
    player.dispose();
    recordingService.dispose();
    super.dispose();
  }

  Future<void> loadLesson() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });
    try {
      final loadedLesson = await apiService.getLesson();
      setState(() {
        lesson = loadedLesson;
        currentViseme = Viseme.rest;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Error loading lesson: $e';
        isLoading = false;
      });
    }
  }

  void startVisemeScheduler(List<VisemeCue> cues) {
    timer?.cancel();
    stopwatch
      ..reset()
      ..start();

    timer = Timer.periodic(const Duration(milliseconds: 16), (_) {
      final t = stopwatch.elapsedMilliseconds;
      Viseme next = Viseme.rest;

      for (final c in cues) {
        if (t >= c.startMs && t < c.endMs) {
          next = c.viseme;
          break;
        }
      }

      if (mounted && next != currentViseme) {
        setState(() => currentViseme = next);
      }
    });
  }

  Future<void> startRecording() async {
    try {
      final path = await recordingService.startRecording();
      if (path != null) {
        setState(() {
          isRecording = true;
          recordingPath = path;
          errorMessage = null;
        });
      } else {
        setState(() {
          errorMessage = 'Microphone permission denied or recording failed';
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error starting recording: $e';
      });
    }
  }

  Future<void> stopRecording() async {
    try {
      final path = await recordingService.stopRecording();
      setState(() {
        isRecording = false;
      });

      if (path != null) {
        // Send recording to backend
        try {
          final feedback = await apiService.submitRecording(
            filePath: path,
            lessonId: lesson?.id ?? 'unknown',
          );

          setState(() {
            errorMessage = null;
            recordingPath = null;
            // Show reward graphic if successful (accuracy >= 70%)
            if (feedback.accuracy >= 70) {
              showRewardGraphic = true;
              recordingScore = feedback.accuracy.toDouble();
              // Auto-hide reward after 3 seconds
              Future.delayed(const Duration(seconds: 3), () {
                if (mounted) {
                  setState(() {
                    showRewardGraphic = false;
                  });
                }
              });
            }
          });

          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Great job! Accuracy: ${feedback.accuracy}%'),
              backgroundColor: Colors.green,
            ),
          );
        } catch (e) {
          setState(() {
            errorMessage = 'Error uploading recording: $e';
          });
        }
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error stopping recording: $e';
        isRecording = false;
      });
    }
  }

  Future<void> playLesson() async {
    final l = lesson;
    if (l == null || isPlaying) return;

    setState(() => isPlaying = true);
    startVisemeScheduler(l.visemes);

    try {
      // Try to play audio (will fail for demo URLs but that's OK)
      try {
        await player.play(UrlSource(l.audioUrl));
      } catch (e) {
        // Expected for demo URLs - just simulate timing
        debugPrint('Audio play failed (expected): $e');
      }

      // Simulate animation completion
      Future.delayed(const Duration(milliseconds: 1000), () {
        if (mounted) {
          stopwatch.stop();
          timer?.cancel();
          setState(() {
            currentViseme = Viseme.rest;
            isPlaying = false;
          });
        }
      });

      player.onPlayerComplete.listen((_) {
        stopwatch.stop();
        timer?.cancel();
        if (mounted) {
          setState(() {
            currentViseme = Viseme.rest;
            isPlaying = false;
          });
        }
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Error playing audio: $e';
        isPlaying = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final l = lesson;
    final isMobile = MediaQuery.of(context).size.width < 600;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Phonetics Learning App'),
        centerTitle: true,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(isMobile ? 16 : 24),
          child: Column(
            children: [
              // Status indicator
              if (errorMessage != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    border: Border.all(color: Colors.red.shade300),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error, color: Colors.red.shade700),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          errorMessage!,
                          style: TextStyle(color: Colors.red.shade700),
                        ),
                      ),
                    ],
                  ),
                ),

              const SizedBox(height: 24),

              // Show reward graphic if recording was successful
              if (showRewardGraphic)
                Card(
                  elevation: 4,
                  color: const Color(0xFFFFF9C4),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        RewardGraphic(score: recordingScore),
                        const SizedBox(height: 16),
                        Text(
                          'Excellent work!',
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                color: Colors.black87,
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                      ],
                    ),
                  ),
                )
              // Show activity graphic when lesson is loaded
              else if (l != null && !showRewardGraphic)
                Card(
                  elevation: 2,
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: ListenChooseGraphic(
                      phoneme: l.phoneme,
                      size: Size(
                        MediaQuery.of(context).size.width - 64,
                        250,
                      ),
                    ),
                  ),
                ),

              const SizedBox(height: 24),

              // Cartoon animal
              Center(
                child: Container(
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.1),
                        blurRadius: 10,
                        offset: const Offset(0, 5),
                      ),
                    ],
                  ),
                  child: CartoonAnimal(viseme: currentViseme),
                ),
              ),

              const SizedBox(height: 32),

              // Lesson info
              if (l != null)
                Card(
                  elevation: 2,
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        Text(
                          l.phoneme,
                          style: Theme.of(context).textTheme.displayMedium?.copyWith(
                                color: const Color(0xFF667eea),
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                        const SizedBox(height: 12),
                        Text(
                          l.prompt,
                          textAlign: TextAlign.center,
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                      ],
                    ),
                  ),
                )
              else
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    'Tap "Get Lesson" to start',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          color: Colors.grey[600],
                        ),
                  ),
                ),

              const SizedBox(height: 32),

              // Buttons
              SizedBox(
                width: double.infinity,
                child: Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  children: [
                    Expanded(
                      child: FilledButton.icon(
                        onPressed: isLoading ? null : loadLesson,
                        icon: isLoading
                            ? SizedBox(
                                height: 20,
                                width: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation(
                                    Theme.of(context).colorScheme.onPrimary,
                                  ),
                                ),
                              )
                            : const Icon(Icons.refresh),
                        label: const Text('Get Lesson'),
                      ),
                    ),
                    Expanded(
                      child: FilledButton.tonalIcon(
                        onPressed: (l == null || isPlaying) ? null : playLesson,
                        icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
                        label: Text(isPlaying ? 'Playing...' : 'Play & Animate'),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Recording section
              if (l != null)
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.orange[50],
                    border: Border.all(color: Colors.orange[200]!),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    children: [
                      Row(
                        children: [
                          Icon(Icons.mic, color: Colors.orange[700]),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              isRecording
                                  ? '🔴 Recording...'
                                  : 'Ready to record',
                              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.orange[700],
                                  ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      SizedBox(
                        width: double.infinity,
                        child: FilledButton.tonalIcon(
                          onPressed: isRecording ? stopRecording : startRecording,
                          icon: Icon(
                            isRecording ? Icons.stop : Icons.mic,
                            color: Colors.orange[700],
                          ),
                          label: Text(
                            isRecording ? 'Stop Recording' : 'Start Recording',
                          ),
                          style: FilledButton.styleFrom(
                            backgroundColor: Colors.orange[100],
                            foregroundColor: Colors.orange[700],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              const SizedBox(height: 24),

              // Features info
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.blue[50],
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.blue[200]!),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '✨ Features',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 8),
                    ...[
                      'Real-time mouth animation (visemes)',
                      'Audio playback synchronization',
                      'Phoneme-specific lessons',
                      'Progress tracking ready',
                    ]
                        .map(
                          (feature) => Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4),
                            child: Row(
                              children: [
                                const Icon(Icons.check_circle,
                                    size: 16, color: Colors.green),
                                const SizedBox(width: 8),
                                Text(feature,
                                    style:
                                        Theme.of(context).textTheme.bodySmall),
                              ],
                            ),
                          ),
                        ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
