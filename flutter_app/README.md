# Phonetics Learning App - Flutter Frontend

A kid-friendly, research-backed phonetics learning application built with Flutter and powered by spaced repetition + adaptive difficulty algorithms.

## 🎯 Features

### For Kids
- **Today Screen**: Daily mission with streak tracking and motivational rewards
- **Practice Runner**: Interactive activities (Listen→Choose, Build Word, Read→Pick)
- **Sound Garden**: Gamified progress tracking with plant growth metaphors
- **Immediate Feedback**: Gentle encouragement with no "failure" vibe
- **Micro-rewards**: Stars, streaks, and sticker unlocks

### For Parents
- **Gated Dashboard**: Hold-to-unlock parent access with security
- **Progress Analytics**: Mastery charts, confusion pairs, recommended practice time
- **Learning Algorithm Control**: Adjust session length, difficulty cap, accessibility options
- **SM-2 Algorithm Transparency**: View spaced repetition schedule and mastery metrics
- **Dyslexia-friendly Options**: Alternative fonts and high-contrast mode

## 🏗️ Architecture

```
lib/
├── main.dart              # App entry point
├── config/
│   ├── theme.dart         # Pastel color system, typography, spacing
│   ├── api_config.dart    # Backend URL and timeouts
│   └── router.dart        # GoRouter navigation setup
├── models/
│   └── models.dart        # Lesson, SkillProgress, SessionItem, SessionFeedback
├── providers/
│   └── providers.dart     # Riverpod state management (SessionNotifier, etc.)
├── screens/
│   ├── today/
│   │   └── today_screen.dart
│   ├── practice/
│   │   └── practice_screen.dart
│   └── progress/
│       ├── progress_screen.dart
│       └── parent_screen.dart
├── services/
│   └── api_service.dart   # HTTP client for backend communication
└── widgets/
    ├── reusable_widgets.dart  # BigPrimaryButton, SoftCard, LetterTile, MasteryPlant, etc.
    └── activities.dart        # ListenChooseActivity, BuildWordActivity, ReadPickActivity
```

## 🚀 Getting Started

### Prerequisites
- Flutter 3.0+
- Dart 3.0+
- Backend server running on `http://localhost:8000`

### Installation

1. **Install dependencies**
   ```bash
   cd flutter_app
   flutter pub get
   ```

2. **Run the app**
   ```bash
   flutter run -d chrome  # Web
   flutter run            # Mobile device
   ```

3. **Build for production**
   ```bash
   flutter build web --release
   flutter build apk --release    # Android
   flutter build ios --release    # iOS
   ```

## 🎨 Design System

### Color Palette (Cute Pastel)
- **Primary**: `#B39DDB` (Soft Purple)
- **Secondary**: `#81C784` (Soft Green)
- **Accent**: `#FFAB91` (Soft Coral)
- **Success**: `#66BB6A` (Green)
- **Error**: `#EF5350` (Red)

### Typography
- **Headings**: Fredoka (bold, friendly)
- **Body**: Nunito (readable, modern)
- **Sizes**: 32px (display), 24px (h1), 20px (h2), 16px (body), 14px (small)

### Spacing & Radius
- **Spacing**: 4, 8, 16, 24, 32 px
- **Border Radius**: 8, 12, 16, 24, 32 px

## 🧠 Algorithm Integration

### Session Building
When user taps "Start Lesson":
```dart
final session = await apiService.buildSession();
// Backend returns 60% due reviews, 30% current stage, 10% challenge
// Each item includes phoneme, activity type, example words
```

### Quality Scoring (0-5)
```dart
quality = _calculateQuality(correct, secondsSpent, hintsUsed);
// Factors: correctness, speed, hint usage
// 5 = fast + correct + no hints
// 1 = incorrect
```

### Feedback Loop
```dart
final feedback = SessionFeedback(
  itemId: item.id,
  correct: correct,
  secondsSpent: secondsSpent,
  hintsUsed: hintsUsed,
  quality: quality,
);
await apiService.submitFeedback(feedback);
// Backend updates SM-2 factor and schedules next review
```

## 📊 Key Screens

### Today Screen
- Avatar + streak display
- "Start Lesson" CTA
- Review due / New sounds cards
- Star reward path (0/5)

### Practice Shell
- Progress dots (●●○○○)
- Dynamic activity widget
- Bottom "Check" / "Next" button
- Hint button (top-right)

### Sound Garden
- Grid of plants: 🌱 (seed), 🌿 (sprout), 🌻 (flower)
- Tap to hear phoneme + example words
- Visual mastery progression

### Parent Dashboard (Gated)
- Mastery overview (e.g., 8/15 mastered)
- "Areas to focus" list (confusion pairs)
- Session settings (3/5/7 min)
- Difficulty cap selector
- SM-2 transparency info

## 🔗 API Endpoints Used

```
GET  /api/lesson                    # Get single lesson
POST /api/learning/build-session    # Start session (60/30/10 mix)
POST /api/learning/feedback         # Submit question feedback
GET  /api/learning/progress         # Get skill progress list
GET  /api/admin/stats               # Parent dashboard stats
```

## 🎮 Activity Widgets

### 1. Listen→Choose (Phoneme Recognition)
- Big speaker button (tap to replay)
- 3-4 giant letter tiles
- Feedback: pop + sparkle (correct), shake (incorrect)
- Hint: shows correct tile after 2+ replays

### 2. Build Word (CVC/CCVC)
- Picture at top (placeholder)
- Empty slots: `_ _ _`
- Draggable/tap letter tiles
- Blend animation on submit

### 3. Read→Pick Picture (Comprehension)
- Large word in card ("ship")
- 3 picture options
- Read-aloud button (counts as hint)
- Image selection feedback

## 🛠️ State Management (Riverpod)

```dart
// API service provider
final apiServiceProvider = Provider((ref) => ApiService());

// Session items
final sessionProvider = StateNotifierProvider<SessionNotifier, List<SessionItem>>();

// Progress data
final progressProvider = FutureProvider((ref) async { ... });

// Session metadata
final sessionStartTimeProvider = StateProvider<DateTime?>((ref) => null);
final currentStreakProvider = StateProvider<int>((ref) => 0);
```

## 🎯 Next Steps

1. **Audio Integration**: Wire up `just_audio` for phoneme playback
2. **Speech Recognition**: Add MediaRecorder for student pronunciation
3. **Animations**: Use `flutter_animate` for tile bounces, checkmark pops
4. **Local Storage**: Persist progress with `sqflite` for offline access
5. **Parent Gate**: Add math puzzle alternative to hold-to-unlock
6. **Customization**: Dyslexia-friendly fonts, high-contrast themes

## 📚 Resources

- [Flutter Docs](https://flutter.dev/docs)
- [Riverpod Guide](https://riverpod.dev)
- [GoRouter Docs](https://pub.dev/packages/go_router)
- [Material 3 Design](https://m3.material.io)

## 📝 License

Same as parent project.
