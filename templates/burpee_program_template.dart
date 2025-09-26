import 'dart:math';

/// 버피 전문 운동 프로그램
class BurpeePrograms {

  /// 6주 버피 마스터 프로그램
  static Map<int, Map<int, BurpeeWorkout>> get sixWeekProgram => {
    1: {
      // Week 1: 버피 기초 마스터
      1: const BurpeeWorkout(
        sets: [2, 3, 2, 2, 3],
        restSeconds: 120,
        notes: '버피 동작 분해 연습 - 천천히 정확하게',
        exerciseType: 'Modified Burpees',
        chadLevel: '☕ 베이비 차드',
        difficulty: BurpeeDifficulty.beginner,
        variations: ['스텝백 버피', '점프 없는 버피'],
        specialInstructions: '각 동작을 천천히 정확하게 수행',
      ),
      2: const BurpeeWorkout(
        sets: [3, 4, 3, 3, 4],
        restSeconds: 120,
        notes: '리듬감 익히기 - 일정한 속도 유지',
        exerciseType: 'Rhythm Burpees',
        chadLevel: '☕ 베이비 차드',
        difficulty: BurpeeDifficulty.beginner,
        variations: ['템포 버피', '카운트 버피'],
        specialInstructions: '1-2-3-4 박자에 맞춰 동작',
      ),
      3: const BurpeeWorkout(
        sets: [4, 5, 4, 4, 5],
        restSeconds: 110,
        notes: '체력 향상 - 연속 동작 연습',
        exerciseType: 'Continuous Burpees',
        chadLevel: '🥉 브론즈 차드',
        difficulty: BurpeeDifficulty.beginner,
        variations: ['논스톱 버피', '플로우 버피'],
        specialInstructions: '세트 내에서 멈추지 말고 연속 진행',
      ),
    },
    2: {
      // Week 2: 강도 증가
      1: const BurpeeWorkout(
        sets: [5, 7, 5, 5, 6],
        restSeconds: 110,
        notes: '파워 개발 - 폭발적 점프',
        exerciseType: 'Power Burpees',
        chadLevel: '🥉 브론즈 차드',
        difficulty: BurpeeDifficulty.intermediate,
        variations: ['하이 점프 버피', '니 터치 버피'],
        specialInstructions: '점프 시 최대한 높이 올라가기',
      ),
      2: const BurpeeWorkout(
        sets: [6, 8, 6, 6, 7],
        restSeconds: 100,
        notes: '지구력 훈련 - 더 긴 세트',
        exerciseType: 'Endurance Burpees',
        chadLevel: '💯 라이징 차드',
        difficulty: BurpeeDifficulty.intermediate,
        variations: ['롱 버피', '마라톤 버피'],
        specialInstructions: '페이스 조절하며 끝까지 완주',
      ),
      3: const BurpeeWorkout(
        sets: [7, 10, 7, 7, 8],
        restSeconds: 100,
        notes: '스피드 훈련 - 빠른 전환',
        exerciseType: 'Speed Burpees',
        chadLevel: '💯 라이징 차드',
        difficulty: BurpeeDifficulty.intermediate,
        variations: ['스피드 버피', '라이트닝 버피'],
        specialInstructions: '동작 전환을 최대한 빠르게',
      ),
    },
    3: {
      // Week 3: 중급 도전
      1: const BurpeeWorkout(
        sets: [8, 12, 8, 8, 10],
        restSeconds: 90,
        notes: '복합 동작 - 푸쉬업 추가',
        exerciseType: 'Pushup Burpees',
        chadLevel: '🦾 스틸 차드',
        difficulty: BurpeeDifficulty.advanced,
        variations: ['푸쉬업 버피', '다이아몬드 버피'],
        specialInstructions: '플랭크 자세에서 완전한 푸쉬업 수행',
      ),
      2: const BurpeeWorkout(
        sets: [10, 15, 10, 10, 12],
        restSeconds: 90,
        notes: '변형 동작 - 다양한 스타일',
        exerciseType: 'Variation Burpees',
        chadLevel: '🦾 스틸 차드',
        difficulty: BurpeeDifficulty.advanced,
        variations: ['스타 점프 버피', '180도 버피'],
        specialInstructions: '매 세트마다 다른 변형 적용',
      ),
      3: const BurpeeWorkout(
        sets: [12, 18, 12, 12, 15],
        restSeconds: 85,
        notes: '체력 한계 도전 - 더 높은 강도',
        exerciseType: 'Challenge Burpees',
        chadLevel: '👑 레전드 차드',
        difficulty: BurpeeDifficulty.expert,
        variations: ['더블 점프 버피', '플라이오 버피'],
        specialInstructions: '한계를 넘어서는 강도로 도전',
      ),
    },
  };

  /// 특수 버피 챌린지 프로그램
  static Map<String, SpecialBurpeeProgram> get specialPrograms => {
    'burpee_hell': const SpecialBurpeeProgram(
      name: '버피 지옥 100개',
      description: '한 번에 100개 연속 버피 도전',
      duration: '논스톱 지옥',
      targetReps: 100,
      chadLevel: '😈 버피 데몬',
      instructions: '100개를 완료할 때까지 멈추지 마라',
    ),
    'tabata_burpees': const SpecialBurpeeProgram(
      name: '타바타 버피 데스',
      description: '20초 올아웃, 10초 휴식 x 8라운드',
      duration: '4분 지옥',
      targetReps: 64,
      chadLevel: '🔥 타바타 킬러',
      instructions: '4분간 멈추지 말고 최대 강도로',
    ),
    'pyramid_burpees': const SpecialBurpeeProgram(
      name: '버피 피라미드 클라이밍',
      description: '1-2-3-4-5-4-3-2-1개씩 진행',
      duration: '9라운드 완주',
      targetReps: 25,
      chadLevel: '⛰️ 피라미드 차드',
      instructions: '피라미드를 완성하라',
    ),
  };

  /// 일일 버피 챌린지
  static List<DailyBurpeeChallenge> get dailyChallenges => [
    const DailyBurpeeChallenge(
      name: '💪 퀵 파워 버피',
      description: '15개 버피를 3분 안에',
      targetReps: 15,
      timeLimit: 180,
      reward: '⚡ 스피드 배지',
      minLevel: 1,
    ),
    const DailyBurpeeChallenge(
      name: '🔥 미드나잇 버피',
      description: '30개 버피를 논스톱으로',
      targetReps: 30,
      timeLimit: 600,
      reward: '🌙 미드나잇 배지',
      minLevel: 2,
    ),
    const DailyBurpeeChallenge(
      name: '💥 익스플로시브 버피',
      description: '50개 버피를 8분 안에',
      targetReps: 50,
      timeLimit: 480,
      reward: '💥 폭발력 배지',
      minLevel: 3,
    ),
    const DailyBurpeeChallenge(
      name: '👑 레전드 버피',
      description: '75개 버피를 10분 안에',
      targetReps: 75,
      timeLimit: 600,
      reward: '👑 레전드 배지',
      minLevel: 4,
    ),
  ];

  /// 레벨별 추천 프로그램
  static String getRecommendedProgram(int userLevel) {
    switch (userLevel) {
      case 1: return '6주 기초 프로그램 (Week 1-2)';
      case 2: return '6주 기초 프로그램 + 타바타 챌린지';
      case 3: return '6주 완전 프로그램 + 특수 챌린지';
      case 4: return '고급 프로그램 + 버피 지옥';
      case 5: return '모든 챌린지 + 커스텀 극한 도전';
      default: return '6주 기초 프로그램';
    }
  }
}

enum BurpeeDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
  legendary,
}

class BurpeeWorkout {
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;
  final BurpeeDifficulty difficulty;
  final List<String> variations;
  final String specialInstructions;

  const BurpeeWorkout({
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
    int setTime = sets.length * 3; // 버피는 세트당 3분 예상
    int restTime = (sets.length - 1) * (restSeconds ~/ 60);
    return setTime + restTime;
  }
}

class SpecialBurpeeProgram {
  final String name;
  final String description;
  final String duration;
  final int targetReps;
  final String chadLevel;
  final String instructions;

  const SpecialBurpeeProgram({
    required this.name,
    required this.description,
    required this.duration,
    required this.targetReps,
    required this.chadLevel,
    required this.instructions,
  });
}

class DailyBurpeeChallenge {
  final String name;
  final String description;
  final int targetReps;
  final int timeLimit;
  final String reward;
  final int minLevel;

  const DailyBurpeeChallenge({
    required this.name,
    required this.description,
    required this.targetReps,
    required this.timeLimit,
    required this.reward,
    this.minLevel = 1,
  });
}