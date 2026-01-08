class Lesson {
  final String id;
  final String phoneme;
  final String audioUrl;
  final List<String> exampleWords;
  final String viseme;

  Lesson({
    required this.id,
    required this.phoneme,
    required this.audioUrl,
    required this.exampleWords,
    required this.viseme,
  });

  factory Lesson.fromJson(Map<String, dynamic> json) {
    return Lesson(
      id: json['id'] ?? '',
      phoneme: json['phoneme'] ?? '',
      audioUrl: json['audio_url'] ?? '',
      exampleWords: List<String>.from(json['example_words'] ?? []),
      viseme: json['viseme'] ?? 'rest',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'phoneme': phoneme,
      'audio_url': audioUrl,
      'example_words': exampleWords,
      'viseme': viseme,
    };
  }
}

class SkillProgress {
  final String skillId;
  final double mastery;
  final int totalAttempts;
  final int correctAttempts;
  final DateTime dueAt;
  final double sm2Factor;
  final int interval;

  SkillProgress({
    required this.skillId,
    required this.mastery,
    required this.totalAttempts,
    required this.correctAttempts,
    required this.dueAt,
    this.sm2Factor = 2.5,
    this.interval = 1,
  });

  factory SkillProgress.fromJson(Map<String, dynamic> json) {
    return SkillProgress(
      skillId: json['skill_id'] ?? '',
      mastery: (json['mastery'] ?? 0.0).toDouble(),
      totalAttempts: json['total_attempts'] ?? 0,
      correctAttempts: json['correct_attempts'] ?? 0,
      dueAt: DateTime.parse(json['due_at'] ?? DateTime.now().toIso8601String()),
      sm2Factor: (json['sm2_factor'] ?? 2.5).toDouble(),
      interval: json['interval'] ?? 1,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'skill_id': skillId,
      'mastery': mastery,
      'total_attempts': totalAttempts,
      'correct_attempts': correctAttempts,
      'due_at': dueAt.toIso8601String(),
      'sm2_factor': sm2Factor,
      'interval': interval,
    };
  }
}

class SessionItem {
  final String id;
  final String skillId;
  final String type; // 'listen_choose', 'build_word', 'read_pick'
  final Lesson lesson;

  SessionItem({
    required this.id,
    required this.skillId,
    required this.type,
    required this.lesson,
  });
}

class SessionFeedback {
  final String itemId;
  final bool correct;
  final int secondsSpent;
  final int hintsUsed;
  final int quality; // 0-5

  SessionFeedback({
    required this.itemId,
    required this.correct,
    required this.secondsSpent,
    required this.hintsUsed,
    required this.quality,
  });

  Map<String, dynamic> toJson() {
    return {
      'item_id': itemId,
      'correct': correct,
      'seconds_spent': secondsSpent,
      'hints_used': hintsUsed,
      'quality': quality,
    };
  }
}

class ProgressData {
  final int totalSessions;
  final int completedToday;
  final int streak;
  final Map<String, dynamic> wordMastery;

  ProgressData({
    required this.totalSessions,
    required this.completedToday,
    required this.streak,
    required this.wordMastery,
  });

  factory ProgressData.fromJson(Map<String, dynamic> json) {
    return ProgressData(
      totalSessions: json['total_sessions'] ?? 0,
      completedToday: json['completed_today'] ?? 0,
      streak: json['streak'] ?? 0,
      wordMastery: json['word_mastery'] ?? {},
    );
  }
}

class AdminStats {
  final int totalUsers;
  final int activeUsers;
  final int totalSessions;
  final Map<String, dynamic> recentActivity;
  final int totalTime;
  final int masteredCount;
  final int streak;
  final int reviewDue;
  final String nextReview;
  final double masteryThreshold;

  AdminStats({
    required this.totalUsers,
    required this.activeUsers,
    required this.totalSessions,
    required this.recentActivity,
    this.totalTime = 0,
    this.masteredCount = 0,
    this.streak = 0,
    this.reviewDue = 0,
    this.nextReview = "Tomorrow",
    this.masteryThreshold = 0.8,
  });

  factory AdminStats.fromJson(Map<String, dynamic> json) {
    return AdminStats(
      totalUsers: json['total_users'] ?? 0,
      activeUsers: json['active_users'] ?? 0,
      totalSessions: json['total_sessions'] ?? 0,
      recentActivity: json['recent_activity'] ?? {},
      totalTime: json['total_time'] ?? 0,
      masteredCount: json['mastered_count'] ?? 0,
      streak: json['streak'] ?? 0,
      reviewDue: json['review_due'] ?? 0,
      nextReview: json['next_review'] ?? "Tomorrow",
      masteryThreshold: (json['mastery_threshold'] ?? 0.8).toDouble(),
    );
  }
}
