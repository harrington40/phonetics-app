import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:phonetics_poc/models/lesson.dart';

class ApiService {
  final String baseUrl;

  ApiService({this.baseUrl = 'http://127.0.0.1:8000'});

  Future<Lesson> getLesson() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/lesson'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        return Lesson.fromJson(data);
      } else {
        throw Exception('Failed to load lesson: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching lesson: $e');
    }
  }

  Future<LessonFeedback> submitRecording({
    required String lessonId,
    required String audioPath,
    required Duration duration,
  }) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/api/feedback'),
      );
      request.fields['lesson_id'] = lessonId;
      request.fields['duration_ms'] = duration.inMilliseconds.toString();
      request.files.add(await http.MultipartFile.fromPath('audio', audioPath));

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        return LessonFeedback.fromJson(data);
      } else {
        throw Exception('Failed to submit recording: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error submitting recording: $e');
    }
  }

  Future<List<Lesson>> getLessonProgression({
    required String userId,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/progression/$userId'),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        return data.map((l) => Lesson.fromJson(l as Map<String, dynamic>)).toList();
      } else {
        throw Exception('Failed to load progression: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching progression: $e');
    }
  }

  /// Get audio WAV file for a phoneme using query parameter
  /// Usage: getPhonemeAudio('/m/')
  Future<List<int>> getPhonemeAudio(String phoneme) async {
    try {
      final uri = Uri.parse('$baseUrl/api/audio').replace(
        queryParameters: {'phoneme': phoneme},
      );
      final response = await http.get(uri);
      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        throw Exception('Failed to get audio: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching audio: $e');
    }
  }
}

class LessonFeedback {
  final bool passed;
  final String message;
  final double score;
  final List<String> hints;

  LessonFeedback({
    required this.passed,
    required this.message,
    required this.score,
    required this.hints,
  });

  factory LessonFeedback.fromJson(Map<String, dynamic> json) {
    return LessonFeedback(
      passed: json['passed'] as bool,
      message: json['message'] as String,
      score: (json['score'] as num).toDouble(),
      hints: List<String>.from(json['hints'] as List? ?? []),
    );
  }
}
