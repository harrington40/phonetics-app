import 'package:flutter/material.dart';
import 'dart:math' as math;

/// Kid-friendly animated graphics for phonetics learning activities
/// Supports 5 activity types with smooth animations

// Color palette matching web version for consistency
const Color primaryColor = Color(0xFFB39DDB); // Soft Purple
const Color secondaryColor = Color(0xFF81C784); // Soft Green
const Color accentColor = Color(0xFFFFAB91); // Coral
const Color warningColor = Color(0xFFFFC107); // Amber
const Color goldColor = Color(0xFFFFD700); // Golden Yellow
const Color pinkColor = Color(0xFFFF69B4); // Hot Pink
const Color orangeColor = Color(0xFFFF9800); // Deep Orange

/// Listen & Choose Activity Graphic - for phoneme listening
class ListenChooseGraphic extends StatefulWidget {
  final String? phoneme;
  final Size size;

  const ListenChooseGraphic({
    Key? key,
    this.phoneme,
    this.size = const Size(300, 300),
  }) : super(key: key);

  @override
  State<ListenChooseGraphic> createState() => _ListenChooseGraphicState();
}

class _ListenChooseGraphicState extends State<ListenChooseGraphic>
    with SingleTickerProviderStateMixin {
  late AnimationController animationController;

  @override
  void initState() {
    super.initState();
    animationController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.size.width,
      height: widget.size.height,
      child: CustomPaint(
        painter: ListenChoosePainter(animation: animationController),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Text(
                '🎵 Tap to Answer',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class ListenChoosePainter extends CustomPainter {
  final Animation<double> animation;

  ListenChoosePainter({required this.animation}) : super(repaint: animation);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2.5);
    final paint = Paint();

    // Background circle
    paint.color = primaryColor.withOpacity(0.1);
    canvas.drawCircle(center, 120, paint);

    // Happy character face
    _drawCharacter(canvas, center, goldColor, size);

    // Musical notes
    _drawMusicalNote(canvas, Offset(center.dx - 60, center.dy - 80), size);
    _drawMusicalNote(canvas, Offset(center.dx + 70, center.dy - 60), size);

    // Speaker icon
    paint.color = primaryColor;
    paint.style = PaintingStyle.fill;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(
          center: Offset(center.dx, center.dy + 40),
          width: 40,
          height: 50,
        ),
        const Radius.circular(5),
      ),
      paint,
    );

    // Animated sound waves
    paint.color = secondaryColor;
    paint.style = PaintingStyle.stroke;
    paint.strokeWidth = 2;

    for (int i = 1; i <= 2; i++) {
      final radius = 20.0 + (i * 15.0) + (animation.value * 30.0);
      final opacity = math.max(0.0, 0.8 - (animation.value * 1.0) - (i * 0.2));
      paint.color = secondaryColor.withOpacity(opacity.toDouble());
      canvas.drawCircle(
        Offset(center.dx, center.dy + 40),
        radius.toDouble(),
        paint,
      );
    }
  }

  void _drawCharacter(Canvas canvas, Offset center, Color faceColor, Size size) {
    final paint = Paint();

    // Face
    paint.color = faceColor;
    paint.style = PaintingStyle.fill;
    canvas.drawCircle(center, 35, paint);

    // Eyes
    paint.color = Colors.black;
    canvas.drawCircle(Offset(center.dx - 15, center.dy - 10), 5, paint);
    canvas.drawCircle(Offset(center.dx + 15, center.dy - 10), 5, paint);

    // Smile
    paint.style = PaintingStyle.stroke;
    paint.strokeWidth = 3;
    paint.strokeCap = StrokeCap.round;
    final smilePath = Path();
    smilePath.moveTo(center.dx - 20, center.dy + 10);
    smilePath.quadraticBezierTo(center.dx, center.dy + 25, center.dx + 20, center.dy + 10);
    canvas.drawPath(smilePath, paint);
  }

  void _drawMusicalNote(Canvas canvas, Offset position, Size size) {
    final textPainter = TextPainter(
      text: const TextSpan(
        text: '♪',
        style: TextStyle(fontSize: 35, color: Colors.black87),
      ),
      textDirection: TextDirection.ltr,
    );
    textPainter.layout();
    textPainter.paint(canvas, position);
  }

  @override
  bool shouldRepaint(ListenChoosePainter oldDelegate) => true;
}

/// Build Word Activity Graphic - for letter combination
class BuildWordGraphic extends StatefulWidget {
  final List<String> letters;
  final Size size;

  const BuildWordGraphic({
    Key? key,
    this.letters = const ['C', 'A', 'T'],
    this.size = const Size(300, 300),
  }) : super(key: key);

  @override
  State<BuildWordGraphic> createState() => _BuildWordGraphicState();
}

class _BuildWordGraphicState extends State<BuildWordGraphic>
    with SingleTickerProviderStateMixin {
  late AnimationController animationController;

  @override
  void initState() {
    super.initState();
    animationController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.size.width,
      height: widget.size.height,
      child: CustomPaint(
        painter: BuildWordPainter(
          letters: widget.letters,
          animation: animationController,
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Text(
                '🔤 Drag Letters',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class BuildWordPainter extends CustomPainter {
  final List<String> letters;
  final Animation<double> animation;

  const BuildWordPainter({
    required this.letters,
    required this.animation,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint();

    // Background circle
    paint.color = secondaryColor.withOpacity(0.1);
    canvas.drawCircle(Offset(size.width / 2, size.height / 2), 120, paint);

    // Builder character
    _drawCharacter(
      canvas,
      Offset(size.width / 2, size.height / 4),
      orangeColor,
    );

    // Letter blocks
    final blockColors = [accentColor, secondaryColor, primaryColor];
    final startX = 60.0;
    const blockSize = 50.0;
    const spacing = 65.0;

    for (int i = 0; i < letters.length; i++) {
      final blockY = 130.0 + (animation.value > 0.5 ? animation.value : 1 - animation.value) * 10;
      final x = startX + (i * spacing);

      // Block
      paint.color = blockColors[i % blockColors.length];
      paint.style = PaintingStyle.fill;
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromLTWH(x, blockY + (i * 0.1), blockSize, blockSize),
          const Radius.circular(8),
        ),
        paint,
      );

      // Letter text
      final textPainter = TextPainter(
        text: TextSpan(
          text: letters[i],
          style: const TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        textDirection: TextDirection.ltr,
      );
      textPainter.layout();
      textPainter.paint(
        canvas,
        Offset(
          x + (blockSize / 2) - (textPainter.width / 2),
          blockY + (blockSize / 2) - (textPainter.height / 2) + (i * 0.1),
        ),
      );
    }

    // Result word display
    paint.color = warningColor;
    paint.style = PaintingStyle.fill;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(
          center: Offset(size.width / 2, size.height * 0.7),
          width: 140,
          height: 50,
        ),
        const Radius.circular(8),
      ),
      paint,
    );

    final word = letters.join('');
    final wordPainter = TextPainter(
      text: TextSpan(
        text: word,
        style: const TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Colors.black87,
        ),
      ),
      textDirection: TextDirection.ltr,
    );
    wordPainter.layout();
    wordPainter.paint(
      canvas,
      Offset(
        (size.width / 2) - (wordPainter.width / 2),
        (size.height * 0.7) - (wordPainter.height / 2),
      ),
    );
  }

  void _drawCharacter(Canvas canvas, Offset center, Color faceColor) {
    final paint = Paint()
      ..color = faceColor
      ..style = PaintingStyle.fill;

    canvas.drawCircle(center, 35, paint);

    paint.color = Colors.black;
    canvas.drawCircle(Offset(center.dx - 15, center.dy - 10), 5, paint);
    canvas.drawCircle(Offset(center.dx + 15, center.dy - 10), 5, paint);

    paint.style = PaintingStyle.stroke;
    paint.strokeWidth = 3;
    paint.strokeCap = StrokeCap.round;
    final smilePath = Path();
    smilePath.moveTo(center.dx - 20, center.dy + 10);
    smilePath.quadraticBezierTo(center.dx, center.dy + 25, center.dx + 20, center.dy + 10);
    canvas.drawPath(smilePath, paint);
  }

  @override
  bool shouldRepaint(BuildWordPainter oldDelegate) => true;
}

/// Read & Pick Activity Graphic - for vocabulary
class ReadPickGraphic extends StatelessWidget {
  final Size size;

  const ReadPickGraphic({
    Key? key,
    this.size = const Size(300, 300),
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: size.width,
      height: size.height,
      child: CustomPaint(
        painter: ReadPickPainter(),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Text(
                '📖 Tap Picture',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class ReadPickPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint();
    final center = Offset(size.width / 2, size.height / 2.5);

    // Background circle
    paint.color = warningColor.withOpacity(0.1);
    canvas.drawCircle(center, 120, paint);

    // Reading character
    paint.color = pinkColor;
    paint.style = PaintingStyle.fill;
    canvas.drawCircle(center, 35, paint);

    paint.color = Colors.black;
    canvas.drawCircle(Offset(center.dx - 15, center.dy - 10), 5, paint);
    canvas.drawCircle(Offset(center.dx + 15, center.dy - 10), 5, paint);

    paint.style = PaintingStyle.stroke;
    paint.strokeWidth = 3;
    paint.strokeCap = StrokeCap.round;
    final smilePath = Path();
    smilePath.moveTo(center.dx - 20, center.dy + 10);
    smilePath.quadraticBezierTo(center.dx, center.dy + 25, center.dx + 20, center.dy + 10);
    canvas.drawPath(smilePath, paint);

    // Open book
    paint.style = PaintingStyle.fill;
    paint.color = primaryColor;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(100, 130, 50, 80),
        const Radius.circular(5),
      ),
      paint,
    );

    paint.color = accentColor;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(150, 130, 50, 80),
        const Radius.circular(5),
      ),
      paint,
    );

    // Book spine
    paint.color = const Color(0xFF999999);
    paint.style = PaintingStyle.stroke;
    paint.strokeWidth = 2;
    canvas.drawLine(const Offset(150, 130), const Offset(150, 210), paint);

    // Words in book
    final wordPainter1 = TextPainter(
      text: const TextSpan(
        text: 'dog',
        style: TextStyle(fontSize: 16, color: Colors.white),
      ),
      textDirection: TextDirection.ltr,
    );
    wordPainter1.layout();
    wordPainter1.paint(canvas, const Offset(117, 160));

    final wordPainter2 = TextPainter(
      text: const TextSpan(
        text: 'cat',
        style: TextStyle(fontSize: 16, color: Colors.white),
      ),
      textDirection: TextDirection.ltr,
    );
    wordPainter2.layout();
    wordPainter2.paint(canvas, const Offset(167, 180));
  }

  @override
  bool shouldRepaint(ReadPickPainter oldDelegate) => false;
}

/// Reward Graphic - for celebration
class RewardGraphic extends StatefulWidget {
  final double score; // 0-100
  final Size size;

  const RewardGraphic({
    Key? key,
    this.score = 100,
    this.size = const Size(300, 300),
  }) : super(key: key);

  @override
  State<RewardGraphic> createState() => _RewardGraphicState();
}

class _RewardGraphicState extends State<RewardGraphic>
    with SingleTickerProviderStateMixin {
  late AnimationController animationController;

  @override
  void initState() {
    super.initState();
    animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.size.width,
      height: widget.size.height,
      child: CustomPaint(
        painter: RewardPainter(animation: animationController, score: widget.score),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Text(
                '🏆 Great Job!',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class RewardPainter extends CustomPainter {
  final Animation<double> animation;
  final double score;

  const RewardPainter({required this.animation, required this.score});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint();
    final center = Offset(size.width / 2, size.height / 2.5);

    // Background circle
    paint.color = goldColor.withOpacity(0.1);
    canvas.drawCircle(center, 120, paint);

    // Celebrating character
    paint.color = pinkColor;
    paint.style = PaintingStyle.fill;
    canvas.drawCircle(center, 35, paint);

    paint.color = Colors.black;
    canvas.drawCircle(Offset(center.dx - 15, center.dy - 10), 5, paint);
    canvas.drawCircle(Offset(center.dx + 15, center.dy - 10), 5, paint);

    paint.style = PaintingStyle.stroke;
    paint.strokeWidth = 3;
    paint.strokeCap = StrokeCap.round;
    final smilePath = Path();
    smilePath.moveTo(center.dx - 20, center.dy + 10);
    smilePath.quadraticBezierTo(center.dx, center.dy + 25, center.dx + 20, center.dy + 10);
    canvas.drawPath(smilePath, paint);

    // Trophy
    _drawTrophy(canvas, Offset(center.dx, center.dy + 70), size);

    // Stars
    _drawStar(canvas, Offset(center.dx - 50, center.dy - 30), 20);
    _drawStar(canvas, Offset(center.dx + 60, center.dy - 20), 20);
    _drawStar(canvas, Offset(center.dx, center.dy - 70), 25);

    // Score text
    final scorePainter = TextPainter(
      text: TextSpan(
        text: '${score.toStringAsFixed(0)}%',
        style: const TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Colors.black87,
        ),
      ),
      textDirection: TextDirection.ltr,
    );
    scorePainter.layout();
    scorePainter.paint(
      canvas,
      Offset(
        (size.width / 2) - (scorePainter.width / 2),
        size.height * 0.8,
      ),
    );
  }

  void _drawTrophy(Canvas canvas, Offset position, Size size) {
    final paint = Paint()
      ..color = goldColor
      ..style = PaintingStyle.fill;

    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(
          center: Offset(position.dx, position.dy),
          width: 50,
          height: 40,
        ),
        const Radius.circular(3),
      ),
      paint,
    );

    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromCenter(
          center: Offset(position.dx, position.dy + 40),
          width: 30,
          height: 8,
        ),
        const Radius.circular(3),
      ),
      paint,
    );
  }

  void _drawStar(Canvas canvas, Offset position, double size) {
    final paint = Paint()
      ..color = goldColor
      ..style = PaintingStyle.fill;

    const points = 5;
    final outerRadius = size;
    final innerRadius = size / 2.4;

    final path = Path();
    for (int i = 0; i < points * 2; i++) {
      final radius = i.isEven ? outerRadius : innerRadius;
      final angle = (i * math.pi) / points - math.pi / 2;
      final x = position.dx + radius * math.cos(angle);
      final y = position.dy + radius * math.sin(angle);

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    path.close();
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(RewardPainter oldDelegate) => true;
}

/// Progress Plant Graphic - for mastery tracking
class ProgressPlantGraphic extends StatefulWidget {
  final double masteryPercent; // 0-100
  final Size size;

  const ProgressPlantGraphic({
    Key? key,
    this.masteryPercent = 50,
    this.size = const Size(300, 300),
  }) : super(key: key);

  @override
  State<ProgressPlantGraphic> createState() => _ProgressPlantGraphicState();
}

class _ProgressPlantGraphicState extends State<ProgressPlantGraphic>
    with SingleTickerProviderStateMixin {
  late AnimationController animationController;

  @override
  void initState() {
    super.initState();
    animationController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.size.width,
      height: widget.size.height,
      child: CustomPaint(
        painter: ProgressPlantPainter(
          masteryPercent: widget.masteryPercent,
          animation: animationController,
        ),
      ),
    );
  }
}

class ProgressPlantPainter extends CustomPainter {
  final double masteryPercent;
  final Animation<double> animation;

  const ProgressPlantPainter({
    required this.masteryPercent,
    required this.animation,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint();
    final stage = (masteryPercent / 33).floor().clamp(0, 3);

    // Background
    paint.color = secondaryColor.withOpacity(0.1);
    canvas.drawCircle(Offset(size.width / 2, size.height / 2), 120, paint);

    // Soil
    paint.color = const Color(0xFF8B4513);
    paint.style = PaintingStyle.fill;
    canvas.drawOval(
      Rect.fromCenter(
        center: Offset(size.width / 2, size.height * 0.8),
        width: 60,
        height: 30,
      ),
      paint,
    );

    // Stem
    paint.color = const Color(0xFF558B2F);
    paint.style = PaintingStyle.stroke;
    paint.strokeWidth = 4 + (stage * 1.0);
    paint.strokeCap = StrokeCap.round;
    canvas.drawLine(
      Offset(size.width / 2, stage == 0 ? size.height * 0.75 : size.height * 0.65),
      Offset(size.width / 2, size.height * 0.2 - (stage * 20)),
      paint,
    );

    // Leaves
    if (stage >= 1) {
      _drawLeaf(canvas, Offset(size.width / 2 - 25, size.height * 0.55), secondaryColor);
      _drawLeaf(canvas, Offset(size.width / 2 + 25, size.height * 0.5), secondaryColor);
    }

    if (stage >= 2) {
      _drawLeaf(canvas, Offset(size.width / 2 - 30, size.height * 0.4), const Color(0xFF7CB342));
      _drawLeaf(canvas, Offset(size.width / 2 + 30, size.height * 0.35), const Color(0xFF7CB342));
    }

    // Flower
    if (stage >= 3) {
      _drawFlower(canvas, Offset(size.width / 2, size.height * 0.15));
    }

    // Progress bar
    paint.color = Colors.grey[300]!;
    paint.style = PaintingStyle.fill;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(50, size.height * 0.85, 200, 20),
        const Radius.circular(10),
      ),
      paint,
    );

    paint.color = secondaryColor;
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(50, size.height * 0.85, 200 * (masteryPercent / 100), 20),
        const Radius.circular(10),
      ),
      paint,
    );

    // Percentage text
    final percentPainter = TextPainter(
      text: TextSpan(
        text: '${masteryPercent.toStringAsFixed(0)}%',
        style: const TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: Colors.black87,
        ),
      ),
      textDirection: TextDirection.ltr,
    );
    percentPainter.layout();
    percentPainter.paint(
      canvas,
      Offset(
        (size.width / 2) - (percentPainter.width / 2),
        size.height * 0.855,
      ),
    );
  }

  void _drawLeaf(Canvas canvas, Offset center, Color color) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;
    canvas.drawOval(
      Rect.fromCenter(center: center, width: 20, height: 36),
      paint,
    );
  }

  void _drawFlower(Canvas canvas, Offset center) {
    const petals = 5;
    const petalRadius = 15;
    const petalSize = 10;

    final paint = Paint()
      ..color = const Color(0xFFFF1493)
      ..style = PaintingStyle.fill;

    for (int i = 0; i < petals; i++) {
      final angle = (i * 2 * math.pi) / petals.toDouble();
      final px = center.dx + petalRadius * math.cos(angle);
      final py = center.dy + petalRadius * math.sin(angle);
      canvas.drawCircle(Offset(px, py), petalSize.toDouble(), paint);
    }

    paint.color = goldColor;
    canvas.drawCircle(center, 8, paint);
  }

  @override
  bool shouldRepaint(ProgressPlantPainter oldDelegate) => true;
}
