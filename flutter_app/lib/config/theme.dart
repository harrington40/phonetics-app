import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Cute pastel color system for the app
class AppColors {
  // Primary colors (pastel)
  static const primaryPastel = Color(0xFFB39DDB); // Soft purple
  static const secondaryPastel = Color(0xFF81C784); // Soft green
  static const accentPastel = Color(0xFFFFAB91); // Soft coral

  // Feedback
  static const successGreen = Color(0xFF66BB6A);
  static const errorRed = Color(0xFFEF5350);

  // Backgrounds
  static const bgLight = Color(0xFFFAFAFA);
  static const bgCard = Color(0xFFFFFFFF);

  // Text
  static const textDark = Color(0xFF212121);
  static const textMuted = Color(0xFF757575);

  // Gradients for cards
  static LinearGradient cardGradientPurple = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFE1BEE7).withOpacity(0.5),
      Color(0xFFB39DDB).withOpacity(0.3),
    ],
  );

  static LinearGradient cardGradientGreen = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFC8E6C9).withOpacity(0.5),
      Color(0xFF81C784).withOpacity(0.3),
    ],
  );

  static LinearGradient cardGradientOrange = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFFFCCBC).withOpacity(0.5),
      Color(0xFFFFAB91).withOpacity(0.3),
    ],
  );
}

/// Typography system
class AppTypography {
  static TextStyle get display1 => GoogleFonts.fredoka(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        color: AppColors.textDark,
      );

  static TextStyle get heading1 => GoogleFonts.fredoka(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: AppColors.textDark,
      );

  static TextStyle get heading2 => GoogleFonts.fredoka(
        fontSize: 20,
        fontWeight: FontWeight.w600,
        color: AppColors.textDark,
      );

  static TextStyle get body => GoogleFonts.nunito(
        fontSize: 16,
        fontWeight: FontWeight.w400,
        color: AppColors.textDark,
      );

  static TextStyle get bodySmall => GoogleFonts.nunito(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        color: AppColors.textDark,
      );

  static TextStyle get button => GoogleFonts.fredoka(
        fontSize: 16,
        fontWeight: FontWeight.bold,
        color: Colors.white,
      );

  static TextStyle get buttonSmall => GoogleFonts.fredoka(
        fontSize: 14,
        fontWeight: FontWeight.w600,
        color: Colors.white,
      );
}

/// Spacing constants
class AppSpacing {
  static const xs = 4.0;
  static const sm = 8.0;
  static const md = 16.0;
  static const lg = 24.0;
  static const xl = 32.0;
}

/// Border radius constants
class AppRadius {
  static const xs = 8.0;
  static const sm = 12.0;
  static const md = 16.0;
  static const lg = 24.0;
  static const xl = 32.0;
}
