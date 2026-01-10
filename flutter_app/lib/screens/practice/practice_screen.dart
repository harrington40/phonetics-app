import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../config/theme.dart';
import '../../models/models.dart';
import '../../providers/providers.dart';
import '../../widgets/activities.dart';
import '../../widgets/reusable_widgets.dart';

class PracticeScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends ConsumerState<PracticeScreen> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final session = ref.watch(sessionProvider);

    if (session.isEmpty) {
      return Scaffold(
        backgroundColor: AppColors.bgLight,
        body: Center(
          child: Text('No items in session', style: AppTypography.heading2),
        ),
      );
    }

    final item = session[_currentIndex];

    return PopScope(
      canPop: false,
      onPopInvoked: (didPop) {
        if (didPop) return;
        _showExitDialog(context);
      },
      child: Scaffold(
        backgroundColor: AppColors.bgLight,
        appBar: AppBar(
          backgroundColor: AppColors.bgLight,
          elevation: 0,
          leading: IconButton(
            icon: Icon(Icons.arrow_back, color: AppColors.textDark),
            onPressed: () => _showExitDialog(context),
          ),
          actions: [
            Padding(
              padding: EdgeInsets.all(AppSpacing.md),
              child: Center(
                child: ProgressDots(
                  current: _currentIndex + 1,
                  total: session.length,
                ),
              ),
            ),
          ],
        ),
        body: Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: Column(
            children: [
              Expanded(
                child: SingleChildScrollView(
                  child: _buildActivityWidget(item),
                ),
              ),
              SizedBox(height: AppSpacing.lg),
              // Bottom button (Check / Next)
              BigPrimaryButton(
                label: _currentIndex < session.length - 1 ? 'Next' : 'Finish',
                onPressed: () => _handleNext(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildActivityWidget(SessionItem item) {
    switch (item.type) {
      case 'listen_choose':
        return ListenChooseActivity(
          item: item,
          onSubmit: (hints, seconds, correct) {
            _submitFeedback(item, hints, seconds, correct);
          },
        );
      case 'build_word':
        return BuildWordActivity(
          item: item,
          onSubmit: (hints, seconds, correct) {
            _submitFeedback(item, hints, seconds, correct);
          },
        );
      case 'read_pick':
        return ReadPickActivity(
          item: item,
          onSubmit: (hints, seconds, correct) {
            _submitFeedback(item, hints, seconds, correct);
          },
        );
      default:
        return SizedBox.shrink();
    }
  }

  Future<void> _submitFeedback(
    SessionItem item,
    int hintsUsed,
    int secondsSpent,
    bool correct,
  ) async {
    final apiService = ref.read(apiServiceProvider);
    final quality = _calculateQuality(correct, secondsSpent, hintsUsed);

    try {
      final feedback = SessionFeedback(
        itemId: item.id,
        correct: correct,
        secondsSpent: secondsSpent,
        hintsUsed: hintsUsed,
        quality: quality,
      );

      await apiService.submitFeedback(feedback);
      print('Feedback submitted: quality=$quality');
    } catch (e) {
      print('Error submitting feedback: $e');
    }
  }

  int _calculateQuality(bool correct, int secondsSpent, int hintsUsed) {
    if (!correct) return 1; // Incorrect = quality 1

    // Perfect: fast, no hints
    if (secondsSpent < 5 && hintsUsed == 0) return 5;

    // Good: medium speed, few hints
    if (secondsSpent < 10 && hintsUsed <= 1) return 4;

    // OK: slower, some hints
    if (secondsSpent < 20 && hintsUsed <= 2) return 3;

    // Slow but correct
    return 2;
  }

  void _handleNext() {
    final session = ref.read(sessionProvider);

    if (_currentIndex < session.length - 1) {
      setState(() => _currentIndex++);
    } else {
      // End of session
      _showEndSessionReward();
    }
  }

  void _showEndSessionReward() {
    final startTime = ref.read(sessionStartTimeProvider);
    final duration = startTime != null
        ? DateTime.now().difference(startTime).inSeconds
        : 0;

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        backgroundColor: AppColors.bgCard,
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            RewardBadge(
              text: 'Great job today!',
              starsCount: 3,
            ),
            SizedBox(height: AppSpacing.lg),
            Text(
              'You practiced for ${duration ~/ 60} minutes',
              style: AppTypography.body,
              textAlign: TextAlign.center,
            ),
            SizedBox(height: AppSpacing.md),
            Text(
              '📚 Come back tomorrow for more!',
              style: AppTypography.bodySmall,
              textAlign: TextAlign.center,
            ),
          ],
        ),
        actions: [
          Center(
            child: ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
                context.go('/today');
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primaryPastel,
              ),
              child: Text('Back Home', style: AppTypography.button),
            ),
          ),
        ],
      ),
    );
  }

  Future<bool> _showExitDialog(BuildContext context) async {
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        backgroundColor: AppColors.bgCard,
        title: Text('Leave practice?', style: AppTypography.heading2),
        content: Text(
          'Your progress will be saved.',
          style: AppTypography.body,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('Keep practicing'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context, true);
              context.go('/today');
            },
            child: Text('Leave'),
          ),
        ],
      ),
    );

    return result ?? false;
  }
}
