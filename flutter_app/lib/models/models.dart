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
