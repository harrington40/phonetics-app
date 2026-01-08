import 'package:flutter/material.dart';
import '../config/theme.dart';

/// Large primary button (kid-friendly, bottom anchored)
class BigPrimaryButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final bool isLoading;

  const BigPrimaryButton({
    required this.label,
    required this.onPressed,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 60,
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primaryPastel,
          disabledBackgroundColor: AppColors.primaryPastel.withValues(alpha: 0.5),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.lg),
          ),
          elevation: 4,
        ),
        child: isLoading
            ? SizedBox(
                width: 24,
                height: 24,
                child: CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                  strokeWidth: 2,
                ),
              )
            : Text(label, style: AppTypography.button),
      ),
    );
  }
}

/// Soft card with pastel gradient
class SoftCard extends StatelessWidget {
  final Widget child;
  final LinearGradient? gradient;
  final double padding;

  const SoftCard({
    required this.child,
    this.gradient,
    this.padding = AppSpacing.md,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: gradient ?? AppColors.cardGradientPurple,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      padding: EdgeInsets.all(padding),
      child: child,
    );
  }
}

/// Letter tile for word building activity
class LetterTile extends StatefulWidget {
  final String letter;
  final VoidCallback onTap;
  final bool isSelected;

  const LetterTile({
    required this.letter,
    required this.onTap,
    this.isSelected = false,
  });

  @override
  State<LetterTile> createState() => _LetterTileState();
}

class _LetterTileState extends State<LetterTile>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 200),
      vsync: this,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleTap() {
    _controller.forward().then((_) {
      _controller.reverse();
    });
    widget.onTap();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: Tween<double>(begin: 1.0, end: 0.95).animate(_controller),
      child: GestureDetector(
        onTap: _handleTap,
        child: Container(
          width: 60,
          height: 60,
          decoration: BoxDecoration(
            color: widget.isSelected
                ? AppColors.secondaryPastel
                : AppColors.primaryPastel,
            borderRadius: BorderRadius.circular(AppRadius.md),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.1),
                blurRadius: 4,
                offset: Offset(0, 2),
              ),
            ],
          ),
          child: Center(
            child: Text(
              widget.letter.toUpperCase(),
              style: AppTypography.heading1.copyWith(
                color: Colors.white,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

/// Progress dots for question index
class ProgressDots extends StatelessWidget {
  final int current;
  final int total;

  const ProgressDots({
    required this.current,
    required this.total,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(
        total,
        (index) => Container(
          width: 8,
          height: 8,
          margin: EdgeInsets.symmetric(horizontal: AppSpacing.xs),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: index < current
                ? AppColors.primaryPastel
                : AppColors.primaryPastel.withOpacity(0.3),
          ),
        ),
      ),
    );
  }
}

/// Reward badge for end-of-session rewards
class RewardBadge extends StatefulWidget {
  final String text;
  final int starsCount;

  const RewardBadge({
    required this.text,
    required this.starsCount,
  });

  @override
  State<RewardBadge> createState() => _RewardBadgeState();
}

class _RewardBadgeState extends State<RewardBadge>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(milliseconds: 600),
      vsync: this,
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: Tween<double>(begin: 1.0, end: 1.1).animate(
        CurvedAnimation(parent: _controller, curve: Curves.elasticInOut),
      ),
      child: Container(
        padding: EdgeInsets.all(AppSpacing.md),
        decoration: BoxDecoration(
          gradient: AppColors.cardGradientOrange,
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(
                widget.starsCount,
                (index) => Padding(
                  padding: EdgeInsets.symmetric(horizontal: AppSpacing.sm),
                  child: Icon(
                    Icons.star,
                    color: Color(0xFFFFD700),
                    size: 32,
                  ),
                ),
              ),
            ),
            SizedBox(height: AppSpacing.md),
            Text(
              widget.text,
              style: AppTypography.heading2,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

/// Sound Garden plant representing mastery level
class MasteryPlant extends StatelessWidget {
  final double mastery; // 0.0 to 1.0
  final String phoneme;
  final VoidCallback onTap;

  const MasteryPlant({
    required this.mastery,
    required this.phoneme,
    required this.onTap,
  });

  String get _stage {
    if (mastery < 0.3) return 'seed';
    if (mastery < 0.7) return 'sprout';
    return 'flower';
  }

  String get _emoji {
    switch (_stage) {
      case 'seed':
        return '🌱';
      case 'sprout':
        return '🌿';
      case 'flower':
        return '🌻';
      default:
        return '🌱';
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.all(AppSpacing.md),
        decoration: BoxDecoration(
          gradient: AppColors.cardGradientGreen,
          borderRadius: BorderRadius.circular(AppRadius.md),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(_emoji, style: TextStyle(fontSize: 48)),
            SizedBox(height: AppSpacing.sm),
            Text(
              phoneme,
              style: AppTypography.heading2,
            ),
            SizedBox(height: AppSpacing.xs),
            ClipRRect(
              borderRadius: BorderRadius.circular(AppRadius.sm),
              child: LinearProgressIndicator(
                value: mastery,
                minHeight: 4,
                backgroundColor: Colors.white.withOpacity(0.5),
                valueColor:
                    AlwaysStoppedAnimation<Color>(AppColors.secondaryPastel),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
