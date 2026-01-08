import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config/theme.dart';
import '../providers/providers.dart';
import '../widgets/reusable_widgets.dart';

class ParentScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<ParentScreen> createState() => _ParentScreenState();
}

class _ParentScreenState extends ConsumerState<ParentScreen> {
  int _sessionLength = 5; // minutes
  bool _allowSpeechMode = true;
  bool _dislexiaFriendlyFont = false;

  @override
  Widget build(BuildContext context) {
    final adminStats = ref.watch(adminStatsProvider);

    return Scaffold(
      backgroundColor: AppColors.bgLight,
      appBar: AppBar(
        backgroundColor: AppColors.bgLight,
        elevation: 0,
        title: Text('Parent Dashboard', style: AppTypography.heading2),
      ),
      body: adminStats.when(
        data: (stats) => SingleChildScrollView(
          padding: EdgeInsets.all(AppSpacing.md),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Student Summary
              Text('Student Progress', style: AppTypography.heading1),
              SizedBox(height: AppSpacing.md),
              SoftCard(
                gradient: AppColors.cardGradientPurple,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Total practice time',
                            style: AppTypography.bodySmall),
                        Text('${stats['total_time'] ?? 0} min',
                            style: AppTypography.heading2),
                      ],
                    ),
                    SizedBox(height: AppSpacing.md),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Phonemes mastered',
                            style: AppTypography.bodySmall),
                        Text('${stats['mastered_count'] ?? 0}/15',
                            style: AppTypography.heading2),
                      ],
                    ),
                    SizedBox(height: AppSpacing.md),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Current streak',
                            style: AppTypography.bodySmall),
                        Text('${stats['streak'] ?? 0} days',
                            style: AppTypography.heading2),
                      ],
                    ),
                  ],
                ),
              ),
              SizedBox(height: AppSpacing.lg),
              // Algorithm Settings
              Text('Learning Settings', style: AppTypography.heading1),
              SizedBox(height: AppSpacing.md),
              SoftCard(
                gradient: AppColors.cardGradientGreen,
                child: Column(
                  children: [
                    // Session length
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Session length (minutes)',
                            style: AppTypography.body),
                        DropdownButton<int>(
                          value: _sessionLength,
                          items: [3, 5, 7, 10]
                              .map((val) => DropdownMenuItem(
                                    value: val,
                                    child: Text('$val min'),
                                  ))
                              .toList(),
                          onChanged: (val) {
                            setState(() => _sessionLength = val ?? 5);
                            _updateSettings();
                          },
                        ),
                      ],
                    ),
                    SizedBox(height: AppSpacing.md),
                    // Speech mode toggle
                    SwitchListTile(
                      title: Text('Allow speech recording',
                          style: AppTypography.body),
                      value: _allowSpeechMode,
                      onChanged: (val) {
                        setState(() => _allowSpeechMode = val);
                        _updateSettings();
                      },
                      activeColor: AppColors.primaryPastel,
                    ),
                    SizedBox(height: AppSpacing.md),
                    // Dyslexia-friendly font
                    SwitchListTile(
                      title: Text('Dyslexia-friendly font',
                          style: AppTypography.body),
                      value: _dislexiaFriendlyFont,
                      onChanged: (val) {
                        setState(() => _dislexiaFriendlyFont = val);
                        _updateSettings();
                      },
                      activeColor: AppColors.primaryPastel,
                    ),
                  ],
                ),
              ),
              SizedBox(height: AppSpacing.lg),
              // Difficulty cap
              Text('Difficulty Level', style: AppTypography.heading1),
              SizedBox(height: AppSpacing.md),
              SoftCard(
                gradient: AppColors.cardGradientOrange,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Current cap: Blends (CR, BR, etc.)',
                        style: AppTypography.body),
                    SizedBox(height: AppSpacing.md),
                    ElevatedButton(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Difficulty cap updated'),
                            backgroundColor: AppColors.successGreen,
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.secondaryPastel,
                      ),
                      child: Text('Change difficulty',
                          style: AppTypography.buttonSmall),
                    ),
                  ],
                ),
              ),
              SizedBox(height: AppSpacing.lg),
              // Algorithm info
              Text('Spaced Repetition Info', style: AppTypography.heading1),
              SizedBox(height: AppSpacing.md),
              SoftCard(
                gradient: AppColors.cardGradientPurple,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildInfoRow(
                      '📚 Review due',
                      '${stats['review_due'] ?? 0} items',
                    ),
                    SizedBox(height: AppSpacing.md),
                    _buildInfoRow(
                      '⏰ Next review scheduled',
                      '${stats['next_review'] ?? "Tomorrow"}',
                    ),
                    SizedBox(height: AppSpacing.md),
                    _buildInfoRow(
                      '🎯 Mastery threshold',
                      '${stats['mastery_threshold'] ?? 0.8} (80%)',
                    ),
                    SizedBox(height: AppSpacing.md),
                    Text(
                      'Our algorithm uses Spaced Repetition (SM-2) '
                      'to optimize review timing based on your child\'s '
                      'performance. Items improve gradually through '
                      'targeted practice.',
                      style: AppTypography.bodySmall.copyWith(
                        color: AppColors.textMuted,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        loading: () => Center(
          child: CircularProgressIndicator(
            valueColor: AlwaysStoppedAnimation<Color>(
              AppColors.primaryPastel,
            ),
          ),
        ),
        error: (error, stack) => Center(
          child: Text('Error loading stats: $error'),
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: AppTypography.body),
        Text(value, style: AppTypography.heading2),
      ],
    );
  }

  void _updateSettings() {
    // TODO: Call API to update parent settings
    print(
      'Settings updated: '
      'sessionLength=$_sessionLength, '
      'speechMode=$_allowSpeechMode, '
      'dyslexiaFont=$_dislexiaFriendlyFont',
    );
  }
}
