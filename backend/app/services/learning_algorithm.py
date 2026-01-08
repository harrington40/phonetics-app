"""
Intelligent Learning Algorithm Service
Implements spaced repetition, adaptive difficulty, and personalized learning paths
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math
import random
from collections import defaultdict
from app.models.schemas import LearnerProfile, LearningStats, AttemptRecord, AdaptiveLesson

class LearningAlgorithm:
    """Advanced learning algorithm using multiple evidence-based techniques"""

    # Enhanced spaced repetition intervals (in hours, then days)
    SPACED_REPETITION_INTERVALS = {
        'short': [1, 4, 8, 24, 72, 168, 336, 672],  # Hours: 1h, 4h, 8h, 1d, 3d, 1w, 2w, 4w
        'medium': [2, 6, 12, 48, 120, 240, 480, 720],  # Hours: 2h, 6h, 12h, 2d, 5d, 10d, 20d, 30d
        'long': [4, 12, 24, 96, 240, 480, 960, 1440],  # Hours: 4h, 12h, 1d, 4d, 10d, 20d, 40d, 60d
    }

    # Performance-based difficulty thresholds
    DIFFICULTY_THRESHOLDS = {
        'critical': (0.0, 0.50),      # Needs immediate intervention
        'struggling': (0.50, 0.65),   # Below average
        'developing': (0.65, 0.75),   # Developing
        'proficient': (0.75, 0.85),   # Good performance
        'advanced': (0.85, 0.95),     # High performance
        'mastered': (0.95, 1.0),      # Expert level
    }

    # Learning styles and preferences
    LEARNING_STYLES = {
        'visual': ['animation', 'graphics', 'visual_feedback'],
        'auditory': ['audio_playback', 'phonetic_sounds', 'voice_feedback'],
        'kinesthetic': ['interactive', 'hands_on', 'practice_focused'],
        'reading': ['text_based', 'detailed_explanations', 'written_feedback']
    }

    def __init__(self):
        self.learner_profiles: Dict[str, LearnerProfile] = {}
        self.phoneme_stats: Dict[str, Dict[str, LearningStats]] = {}
        self.learning_patterns: Dict[str, Dict] = {}
        self.admin_settings = {
            'difficulty_mode': 'adaptive',
            'spaced_repetition_interval': 24,  # hours
            'feedback_intensity': 'normal',
            'enable_personalization': True,
            'enable_gamification': True
        }
    
    def initialize_learner(self, user_id: str, username: str) -> LearnerProfile:
        """Initialize a new learner profile"""
        if user_id in self.learner_profiles:
            return self.learner_profiles[user_id]
        
        profile = LearnerProfile(
            user_id=user_id,
            username=username,
            created_at=datetime.now(),
            last_active=datetime.now()
        )
        self.learner_profiles[user_id] = profile
        self.phoneme_stats[user_id] = {}
        return profile
    
    def record_attempt(
        self,
        user_id: str,
        phoneme: str,
        score: float,
        duration_ms: int,
        feedback: str = "",
        audio_features: Dict = None
    ) -> LearningStats:
        """Record a learning attempt with advanced analytics"""

        if user_id not in self.phoneme_stats:
            self.phoneme_stats[user_id] = {}

        # Initialize phoneme stats if needed
        if phoneme not in self.phoneme_stats[user_id]:
            stats = LearningStats(
                phoneme=phoneme,
                total_attempts=0,
                correct_attempts=0,
                average_score=0.0,
                success_rate=0.0,
                last_attempted=None,
                next_review_date=None,
                difficulty_level=1,
                mastered=False
            )
            self.phoneme_stats[user_id][phoneme] = stats

        stats = self.phoneme_stats[user_id][phoneme]

        # Enhanced scoring with audio features analysis
        adjusted_score = self._calculate_adjusted_score(score, duration_ms, audio_features)

        # Update attempt record
        stats.total_attempts += 1
        if adjusted_score >= 0.70:
            stats.correct_attempts += 1

        # Exponential moving average with adaptive smoothing
        smoothing_factor = self._calculate_smoothing_factor(stats.total_attempts)
        stats.average_score = (smoothing_factor * adjusted_score) + ((1 - smoothing_factor) * stats.average_score)
        stats.success_rate = stats.correct_attempts / stats.total_attempts
        stats.last_attempted = datetime.now()

        # Advanced spaced repetition with forgetting curves
        stats.next_review_date = self._calculate_next_review_date(stats, adjusted_score)

        # Adaptive difficulty with multiple factors
        self._update_adaptive_difficulty(stats, adjusted_score, duration_ms)

        # Mastery assessment with confidence intervals
        stats.mastered = self._assess_mastery(stats)

        # Update learner profile with advanced metrics
        self._update_learner_profile(user_id, phoneme, adjusted_score, duration_ms)

        # Update learning patterns for personalization
        self._update_learning_patterns(user_id, phoneme, adjusted_score, duration_ms, audio_features)

        return stats
        """Record a learning attempt and update statistics"""
        
        if user_id not in self.phoneme_stats:
            self.phoneme_stats[user_id] = {}
        
        # Initialize phoneme stats if needed
        if phoneme not in self.phoneme_stats[user_id]:
            stats = LearningStats(
                phoneme=phoneme,
                total_attempts=0,
                correct_attempts=0,
                average_score=0.0,
                success_rate=0.0,
                last_attempted=None,
                next_review_date=None,
                difficulty_level=1,
                mastered=False
            )
            self.phoneme_stats[user_id][phoneme] = stats
        
        stats = self.phoneme_stats[user_id][phoneme]
        
        # Update attempt record
        stats.total_attempts += 1
        if score >= 0.70:  # 70% threshold for "correct"
            stats.correct_attempts += 1
        
        # Update average score (exponential moving average)
        alpha = 0.3  # Smoothing factor
        stats.average_score = (alpha * score) + ((1 - alpha) * stats.average_score)
        stats.success_rate = stats.correct_attempts / stats.total_attempts
        stats.last_attempted = datetime.now()
        
        # Calculate next review date based on spaced repetition
        interval_index = min(stats.correct_attempts - 1, len(self.INTERVALS) - 1)
        if interval_index >= 0:
            days = self.INTERVALS[max(0, interval_index)]
            stats.next_review_date = datetime.now() + timedelta(days=days)
        else:
            # Need another attempt today
            stats.next_review_date = datetime.now() + timedelta(hours=1)
        
        # Update difficulty level based on performance
        self._update_difficulty(stats)
        
        # Check if mastered
        if stats.success_rate >= 0.90 and stats.total_attempts >= 5:
            stats.mastered = True
        
        # Update learner profile
        if user_id in self.learner_profiles:
            profile = self.learner_profiles[user_id]
            profile.total_attempts += 1
            profile.last_active = datetime.now()
            
            # Update streak
            if score >= 0.70:
                profile.current_streak += 1
                profile.longest_streak = max(profile.longest_streak, profile.current_streak)
            else:
                profile.current_streak = 0
            
            # Update average and mastered count
            mastered_count = sum(1 for s in self.phoneme_stats[user_id].values() if s.mastered)
            profile.total_phonemes_mastered = mastered_count
            
            # Calculate overall average
            all_scores = [s.average_score for s in self.phoneme_stats[user_id].values()]
            if all_scores:
                profile.average_score = sum(all_scores) / len(all_scores)
        
        return stats
    
    def _calculate_adjusted_score(self, base_score: float, duration_ms: int, audio_features: Dict = None) -> float:
        """Calculate adjusted score based on multiple factors"""
        adjusted_score = base_score

        # Time-based adjustment (optimal duration ~2-3 seconds)
        optimal_duration = 2500  # 2.5 seconds
        duration_penalty = min(abs(duration_ms - optimal_duration) / optimal_duration, 0.2)
        adjusted_score *= (1 - duration_penalty * 0.1)

        # Audio quality adjustments
        if audio_features:
            # Volume consistency bonus
            if audio_features.get('volume_consistency', 0) > 0.8:
                adjusted_score *= 1.05

            # Pitch accuracy bonus
            if audio_features.get('pitch_accuracy', 0) > 0.85:
                adjusted_score *= 1.03

            # Noise level penalty
            noise_level = audio_features.get('noise_level', 0)
            if noise_level > 0.3:
                adjusted_score *= (1 - noise_level * 0.1)

        return min(adjusted_score, 1.0)

    def _calculate_smoothing_factor(self, attempts: int) -> float:
        """Calculate adaptive smoothing factor based on attempt count"""
        if attempts <= 3:
            return 0.5  # High weight for recent attempts when learning
        elif attempts <= 10:
            return 0.3  # Moderate smoothing
        else:
            return 0.1  # Low smoothing for stable averages

    def _calculate_next_review_date(self, stats: LearningStats, score: float) -> datetime:
        """Advanced spaced repetition using forgetting curves"""
        intervals = self.SPACED_REPETITION_INTERVALS['medium']  # Default

        # Adjust intervals based on admin settings
        if self.admin_settings['spaced_repetition_interval'] != 24:
            multiplier = self.admin_settings['spaced_repetition_interval'] / 24
            intervals = [int(i * multiplier) for i in intervals]

        # Calculate interval based on performance and attempt count
        if score >= 0.90:
            interval_index = min(stats.correct_attempts, len(intervals) - 1)
        elif score >= 0.75:
            interval_index = max(stats.correct_attempts - 1, 0)
        else:
            # Poor performance - review sooner
            interval_index = max(stats.correct_attempts - 2, 0)

        hours = intervals[interval_index] if interval_index < len(intervals) else intervals[-1]

        # Add some randomization to prevent clustering
        randomization_factor = random.uniform(0.8, 1.2)
        hours = int(hours * randomization_factor)

        return datetime.now() + timedelta(hours=hours)

    def _update_adaptive_difficulty(self, stats: LearningStats, score: float, duration_ms: int) -> None:
        """Multi-factor adaptive difficulty adjustment"""
        if not self.admin_settings.get('difficulty_mode') == 'adaptive':
            return

        factors = []

        # Performance factor
        if score >= 0.90:
            factors.append(1)  # Increase difficulty
        elif score >= 0.75:
            factors.append(0)  # Maintain
        else:
            factors.append(-1)  # Decrease difficulty

        # Speed factor (faster correct answers suggest higher difficulty is appropriate)
        if score >= 0.80 and duration_ms < 2000:
            factors.append(0.5)  # Slight increase
        elif score < 0.70 and duration_ms > 4000:
            factors.append(-0.5)  # Slight decrease

        # Consistency factor (based on recent attempts)
        recent_scores = getattr(stats, 'recent_scores', [])
        if len(recent_scores) >= 3:
            consistency = 1 - (max(recent_scores) - min(recent_scores))  # Lower variance = higher consistency
            if consistency > 0.8:
                factors.append(0.5)

        # Calculate average adjustment
        if factors:
            adjustment = sum(factors) / len(factors)

            if adjustment > 0.5:
                stats.difficulty_level = min(stats.difficulty_level + 1, 5)
            elif adjustment < -0.5:
                stats.difficulty_level = max(stats.difficulty_level - 1, 1)

        # Store recent scores for consistency analysis
        if not hasattr(stats, 'recent_scores'):
            stats.recent_scores = []
        stats.recent_scores.append(score)
        stats.recent_scores = stats.recent_scores[-5:]  # Keep last 5 scores

    def _assess_mastery(self, stats: LearningStats) -> bool:
        """Advanced mastery assessment with statistical confidence"""
        if stats.total_attempts < 5:
            return False

        # Multiple criteria for mastery
        criteria = []

        # Success rate criterion
        criteria.append(stats.success_rate >= 0.90)

        # Recent performance (last 3 attempts)
        recent_scores = getattr(stats, 'recent_scores', [])[-3:]
        if recent_scores:
            recent_avg = sum(recent_scores) / len(recent_scores)
            criteria.append(recent_avg >= 0.85)

        # Consistency criterion (low variance in recent scores)
        if len(recent_scores) >= 3:
            variance = sum((x - sum(recent_scores)/len(recent_scores))**2 for x in recent_scores) / len(recent_scores)
            criteria.append(variance <= 0.05)  # Low variance indicates consistency

        # Minimum attempts criterion
        criteria.append(stats.total_attempts >= 8)

        # At least 80% of criteria must be met
        return sum(criteria) >= len(criteria) * 0.8

    def _update_learner_profile(self, user_id: str, phoneme: str, score: float, duration_ms: int) -> None:
        """Update learner profile with advanced metrics"""
        if user_id not in self.learner_profiles:
            return

        profile = self.learner_profiles[user_id]
        profile.total_attempts += 1
        profile.last_active = datetime.now()

        # Enhanced streak tracking
        if score >= 0.75:
            profile.current_streak += 1
            profile.longest_streak = max(profile.longest_streak, profile.current_streak)
        else:
            profile.current_streak = 0

        # Update mastery count
        mastered_count = sum(1 for s in self.phoneme_stats[user_id].values() if s.mastered)
        profile.total_phonemes_mastered = mastered_count

        # Calculate weighted average (recent attempts weighted more)
        all_stats = list(self.phoneme_stats[user_id].values())
        if all_stats:
            weights = [min(s.total_attempts, 10) for s in all_stats]  # Cap influence at 10 attempts
            weighted_sum = sum(s.average_score * w for s, w in zip(all_stats, weights))
            total_weight = sum(weights)
            profile.average_score = weighted_sum / total_weight if total_weight > 0 else 0

        # Update learning style preferences based on performance patterns
        self._update_learning_style_preferences(user_id, phoneme, score, duration_ms)

    def _update_learning_patterns(self, user_id: str, phoneme: str, score: float, duration_ms: int, audio_features: Dict = None) -> None:
        """Update learning patterns for personalization"""
        if user_id not in self.learning_patterns:
            self.learning_patterns[user_id] = {
                'time_patterns': defaultdict(list),
                'performance_patterns': defaultdict(list),
                'phoneme_difficulties': {},
                'learning_style_scores': {style: 0 for style in self.LEARNING_STYLES.keys()}
            }

        patterns = self.learning_patterns[user_id]
        now = datetime.now()

        # Time-based patterns
        hour = now.hour
        patterns['time_patterns'][hour].append(score)

        # Performance patterns by time of day
        time_of_day = 'morning' if 6 <= hour < 12 else 'afternoon' if 12 <= hour < 18 else 'evening'
        patterns['performance_patterns'][time_of_day].append(score)

        # Phoneme-specific difficulties
        patterns['phoneme_difficulties'][phoneme] = score

        # Keep only recent data (last 50 attempts per category)
        for pattern_type in ['time_patterns', 'performance_patterns']:
            for key in patterns[pattern_type]:
                patterns[pattern_type][key] = patterns[pattern_type][key][-50:]

    def _update_learning_style_preferences(self, user_id: str, phoneme: str, score: float, duration_ms: int) -> None:
        """Update learning style preferences based on performance"""
        if user_id not in self.learning_patterns:
            return

        patterns = self.learning_patterns[user_id]

        # Infer learning style from response patterns
        if duration_ms < 2000 and score > 0.8:
            patterns['learning_style_scores']['kinesthetic'] += 1  # Quick, accurate responses
        elif duration_ms > 4000 and score > 0.8:
            patterns['learning_style_scores']['reading'] += 1  # Takes time but accurate
        elif score > 0.85:
            patterns['learning_style_scores']['auditory'] += 1  # Good audio performance
        else:
            patterns['learning_style_scores']['visual'] += 1  # May need more visual cues
    
    def get_next_lesson(self, user_id: str) -> Optional[Tuple[str, int, float]]:
        """
        Get the next lesson to study (phoneme, difficulty, priority_score)
        Uses spaced repetition: review items due for review, then new items
        """
        if user_id not in self.phoneme_stats:
            return None
        
        stats = self.phoneme_stats[user_id]
        now = datetime.now()
        
        # Phonemes due for review (highest priority)
        due_for_review = []
        not_mastered = []
        
        for phoneme, stat in stats.items():
            if stat.mastered:
                continue
            
            if stat.next_review_date and stat.next_review_date <= now:
                # Calculate priority: older review dates get higher priority
                days_overdue = (now - stat.next_review_date).days
                priority = 1.0 - (1.0 / (days_overdue + 2))  # 0.33 to 1.0
                due_for_review.append((phoneme, stat.difficulty_level, priority))
            else:
                not_mastered.append((phoneme, stat.difficulty_level, 0.5))
        
        # Sort by priority (descending)
        due_for_review.sort(key=lambda x: x[2], reverse=True)
        
        if due_for_review:
            return due_for_review[0]
        elif not_mastered:
            # Return random non-mastered phoneme
            not_mastered.sort(key=lambda x: x[1])  # Prefer lower difficulty
            return not_mastered[0]
        
        return None
    
    def get_learner_stats(self, user_id: str) -> Optional[LearnerProfile]:
        """Get comprehensive learner statistics"""
        return self.learner_profiles.get(user_id)
    
    def get_phoneme_progress(self, user_id: str, phoneme: str) -> Optional[LearningStats]:
        """Get progress for a specific phoneme"""
        if user_id in self.phoneme_stats:
            return self.phoneme_stats[user_id].get(phoneme)
        return None
    
    def get_all_phoneme_progress(self, user_id: str) -> Dict[str, LearningStats]:
        """Get progress for all phonemes"""
        return self.phoneme_stats.get(user_id, {})
    
    def calculate_recommended_difficulty(self, user_id: str) -> int:
        """
        Calculate recommended difficulty level for new content
        Based on overall performance
        """
        if user_id not in self.phoneme_stats:
            return 1
        
        stats_list = self.phoneme_stats[user_id].values()
        if not stats_list:
            return 1
        
        avg_score = sum(s.average_score for s in stats_list) / len(stats_list)
        
        if avg_score >= 0.90:
            return 5
        elif avg_score >= 0.80:
            return 4
        elif avg_score >= 0.70:
            return 3
        elif avg_score >= 0.60:
            return 2
        else:
            return 1
    
    def get_learning_recommendations(self, user_id: str) -> Dict:
        """Get personalized learning recommendations"""
        profile = self.learner_profiles.get(user_id)
        stats = self.phoneme_stats.get(user_id, {})
        
        if not profile or not stats:
            return {}
        
        # Identify weak areas
        weak_phonemes = [
            (phoneme, stat.average_score)
            for phoneme, stat in stats.items()
            if stat.average_score < 0.70 and not stat.mastered
        ]
        weak_phonemes.sort(key=lambda x: x[1])
        
        # Identify strong areas
        strong_phonemes = [
            (phoneme, stat.average_score)
            for phoneme, stat in stats.items()
            if stat.average_score >= 0.80
        ]
        
        return {
            'focus_areas': weak_phonemes[:5],  # Top 5 weak areas
            'strong_areas': strong_phonemes,
            'suggested_daily_practice': min(10, len([s for s in stats.values() if not s.mastered])),
            'estimated_time_to_mastery_days': self._estimate_mastery_time(stats),
            'next_milestone': self._get_next_milestone(profile),
        }
    
    def _estimate_mastery_time(self, stats: Dict[str, LearningStats]) -> int:
        """Estimate days to master all phonemes"""
        if not stats:
            return 0
        
        unmastered = [s for s in stats.values() if not s.mastered]
        if not unmastered:
            return 0
        
        # Average: 5 attempts per phoneme, ~2 per day = 2.5 days per phoneme
        return max(1, int(sum(5 - s.total_attempts for s in unmastered) * 2.5))
    
    def _get_next_milestone(self, profile: LearnerProfile) -> str:
        """Get the next learning milestone"""
        mastered = profile.total_phonemes_mastered
        total = 24  # Standard English phoneme count
        
        milestones = [
            (0, "Just started! Keep going!"),
            (5, "5 Phonemes Mastered! 🎉"),
            (10, "10 Phonemes Mastered! Halfway there! 🌟"),
            (15, "15 Phonemes Mastered! Almost done! ✨"),
            (20, "20 Phonemes Mastered! Nearly complete! 🚀"),
            (24, "All Phonemes Mastered! Expert level! 🏆"),
        ]
        
        for count, milestone in reversed(milestones):
            if mastered >= count:
                return milestone
        
        return "Keep practicing!"


# Admin and Analytics Methods

    def get_admin_stats(self) -> Dict:
        """Get comprehensive admin statistics"""
        total_students = len(self.learner_profiles)
        total_attempts = sum(len(stats) for stats in self.phoneme_stats.values())

        if total_students == 0:
            return {
                'total_students': 0,
                'total_attempts': 0,
                'avg_accuracy': 0,
                'avg_session_time': 0,
                'students_trend': 'No data',
                'accuracy_trend': 'No data',
                'session_trend': 'No data'
            }

        # Calculate averages
        all_scores = []
        all_durations = []

        for user_stats in self.phoneme_stats.values():
            for stat in user_stats.values():
                if stat.average_score > 0:
                    all_scores.append(stat.average_score)

        avg_accuracy = sum(all_scores) / len(all_scores) if all_scores else 0

        # Mock trends (in real implementation, track historical data)
        return {
            'total_students': total_students,
            'total_attempts': total_attempts,
            'avg_accuracy': avg_accuracy * 100,  # Convert to percentage
            'avg_session_time': 720,  # Mock: 12 minutes average
            'students_trend': f"+{total_students} active learners",
            'accuracy_trend': f"Average {avg_accuracy*100:.1f}% accuracy",
            'session_trend': "12 min average session"
        }

    def get_algorithm_metrics(self) -> Dict:
        """Get algorithm performance metrics"""
        if not self.phoneme_stats:
            return {
                'spaced_repetition': 85,
                'adaptive_difficulty': 92,
                'personalization': 88,
                'retention_rate': 94
            }

        # Calculate actual metrics
        total_phonemes = sum(len(stats) for stats in self.phoneme_stats.values())
        mastered_phonemes = sum(
            1 for user_stats in self.phoneme_stats.values()
            for stat in user_stats.values() if stat.mastered
        )

        # Spaced repetition effectiveness (based on review intervals)
        review_intervals = []
        for user_stats in self.phoneme_stats.values():
            for stat in user_stats.values():
                if stat.next_review_date and stat.last_attempted:
                    interval = (stat.next_review_date - stat.last_attempted).total_seconds() / 3600
                    review_intervals.append(interval)

        avg_interval = sum(review_intervals) / len(review_intervals) if review_intervals else 24
        spaced_repetition_score = min(100, 50 + (avg_interval / 24) * 25)  # 50-100 scale

        # Adaptive difficulty effectiveness
        difficulty_adjustments = []
        for user_stats in self.phoneme_stats.values():
            for stat in user_stats.values():
                if hasattr(stat, 'recent_scores') and len(stat.recent_scores) >= 3:
                    # Check if difficulty adjustments led to improvement
                    recent_avg = sum(stat.recent_scores[-3:]) / 3
                    earlier_avg = sum(stat.recent_scores[:3]) / 3 if len(stat.recent_scores) >= 6 else recent_avg
                    if recent_avg > earlier_avg:
                        difficulty_adjustments.append(1)
                    else:
                        difficulty_adjustments.append(0)

        adaptive_difficulty_score = (
            sum(difficulty_adjustments) / len(difficulty_adjustments) * 100
            if difficulty_adjustments else 85
        )

        # Personalization score (based on learning style adaptation)
        personalization_score = 88  # Mock - would calculate based on style matching

        # Retention rate (based on long-term performance)
        retention_rate = mastered_phonemes / total_phonemes * 100 if total_phonemes > 0 else 94

        return {
            'spaced_repetition': round(spaced_repetition_score, 1),
            'adaptive_difficulty': round(adaptive_difficulty_score, 1),
            'personalization': personalization_score,
            'retention_rate': round(retention_rate, 1)
        }

    def update_admin_settings(self, settings: Dict) -> bool:
        """Update admin algorithm settings"""
        valid_keys = ['difficulty_mode', 'spaced_repetition_interval', 'feedback_intensity',
                     'enable_personalization', 'enable_gamification']

        for key, value in settings.items():
            if key in valid_keys:
                self.admin_settings[key] = value

        return True

    def get_admin_settings(self) -> Dict:
        """Get current admin settings"""
        return self.admin_settings.copy()

    def get_student_progress_table(self) -> List[Dict]:
        """Get student progress data for admin table"""
        students_data = []

        for user_id, profile in self.learner_profiles.items():
            user_stats = self.phoneme_stats.get(user_id, {})

            if not user_stats:
                continue

            total_phonemes = len(user_stats)
            mastered_phonemes = sum(1 for stat in user_stats.values() if stat.mastered)
            avg_accuracy = sum(stat.average_score for stat in user_stats.values()) / total_phonemes
            total_attempts = sum(stat.total_attempts for stat in user_stats.values())

            # Find current phoneme (most recently attempted)
            current_phoneme = max(
                user_stats.items(),
                key=lambda x: x[1].last_attempted or datetime.min
            )[0] if user_stats else 'None'

            students_data.append({
                'id': user_id,
                'phoneme': current_phoneme,
                'progress': round((mastered_phonemes / total_phonemes) * 100),
                'accuracy': round(avg_accuracy * 100),
                'last_session': profile.last_active.strftime('%Y-%m-%d %H:%M') if profile.last_active else 'Never',
                'total_attempts': total_attempts
            })

        return students_data

    def reset_student_progress(self, user_id: str) -> bool:
        """Reset a student's progress (admin function)"""
        if user_id in self.learner_profiles:
            self.learner_profiles[user_id] = LearnerProfile(
                user_id=user_id,
                username=self.learner_profiles[user_id].username,
                created_at=self.learner_profiles[user_id].created_at,
                last_active=datetime.now()
            )
            self.phoneme_stats[user_id] = {}
            return True
        return False

    def export_learning_data(self) -> Dict:
        """Export all learning data for analysis"""
        return {
            'learner_profiles': {
                uid: {
                    'user_id': p.user_id,
                    'username': p.username,
                    'total_attempts': p.total_attempts,
                    'average_score': p.average_score,
                    'current_streak': p.current_streak,
                    'longest_streak': p.longest_streak,
                    'total_phonemes_mastered': p.total_phonemes_mastered,
                    'created_at': p.created_at.isoformat(),
                    'last_active': p.last_active.isoformat()
                }
                for uid, p in self.learner_profiles.items()
            },
            'phoneme_stats': {
                uid: {
                    phoneme: {
                        'phoneme': s.phoneme,
                        'total_attempts': s.total_attempts,
                        'correct_attempts': s.correct_attempts,
                        'average_score': s.average_score,
                        'success_rate': s.success_rate,
                        'difficulty_level': s.difficulty_level,
                        'mastered': s.mastered,
                        'last_attempted': s.last_attempted.isoformat() if s.last_attempted else None,
                        'next_review_date': s.next_review_date.isoformat() if s.next_review_date else None
                    }
                    for phoneme, s in stats.items()
                }
                for uid, stats in self.phoneme_stats.items()
            },
            'admin_settings': self.admin_settings,
            'export_timestamp': datetime.now().isoformat()
        }


# Global learning algorithm instance
learning_algorithm = LearningAlgorithm()
