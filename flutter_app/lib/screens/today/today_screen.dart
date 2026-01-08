import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../config/theme.dart';
import '../providers/providers.dart';
import '../widgets/reusable_widgets.dart';

class TodayScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final progressData = ref.watch(progressProvider);

    return Scaffold(
      backgroundColor: AppColors.bgLight,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.all(AppSpacing.md),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header with avatar and streak
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Good morning! 👋', style: AppTypography.heading1),
                        SizedBox(height: AppSpacing.sm),
                        Row(
                          children: [
                            Icon(Icons.local_fire_department,
                                color: Color(0xFFFF6B6B), size: 24),
                            SizedBox(width: AppSpacing.sm),
                            Text('7-day streak',
                                style: AppTypography.body),
                          ],
                        ),
                      ],
                    ),
                    // Parent icon (gate)
                    IconButton(
                      icon: Icon(Icons.lock_outline),
                      onPressed: () => _showParentGate(context),
                      color: AppColors.textMuted,
                    ),
                  ],
                ),
                SizedBox(height: AppSpacing.lg),
                // Mission card
                Text('Today\'s mission: 5 minutes', style: AppTypography.heading2),
                SizedBox(height: AppSpacing.md),
                SoftCard(
                  gradient: AppColors.cardGradientPurple,
                  child: Column(
                    children: [
                      Icon(Icons.play_arrow, size: 48, color: AppColors.primaryPastel),
                      SizedBox(height: AppSpacing.md),
                      Text('Ready to practice?', style: AppTypography.heading2),
                      SizedBox(height: AppSpacing.md),
                      BigPrimaryButton(
                        label: 'Start Lesson',
                        onPressed: () => _startSession(context, ref),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: AppSpacing.lg),
                // Info cards
                Row(
                  children: [
                    Expanded(
                      child: SoftCard(
                        gradient: AppColors.cardGradientGreen,
                        padding: AppSpacing.md,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Review due', style: AppTypography.bodySmall),
                            SizedBox(height: AppSpacing.sm),
                            Text('6', style: AppTypography.heading1),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(width: AppSpacing.md),
                    Expanded(
                      child: SoftCard(
                        gradient: AppColors.cardGradientOrange,
                        padding: AppSpacing.md,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('New sounds', style: AppTypography.bodySmall),
                            SizedBox(height: AppSpacing.sm),
                            Text('1', style: AppTypography.heading1),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(height: AppSpacing.lg),
                // Reward path (stars)
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Today\'s reward path', style: AppTypography.heading2),
                    SizedBox(height: AppSpacing.md),
                    SoftCard(
                      gradient: AppColors.cardGradientOrange,
                      padding: AppSpacing.md,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: List.generate(
                          5,
                          (index) => Icon(
                            Icons.star,
                            size: 32,
                            color: index < 2
                                ? Color(0xFFFFD700)
                                : Color(0xFFFFD700).withOpacity(0.3),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _startSession(BuildContext context, WidgetRef ref) async {
    final sessionNotifier = ref.read(sessionProvider.notifier);
    await sessionNotifier.buildSession();
    
    if (context.mounted) {
      ref.read(sessionStartTimeProvider.notifier).state = DateTime.now();
      context.go('/practice');
    }
  }

  void _showParentGate(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => ParentGateDialog(),
    );
  }
}

class ParentGateDialog extends StatefulWidget {
  @override
  State<ParentGateDialog> createState() => _ParentGateDialogState();
}

class _ParentGateDialogState extends State<ParentGateDialog> {
  int _secondsHeld = 0;
  bool _isPressed = false;

  void _onPressDown() {
    _isPressed = true;
    _startCountdown();
  }

  void _onPressUp() {
    _isPressed = false;
    setState(() => _secondsHeld = 0);
  }

  void _startCountdown() {
    Future.delayed(Duration(milliseconds: 100), () {
      if (_isPressed && mounted && _secondsHeld < 2) {
        setState(() => _secondsHeld++);
        _startCountdown();
      } else if (_secondsHeld >= 2 && mounted) {
        Navigator.pop(context);
        // Navigate to parent view
        GoRouter.of(context).go('/parent');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadius.lg),
      ),
      backgroundColor: AppColors.bgCard,
      title: Text('Parent Access', style: AppTypography.heading2),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            'Hold the button for 2 seconds',
            style: AppTypography.body,
            textAlign: TextAlign.center,
          ),
          SizedBox(height: AppSpacing.lg),
          GestureDetector(
            onLongPress: _onPressDown,
            onLongPressUp: _onPressUp,
            child: Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _secondsHeld >= 2
                    ? AppColors.successGreen
                    : AppColors.primaryPastel,
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      '${_secondsHeld}s',
                      style: AppTypography.heading1.copyWith(
                        color: Colors.white,
                      ),
                    ),
                    if (_secondsHeld < 2)
                      Text(
                        '/ 2',
                        style: AppTypography.bodySmall.copyWith(
                          color: Colors.white,
                        ),
                      ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text('Cancel'),
        ),
      ],
    );
  }
}
