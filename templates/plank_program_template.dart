import 'dart:math';

/// 플랭크 전문 운동 프로그램
class PlankPrograms {

  /// 8주 플랭크 마스터 프로그램 (초 단위)
  static Map<int, Map<int, PlankWorkout>> get eightWeekProgram => {
    1: {
      // Week 1: 플랭크 기초 자세
      1: const PlankWorkout(
        sets: [15, 20, 15, 15, 18], // 초 단위
        restSeconds: 60,
        notes: '올바른 플랭크 자세 학습 - 몸 일직선',
        exerciseType: 'Basic Plank',
        chadLevel: '☕ 베이비 차드',
        difficulty: PlankDifficulty.beginner,
        variations: ['무릎 플랭크', '벽 플랭크'],
        specialInstructions: '엉덩이 들지 않기, 복부에 힘주기',
        unit: 'seconds',
      ),
      2: const PlankWorkout(
        sets: [20, 25, 20, 20, 22],
        restSeconds: 60,
        notes: '코어 안정화 - 호흡 조절',
        exerciseType: 'Breathing Plank',
        chadLevel: '☕ 베이비 차드',
        difficulty: PlankDifficulty.beginner,
        variations: ['브리딩 플랭크', '메디테이션 플랭크'],
        specialInstructions: '자연스럽게 호흡하며 복부 수축',
        unit: 'seconds',
      ),
      3: const PlankWorkout(
        sets: [25, 30, 25, 25, 28],
        restSeconds: 55,
        notes: '지구력 향상 - 더 오래 버티기',
        exerciseType: 'Endurance Plank',
        chadLevel: '🥉 브론즈 차드',
        difficulty: PlankDifficulty.beginner,
        variations: ['롱 플랭크', '지구력 플랭크'],
        specialInstructions: '떨림이 와도 끝까지 버티기',
        unit: 'seconds',
      ),
    },
    2: {
      // Week 2: 강도 증가
      1: const PlankWorkout(
        sets: [30, 40, 30, 30, 35],
        restSeconds: 55,
        notes: '동적 플랭크 - 움직임 추가',
        exerciseType: 'Dynamic Plank',
        chadLevel: '🥉 브론즈 차드',
        difficulty: PlankDifficulty.intermediate,
        variations: ['플랭크 업다운', '플랭크 탭'],
        specialInstructions: '플랭크 자세를 유지하며 동작 수행',
        unit: 'seconds',
      ),
      2: const PlankWorkout(
        sets: [35, 45, 35, 35, 40],
        restSeconds: 50,
        notes: '사이드 플랭크 도입 - 측면 강화',
        exerciseType: 'Side Plank',
        chadLevel: '💯 라이징 차드',
        difficulty: PlankDifficulty.intermediate,
        variations: ['사이드 플랭크', '사이드 크런치'],
        specialInstructions: '양쪽 번갈아가며 진행',
        unit: 'seconds',
      ),
      3: const PlankWorkout(
        sets: [40, 50, 40, 40, 45],
        restSeconds: 50,
        notes: '플랭크 변형 - 다양한 자세',
        exerciseType: 'Plank Variations',
        chadLevel: '💯 라이징 차드',
        difficulty: PlankDifficulty.intermediate,
        variations: ['리버스 플랭크', '하이 플랭크'],
        specialInstructions: '매 세트마다 다른 변형 적용',
        unit: 'seconds',
      ),
    },
    3: {
      // Week 3: 고급 플랭크
      1: const PlankWorkout(
        sets: [45, 60, 45, 45, 55],
        restSeconds: 45,
        notes: '원 암 플랭크 - 단일 팔 지지',
        exerciseType: 'Single Arm Plank',
        chadLevel: '🦾 스틸 차드',
        difficulty: PlankDifficulty.advanced,
        variations: ['원 암 플랭크', '팔 교대 플랭크'],
        specialInstructions: '한 팔씩 번갈아가며 들어올리기',
        unit: 'seconds',
      ),
      2: const PlankWorkout(
        sets: [50, 70, 50, 50, 60],
        restSeconds: 45,
        notes: '플랭크 잭 - 점프 동작 추가',
        exerciseType: 'Plank Jacks',
        chadLevel: '🦾 스틸 차드',
        difficulty: PlankDifficulty.advanced,
        variations: ['플랭크 잭', '플랭크 점프'],
        specialInstructions: '다리를 벌렸다 모으기 반복',
        unit: 'seconds',
      ),
      3: const PlankWorkout(
        sets: [60, 80, 60, 60, 70],
        restSeconds: 40,
        notes: '마운틴 클라이머 플랭크 - 고강도',
        exerciseType: 'Mountain Climber Plank',
        chadLevel: '👑 레전드 차드',
        difficulty: PlankDifficulty.expert,
        variations: ['마운틴 클라이머', '크로스 마운틴 클라이머'],
        specialInstructions: '무릎을 가슴쪽으로 빠르게 교대',
        unit: 'seconds',
      ),
    },
  };

  /// 특수 플랭크 챌린지
  static Map<String, SpecialPlankProgram> get specialPrograms => {
    'plank_master': const SpecialPlankProgram(
      name: '10분 플랭크 마스터',
      description: '10분 연속 플랭크 유지 도전',
      duration: '600초 논스톱',
      targetSeconds: 600,
      chadLevel: '🏆 플랭크 신',
      instructions: '10분을 완료할 때까지 절대 포기하지 마라',
    ),
    'plank_pyramid': const SpecialPlankProgram(
      name: '플랭크 피라미드 클라이밍',
      description: '30-60-90-60-30초 피라미드',
      duration: '5라운드 완주',
      targetSeconds: 270,
      chadLevel: '⛰️ 피라미드 마스터',
      instructions: '피라미드를 오르락내리락하며 완성',
    ),
    'iron_plank': const SpecialPlankProgram(
      name: '아이언 플랭크 챌린지',
      description: '5분 연속 플랭크 + 변형 동작',
      duration: '5분 + 변형',
      targetSeconds: 300,
      chadLevel: '🛡️ 아이언 코어',
      instructions: '5분 플랭크 후 1분간 플랭크 잭',
    ),
  };

  /// 일일 플랭크 챌린지
  static List<DailyPlankChallenge> get dailyChallenges => [
    const DailyPlankChallenge(
      name: '🔥 아이언 코어',
      description: '2분 연속 플랭크 유지',
      targetSeconds: 120,
      timeLimit: 120,
      reward: '🛡️ 아이언 배지',
      minLevel: 1,
    ),
    const DailyPlankChallenge(
      name: '💪 스틸 코어',
      description: '3분 연속 플랭크 유지',
      targetSeconds: 180,
      timeLimit: 180,
      reward: '⚔️ 스틸 배지',
      minLevel: 2,
    ),
    const DailyPlankChallenge(
      name: '🦾 다이아몬드 코어',
      description: '5분 연속 플랭크 유지',
      targetSeconds: 300,
      timeLimit: 300,
      reward: '💎 다이아몬드 배지',
      minLevel: 3,
    ),
    const DailyPlankChallenge(
      name: '👑 레전드 코어',
      description: '8분 연속 플랭크 유지',
      targetSeconds: 480,
      timeLimit: 480,
      reward: '👑 레전드 배지',
      minLevel: 4,
    ),
  ];

  /// 레벨별 추천 프로그램
  static String getRecommendedProgram(int userLevel) {
    switch (userLevel) {
      case 1: return '8주 기초 프로그램 (Week 1-2)';
      case 2: return '8주 기초 프로그램 + 아이언 코어';
      case 3: return '8주 완전 프로그램 + 특수 챌린지';
      case 4: return '고급 프로그램 + 플랭크 마스터';
      case 5: return '모든 챌린지 + 10분 마스터';
      default: return '8주 기초 프로그램';
    }
  }
}

enum PlankDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
  legendary,
}

class PlankWorkout {
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;
  final PlankDifficulty difficulty;
  final List<String> variations;
  final String specialInstructions;
  final String unit;

  const PlankWorkout({
    required this.sets,
    required this.restSeconds,
    required this.notes,
    required this.exerciseType,
    required this.chadLevel,
    required this.difficulty,
    required this.variations,
    required this.specialInstructions,
    this.unit = 'seconds',
  });

  int get totalSeconds => sets.fold(0, (sum, seconds) => sum + seconds);

  int get estimatedDurationMinutes {
    int setTime = (totalSeconds ~/ 60) + 1;
    int restTime = (sets.length - 1) * (restSeconds ~/ 60);
    return setTime + restTime;
  }
}

class SpecialPlankProgram {
  final String name;
  final String description;
  final String duration;
  final int targetSeconds;
  final String chadLevel;
  final String instructions;

  const SpecialPlankProgram({
    required this.name,
    required this.description,
    required this.duration,
    required this.targetSeconds,
    required this.chadLevel,
    required this.instructions,
  });
}

class DailyPlankChallenge {
  final String name;
  final String description;
  final int targetSeconds;
  final int timeLimit;
  final String reward;
  final int minLevel;

  const DailyPlankChallenge({
    required this.name,
    required this.description,
    required this.targetSeconds,
    required this.timeLimit,
    required this.reward,
    this.minLevel = 1,
  });
}