class Lesson {
  final String id;
  final String phoneme;
  final String prompt;
  final String audioUrl;
  final List<VisemeCue> visemes;

  Lesson({
    required this.id,
    required this.phoneme,
    required this.prompt,
    required this.audioUrl,
    required this.visemes,
  });

  factory Lesson.fromJson(Map<String, dynamic> json) {
    return Lesson(
      id: json['id'] as String? ?? '',
      phoneme: json['phoneme'] as String,
      prompt: json['prompt'] as String,
      audioUrl: json['audio_url'] as String,
      visemes: (json['visemes'] as List?)
          ?.map((v) => VisemeCue.fromJson(v as Map<String, dynamic>))
          .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'phoneme': phoneme,
        'prompt': prompt,
        'audio_url': audioUrl,
        'visemes': visemes.map((v) => v.toJson()).toList(),
      };
}

enum Viseme { rest, smile, open, round }

Viseme parseViseme(String s) {
  switch (s) {
    case 'smile':
      return Viseme.smile;
    case 'open':
      return Viseme.open;
    case 'round':
      return Viseme.round;
    default:
      return Viseme.rest;
  }
}

String visemeToString(Viseme v) => v.toString().split('.').last;

class VisemeCue {
  final Viseme viseme;
  final int startMs;
  final int endMs;

  VisemeCue({
    required this.viseme,
    required this.startMs,
    required this.endMs,
  });

  factory VisemeCue.fromJson(Map<String, dynamic> json) {
    return VisemeCue(
      viseme: parseViseme(json['viseme'] as String),
      startMs: json['start_ms'] as int,
      endMs: json['end_ms'] as int,
    );
  }

  Map<String, dynamic> toJson() => {
        'viseme': visemeToString(viseme),
        'start_ms': startMs,
        'end_ms': endMs,
      };
}
