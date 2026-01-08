import 'package:flutter/material.dart';
import '../models/models.dart';
import '../config/theme.dart';
import 'reusable_widgets.dart';
import 'activity_graphics.dart';

/// Activity A: Listen → Choose (phoneme recognition)
class ListenChooseActivity extends StatefulWidget {
  final SessionItem item;
  final Function(int hintsUsed, int secondsSpent, bool correct) onSubmit;

  const ListenChooseActivity({
    required this.item,
    required this.onSubmit,
  });

  @override
  State<ListenChooseActivity> createState() => _ListenChooseActivityState();
}

class _ListenChooseActivityState extends State<ListenChooseActivity> {
  int? selectedIndex;
  int hintsUsed = 0;
  int secondsSpent = 0;
  int replayCount = 0;
  bool hasSubmitted = false;

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  void _startTimer() {
    Future.delayed(Duration(seconds: 1), () {
      if (!hasSubmitted && mounted) {
        setState(() => secondsSpent++);
        _startTimer();
      }
    });
  }

  void _handleReplay() {
    setState(() => replayCount++);
    if (replayCount > 2) {
      setState(() => hintsUsed++);
    }
    // TODO: Play audio via just_audio
    print('Playing audio for: ${widget.item.lesson.phoneme}');
  }

  void _showHint() {
    setState(() => hintsUsed++);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'The sound is: ${widget.item.lesson.phoneme}',
          style: AppTypography.body,
        ),
        backgroundColor: AppColors.accentPastel,
        duration: Duration(seconds: 2),
      ),
    );
  }

  void _handleSubmit() {
    final correct = selectedIndex == 0; // Assume first option is correct
    setState(() => hasSubmitted = true);

    // Show feedback
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        backgroundColor: AppColors.bgCard,
        title: Text(
          correct ? 'Nice work! 🎉' : 'Try again! 💪',
          style: AppTypography.heading2,
        ),
        content: Text(
          correct
              ? 'You got it right!'
              : 'The correct sound is: ${widget.item.lesson.phoneme}',
          style: AppTypography.body,
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              widget.onSubmit(hintsUsed, secondsSpent, correct);
            },
            child: Text('Continue', style: AppTypography.buttonSmall),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final options = ['${widget.item.lesson.phoneme}', 'b', 'p', 'm'];
    options.shuffle();

    return Column(
      children: [
        // Animated graphics
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: ListenChooseGraphic(
            phoneme: widget.item.lesson.phoneme,
            size: Size(280, 240),
          ),
        ),
        SizedBox(height: AppSpacing.md),
        // Header with hint button
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Listen', style: AppTypography.heading2),
              IconButton(
                onPressed: _showHint,
                icon: Icon(Icons.lightbulb_outline),
                color: AppColors.primaryPastel,
              ),
            ],
          ),
        ),
        // Speaker button
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: FloatingActionButton.large(
            onPressed: _handleReplay,
            backgroundColor: AppColors.secondaryPastel,
            child: Icon(Icons.volume_up, size: 32, color: Colors.white),
          ),
        ),
        SizedBox(height: AppSpacing.lg),
        // Instructions
        Text(
          'Tap the sound you hear',
          style: AppTypography.bodySmall.copyWith(
            color: AppColors.textMuted,
          ),
        ),
        SizedBox(height: AppSpacing.lg),
        // Options grid
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: GridView.count(
            crossAxisCount: 2,
            childAspectRatio: 1,
            mainAxisSpacing: AppSpacing.md,
            crossAxisSpacing: AppSpacing.md,
            shrinkWrap: true,
            children: List.generate(
              options.length,
              (index) => GestureDetector(
                onTap: () => setState(() => selectedIndex = index),
                child: Container(
                  decoration: BoxDecoration(
                    color: selectedIndex == index
                        ? AppColors.primaryPastel
                        : AppColors.bgCard,
                    borderRadius: BorderRadius.circular(AppRadius.lg),
                    border: Border.all(
                      color: AppColors.primaryPastel,
                      width: 2,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.1),
                        blurRadius: 4,
                      ),
                    ],
                  ),
                  child: Center(
                    child: Text(
                      options[index],
                      style: AppTypography.heading1.copyWith(
                        color: selectedIndex == index
                            ? Colors.white
                            : AppColors.textDark,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

/// Activity B: Build the Word (CVC / CCVC)
class BuildWordActivity extends StatefulWidget {
  final SessionItem item;
  final Function(int hintsUsed, int secondsSpent, bool correct) onSubmit;

  const BuildWordActivity({
    required this.item,
    required this.onSubmit,
  });

  @override
  State<BuildWordActivity> createState() => _BuildWordActivityState();
}

class _BuildWordActivityState extends State<BuildWordActivity> {
  late List<String> letters;
  late List<String> slots;
  int hintsUsed = 0;
  int secondsSpent = 0;
  bool hasSubmitted = false;

  @override
  void initState() {
    super.initState();
    // Example: "cat" -> ['c', 'a', 't']
    letters = 'cat'.split('')..shuffle();
    slots = List.filled(3, '');
    _startTimer();
  }

  void _startTimer() {
    Future.delayed(Duration(seconds: 1), () {
      if (!hasSubmitted && mounted) {
        setState(() => secondsSpent++);
        _startTimer();
      }
    });
  }

  void _handleLetterTap(int letterIndex) {
    for (int i = 0; i < slots.length; i++) {
      if (slots[i].isEmpty) {
        setState(() {
          slots[i] = letters[letterIndex];
          letters.removeAt(letterIndex);
        });
        break;
      }
    }
  }

  void _handleUndo(int slotIndex) {
    setState(() {
      letters.add(slots[slotIndex]);
      slots[slotIndex] = '';
      letters.shuffle();
    });
  }

  void _handleSubmit() {
    final word = slots.join();
    final correct = word == 'cat'; // Simplified check

    setState(() => hasSubmitted = true);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        backgroundColor: AppColors.bgCard,
        title: Text(
          correct ? 'Perfect blend! 🎉' : 'Try again! 💪',
          style: AppTypography.heading2,
        ),
        content: Text(
          correct ? 'You spelled "$word" correctly!' : 'The word is: cat',
          style: AppTypography.body,
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              widget.onSubmit(hintsUsed, secondsSpent, correct);
            },
            child: Text('Continue', style: AppTypography.buttonSmall),
          ),
        ],
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Animated graphics
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: BuildWordGraphic(
            letters: ['C', 'A', 'T'],
            size: Size(280, 240),
          ),
        ),
        SizedBox(
          height: AppSpacing.md,
          child: Container(
            width: 120,
            height: 120,
            decoration: BoxDecoration(
              color: AppColors.primaryPastel.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(AppRadius.md),
            ),
            child: Icon(Icons.image, size: 60, color: AppColors.primaryPastel),
          ),
        ),
        // Slots for letters
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(
              slots.length,
              (index) => GestureDetector(
                onTap: slots[index].isNotEmpty
                    ? () => _handleUndo(index)
                    : null,
                child: Container(
                  width: 60,
                  height: 60,
                  margin: EdgeInsets.symmetric(horizontal: AppSpacing.sm),
                  decoration: BoxDecoration(
                    color: slots[index].isNotEmpty
                        ? AppColors.secondaryPastel
                        : Colors.transparent,
                    border: Border.all(
                      color: AppColors.primaryPastel,
                      width: 2,
                    ),
                    borderRadius: BorderRadius.circular(AppRadius.md),
                  ),
                  child: Center(
                    child: Text(
                      slots[index],
                      style: AppTypography.heading1.copyWith(
                        color: slots[index].isNotEmpty
                            ? Colors.white
                            : AppColors.textMuted,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
        SizedBox(height: AppSpacing.lg),
        // Available letters
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: Wrap(
            spacing: AppSpacing.md,
            runSpacing: AppSpacing.md,
            children: List.generate(
              letters.length,
              (index) => LetterTile(
                letter: letters[index],
                onTap: () => _handleLetterTap(index),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

/// Activity C: Read → Pick Picture (decodable word comprehension)
class ReadPickActivity extends StatefulWidget {
  final SessionItem item;
  final Function(int hintsUsed, int secondsSpent, bool correct) onSubmit;

  const ReadPickActivity({
    required this.item,
    required this.onSubmit,
  });

  @override
  State<ReadPickActivity> createState() => _ReadPickActivityState();
}

class _ReadPickActivityState extends State<ReadPickActivity> {
  int? selectedImage;
  int hintsUsed = 0;
  int secondsSpent = 0;
  bool hasSubmitted = false;

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  void _startTimer() {
    Future.delayed(Duration(seconds: 1), () {
      if (!hasSubmitted && mounted) {
        setState(() => secondsSpent++);
        _startTimer();
      }
    });
  }

  void _handleReadAloud() {
    setState(() => hintsUsed++);
    // TODO: Play word audio
    print('Reading aloud: cat');
  }

  void _handleSubmit() {
    final correct = selectedImage == 0; // Assume first image is correct
    setState(() => hasSubmitted = true);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        backgroundColor: AppColors.bgCard,
        title: Text(
          correct ? 'Great reading! 🎉' : 'Try again! 📖',
          style: AppTypography.heading2,
        ),
        content: Text(
          correct ? 'You picked the right picture!' : 'That\'s a dog, not a cat!',
          style: AppTypography.body,
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              widget.onSubmit(hintsUsed, secondsSpent, correct);
            },
            child: Text('Continue', style: AppTypography.buttonSmall),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Animated graphics
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: ReadPickGraphic(
            size: Size(280, 240),
          ),
        ),
        SizedBox(height: AppSpacing.md),
        // Word to read
        Padding(
          padding: EdgeInsets.all(AppSpacing.lg),
          child: Container(
            padding: EdgeInsets.all(AppSpacing.md),
            decoration: BoxDecoration(
              gradient: AppColors.cardGradientOrange,
              borderRadius: BorderRadius.circular(AppRadius.lg),
            ),
            child: Text('cat', style: AppTypography.display1),
          ),
        ),
        // Read-aloud button
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: ElevatedButton.icon(
            onPressed: _handleReadAloud,
            icon: Icon(Icons.volume_up),
            label: Text('Read to me'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.secondaryPastel,
              padding: EdgeInsets.symmetric(
                horizontal: AppSpacing.lg,
                vertical: AppSpacing.md,
              ),
            ),
          ),
        ),
        SizedBox(height: AppSpacing.lg),
        // Picture options
        Padding(
          padding: EdgeInsets.all(AppSpacing.md),
          child: GridView.count(
            crossAxisCount: 2,
            childAspectRatio: 1,
            mainAxisSpacing: AppSpacing.md,
            crossAxisSpacing: AppSpacing.md,
            shrinkWrap: true,
            children: List.generate(
              3,
              (index) => GestureDetector(
                onTap: () => setState(() => selectedImage = index),
                child: Container(
                  decoration: BoxDecoration(
                    color: selectedImage == index
                        ? AppColors.primaryPastel
                        : AppColors.bgCard,
                    borderRadius: BorderRadius.circular(AppRadius.lg),
                    border: Border.all(
                      color: AppColors.primaryPastel,
                      width: selectedImage == index ? 3 : 1,
                    ),
                  ),
                  child: Icon(
                    index == 0 ? Icons.pets : Icons.home,
                    size: 48,
                    color: selectedImage == index
                        ? Colors.white
                        : AppColors.primaryPastel,
                  ),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
