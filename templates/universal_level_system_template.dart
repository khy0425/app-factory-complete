import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// 범용 운동 앱 레벨 선택 시스템 템플릿
/// 모든 운동 타입에 적용 가능한 확장 가능한 구조
class UniversalLevelSelectionScreen extends StatefulWidget {
  final String appName;
  final String exerciseType;
  final List<UniversalUserLevel> levels;
  final Color primaryColor;
  final String backgroundImagePath;

  const UniversalLevelSelectionScreen({
    super.key,
    required this.appName,
    required this.exerciseType,
    required this.levels,
    this.primaryColor = const Color(0xFFFFD700),
    this.backgroundImagePath = '',
  });

  @override
  State<UniversalLevelSelectionScreen> createState() => _UniversalLevelSelectionScreenState();
}

class _UniversalLevelSelectionScreenState extends State<UniversalLevelSelectionScreen> {
  int? selectedLevel;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1A1A1A),
      appBar: AppBar(
        title: Text(
          '💪 당신의 ${widget.exerciseType} 레벨은?',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: widget.primaryColor,
          ),
        ),
        backgroundColor: const Color(0xFF2A2A2A),
        centerTitle: true,
      ),
      body: Column(
        children: [
          _buildHeaderInfo(),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              itemCount: widget.levels.length,
              itemBuilder: (context, index) {
                final level = widget.levels[index];
                final isSelected = selectedLevel == level.id;

                return _buildLevelCard(level, isSelected);
              },
            ),
          ),
          if (selectedLevel != null) _buildStartButton(),
        ],
      ),
    );
  }

  Widget _buildHeaderInfo() {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFF2A2A2A).withOpacity(0.8),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: widget.primaryColor.withOpacity(0.3)),
        ),
        child: Text(
          '🔥 정직하게 선택하세요!\n실력에 맞는 프로그램으로 더 빠르고 효과적인 성장! 만삣삐!',
          style: const TextStyle(
            fontSize: 16,
            color: Colors.white70,
            height: 1.5,
            fontWeight: FontWeight.w500,
          ),
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  Widget _buildLevelCard(UniversalUserLevel level, bool isSelected) {
    return GestureDetector(
      onTap: () => setState(() => selectedLevel = level.id),
      child: Container(
        margin: const EdgeInsets.only(bottom: 16),
        decoration: BoxDecoration(
          color: isSelected ? level.color.withOpacity(0.2) : const Color(0xFF2A2A2A),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: isSelected ? level.color : Colors.transparent,
            width: 3,
          ),
          boxShadow: isSelected ? [
            BoxShadow(
              color: level.color.withOpacity(0.3),
              blurRadius: 12,
              spreadRadius: 2,
            ),
          ] : null,
        ),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Row(
            children: [
              // Chad 이미지
              Container(
                width: 90,
                height: 90,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(45),
                  border: Border.all(
                    color: isSelected ? level.color : Colors.white24,
                    width: 3,
                  ),
                  image: DecorationImage(
                    image: AssetImage(level.imagePath),
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              const SizedBox(width: 16),
              // 레벨 정보
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      level.title,
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: isSelected ? level.color : Colors.white,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      level.subtitle,
                      style: const TextStyle(
                        fontSize: 14,
                        color: Colors.white70,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      level.description,
                      style: const TextStyle(
                        fontSize: 13,
                        color: Colors.white60,
                        height: 1.3,
                      ),
                    ),
                    const SizedBox(height: 12),
                    // 능력 지표들
                    Row(
                      children: [
                        _buildStatChip(level.primaryStat, level.color),
                        const SizedBox(width: 8),
                        _buildStatChip(level.secondaryStat, level.color),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: level.color.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: level.color.withOpacity(0.4)),
                      ),
                      child: Text(
                        level.chadLevel,
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: level.color,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              // 선택 표시
              if (isSelected)
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: level.color,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.check,
                    color: Colors.white,
                    size: 24,
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatChip(String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: color,
        ),
      ),
    );
  }

  Widget _buildStartButton() {
    final selectedLevelData = widget.levels.firstWhere((l) => l.id == selectedLevel);

    return Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          // 선택된 레벨 상세 정보
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: selectedLevelData.color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: selectedLevelData.color.withOpacity(0.3),
              ),
            ),
            child: Column(
              children: [
                Text(
                  "🎯 ${selectedLevelData.workoutType}",
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  selectedLevelData.trainingFocus,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            height: 56,
            child: ElevatedButton(
              onPressed: () => _startWithSelectedLevel(),
              style: ElevatedButton.styleFrom(
                backgroundColor: widget.primaryColor,
                foregroundColor: Colors.black,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
              ),
              child: Text(
                '🔥 ${widget.appName} 시작하기! 만삣삐! 🔥',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _startWithSelectedLevel() async {
    if (selectedLevel == null) return;

    final level = widget.levels.firstWhere((l) => l.id == selectedLevel);
    final prefs = await SharedPreferences.getInstance();

    // 범용 사용자 레벨 정보 저장
    await prefs.setInt('user_level_id', level.id);
    await prefs.setString('exercise_type', widget.exerciseType);
    await prefs.setString('user_chad_level', level.chadLevel);
    await prefs.setString('workout_type', level.workoutType);
    await prefs.setString('training_focus', level.trainingFocus);
    await prefs.setMap('level_config', level.toMap());
    await prefs.setBool('has_selected_level', true);

    if (!mounted) return;

    // 메인 화면으로 이동
    Navigator.of(context).pushReplacementNamed('/home');
  }
}

/// 범용 사용자 레벨 데이터 구조
class UniversalUserLevel {
  final int id;
  final String title;
  final String subtitle;
  final String description;
  final String primaryStat;
  final String secondaryStat;
  final String chadLevel;
  final String workoutType;
  final String trainingFocus;
  final String imagePath;
  final Color color;
  final Map<String, dynamic> customConfig;

  const UniversalUserLevel({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.description,
    required this.primaryStat,
    required this.secondaryStat,
    required this.chadLevel,
    required this.workoutType,
    required this.trainingFocus,
    required this.imagePath,
    required this.color,
    this.customConfig = const {},
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'subtitle': subtitle,
      'description': description,
      'primaryStat': primaryStat,
      'secondaryStat': secondaryStat,
      'chadLevel': chadLevel,
      'workoutType': workoutType,
      'trainingFocus': trainingFocus,
      'imagePath': imagePath,
      'color': color.value,
      'customConfig': customConfig,
    };
  }
}

/// 운동별 레벨 시스템 팩토리
class ExerciseLevelFactory {

  /// 팔굽혀펴기 레벨 시스템
  static List<UniversalUserLevel> get pushupLevels => [
    const UniversalUserLevel(
      id: 1,
      title: "🥺 완전 초보자",
      subtitle: "팔굽혀펴기를 처음 시작해요",
      description: "무릎 팔굽혀펴기도\n5개가 힘들어요",
      primaryStat: "0-10개",
      secondaryStat: "무릎 푸쉬업",
      chadLevel: "☕ 베이비 차드",
      workoutType: "기초 근력 형성",
      trainingFocus: "올바른 자세 학습과 기초 체력",
      imagePath: "assets/images/커피차드.png",
      color: Color(0xFF8D6E63),
      customConfig: {"startingWeek": 1, "startingDay": 1, "pushupType": "knee"},
    ),
    const UniversalUserLevel(
      id: 2,
      title: "💪 운동 경험자",
      subtitle: "기본 팔굽혀펴기 가능해요",
      description: "표준 팔굽혀펴기\n10-30개 정도 할 수 있어요",
      primaryStat: "10-30개",
      secondaryStat: "표준 푸쉬업",
      chadLevel: "🥉 브론즈 차드",
      workoutType: "기본 근력 강화",
      trainingFocus: "세트 증가와 지구력 향상",
      imagePath: "assets/images/정면차드.jpg",
      color: Color(0xFFCD7F32),
      customConfig: {"startingWeek": 2, "startingDay": 1, "pushupType": "standard"},
    ),
    // ... 더 많은 레벨들
  ];

  /// 플랭크 레벨 시스템
  static List<UniversalUserLevel> get plankLevels => [
    const UniversalUserLevel(
      id: 1,
      title: "🥺 완전 초보자",
      subtitle: "플랭크를 처음 시작해요",
      description: "10초도 버티기\n힘들어요",
      primaryStat: "5-20초",
      secondaryStat: "기본 플랭크",
      chadLevel: "☕ 베이비 차드",
      workoutType: "코어 기초 형성",
      trainingFocus: "올바른 플랭크 자세와 기초 코어 힘",
      imagePath: "assets/images/커피차드.png",
      color: Color(0xFF4CAF50),
      customConfig: {"startingTime": 10, "targetTime": 300, "plankType": "basic"},
    ),
    // ... 더 많은 레벨들
  ];

  /// 버피 레벨 시스템
  static List<UniversalUserLevel> get burpeeLevels => [
    const UniversalUserLevel(
      id: 1,
      title: "🥺 완전 초보자",
      subtitle: "버피를 처음 시작해요",
      description: "버피 3개도\n매우 힘들어요",
      primaryStat: "1-5개",
      secondaryStat: "천천히 버피",
      chadLevel: "☕ 베이비 차드",
      workoutType: "전신 기초 운동",
      trainingFocus: "버피 동작 익히기와 기초 체력",
      imagePath: "assets/images/커피차드.png",
      color: Color(0xFF9C27B0),
      customConfig: {"startingReps": 3, "targetReps": 100, "burpeeType": "modified"},
    ),
    // ... 더 많은 레벨들
  ];

  /// 턱걸이 레벨 시스템
  static List<UniversalUserLevel> get pullupLevels => [
    const UniversalUserLevel(
      id: 1,
      title: "🥺 완전 초보자",
      subtitle: "턱걸이를 처음 시작해요",
      description: "턱걸이 1개도\n할 수 없어요",
      primaryStat: "0개",
      secondaryStat: "매달리기만",
      chadLevel: "☕ 베이비 차드",
      workoutType: "등 근력 기초",
      trainingFocus: "매달리기와 네거티브 연습",
      imagePath: "assets/images/커피차드.png",
      color: Color(0xFF2196F3),
      customConfig: {"startingReps": 0, "targetReps": 20, "pullupType": "assisted"},
    ),
    // ... 더 많은 레벨들
  ];

  /// 점프잭 레벨 시스템
  static List<UniversalUserLevel> get jumpingJackLevels => [
    const UniversalUserLevel(
      id: 1,
      title: "🥺 완전 초보자",
      subtitle: "점프잭을 처음 시작해요",
      description: "30초도 연속으로\n하기 힘들어요",
      primaryStat: "10-30초",
      secondaryStat: "느린 점프잭",
      chadLevel: "☕ 베이비 차드",
      workoutType: "유산소 기초",
      trainingFocus: "리듬감과 기초 유산소 능력",
      imagePath: "assets/images/커피차드.png",
      color: Color(0xFFFF5722),
      customConfig: {"startingTime": 30, "targetTime": 1200, "jumpType": "basic"},
    ),
    // ... 더 많은 레벨들
  ];

  /// 런지 레벨 시스템
  static List<UniversalUserLevel> get lungeLevels => [
    const UniversalUserLevel(
      id: 1,
      title: "🥺 완전 초보자",
      subtitle: "런지를 처음 시작해요",
      description: "런지 10개도\n균형 잡기 힘들어요",
      primaryStat: "5-15개",
      secondaryStat: "기본 런지",
      chadLevel: "☕ 베이비 차드",
      workoutType: "하체 기초 운동",
      trainingFocus: "균형감과 올바른 런지 자세",
      imagePath: "assets/images/커피차드.png",
      color: Color(0xFF795548),
      customConfig: {"startingReps": 10, "targetReps": 200, "lungeType": "static"},
    ),
    // ... 더 많은 레벨들
  ];

  /// 운동 타입별 레벨 시스템 가져오기
  static List<UniversalUserLevel> getLevelsForExercise(String exerciseType) {
    switch (exerciseType.toLowerCase()) {
      case 'pushup':
      case '팔굽혀펴기':
        return pushupLevels;
      case 'plank':
      case '플랭크':
        return plankLevels;
      case 'burpee':
      case '버피':
        return burpeeLevels;
      case 'pullup':
      case '턱걸이':
        return pullupLevels;
      case 'jumping_jack':
      case '점프잭':
        return jumpingJackLevels;
      case 'lunge':
      case '런지':
        return lungeLevels;
      case 'squat':
      case '스쿼트':
        return []; // 이미 구현된 스쿼트 레벨 사용
      case 'running':
      case '러닝':
        return []; // 이미 구현된 러닝 레벨 사용
      default:
        return _getDefaultLevels();
    }
  }

  static List<UniversalUserLevel> _getDefaultLevels() {
    return [
      const UniversalUserLevel(
        id: 1,
        title: "🥺 완전 초보자",
        subtitle: "운동을 처음 시작해요",
        description: "기본 동작도\n어려워해요",
        primaryStat: "입문자",
        secondaryStat: "기초 동작",
        chadLevel: "☕ 베이비 차드",
        workoutType: "기초 체력 형성",
        trainingFocus: "올바른 자세 학습",
        imagePath: "assets/images/커피차드.png",
        color: Color(0xFF8D6E63),
      ),
      // ... 기본 레벨들
    ];
  }
}