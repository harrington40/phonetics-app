import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../config/theme.dart';
import '../../providers/providers.dart';
import '../../widgets/reusable_widgets.dart';

class ProgressScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<ProgressScreen> createState() => _ProgressScreenState();
}

class _ProgressScreenState extends ConsumerState<ProgressScreen> {
  bool _isKidView = true;

  @override
  Widget build(BuildContext context) {
    final progressData = ref.watch(progressProvider);

    return Scaffold(
      backgroundColor: AppColors.bgLight,
      appBar: AppBar(
        backgroundColor: AppColors.bgLight,
        elevation: 0,
        title: Text(
          _isKidView ? 'Sound Garden 🌻' : 'Progress',
          style: AppTypography.heading2,
        ),
      ),
      body: progressData.when(
        data: (progress) => _isKidView
            ? _buildKidView(progress)
            : _buildParentView(progress),
        loading: () => Center(
          child: CircularProgressIndicator(
            valueColor: AlwaysStoppedAnimation<Color>(
              AppColors.primaryPastel,
            ),
          ),
        ),
        error: (error, stack) => Center(
          child: Text('Error loading progress: $error'),
        ),
      ),
    );
  }

  Widget _buildKidView(List data) {
    // Sound Garden with plants (mastery visualization)
    const phonemes = [
      'a', 'e', 'i', 'o', 'u', // vowels
      'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', // consonants
    ];

    return SingleChildScrollView(
      padding: EdgeInsets.all(AppSpacing.md),
      child: Column(
        children: [
          // Playful introduction
          SoftCard(
            gradient: AppColors.cardGradientGreen,
            child: Column(
              children: [
                Text('🌱 Sound Garden 🌻', style: AppTypography.heading1),
                SizedBox(height: AppSpacing.md),
                Text(
                  'Watch your sounds grow as you practice!',
                  style: AppTypography.bodySmall,
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
          SizedBox(height: AppSpacing.lg),
          // Grid of plants
          GridView.count(
            crossAxisCount: 3,
            childAspectRatio: 1,
            mainAxisSpacing: AppSpacing.md,
            crossAxisSpacing: AppSpacing.md,
            shrinkWrap: true,
            physics: NeverScrollableScrollPhysics(),
            children: List.generate(
              phonemes.length,
              (index) {
                final mastery =
                    (index % 10 + 1) / 10.0; // Simulated mastery 0.1 - 1.0
                return MasteryPlant(
                  phoneme: phonemes[index],
                  mastery: mastery,
                  onTap: () => _showPhonemeDetails(phonemes[index]),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildParentView(List data) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(AppSpacing.md),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Mastery chart
          Text('Mastery Overview', style: AppTypography.heading2),
          SizedBox(height: AppSpacing.md),
          SoftCard(
            gradient: AppColors.cardGradientPurple,
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Mastered', style: AppTypography.body),
                    Text('8/15', style: AppTypography.heading2),
                  ],
                ),
                SizedBox(height: AppSpacing.md),
                ClipRRect(
                  borderRadius: BorderRadius.circular(AppRadius.sm),
                  child: LinearProgressIndicator(
                    value: 8 / 15,
                    minHeight: 8,
                    backgroundColor: Colors.white.withValues(alpha: 0.5),
                    valueColor: AlwaysStoppedAnimation<Color>(
                      AppColors.primaryPastel,
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: AppSpacing.lg),
          // Most missed
          Text('Areas to focus', style: AppTypography.heading2),
          SizedBox(height: AppSpacing.md),
          ...['sh-ch confusion', 'blends (br, cr, etc.)', 'long vowels']
              .map((area) => Padding(
                    padding: EdgeInsets.only(bottom: AppSpacing.md),
                    child: SoftCard(
                      gradient: AppColors.cardGradientOrange,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(area, style: AppTypography.body),
                          Icon(Icons.priority_high, color: AppColors.errorRed),
                        ],
                      ),
                    ),
                  ))
              .toList(),
          SizedBox(height: AppSpacing.lg),
          // Recommended practice
          SoftCard(
            gradient: AppColors.cardGradientGreen,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Recommended Practice',
                    style: AppTypography.heading2),
                SizedBox(height: AppSpacing.md),
                Row(
                  children: [
                    Icon(Icons.timer, color: AppColors.secondaryPastel),
                    SizedBox(width: AppSpacing.md),
                    Text('5 minutes daily',
                        style: AppTypography.body),
                  ],
                ),
                SizedBox(height: AppSpacing.sm),
                Row(
                  children: [
                    Icon(Icons.trending_up,
                        color: AppColors.secondaryPastel),
                    SizedBox(width: AppSpacing.md),
                    Text('Current stage: Early readers',
                        style: AppTypography.body),
                  ],
                ),
              ],
            ),
          ),
          SizedBox(height: AppSpacing.lg),
          // Switch view button
          Center(
            child: ElevatedButton(
              onPressed: () {
                setState(() => _isKidView = !_isKidView);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.secondaryPastel,
              ),
              child: Text(
                _isKidView ? 'Show kid view' : 'Show parent view',
                style: AppTypography.buttonSmall,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showPhonemeDetails(String phoneme) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        backgroundColor: AppColors.bgCard,
        title: Text('Sound: $phoneme', style: AppTypography.heading2),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            FloatingActionButton.large(
              onPressed: () {
                print('Playing audio for $phoneme');
              },
              backgroundColor: AppColors.primaryPastel,
              child: Icon(Icons.volume_up, color: Colors.white),
            ),
            SizedBox(height: AppSpacing.lg),
            Text('Example words:', style: AppTypography.heading2),
            SizedBox(height: AppSpacing.md),
            ...['cat', 'car', 'cut']
                .map((word) => Padding(
                      padding: EdgeInsets.only(bottom: AppSpacing.sm),
                      child: Text('• $word', style: AppTypography.body),
                    ))
                .toList(),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Close'),
          ),
        ],
      ),
    );
  }
}
