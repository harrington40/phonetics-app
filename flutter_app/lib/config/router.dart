import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../screens/today/today_screen.dart';
import '../screens/practice/practice_screen.dart';
import '../screens/progress/progress_screen.dart';
import '../screens/progress/parent_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/today',
  routes: [
    GoRoute(
      path: '/today',
      builder: (context, state) => TodayScreen(),
    ),
    GoRoute(
      path: '/practice',
      builder: (context, state) => PracticeScreen(),
    ),
    GoRoute(
      path: '/progress',
      builder: (context, state) => ProgressScreen(),
    ),
    GoRoute(
      path: '/parent',
      builder: (context, state) => ParentScreen(),
    ),
  ],
  errorBuilder: (context, state) {
    return Scaffold(
      body: Center(
        child: Text('Page not found: ${state.uri}'),
      ),
    );
  },
);
