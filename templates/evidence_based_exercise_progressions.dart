import 'dart:math';

/// 과학적 연구 기반 운동 진행 프로그램
/// ACSM 가이드라인과 최신 연구 결과를 반영한 체계적 진행
///
/// 📚 주요 참고 연구:
/// • Pull-up: "Effect of Progressive Calisthenic Push-up Training" (PubMed: 29466268)
/// • Lunge: "8-week lunge exercise on unstable surface" (PMC: 9925109)
/// • Plank: "Progression of Core Stability Exercises" (PubMed: 28157133)
/// • Burpee: "International Standards for 3-Minute Burpee Test" (PMC: 6815084)
/// • ACSM: "Guidelines for Exercise Testing and Prescription" (2024)
/// • Minute Calisthenics: "randomized controlled study" (BMC: 12889-020-09355-4)
class EvidenceBasedExerciseProgressions {

  /// 풀업 진행 프로그램 (연구 기반)
  /// 참고: Dead hang → Negative → Assisted → Full pull-up
  static Map<int, Map<int, PullUpWorkout>> get scientificPullUpProgram => {
    1: {
      // Week 1-2: 기초 근력 및 그립 강도 개발
      1: const PullUpWorkout(
        exercises: [
          ExerciseSet(
            name: 'Dead Hang',
            sets: [10, 15, 10, 10, 12], // 초 단위
            restSeconds: 90,
            notes: '바에 매달리기 - 어깨 활성화',
            instructions: '어깨를 아래로 당기며 코어 활성화',
          ),
          ExerciseSet(
            name: 'Assisted Pull-ups (Band)',
            sets: [3, 5, 3, 3, 4], // 개수
            restSeconds: 120,
            notes: '밴드 보조 풀업 - 올바른 폼 학습',
            instructions: '턱이 바 위로 완전히 올라가기',
          ),
        ],
        chadLevel: '☕ 베이비 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: 'Dead hang 30초-1분 목표 (Harvard Spaulding Rehabilitation)',
      ),
      2: const PullUpWorkout(
        exercises: [
          ExerciseSet(
            name: 'Dead Hang',
            sets: [15, 20, 15, 15, 18],
            restSeconds: 90,
            notes: '매달리기 시간 증가',
            instructions: '1분 연속 매달리기 목표',
          ),
          ExerciseSet(
            name: 'Negative Pull-ups',
            sets: [2, 3, 2, 2, 3],
            restSeconds: 150,
            notes: '네거티브 풀업 - 천천히 내려오기',
            instructions: '3-5초에 걸쳐 천천히 하강',
          ),
          ExerciseSet(
            name: 'Inverted Rows',
            sets: [5, 8, 5, 5, 6],
            restSeconds: 90,
            notes: '수평 당기기 - 풀업 준비 운동',
            instructions: '몸을 일직선으로 유지하며 가슴을 바에',
          ),
        ],
        chadLevel: '🥉 브론즈 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: '네거티브 동작시 근력 56% 향상 (Calisthenics Research Study)',
      ),
    },
    2: {
      // Week 3-4: 보조 풀업에서 독립적 풀업으로
      1: const PullUpWorkout(
        exercises: [
          ExerciseSet(
            name: 'Jumping Pull-ups',
            sets: [3, 5, 3, 3, 4],
            restSeconds: 120,
            notes: '점프 보조 풀업 - 상승 연습',
            instructions: '점프로 시작해서 천천히 내려오기',
          ),
          ExerciseSet(
            name: 'Assisted Pull-ups (Light Band)',
            sets: [2, 4, 2, 2, 3],
            restSeconds: 150,
            notes: '가벼운 밴드 보조 - 독립적 풀업 준비',
            instructions: '보조 최소화하며 완전한 동작',
          ),
          ExerciseSet(
            name: 'Lat Pulldowns',
            sets: [8, 12, 8, 8, 10],
            restSeconds: 90,
            notes: '래트 풀다운 - 근력 보강',
            instructions: '풀업과 유사한 근육 활성화',
          ),
        ],
        chadLevel: '💯 라이징 차드',
        difficulty: ExerciseDifficulty.intermediate,
        researchNote: '주 3회 훈련시 근력 향상 56% 증가 (Sports Science Research)',
      ),
    },
  };

  /// 런지 진행 프로그램 (8주 연구 기반)
  /// 참고: 8주간 주3회, 10% 체중 부하까지 진행
  static Map<int, Map<int, LungeWorkout>> get scientificLungeProgram => {
    1: {
      // Week 1-2: 기본 런지 패턴 학습 (연구 프로토콜 적용)
      1: const LungeWorkout(
        exercises: [
          ExerciseSet(
            name: 'Bodyweight Forward Lunges',
            sets: [8, 10, 8, 8, 10], // 각 다리당
            restSeconds: 90,
            notes: '기본 앞 런지 - 올바른 폼 학습',
            instructions: '무릎 90도, 앞 무릎이 발끝 넘지 않게',
          ),
          ExerciseSet(
            name: 'Static Lunges',
            sets: [10, 12, 10, 10, 12],
            restSeconds: 60,
            notes: '정적 런지 - 균형감각 개발',
            instructions: '한 자세에서 반복, 균형 유지',
          ),
        ],
        chadLevel: '☕ 베이비 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: 'OMNI scale 6-8 강도 (PMC: 9925109 - 8주 런지 연구)',
      ),
      2: const LungeWorkout(
        exercises: [
          ExerciseSet(
            name: 'Walking Lunges',
            sets: [10, 15, 10, 10, 12],
            restSeconds: 90,
            notes: '워킹 런지 - 동적 균형',
            instructions: '앞으로 걸으며 런지, 공간 확보 필요',
          ),
          ExerciseSet(
            name: 'Reverse Lunges',
            sets: [8, 12, 8, 8, 10],
            restSeconds: 90,
            notes: '리버스 런지 - 무릎 보호',
            instructions: '뒤로 스텝하며 런지',
          ),
          ExerciseSet(
            name: 'Side Lunges',
            sets: [6, 10, 6, 6, 8],
            restSeconds: 90,
            notes: '사이드 런지 - 측면 강화',
            instructions: '옆으로 크게 스텝, 한쪽 다리로 체중 지지',
          ),
        ],
        chadLevel: '🥉 브론즈 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: '긴 스텝이 근육 활성화 더 효과적 (MDPI Journal Study)',
      ),
    },
    2: {
      // Week 3-4: 부하 추가 (연구에서 10% 체중 사용)
      1: const LungeWorkout(
        exercises: [
          ExerciseSet(
            name: 'Weighted Forward Lunges',
            sets: [8, 10, 8, 8, 10],
            restSeconds: 120,
            notes: '중량 추가 런지 - 5% 체중 부하',
            instructions: '덤벨이나 물병 사용, 3-5kg',
          ),
          ExerciseSet(
            name: 'Bulgarian Split Squats',
            sets: [6, 8, 6, 6, 8],
            restSeconds: 120,
            notes: '불가리안 스플릿 스쿼트 - 고급 변형',
            instructions: '뒷발을 의자에 올리고 런지',
          ),
        ],
        chadLevel: '💯 라이징 차드',
        difficulty: ExerciseDifficulty.intermediate,
        researchNote: '10% 체중 부하까지 안전 (PMC: 9925109 - 중년 여성 대상)',
      ),
    },
  };

  /// 플랭크 진행 프로그램 (근전도 연구 기반)
  /// 참고: Stable → Suspended 진행
  static Map<int, Map<int, PlankWorkout>> get scientificPlankProgram => {
    1: {
      // Week 1-2: 안정 표면에서 기초 플랭크
      1: const PlankWorkout(
        exercises: [
          ExerciseSet(
            name: 'Stable Prone Plank',
            sets: [15, 20, 15, 15, 18], // 초 단위
            restSeconds: 60,
            notes: '기본 플랭크 - 10-30초 목표',
            instructions: '몸 일직선, 엉덩이 들지 않기',
          ),
          ExerciseSet(
            name: 'Knee Plank (Modified)',
            sets: [20, 30, 20, 20, 25],
            restSeconds: 45,
            notes: '무릎 플랭크 - 초보자용',
            instructions: '무릎을 바닥에 대고 플랭크',
          ),
        ],
        chadLevel: '☕ 베이비 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: '30초 미만은 초보자 수준 (Harvard Health Publishing)',
      ),
      2: const PlankWorkout(
        exercises: [
          ExerciseSet(
            name: 'Stable Prone Plank',
            sets: [25, 35, 25, 25, 30],
            restSeconds: 60,
            notes: '플랭크 시간 증가 - 30초+ 목표',
            instructions: '코어 근지구력 개발',
          ),
          ExerciseSet(
            name: 'Stable Lateral Plank',
            sets: [15, 20, 15, 15, 18],
            restSeconds: 60,
            notes: '사이드 플랭크 - 측면 코어',
            instructions: '몸을 옆으로 기울여서 플랭크',
          ),
        ],
        chadLevel: '🥉 브론즈 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: '측면 플랭크가 요추 강화 효과적 (PubMed: 28157133)',
      ),
    },
    2: {
      // Week 3-4: 고급 플랭크 변형
      1: const PlankWorkout(
        exercises: [
          ExerciseSet(
            name: 'Unilateral Stable Prone Plank',
            sets: [10, 15, 10, 10, 12],
            restSeconds: 90,
            notes: '한 팔 플랭크 - 불안정성 증가',
            instructions: '한 팔씩 번갈아가며 들어올리기',
          ),
          ExerciseSet(
            name: 'Stable Roll-out Plank',
            sets: [8, 12, 8, 8, 10],
            restSeconds: 120,
            notes: '롤아웃 플랭크 - 복직근 강화',
            instructions: '팔을 앞으로 뻗으며 플랭크',
          ),
        ],
        chadLevel: '💯 라이징 차드',
        difficulty: ExerciseDifficulty.intermediate,
        researchNote: '롤아웃이 복직근 활성화 최대 (PubMed: 28157133 - EMG 연구)',
      ),
    },
  };

  /// 버피 진행 프로그램 (3분 버피 테스트 기반)
  /// 참고: 국제 표준 연구 - 37-66개/3분이 평균
  static Map<int, Map<int, BurpeeWorkout>> get scientificBurpeeProgram => {
    1: {
      // Week 1: 수정된 버피로 시작 (초보자 권장)
      1: const BurpeeWorkout(
        exercises: [
          ExerciseSet(
            name: 'Half Burpees',
            sets: [3, 5, 3, 3, 4],
            restSeconds: 120,
            notes: '반 버피 - 점프 없는 버전',
            instructions: '스쿼트 → 플랭크 → 스쿼트 → 서기',
          ),
          ExerciseSet(
            name: 'Step-back Burpees',
            sets: [2, 4, 2, 2, 3],
            restSeconds: 150,
            notes: '스텝백 버피 - 무릎 보호',
            instructions: '점프 대신 한 발씩 뒤로',
          ),
        ],
        chadLevel: '☕ 베이비 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: '초보자는 수정된 버전부터 시작 (ACSM Guidelines)',
      ),
      2: const BurpeeWorkout(
        exercises: [
          ExerciseSet(
            name: 'Modified Burpees',
            sets: [5, 8, 5, 5, 6],
            restSeconds: 120,
            notes: '수정 버피 - 동작 분해',
            instructions: '각 동작을 천천히 정확하게',
          ),
          ExerciseSet(
            name: 'Standard Burpees',
            sets: [2, 3, 2, 2, 3],
            restSeconds: 180,
            notes: '표준 버피 도입 - 완전한 동작',
            instructions: '스쿼트 → 플랭크 → 푸쉬업 → 점프',
          ),
        ],
        chadLevel: '🥉 브론즈 차드',
        difficulty: ExerciseDifficulty.beginner,
        researchNote: '올바른 폼이 부상 방지에 중요 (Cleveland Clinic)',
      ),
    },
    2: {
      // Week 2: 2주 진행 프로그램 (연구 기반)
      1: const BurpeeWorkout(
        exercises: [
          ExerciseSet(
            name: 'Standard Burpees',
            sets: [8, 10, 8, 8, 10], // 2주 프로그램 Day 4-7
            restSeconds: 120,
            notes: '표준 버피 증가 - 일관된 리듬',
            instructions: '30초 휴식으로 세트 간격',
          ),
          ExerciseSet(
            name: '3-Minute Burpee Test Prep',
            sets: [12, 15, 12, 12, 15], // 2주 프로그램 Day 11-14
            restSeconds: 90,
            notes: '3분 테스트 준비 - 지구력 개발',
            instructions: '평균 37-66개/3분 목표',
          ),
        ],
        chadLevel: '💯 라이징 차드',
        difficulty: ExerciseDifficulty.intermediate,
        researchNote: '2주 프로그램으로 체력 변화 가능 (PMC: 6815084 - 국제표준)',
      ),
    },
  };

  /// ACSM 가이드라인 기반 훈련 원칙
  static Map<String, TrainingPrinciple> get acsm_guidelines => {
    'frequency': const TrainingPrinciple(
      principle: '주 2-3회 저항 훈련',
      evidence: 'ACSM 권장사항 - 근력 발달을 위한 최소 빈도',
      application: '각 운동을 주 2-3회 실시',
    ),
    'sets_reps': const TrainingPrinciple(
      principle: '초보자: 1-2세트, 8-12회',
      evidence: 'ACSM 가이드라인 - 근력과 근비대 동시 발달',
      application: '8-12회 완료 가능한 강도로 설정',
    ),
    'progression': const TrainingPrinciple(
      principle: '점진적 과부하',
      evidence: '반복 횟수와 부하 증가 모두 효과적',
      application: '주당 5-10% 증가 권장',
    ),
    'rest': const TrainingPrinciple(
      principle: '세트 간 휴식 60-120초',
      evidence: '근력 회복과 성장을 위한 최적 시간',
      application: '운동 강도에 따라 조절',
    ),
  };
}

enum ExerciseDifficulty {
  beginner,
  intermediate,
  advanced,
  expert,
}

class ExerciseSet {
  final String name;
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String instructions;

  const ExerciseSet({
    required this.name,
    required this.sets,
    required this.restSeconds,
    required this.notes,
    required this.instructions,
  });
}

class PullUpWorkout {
  final List<ExerciseSet> exercises;
  final String chadLevel;
  final ExerciseDifficulty difficulty;
  final String researchNote;

  const PullUpWorkout({
    required this.exercises,
    required this.chadLevel,
    required this.difficulty,
    required this.researchNote,
  });
}

class LungeWorkout {
  final List<ExerciseSet> exercises;
  final String chadLevel;
  final ExerciseDifficulty difficulty;
  final String researchNote;

  const LungeWorkout({
    required this.exercises,
    required this.chadLevel,
    required this.difficulty,
    required this.researchNote,
  });
}

class PlankWorkout {
  final List<ExerciseSet> exercises;
  final String chadLevel;
  final ExerciseDifficulty difficulty;
  final String researchNote;

  const PlankWorkout({
    required this.exercises,
    required this.chadLevel,
    required this.difficulty,
    required this.researchNote,
  });
}

class BurpeeWorkout {
  final List<ExerciseSet> exercises;
  final String chadLevel;
  final ExerciseDifficulty difficulty;
  final String researchNote;

  const BurpeeWorkout({
    required this.exercises,
    required this.chadLevel,
    required this.difficulty,
    required this.researchNote,
  });
}

class TrainingPrinciple {
  final String principle;
  final String evidence;
  final String application;

  const TrainingPrinciple({
    required this.principle,
    required this.evidence,
    required this.application,
  });
}