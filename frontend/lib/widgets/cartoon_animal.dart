import 'package:flutter/material.dart';
import 'package:phonetics_poc/models/lesson.dart';

class CartoonAnimal extends StatelessWidget {
  final Viseme viseme;
  const CartoonAnimal({super.key, required this.viseme});

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: const Size(260, 260),
      painter: _AnimalPainter(viseme),
    );
  }
}

class _AnimalPainter extends CustomPainter {
  final Viseme viseme;
  _AnimalPainter(this.viseme);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);

    final facePaint = Paint()..color = Colors.orange.shade300;
    final earPaint = Paint()..color = Colors.orange.shade400;
    final eyePaint = Paint()..color = Colors.black87;
    final mouthPaint = Paint()
      ..color = Colors.brown.shade800
      ..style = PaintingStyle.stroke
      ..strokeWidth = 8
      ..strokeCap = StrokeCap.round;

    // Ears
    canvas.drawCircle(center.translate(-70, -80), 35, earPaint);
    canvas.drawCircle(center.translate(70, -80), 35, earPaint);

    // Face
    canvas.drawCircle(center, 95, facePaint);

    // Eyes
    canvas.drawCircle(center.translate(-35, -20), 10, eyePaint);
    canvas.drawCircle(center.translate(35, -20), 10, eyePaint);

    // Nose
    final nosePaint = Paint()..color = Colors.brown.shade700;
    canvas.drawCircle(center.translate(0, 10), 10, nosePaint);

    // Mouth (viseme)
    final mouthCenter = center.translate(0, 45);

    switch (viseme) {
      case Viseme.rest:
        canvas.drawLine(
          mouthCenter.translate(-30, 0),
          mouthCenter.translate(30, 0),
          mouthPaint,
        );
        break;
      case Viseme.smile:
        final rect = Rect.fromCenter(center: mouthCenter, width: 80, height: 45);
        canvas.drawArc(rect, 0.15, 2.84, false, mouthPaint);
        break;
      case Viseme.open:
        final openPaint = Paint()
          ..color = Colors.brown.shade800
          ..style = PaintingStyle.stroke
          ..strokeWidth = 8;
        canvas.drawOval(Rect.fromCenter(center: mouthCenter, width: 45, height: 55), openPaint);
        break;
      case Viseme.round:
        final roundPaint = Paint()
          ..color = Colors.brown.shade800
          ..style = PaintingStyle.stroke
          ..strokeWidth = 8;
        canvas.drawOval(Rect.fromCenter(center: mouthCenter, width: 38, height: 38), roundPaint);
        break;
    }
  }

  @override
  bool shouldRepaint(covariant _AnimalPainter oldDelegate) {
    return oldDelegate.viseme != viseme;
  }
}
