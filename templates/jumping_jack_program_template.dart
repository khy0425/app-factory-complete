import 'dart:math';

/// 점핑잭 전문 운동 프로그램
class JumpingJackPrograms {

  /// 6주 점핑잭 카디오 마스터 프로그램
  static Map<int, Map<int, JumpingJackWorkout>> get sixWeekProgram => {
    1: {
      // Week 1: 점핑잭 기초 및 리듬
      1: const JumpingJackWorkout(
        sets: [10, 15, 10, 10, 12],
        restSeconds: 60,
        notes: '기본 점핑잭 - 리듬감 익히기',
        exerciseType: 'Basic Jumping Jacks',
        chadLevel: '☕ 베이비 차드',
        difficulty: JumpingJackDifficulty.beginner,
        variations: ['슬로우 잭', '하프 잭'],
        specialInstructions: '발과 팔을 동시에 움직이며 리듬 맞추기',
      ),
      2: const JumpingJackWorkout(
        sets: [15, 20, 15, 15, 18],
        restSeconds: 60,
        notes: '스피드 향상 - 빠른 전환',
        exerciseType: 'Speed Jacks',
        chadLevel: '☕ 베이비 차드',
        difficulty: JumpingJackDifficulty.beginner,
        variations: ['패스트 잭', '퀵 잭'],
        specialInstructions: '동작 전환을 빠르게, 정확성 유지',
      ),
      3: const JumpingJackWorkout(
        sets: [20, 25, 20, 20, 22],
        restSeconds: 55,
        notes: '지구력 개발 - 더 긴 세트',
        exerciseType: 'Endurance Jacks',
        chadLevel: '🥉 브론즈 차드',
        difficulty: JumpingJackDifficulty.beginner,
        variations: ['롱 잭', '마라톤 잭'],
        specialInstructions: '일정한 속도로 끝까지 완주',
      ),
    },
    2: {
      // Week 2: 강도 증가 및 변형
      1: const JumpingJackWorkout(
        sets: [25, 35, 25, 25, 30],
        restSeconds: 55,
        notes: '크로스 잭 - 팔 교차 동작',
        exerciseType: 'Cross Jacks',
        chadLevel: '🥉 브론즈 차드',
        difficulty: JumpingJackDifficulty.intermediate,
        variations: ['크로스 오버', 'X-잭'],
        specialInstructions: '팔을 앞에서 교차하며 진행',
      ),
      2: const JumpingJackWorkout(
        sets: [30, 40, 30, 30, 35],
        restSeconds: 50,
        notes: '사이드 잭 - 좌우 이동',
        exerciseType: 'Side Step Jacks',
        chadLevel: '💯 라이징 차드',
        difficulty: JumpingJackDifficulty.intermediate,
        variations: ['래터럴 잭', '사이드 투 사이드'],
        specialInstructions: '좌우로 스텝하며 점핑잭 동작',
      ),
      3: const JumpingJackWorkout(
        sets: [35, 45, 35, 35, 40],
        restSeconds: 50,
        notes: '파워 잭 - 높은 점프',
        exerciseType: 'Power Jacks',
        chadLevel: '💯 라이징 차드',
        difficulty: JumpingJackDifficulty.intermediate,
        variations: ['하이 잭', '익스플로시브 잭'],
        specialInstructions: '최대한 높이 점프하며 동작',
      ),
    },
    3: {
      // Week 3: 고급 변형 및 콤보
      1: const JumpingJackWorkout(
        sets: [40, 55, 40, 40, 50],
        restSeconds: 45,
        notes: '스쿼트 잭 - 하체 강화',
        exerciseType: 'Squat Jacks',
        chadLevel: '🦾 스틸 차드',
        difficulty: JumpingJackDifficulty.advanced,
        variations: ['스쿼트 점프 잭', '수모 잭'],
        specialInstructions: '스쿼트 자세에서 점핑잭 동작',
      ),
      2: const JumpingJackWorkout(
        sets: [45, 60, 45, 45, 55],
        restSeconds: 45,
        notes: '플랭크 잭 - 코어 강화',
        exerciseType: 'Plank Jacks',
        chadLevel: '🦾 스틸 차드',
        difficulty: JumpingJackDifficulty.advanced,
        variations: ['푸쉬업 잭', '플랭크 점프'],
        specialInstructions: '플랭크 자세에서 다리만 점핑잭',
      ),
      3: const JumpingJackWorkout(
        sets: [50, 70, 50, 50, 65],
        restSeconds: 40,
        notes: '스타 점프 - 전신 폭발력',
        exerciseType: 'Star Jumps',
        chadLevel: '👑 레전드 차드',
        difficulty: JumpingJackDifficulty.expert,
        variations: ['스타 잭', '익스플로시브 스타'],
        specialInstructions: '별 모양으로 최대한 크게 점프',
      ),
    },
  };

  /// 특수 점핑잭 챌린지
  static Map<String, SpecialJumpingJackProgram> get specialPrograms => {
    'jack_marathon': const SpecialJumpingJackProgram(
      name: '점핑잭 마라톤 500개',
      description: '한 번에 500개 연속 점핑잭',
      duration: '논스톱 500개',
      targetReps: 500,
      chadLevel: '🏃‍♂️ 잭 마라토너',
      instructions: '500개를 완료할 때까지 절대 멈추지 마라',
    ),
    'tabata_jacks': const SpecialJumpingJackProgram(
      name: '타바타 점핑잭 익스트림',
      description: '20초 올아웃, 10초 휴식 x 8라운드',
      duration: '4분 지옥',
      targetReps: 160,
      chadLevel: '🔥 타바타 킬러',
      instructions: '4분간 멈추지 말고 최대 강도로',
    ),
    'jack_pyramid': const SpecialJumpingJackProgram(
      name: '점핑잭 피라미드 타워',
      description: '10-20-30-40-30-20-10개씩 진행',
      duration: '7라운드 완주',
      targetReps: 160,
      chadLevel: '🏗️ 피라미드 빌더',
      instructions: '피라미드를 건설하듯 차근차근 완성',
    ),
  };

  /// 일일 점핑잭 챌린지
  static List<DailyJumpingJackChallenge> get dailyChallenges => [
    const DailyJumpingJackChallenge(
      name: '💪 카디오 킥스타트',
      description: '100개 점핑잭을 5분 안에',
      targetReps: 100,
      timeLimit: 300,
      reward: '🚀 킥스타트 배지',
      minLevel: 1,
    ),
    const DailyJumpingJackChallenge(
      name: '🔥 번 머신',
      description: '200개 점핑잭을 논스톱으로',
      targetReps: 200,
      timeLimit: 600,
      reward: '🔥 번 배지',
      minLevel: 2,
    ),
    const DailyJumpingJackChallenge(
      name: '💥 익스플로시브 카디오',
      description: '300개 점핑잭을 10분 안에',
      targetReps: 300,
      timeLimit: 600,
      reward: '💥 폭발력 배지',
      minLevel: 3,
    ),
    const DailyJumpingJackChallenge(
      name: '👑 카디오 킹',
      description: '500개 점핑잭을 15분 안에',
      targetReps: 500,
      timeLimit: 900,
      reward: '👑 킹 배지',
      minLevel: 4,
    ),
  ];

  /// 레벨별 추천 프로그램
  static String getRecommendedProgram(int userLevel) {
    switch (userLevel) {
      case 1: return '6주 기초 카디오 (Week 1-2)';
      case 2: return '6주 카디오 프로그램 + 타바타';
      case 3: return '6주 완전 프로그램 + 피라미드';
      case 4: return '고급 프로그램 + 마라톤 500개';
      case 5: return '모든 챌린지 + 익스트림 콤보';
      default: return '6주 기초 카디오';
    }
  }
}

enum JumpingJackDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
  legendary,
}

class JumpingJackWorkout {
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;
  final JumpingJackDifficulty difficulty;
  final List<String> variations;
  final String specialInstructions;

  const JumpingJackWorkout({
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

class SpecialJumpingJackProgram {
  final String name;
  final String description;
  final String duration;
  final int targetReps;
  final String chadLevel;
  final String instructions;

  const SpecialJumpingJackProgram({
    required this.name,
    required this.description,
    required this.duration,
    required this.targetReps,
    required this.chadLevel,
    required this.instructions,
  });
}

class DailyJumpingJackChallenge {
  final String name;
  final String description;
  final int targetReps;
  final int timeLimit;
  final String reward;
  final int minLevel;

  const DailyJumpingJackChallenge({
    required this.name,
    required this.description,
    required this.targetReps,
    required this.timeLimit,
    required this.reward,
    this.minLevel = 1,
  });
}