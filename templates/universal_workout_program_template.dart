import 'dart:math';

/// 범용 운동 프로그램 템플릿
/// 모든 운동 타입에 적용 가능한 확장 가능한 구조
class UniversalWorkoutProgram {
  final String exerciseType;
  final int totalWeeks;
  final Map<int, Map<int, UniversalWorkout>> program;
  final Map<String, SpecialProgram> specialPrograms;
  final List<DailyChallenge> dailyChallenges;

  const UniversalWorkoutProgram({
    required this.exerciseType,
    required this.totalWeeks,
    required this.program,
    required this.specialPrograms,
    required this.dailyChallenges,
  });

  /// 사용자 레벨에 따른 운동 가져오기
  UniversalWorkout getWorkoutForLevel(int week, int day, int userLevel) {
    // 기본 프로그램에서 운동 가져오기
    var workout = program[week]?[day] ?? _getDefaultWorkout();

    // 사용자 레벨에 따라 조정
    return _adjustWorkoutForLevel(workout, userLevel);
  }

  /// 레벨별 운동 강도 조정
  UniversalWorkout _adjustWorkoutForLevel(UniversalWorkout baseWorkout, int userLevel) {
    double multiplier = _getLevelMultiplier(userLevel);

    return UniversalWorkout(
      sets: baseWorkout.sets.map((reps) => (reps * multiplier).round()).toList(),
      restSeconds: baseWorkout.restSeconds,
      notes: baseWorkout.notes,
      exerciseType: baseWorkout.exerciseType,
      chadLevel: _getChadLevelForUser(userLevel),
      difficulty: _getDifficultyForLevel(userLevel),
      variations: baseWorkout.variations,
      specialInstructions: baseWorkout.specialInstructions,
      customConfig: {
        ...baseWorkout.customConfig,
        'userLevel': userLevel,
        'multiplier': multiplier,
      },
    );
  }

  /// 레벨별 승수 계산
  double _getLevelMultiplier(int userLevel) {
    switch (userLevel) {
      case 1: return 0.5;  // 완전 초보자 - 50%
      case 2: return 0.8;  // 운동 경험자 - 80%
      case 3: return 1.0;  // 중급자 - 100% (기본)
      case 4: return 1.3;  // 상급자 - 130%
      case 5: return 1.8;  // 레전드 - 180%
      default: return 1.0;
    }
  }

  /// 레벨별 Chad 레벨 결정
  String _getChadLevelForUser(int userLevel) {
    switch (userLevel) {
      case 1: return "☕ 베이비 차드";
      case 2: return "🥉 브론즈 차드";
      case 3: return "💯 라이징 차드";
      case 4: return "🦾 스틸 차드";
      case 5: return "👑 레전드 차드";
      default: return "💪 차드";
    }
  }

  /// 레벨별 난이도 결정
  ExerciseDifficulty _getDifficultyForLevel(int userLevel) {
    switch (userLevel) {
      case 1: return ExerciseDifficulty.beginner;
      case 2: return ExerciseDifficulty.intermediate;
      case 3: return ExerciseDifficulty.advanced;
      case 4: return ExerciseDifficulty.expert;
      case 5: return ExerciseDifficulty.legendary;
      default: return ExerciseDifficulty.intermediate;
    }
  }

  UniversalWorkout _getDefaultWorkout() {
    return const UniversalWorkout(
      sets: [10, 15, 10, 10, 12],
      restSeconds: 90,
      notes: "기본 운동 세트",
      exerciseType: "Basic Exercise",
      chadLevel: "💪 차드",
      difficulty: ExerciseDifficulty.intermediate,
      variations: [],
      specialInstructions: "올바른 자세로 천천히 수행하세요",
    );
  }
}

/// 범용 운동 데이터 구조
class UniversalWorkout {
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;
  final ExerciseDifficulty difficulty;
  final List<String> variations;
  final String specialInstructions;
  final Map<String, dynamic> customConfig;

  const UniversalWorkout({
    required this.sets,
    required this.restSeconds,
    required this.notes,
    required this.exerciseType,
    required this.chadLevel,
    required this.difficulty,
    required this.variations,
    required this.specialInstructions,
    this.customConfig = const {},
  });

  /// 총 반복 횟수 계산
  int get totalReps => sets.fold(0, (sum, reps) => sum + reps);

  /// 예상 운동 시간 계산 (분)
  int get estimatedDurationMinutes {
    // 세트 시간 + 휴식 시간 대략 계산
    int setTime = sets.length * 2; // 세트당 대략 2분
    int restTime = (sets.length - 1) * (restSeconds ~/ 60);
    return setTime + restTime;
  }

  Map<String, dynamic> toMap() {
    return {
      'sets': sets,
      'restSeconds': restSeconds,
      'notes': notes,
      'exerciseType': exerciseType,
      'chadLevel': chadLevel,
      'difficulty': difficulty.name,
      'variations': variations,
      'specialInstructions': specialInstructions,
      'customConfig': customConfig,
    };
  }
}

/// 특수 프로그램 구조
class SpecialProgram {
  final String name;
  final String description;
  final String duration;
  final int targetValue;
  final String chadLevel;
  final String instructions;
  final Map<String, dynamic> config;

  const SpecialProgram({
    required this.name,
    required this.description,
    required this.duration,
    required this.targetValue,
    required this.chadLevel,
    required this.instructions,
    this.config = const {},
  });
}

/// 일일 챌린지 구조
class DailyChallenge {
  final String name;
  final String description;
  final int targetValue;
  final int timeLimit; // seconds
  final String reward;
  final int minLevel;
  final Map<String, dynamic> config;

  const DailyChallenge({
    required this.name,
    required this.description,
    required this.targetValue,
    required this.timeLimit,
    required this.reward,
    this.minLevel = 1,
    this.config = const {},
  });
}

enum ExerciseDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
  legendary,
}

/// 운동별 프로그램 팩토리
class ExerciseProgramFactory {

  /// 팔굽혀펴기 프로그램 생성
  static UniversalWorkoutProgram createPushupProgram() {
    return UniversalWorkoutProgram(
      exerciseType: "팔굽혀펴기",
      totalWeeks: 6,
      program: {
        1: {
          1: const UniversalWorkout(
            sets: [2, 3, 2, 2, 3],
            restSeconds: 90,
            notes: '완벽한 자세에 집중 - 천천히 내려가기',
            exerciseType: 'Basic Push-ups',
            chadLevel: '☕ 베이비 차드',
            difficulty: ExerciseDifficulty.beginner,
            variations: ['무릎 푸쉬업', '벽 푸쉬업'],
            specialInstructions: '가슴이 바닥에 닿을 때까지 내려가기',
          ),
          2: const UniversalWorkout(
            sets: [3, 5, 3, 3, 4],
            restSeconds: 90,
            notes: '코어 안정화에 집중',
            exerciseType: 'Controlled Push-ups',
            chadLevel: '☕ 베이비 차드',
            difficulty: ExerciseDifficulty.beginner,
            variations: ['3초 하강', '1초 정지'],
            specialInstructions: '복부에 힘을 주고 일직선 유지',
          ),
          // ... 더 많은 일별 운동
        },
        // ... 더 많은 주별 운동
      },
      specialPrograms: {
        'pushup_challenge': const SpecialProgram(
          name: '100개 푸쉬업 챌린지',
          description: '한 번에 100개 연속 푸쉬업 도전',
          duration: '8주',
          targetValue: 100,
          chadLevel: '👑 푸쉬업 킹',
          instructions: '매일 조금씩 늘려가며 목표 달성',
        ),
      },
      dailyChallenges: [
        const DailyChallenge(
          name: '💪 퀴ck 파워 차드',
          description: '20개 푸쉬업을 2분 안에',
          targetValue: 20,
          timeLimit: 120,
          reward: '⚡ 스피드 배지',
          minLevel: 2,
        ),
      ],
    );
  }

  /// 플랭크 프로그램 생성
  static UniversalWorkoutProgram createPlankProgram() {
    return UniversalWorkoutProgram(
      exerciseType: "플랭크",
      totalWeeks: 6,
      program: {
        1: {
          1: const UniversalWorkout(
            sets: [15, 20, 15, 15, 18], // 초 단위
            restSeconds: 60,
            notes: '올바른 플랭크 자세 학습',
            exerciseType: 'Basic Plank',
            chadLevel: '☕ 베이비 차드',
            difficulty: ExerciseDifficulty.beginner,
            variations: ['무릎 플랭크', '벽 플랭크'],
            specialInstructions: '몸을 일직선으로 유지, 엉덩이 들지 않기',
            customConfig: {'unit': 'seconds'},
          ),
          // ... 더 많은 일별 운동
        },
        // ... 더 많은 주별 운동
      },
      specialPrograms: {
        'plank_master': const SpecialProgram(
          name: '10분 플랭크 마스터',
          description: '10분 연속 플랭크 유지 도전',
          duration: '12주',
          targetValue: 600, // 초
          chadLevel: '🏆 플랭크 신',
          instructions: '매주 1분씩 증가하여 목표 달성',
        ),
      },
      dailyChallenges: [
        const DailyChallenge(
          name: '🔥 아이언 플랭크',
          description: '2분 연속 플랭크 유지',
          targetValue: 120,
          timeLimit: 120,
          reward: '🛡️ 아이언 코어 배지',
          minLevel: 2,
        ),
      ],
    );
  }

  /// 버피 프로그램 생성
  static UniversalWorkoutProgram createBurpeeProgram() {
    return UniversalWorkoutProgram(
      exerciseType: "버피",
      totalWeeks: 6,
      program: {
        1: {
          1: const UniversalWorkout(
            sets: [2, 3, 2, 2, 3],
            restSeconds: 120,
            notes: '버피 동작 분해 연습',
            exerciseType: 'Modified Burpees',
            chadLevel: '☕ 베이비 차드',
            difficulty: ExerciseDifficulty.beginner,
            variations: ['스텝백 버피', '점프 없는 버피'],
            specialInstructions: '각 동작을 천천히 정확하게',
          ),
          // ... 더 많은 일별 운동
        },
        // ... 더 많은 주별 운동
      },
      specialPrograms: {
        'burpee_hell': const SpecialProgram(
          name: '버피 지옥 100개',
          description: '한 번에 100개 연속 버피 도전',
          duration: '10주',
          targetValue: 100,
          chadLevel: '😈 버피 데몬',
          instructions: '지옥 같은 훈련을 통해 최강 체력 획득',
        ),
      },
      dailyChallenges: [
        const DailyChallenge(
          name: '💥 익스플로시브 버피',
          description: '5분간 최대한 많은 버피',
          targetValue: 50,
          timeLimit: 300,
          reward: '💥 폭발력 배지',
          minLevel: 3,
        ),
      ],
    );
  }

  /// 운동 타입별 프로그램 가져오기
  static UniversalWorkoutProgram getProgramForExercise(String exerciseType) {
    switch (exerciseType.toLowerCase()) {
      case 'pushup':
      case '팔굽혀펴기':
        return createPushupProgram();
      case 'plank':
      case '플랭크':
        return createPlankProgram();
      case 'burpee':
      case '버피':
        return createBurpeeProgram();
      default:
        return _createDefaultProgram(exerciseType);
    }
  }

  static UniversalWorkoutProgram _createDefaultProgram(String exerciseType) {
    return UniversalWorkoutProgram(
      exerciseType: exerciseType,
      totalWeeks: 6,
      program: {
        1: {
          1: const UniversalWorkout(
            sets: [5, 8, 5, 5, 6],
            restSeconds: 90,
            notes: '기본 동작 학습',
            exerciseType: 'Basic Exercise',
            chadLevel: '☕ 베이비 차드',
            difficulty: ExerciseDifficulty.beginner,
            variations: ['기본 동작'],
            specialInstructions: '올바른 자세로 천천히',
          ),
        },
      },
      specialPrograms: {},
      dailyChallenges: [],
    );
  }
}

/// 프로그램 진행도 추적기
class ProgressTracker {
  final String exerciseType;
  final int userLevel;
  final Map<String, dynamic> userData;

  ProgressTracker({
    required this.exerciseType,
    required this.userLevel,
    this.userData = const {},
  });

  /// 다음 운동 추천
  UniversalWorkout getNextWorkout(int currentWeek, int currentDay) {
    final program = ExerciseProgramFactory.getProgramForExercise(exerciseType);
    return program.getWorkoutForLevel(currentWeek, currentDay, userLevel);
  }

  /// 사용자 진행도 계산
  double calculateProgress(int completedWorkouts, int totalWorkouts) {
    return completedWorkouts / totalWorkouts;
  }

  /// 레벨업 체크
  bool shouldLevelUp(Map<String, dynamic> performanceData) {
    // 성과 데이터를 기반으로 레벨업 판단
    double completionRate = performanceData['completionRate'] ?? 0.0;
    int consecutiveDays = performanceData['consecutiveDays'] ?? 0;

    return completionRate >= 0.8 && consecutiveDays >= 7;
  }

  /// 개인화된 조언 생성
  String getPersonalizedAdvice(Map<String, dynamic> recentPerformance) {
    double avgCompletionRate = recentPerformance['avgCompletionRate'] ?? 0.0;

    if (avgCompletionRate >= 0.9) {
      return "🔥 완벽한 수행! 다음 레벨 도전을 고려해보세요!";
    } else if (avgCompletionRate >= 0.7) {
      return "💪 좋은 진전이에요! 꾸준히 계속하세요!";
    } else {
      return "📈 조금씩 늘려가세요. 완벽보다는 꾸준함이 중요해요!";
    }
  }
}