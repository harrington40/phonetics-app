import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/models.dart';
import '../services/api_service.dart';

final apiServiceProvider = Provider((ref) => ApiService());

final sessionProvider = StateNotifierProvider<SessionNotifier, List<SessionItem>>((ref) {
  return SessionNotifier(ref.watch(apiServiceProvider));
});

final progressProvider = FutureProvider((ref) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.getProgress();
});

final currentStreakProvider = StateProvider<int>((ref) => 0);

final sessionStartTimeProvider = StateProvider<DateTime?>((ref) => null);

final adminStatsProvider = FutureProvider((ref) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.getAdminStats();
});

class SessionNotifier extends StateNotifier<List<SessionItem>> {
  final ApiService apiService;

  SessionNotifier(this.apiService) : super([]);

  Future<void> buildSession() async {
    try {
      final result = await apiService.buildSession();
      // Parse session items from result
      final items = (result['session'] as List<dynamic>?)
          ?.map((item) {
            return SessionItem(
              id: item['id'] ?? '',
              skillId: item['skill_id'] ?? '',
              type: item['type'] ?? 'listen_choose',
              lesson: Lesson.fromJson(item['lesson'] ?? {}),
            );
          })
          .toList() ??
          [];
      state = items;
    } catch (e) {
      print('Error building session: $e');
    }
  }

  void removeItem(String itemId) {
    state = state.where((item) => item.id != itemId).toList();
  }
}
