import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config/api_config.dart';
import '../models/models.dart';

class ApiService {
  Future<Lesson> getLesson() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.backendUrl}/lesson'),
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        return Lesson.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Failed to load lesson: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching lesson: $e');
    }
  }

  Future<Map<String, dynamic>> buildSession() async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.backendUrl}/learning/build-session'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'duration_minutes': 5}),
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to build session: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error building session: $e');
    }
  }

  Future<SkillProgress> submitFeedback(SessionFeedback feedback) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.backendUrl}/learning/feedback'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(feedback.toJson()),
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        return SkillProgress.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Failed to submit feedback: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error submitting feedback: $e');
    }
  }

  Future<List<SkillProgress>> getProgress() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.backendUrl}/learning/progress'),
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data
            .map((item) => SkillProgress.fromJson(item as Map<String, dynamic>))
            .toList();
      } else {
        throw Exception('Failed to load progress: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching progress: $e');
    }
  }

  Future<Map<String, dynamic>> getAdminStats() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.backendUrl}/admin/stats'),
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to load admin stats: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching admin stats: $e');
    }
  }
}
