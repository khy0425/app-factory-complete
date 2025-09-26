import 'dart:math';

/// 런지 전문 운동 프로그램
class LungePrograms {

  /// 7주 런지 마스터 프로그램
  static Map<int, Map<int, LungeWorkout>> get sevenWeekProgram => {
    1: {
      // Week 1: 런지 기초 및 균형감각
      1: const LungeWorkout(
        sets: [8, 12, 8, 8, 10], // 각 다리당
        restSeconds: 75,
        notes: '기본 런지 - 균형감각 익히기',
        exerciseType: 'Basic Lunges',
        chadLevel: '☕ 베이비 차드',
        difficulty: LungeDifficulty.beginner,
        variations: ['스태틱 런지', '지지대 런지'],
        specialInstructions: '무릎이 90도가 되도록, 앞 무릎이 발끝 넘지 않게',
        unit: 'per_leg',
      ),
      2: const LungeWorkout(
        sets: [10, 15, 10, 10, 12],
        restSeconds: 75,
        notes: '알터네이팅 런지 - 다리 교대',
        exerciseType: 'Alternating Lunges',
        chadLevel: '☕ 베이비 차드',
        difficulty: LungeDifficulty.beginner,
        variations: ['스텝 백 런지', '스텝 포워드 런지'],
        specialInstructions: '좌우 다리를 번갈아가며 진행',
        unit: 'per_leg',
      ),
      3: const LungeWorkout(
        sets: [12, 18, 12, 12, 15],
        restSeconds: 70,
        notes: '워킹 런지 - 앞으로 걸으며',
        exerciseType: 'Walking Lunges',
        chadLevel: '🥉 브론즈 차드',
        difficulty: LungeDifficulty.beginner,
        variations: ['포워드 워킹', '백워드 워킹'],
        specialInstructions: '런지하며 앞으로 이동, 공간 확보 필요',
        unit: 'per_leg',
      ),
    },
    2: {
      // Week 2: 강도 증가 및 변형
      1: const LungeWorkout(
        sets: [15, 20, 15, 15, 18],
        restSeconds: 70,
        notes: '리버스 런지 - 뒤로 스텝',
        exerciseType: 'Reverse Lunges',
        chadLevel: '🥉 브론즈 차드',
        difficulty: LungeDifficulty.intermediate,
        variations: ['백 스텝 런지', '디피시트 런지'],
        specialInstructions: '뒤로 스텝하며 런지, 무릎 보호',
        unit: 'per_leg',
      ),
      2: const LungeWorkout(
        sets: [18, 25, 18, 18, 22],
        restSeconds: 65,
        notes: '사이드 런지 - 측면 강화',
        exerciseType: 'Side Lunges',
        chadLevel: '💯 라이징 차드',
        difficulty: LungeDifficulty.intermediate,
        variations: ['래터럴 런지', '코삭 스쿼트'],
        specialInstructions: '옆으로 크게 스텝, 한쪽 다리로 체중 지지',
        unit: 'per_leg',
      ),
      3: const LungeWorkout(
        sets: [20, 30, 20, 20, 25],
        restSeconds: 65,
        notes: '커트시 런지 - 크로스 백',
        exerciseType: 'Curtsy Lunges',
        chadLevel: '💯 라이징 차드',
        difficulty: LungeDifficulty.intermediate,
        variations: ['크로스 백 런지', '커트시 펄스'],
        specialInstructions: '뒤 대각선으로 다리 크로스하여 런지',
        unit: 'per_leg',
      ),
    },
    3: {
      // Week 3: 고급 기술 및 플라이오메트릭
      1: const LungeWorkout(
        sets: [22, 35, 22, 22, 30],
        restSeconds: 60,
        notes: '점프 런지 - 폭발적 파워',
        exerciseType: 'Jump Lunges',
        chadLevel: '🦾 스틸 차드',
        difficulty: LungeDifficulty.advanced,
        variations: ['익스플로시브 런지', '스위치 런지'],
        specialInstructions: '런지 자세에서 점프하여 다리 교대',
        unit: 'per_leg',
      ),
      2: const LungeWorkout(
        sets: [25, 40, 25, 25, 35],
        restSeconds: 60,
        notes: '불가리안 스플릿 스쿼트',
        exerciseType: 'Bulgarian Split Squats',
        chadLevel: '🦾 스틸 차드',
        difficulty: LungeDifficulty.advanced,
        variations: ['리어 풋 엘리베이티드', 'BSS'],
        specialInstructions: '뒷발을 의자나 벤치에 올리고 런지',
        unit: 'per_leg',
      ),
      3: const LungeWorkout(
        sets: [30, 45, 30, 30, 40],
        restSeconds: 55,
        notes: '360도 런지 - 모든 방향',
        exerciseType: '360 Degree Lunges',
        chadLevel: '👑 레전드 차드',
        difficulty: LungeDifficulty.expert,
        variations: ['클록 런지', '멀티 디렉셔널'],
        specialInstructions: '앞-옆-뒤-반대옆 순서로 360도 회전',
        unit: 'per_leg',
      ),
    },
  };

  /// 특수 런지 챌린지
  static Map<String, SpecialLungeProgram> get specialPrograms => {
    'lunge_century': const SpecialLungeProgram(
      name: '런지 센추리 100개',
      description: '각 다리 100개씩 총 200개 런지',
      duration: '200개 완주',
      targetReps: 200,
      chadLevel: '💯 센추리 차드',
      instructions: '각 다리 100개씩, 중간에 멈추지 마라',
    ),
    'lunge_matrix': const SpecialLungeProgram(
      name: '런지 매트릭스 마스터',
      description: '7가지 런지 변형을 각각 20개씩',
      duration: '7변형 x 20개',
      targetReps: 140,
      chadLevel: '🔥 매트릭스 마스터',
      instructions: '기본-리버스-사이드-커트시-점프-불가리안-360도',
    ),
    'lunge_gauntlet': const SpecialLungeProgram(
      name: '런지 건틀릿 러쉬',
      description: '10분간 최대한 많은 런지',
      duration: '10분 러쉬',
      targetReps: 300,
      chadLevel: '⚡ 건틀릿 러너',
      instructions: '10분 타이머 맞추고 최대한 많이',
    ),
  };

  /// 일일 런지 챌린지
  static List<DailyLungeChallenge> get dailyChallenges => [
    const DailyLungeChallenge(
      name: '💪 레그 파워업',
      description: '각 다리 30개씩 총 60개',
      targetReps: 60,
      timeLimit: 300,
      reward: '🦵 파워레그 배지',
      minLevel: 1,
    ),
    const DailyLungeChallenge(
      name: '🔥 런지 번',
      description: '점프 런지 50개를 5분 안에',
      targetReps: 50,
      timeLimit: 300,
      reward: '🔥 번 배지',
      minLevel: 2,
    ),
    const DailyLungeChallenge(
      name: '💥 익스플로시브 레그',
      description: '100개 런지를 논스톱으로',
      targetReps: 100,
      timeLimit: 600,
      reward: '💥 폭발력 배지',
      minLevel: 3,
    ),
    const DailyLungeChallenge(
      name: '👑 런지 킹',
      description: '각 다리 100개씩 총 200개',
      targetReps: 200,
      timeLimit: 900,
      reward: '👑 킹 배지',
      minLevel: 4,
    ),
  ];

  /// 레벨별 추천 프로그램
  static String getRecommendedProgram(int userLevel) {
    switch (userLevel) {
      case 1: return '7주 기초 프로그램 (Week 1-2)';
      case 2: return '7주 런지 프로그램 + 매트릭스';
      case 3: return '7주 완전 프로그램 + 건틀릿';
      case 4: return '고급 프로그램 + 센추리 200개';
      case 5: return '모든 챌린지 + 익스트림 콤보';
      default: return '7주 기초 프로그램';
    }
  }
}

enum LungeDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
  legendary,
}

class LungeWorkout {
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;
  final LungeDifficulty difficulty;
  final List<String> variations;
  final String specialInstructions;
  final String unit;

  const LungeWorkout({
    required this.sets,
    required this.restSeconds,
    required this.notes,
    required this.exerciseType,
    required this.chadLevel,
    required this.difficulty,
    required this.variations,
    required this.specialInstructions,
    this.unit = 'per_leg',
  });

  int get totalReps => sets.fold(0, (sum, reps) => sum + reps);

  int get estimatedDurationMinutes {
    int setTime = sets.length * 3; // 런지는 세트당 3분 예상
    int restTime = (sets.length - 1) * (restSeconds ~/ 60);
    return setTime + restTime;
  }
}

class SpecialLungeProgram {
  final String name;
  final String description;
  final String duration;
  final int targetReps;
  final String chadLevel;
  final String instructions;

  const SpecialLungeProgram({
    required this.name,
    required this.description,
    required this.duration,
    required this.targetReps,
    required this.chadLevel,
    required this.instructions,
  });
}

class DailyLungeChallenge {
  final String name;
  final String description;
  final int targetReps;
  final int timeLimit;
  final String reward;
  final int minLevel;

  const DailyLungeChallenge({
    required this.name,
    required this.description,
    required this.targetReps,
    required this.timeLimit,
    required this.reward,
    this.minLevel = 1,
  });
}