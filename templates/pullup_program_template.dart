import 'dart:math';

/// 풀업 전문 운동 프로그램
class PullupPrograms {

  /// 8주 풀업 마스터 프로그램
  static Map<int, Map<int, PullupWorkout>> get eightWeekProgram => {
    1: {
      // Week 1: 풀업 기초 및 준비 운동
      1: const PullupWorkout(
        sets: [1, 2, 1, 1, 2],
        restSeconds: 120,
        notes: '네거티브 풀업 - 천천히 내려오기',
        exerciseType: 'Negative Pull-ups',
        chadLevel: '☕ 베이비 차드',
        difficulty: PullupDifficulty.beginner,
        variations: ['어시스트 풀업', '밴드 풀업'],
        specialInstructions: '3-5초에 걸쳐 천천히 내려오기',
      ),
      2: const PullupWorkout(
        sets: [2, 3, 2, 2, 3],
        restSeconds: 120,
        notes: '데드 행 - 매달리기 연습',
        exerciseType: 'Dead Hangs',
        chadLevel: '☕ 베이비 차드',
        difficulty: PullupDifficulty.beginner,
        variations: ['패시브 행', '액티브 행'],
        specialInstructions: '어깨 활성화하며 매달리기',
        unit: 'hangs',
      ),
      3: const PullupWorkout(
        sets: [2, 4, 2, 2, 3],
        restSeconds: 110,
        notes: '점프 풀업 - 도움 받아 올라가기',
        exerciseType: 'Jump Pull-ups',
        chadLevel: '🥉 브론즈 차드',
        difficulty: PullupDifficulty.beginner,
        variations: ['점프 어시스트', '박스 어시스트'],
        specialInstructions: '점프로 시작해서 천천히 내려오기',
      ),
    },
    2: {
      // Week 2: 근력 개발
      1: const PullupWorkout(
        sets: [3, 5, 3, 3, 4],
        restSeconds: 110,
        notes: '풀 레인지 풀업 - 완전한 동작',
        exerciseType: 'Full Range Pull-ups',
        chadLevel: '🥉 브론즈 차드',
        difficulty: PullupDifficulty.intermediate,
        variations: ['스트릭트 풀업', '킵핑 풀업'],
        specialInstructions: '턱이 바 위로 완전히 올라가기',
      ),
      2: const PullupWorkout(
        sets: [4, 6, 4, 4, 5],
        restSeconds: 100,
        notes: '그립 변형 - 다양한 손 위치',
        exerciseType: 'Grip Variations',
        chadLevel: '💯 라이징 차드',
        difficulty: PullupDifficulty.intermediate,
        variations: ['와이드 그립', '클로즈 그립'],
        specialInstructions: '매 세트마다 다른 그립 적용',
      ),
      3: const PullupWorkout(
        sets: [5, 7, 5, 5, 6],
        restSeconds: 100,
        notes: '레터럴 풀업 - 좌우 이동',
        exerciseType: 'Lateral Pull-ups',
        chadLevel: '💯 라이징 차드',
        difficulty: PullupDifficulty.intermediate,
        variations: ['좌우 교대', '원 암 프렙'],
        specialInstructions: '바의 한쪽 끝으로 턱 가져가기',
      ),
    },
    3: {
      // Week 3: 고급 기술
      1: const PullupWorkout(
        sets: [6, 9, 6, 6, 8],
        restSeconds: 90,
        notes: '체스트 투 바 - 가슴까지 올리기',
        exerciseType: 'Chest-to-Bar',
        chadLevel: '🦾 스틸 차드',
        difficulty: PullupDifficulty.advanced,
        variations: ['C2B', '하이 풀업'],
        specialInstructions: '가슴이 바에 닿을 때까지 올라가기',
      ),
      2: const PullupWorkout(
        sets: [7, 10, 7, 7, 9],
        restSeconds: 90,
        notes: '머슬업 준비 - 전환 동작',
        exerciseType: 'Muscle-up Prep',
        chadLevel: '🦾 스틸 차드',
        difficulty: PullupDifficulty.advanced,
        variations: ['트랜지션', '키핑 머슬업'],
        specialInstructions: '바 위로 몸 전체 올리기 연습',
      ),
      3: const PullupWorkout(
        sets: [8, 12, 8, 8, 10],
        restSeconds: 85,
        notes: '웨이티드 풀업 - 추가 중량',
        exerciseType: 'Weighted Pull-ups',
        chadLevel: '👑 레전드 차드',
        difficulty: PullupDifficulty.expert,
        variations: ['백팩 풀업', '덤벨 풀업'],
        specialInstructions: '5-10kg 추가 중량으로 진행',
      ),
    },
  };

  /// 특수 풀업 챌린지
  static Map<String, SpecialPullupProgram> get specialPrograms => {
    'pullup_pyramid': const SpecialPullupProgram(
      name: '풀업 피라미드 클라이밍',
      description: '1-2-3-4-5-4-3-2-1개씩 진행',
      duration: '9라운드 완주',
      targetReps: 25,
      chadLevel: '⛰️ 피라미드 마스터',
      instructions: '피라미드를 오르락내리락하며 완성',
    ),
    'pullup_gauntlet': const SpecialPullupProgram(
      name: '풀업 건틀릿 런',
      description: '5가지 그립으로 각각 5개씩',
      duration: '5변형 x 5개',
      targetReps: 25,
      chadLevel: '🏃‍♂️ 건틀릿 러너',
      instructions: '오버핸드→언더핸드→뉴트럴→와이드→클로즈',
    ),
    'max_pullups': const SpecialPullupProgram(
      name: '맥스 풀업 테스트',
      description: '한 번에 최대한 많은 풀업',
      duration: '1세트 올인',
      targetReps: 20,
      chadLevel: '💯 맥스 아웃 차드',
      instructions: '실패할 때까지 최대한 많이',
    ),
  };

  /// 일일 풀업 챌린지
  static List<DailyPullupChallenge> get dailyChallenges => [
    const DailyPullupChallenge(
      name: '💪 퍼스트 풀업',
      description: '완벽한 폼으로 5개 풀업',
      targetReps: 5,
      timeLimit: 300,
      reward: '🥇 퍼스트 배지',
      minLevel: 1,
    ),
    const DailyPullupChallenge(
      name: '🔥 파워 풀업',
      description: '폭발적으로 10개 풀업',
      targetReps: 10,
      timeLimit: 180,
      reward: '💥 파워 배지',
      minLevel: 2,
    ),
    const DailyPullupChallenge(
      name: '⚡ 스피드 풀업',
      description: '15개 풀업을 3분 안에',
      targetReps: 15,
      timeLimit: 180,
      reward: '⚡ 스피드 배지',
      minLevel: 3,
    ),
    const DailyPullupChallenge(
      name: '👑 레전드 풀업',
      description: '20개 풀업을 논스톱으로',
      targetReps: 20,
      timeLimit: 600,
      reward: '👑 레전드 배지',
      minLevel: 4,
    ),
  ];

  /// 레벨별 추천 프로그램
  static String getRecommendedProgram(int userLevel) {
    switch (userLevel) {
      case 1: return '8주 기초 프로그램 (Week 1-2)';
      case 2: return '8주 기초 프로그램 + 피라미드';
      case 3: return '8주 완전 프로그램 + 건틀릿';
      case 4: return '고급 프로그램 + 맥스 테스트';
      case 5: return '모든 챌린지 + 웨이티드 풀업';
      default: return '8주 기초 프로그램';
    }
  }
}

enum PullupDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
  legendary,
}

class PullupWorkout {
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;
  final PullupDifficulty difficulty;
  final List<String> variations;
  final String specialInstructions;
  final String unit;

  const PullupWorkout({
    required this.sets,
    required this.restSeconds,
    required this.notes,
    required this.exerciseType,
    required this.chadLevel,
    required this.difficulty,
    required this.variations,
    required this.specialInstructions,
    this.unit = 'reps',
  });

  int get totalReps => sets.fold(0, (sum, reps) => sum + reps);

  int get estimatedDurationMinutes {
    int setTime = sets.length * 3; // 풀업은 세트당 3분 예상
    int restTime = (sets.length - 1) * (restSeconds ~/ 60);
    return setTime + restTime;
  }
}

class SpecialPullupProgram {
  final String name;
  final String description;
  final String duration;
  final int targetReps;
  final String chadLevel;
  final String instructions;

  const SpecialPullupProgram({
    required this.name,
    required this.description,
    required this.duration,
    required this.targetReps,
    required this.chadLevel,
    required this.instructions,
  });
}

class DailyPullupChallenge {
  final String name;
  final String description;
  final int targetReps;
  final int timeLimit;
  final String reward;
  final int minLevel;

  const DailyPullupChallenge({
    required this.name,
    required this.description,
    required this.targetReps,
    required this.timeLimit,
    required this.reward,
    this.minLevel = 1,
  });
}