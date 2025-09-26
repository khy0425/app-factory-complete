import 'dart:math';

/// 팔굽혀펴기 전문 운동 프로그램
class PushupPrograms {

  /// 6주 푸쉬업 마스터 프로그램
  static Map<int, Map<int, PushupWorkout>> get sixWeekProgram => {
    1: {
      // Week 1: 푸쉬업 기초 마스터
      1: const PushupWorkout(
        sets: [2, 3, 2, 2, 3],
        restSeconds: 90,
        notes: '완벽한 자세에 집중 - 천천히 내려가기',
        exerciseType: 'Basic Push-ups',
        chadLevel: '☕ 베이비 차드',
        difficulty: PushupDifficulty.beginner,
        variations: ['무릎 푸쉬업', '벽 푸쉬업'],
        specialInstructions: '가슴이 바닥에 닿을 때까지 내려가기',
      ),
      2: const PushupWorkout(
        sets: [3, 5, 3, 3, 4],
        restSeconds: 90,
        notes: '코어 안정화에 집중 - 몸 일직선',
        exerciseType: 'Controlled Push-ups',
        chadLevel: '☕ 베이비 차드',
        difficulty: PushupDifficulty.beginner,
        variations: ['3초 하강', '1초 정지'],
        specialInstructions: '복부에 힘을 주고 일직선 유지',
      ),
      3: const PushupWorkout(
        sets: [4, 6, 4, 4, 5],
        restSeconds: 85,
        notes: '강도 증가 - 더 많은 반복',
        exerciseType: 'Volume Push-ups',
        chadLevel: '🥉 브론즈 차드',
        difficulty: PushupDifficulty.beginner,
        variations: ['표준 푸쉬업', '와이드 푸쉬업'],
        specialInstructions: '일정한 속도로 끝까지 완료',
      ),
    },
    2: {
      // Week 2: 중급 발전
      1: const PushupWorkout(
        sets: [5, 8, 5, 5, 6],
        restSeconds: 85,
        notes: '파워 개발 - 폭발적 상승',
        exerciseType: 'Power Push-ups',
        chadLevel: '🥉 브론즈 차드',
        difficulty: PushupDifficulty.intermediate,
        variations: ['클랩 푸쉬업', '익스플로시브 푸쉬업'],
        specialInstructions: '상승 시 폭발적으로 밀어올리기',
      ),
      2: const PushupWorkout(
        sets: [6, 10, 6, 6, 8],
        restSeconds: 80,
        notes: '변형 동작 - 다양한 각도',
        exerciseType: 'Variation Push-ups',
        chadLevel: '💯 라이징 차드',
        difficulty: PushupDifficulty.intermediate,
        variations: ['다이아몬드 푸쉬업', '인클라인 푸쉬업'],
        specialInstructions: '매 세트마다 다른 변형 적용',
      ),
      3: const PushupWorkout(
        sets: [7, 12, 7, 7, 9],
        restSeconds: 80,
        notes: '지구력 훈련 - 더 긴 세트',
        exerciseType: 'Endurance Push-ups',
        chadLevel: '💯 라이징 차드',
        difficulty: PushupDifficulty.intermediate,
        variations: ['롱 푸쉬업', '마라톤 푸쉬업'],
        specialInstructions: '페이스 조절하며 끝까지 완주',
      ),
    },
    3: {
      // Week 3: 고급 도전
      1: const PushupWorkout(
        sets: [8, 15, 8, 8, 12],
        restSeconds: 75,
        notes: '원 암 준비 - 불균형 훈련',
        exerciseType: 'Uneven Push-ups',
        chadLevel: '🦾 스틸 차드',
        difficulty: PushupDifficulty.advanced,
        variations: ['아처 푸쉬업', '원 핸드 프렙'],
        specialInstructions: '한쪽에 더 많은 무게 실어서 진행',
      ),
      2: const PushupWorkout(
        sets: [10, 18, 10, 10, 15],
        restSeconds: 75,
        notes: '플라이오메트릭 - 점프 동작',
        exerciseType: 'Plyometric Push-ups',
        chadLevel: '🦾 스틸 차드',
        difficulty: PushupDifficulty.advanced,
        variations: ['클랩 푸쉬업', '스위치 푸쉬업'],
        specialInstructions: '공중에서 손뼉치기 또는 동작 전환',
      ),
      3: const PushupWorkout(
        sets: [12, 20, 12, 12, 18],
        restSeconds: 70,
        notes: '극한 도전 - 한계 돌파',
        exerciseType: 'Extreme Push-ups',
        chadLevel: '👑 레전드 차드',
        difficulty: PushupDifficulty.expert,
        variations: ['원 암 푸쉬업', '핸드스탠드 푸쉬업'],
        specialInstructions: '한계를 넘어서는 극한 도전',
      ),
    },
  };

  /// 특수 푸쉬업 챌린지
  static Map<String, SpecialPushupProgram> get specialPrograms => {
    'pushup_century': const SpecialPushupProgram(
      name: '100개 푸쉬업 센추리',
      description: '한 번에 100개 연속 푸쉬업 도전',
      duration: '논스톱 100개',
      targetReps: 100,
      chadLevel: '💯 센추리 차드',
      instructions: '100개를 완료할 때까지 절대 포기하지 마라',
    ),
    'pushup_ladder': const SpecialPushupProgram(
      name: '푸쉬업 사다리 오르기',
      description: '1-2-3-4-5-6-7-8-9-10개씩 진행',
      duration: '10라운드 완주',
      targetReps: 55,
      chadLevel: '🪜 래더 마스터',
      instructions: '사다리를 한 단계씩 올라가며 완성',
    ),
    'death_by_pushups': const SpecialPushupProgram(
      name: '데스 바이 푸쉬업',
      description: '1분차 1개, 2분차 2개... 실패까지',
      duration: '실패할 때까지',
      targetReps: 120, // 15분까지 갈 경우
      chadLevel: '💀 데스 차드',
      instructions: '매 분마다 개수가 증가. 언제까지 버틸 수 있나?',
    ),
  };

  /// 일일 푸쉬업 챌린지
  static List<DailyPushupChallenge> get dailyChallenges => [
    const DailyPushupChallenge(
      name: '💪 퀵 파워 차드',
      description: '20개 푸쉬업을 2분 안에',
      targetReps: 20,
      timeLimit: 120,
      reward: '⚡ 스피드 배지',
      minLevel: 1,
    ),
    const DailyPushupChallenge(
      name: '🔥 미드나잇 차드',
      description: '50개 푸쉬업을 논스톱으로',
      targetReps: 50,
      timeLimit: 600,
      reward: '🌙 미드나잇 배지',
      minLevel: 2,
    ),
    const DailyPushupChallenge(
      name: '💥 익스플로시브 차드',
      description: '클랩 푸쉬업 10개를 3분 안에',
      targetReps: 10,
      timeLimit: 180,
      reward: '💥 폭발력 배지',
      minLevel: 3,
    ),
    const DailyPushupChallenge(
      name: '👑 레전드 차드',
      description: '100개 푸쉬업을 10분 안에',
      targetReps: 100,
      timeLimit: 600,
      reward: '👑 레전드 배지',
      minLevel: 4,
    ),
  ];

  /// 레벨별 추천 프로그램
  static String getRecommendedProgram(int userLevel) {
    switch (userLevel) {
      case 1: return '6주 기초 프로그램 (Week 1-2)';
      case 2: return '6주 기초 프로그램 + 래더 챌린지';
      case 3: return '6주 완전 프로그램 + 특수 챌린지';
      case 4: return '고급 프로그램 + 100개 센추리';
      case 5: return '모든 챌린지 + 데스 바이 푸쉬업';
      default: return '6주 기초 프로그램';
    }
  }
}

enum PushupDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
  legendary,
}

class PushupWorkout {
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;
  final PushupDifficulty difficulty;
  final List<String> variations;
  final String specialInstructions;

  const PushupWorkout({
    required this.sets,
    required this.restSeconds,
    required this.notes,
    required this.exerciseType,
    required this.chadLevel,
    required this.difficulty,
    required this.variations,
    required this.specialInstructions,
  });

  int get totalReps => sets.fold(0, (sum, reps) => sum + reps);

  int get estimatedDurationMinutes {
    int setTime = sets.length * 2; // 세트당 대략 2분
    int restTime = (sets.length - 1) * (restSeconds ~/ 60);
    return setTime + restTime;
  }
}

class SpecialPushupProgram {
  final String name;
  final String description;
  final String duration;
  final int targetReps;
  final String chadLevel;
  final String instructions;

  const SpecialPushupProgram({
    required this.name,
    required this.description,
    required this.duration,
    required this.targetReps,
    required this.chadLevel,
    required this.instructions,
  });
}

class DailyPushupChallenge {
  final String name;
  final String description;
  final int targetReps;
  final int timeLimit;
  final String reward;
  final int minLevel;

  const DailyPushupChallenge({
    required this.name,
    required this.description,
    required this.targetReps,
    required this.timeLimit,
    required this.reward,
    this.minLevel = 1,
  });
}