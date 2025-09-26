#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 운동 앱 생성기 - 레벨 시스템 통합
초보자부터 고수까지 모든 사용자를 위한 완전한 운동 앱 자동 생성
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

class EnhancedFitnessAppGenerator:
    def __init__(self):
        self.base_dir = Path(".")
        self.templates_dir = self.base_dir / "templates"
        self.flutter_apps_dir = self.base_dir / "flutter_apps"

        # 운동별 설정 데이터
        self.exercise_configs = {
            "pushup": {
                "app_name": "푸쉬업 마스터",
                "description": "완벽한 팔굽혀펴기 마스터 되기",
                "korean_name": "푸쉬업PT",
                "package_name": "pushuppt",
                "primary_color": "#FF6B35",
                "icon_color": "#FF4500",
                "chad_theme": "파워",
                "exercise_unit": "개",
                "difficulty_levels": 5,
                "weekly_progression": True,
                "max_target": 100,
                "special_features": ["다이아몬드 푸쉬업", "한손 푸쉬업", "클랩 푸쉬업"]
            },
            "plank": {
                "app_name": "플랭크 챔피언",
                "description": "강철 코어 플랭크 챔피언 되기",
                "korean_name": "플랭크PT",
                "package_name": "plankpt",
                "primary_color": "#4CAF50",
                "icon_color": "#2E7D32",
                "chad_theme": "안정성",
                "exercise_unit": "초",
                "difficulty_levels": 5,
                "weekly_progression": True,
                "max_target": 600,  # 10분
                "special_features": ["사이드 플랭크", "플랭크 업다운", "플랭크 잭"]
            },
            "burpee": {
                "app_name": "버피 비스트",
                "description": "최강 전신 운동 버피 비스트",
                "korean_name": "버피PT",
                "package_name": "burpeept",
                "primary_color": "#9C27B0",
                "icon_color": "#7B1FA2",
                "chad_theme": "지옥",
                "exercise_unit": "개",
                "difficulty_levels": 5,
                "weekly_progression": True,
                "max_target": 100,
                "special_features": ["버피 박스 점프", "버피 풀업", "데빌 버피"]
            },
            "pullup": {
                "app_name": "풀업 프로",
                "description": "등근육 최강자 풀업 프로",
                "korean_name": "턱걸이PT",
                "package_name": "pulluppt",
                "primary_color": "#2196F3",
                "icon_color": "#1976D2",
                "chad_theme": "등근육",
                "exercise_unit": "개",
                "difficulty_levels": 5,
                "weekly_progression": True,
                "max_target": 30,
                "special_features": ["와이드 그립", "L-sitt 풀업", "머슬업"]
            },
            "jumping_jack": {
                "app_name": "점프잭 제다이",
                "description": "유산소 마스터 점프잭 제다이",
                "korean_name": "점프잭PT",
                "package_name": "jumpingjackpt",
                "primary_color": "#FF5722",
                "icon_color": "#D84315",
                "chad_theme": "유산소",
                "exercise_unit": "초",
                "difficulty_levels": 5,
                "weekly_progression": True,
                "max_target": 1200,  # 20분
                "special_features": ["크로스 잭", "파워 잭", "스타 점프"]
            },
            "lunge": {
                "app_name": "런지 레전드",
                "description": "하체 균형 마스터 런지 레전드",
                "korean_name": "런지PT",
                "package_name": "lungept",
                "primary_color": "#795548",
                "icon_color": "#5D4037",
                "chad_theme": "균형",
                "exercise_unit": "개",
                "difficulty_levels": 5,
                "weekly_progression": True,
                "max_target": 200,
                "special_features": ["점프 런지", "사이드 런지", "워킹 런지"]
            }
        }

    def create_complete_app(self, exercise_type, custom_config=None):
        """완전한 레벨 시스템을 갖춘 운동 앱 생성"""
        if exercise_type not in self.exercise_configs:
            print(f"❌ 지원하지 않는 운동 타입: {exercise_type}")
            return False

        config = self.exercise_configs[exercise_type].copy()
        if custom_config:
            config.update(custom_config)

        print(f"🚀 {config['app_name']} 앱 생성 시작...")

        try:
            # 1. 기본 앱 구조 생성
            app_path = self._create_base_app_structure(config)

            # 2. 레벨 시스템 통합
            self._integrate_level_system(app_path, config)

            # 3. 운동 프로그램 생성
            self._create_workout_programs(app_path, config)

            # 4. UI 화면들 생성
            self._create_ui_screens(app_path, config)

            # 5. 알림 시스템 적용
            self._apply_notification_system(app_path, config)

            # 6. 설정 및 마무리
            self._finalize_app(app_path, config)

            print(f"✅ {config['app_name']} 앱 생성 완료!")
            print(f"📁 경로: {app_path}")

            return True

        except Exception as e:
            print(f"❌ 앱 생성 중 오류 발생: {str(e)}")
            return False

    def _create_base_app_structure(self, config):
        """기본 앱 구조 생성"""
        app_path = self.flutter_apps_dir / config['package_name']

        # 기존 앱이 있으면 백업
        if app_path.exists():
            backup_path = app_path.with_name(f"{config['package_name']}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.move(str(app_path), str(backup_path))
            print(f"📦 기존 앱 백업: {backup_path}")

        # 템플릿에서 복사
        template_path = self.base_dir / "templates" / "flutter_app_template"
        if not template_path.exists():
            # Mission100을 템플릿으로 사용
            template_path = self.flutter_apps_dir / "mission100_v3"

        shutil.copytree(str(template_path), str(app_path))

        # pubspec.yaml 업데이트
        self._update_pubspec(app_path, config)

        return app_path

    def _integrate_level_system(self, app_path, config):
        """레벨 시스템 통합"""
        print(f"🎯 레벨 시스템 통합 중...")

        # 레벨 선택 화면 생성
        level_screen_content = self._generate_level_selection_screen(config)
        level_screen_path = app_path / "lib" / "screens" / "level_selection_screen.dart"
        level_screen_path.parent.mkdir(parents=True, exist_ok=True)

        with open(level_screen_path, 'w', encoding='utf-8') as f:
            f.write(level_screen_content)

        # 레벨별 운동 데이터 생성
        workout_data_content = self._generate_workout_data(config)
        workout_data_path = app_path / "lib" / "utils" / f"scientific_{config['package_name']}_data.dart"
        workout_data_path.parent.mkdir(parents=True, exist_ok=True)

        with open(workout_data_path, 'w', encoding='utf-8') as f:
            f.write(workout_data_content)

    def _create_workout_programs(self, app_path, config):
        """운동 프로그램 생성"""
        print(f"💪 운동 프로그램 생성 중...")

        # 기본 프로그램
        basic_program = self._generate_basic_program(config)

        # 고급 프로그램
        advanced_program = self._generate_advanced_program(config)

        # 특수 챌린지
        special_challenges = self._generate_special_challenges(config)

        # 파일로 저장
        programs_dir = app_path / "lib" / "utils"
        programs_dir.mkdir(parents=True, exist_ok=True)

        # 프로그램 파일들 생성
        self._save_program_files(programs_dir, config, basic_program, advanced_program, special_challenges)

    def _create_ui_screens(self, app_path, config):
        """UI 화면들 생성"""
        print(f"🎨 UI 화면 생성 중...")

        screens_dir = app_path / "lib" / "screens"
        screens_dir.mkdir(parents=True, exist_ok=True)

        # 메인 화면
        main_screen_content = self._generate_main_screen(config)
        with open(screens_dir / "main_screen.dart", 'w', encoding='utf-8') as f:
            f.write(main_screen_content)

        # 운동 화면
        workout_screen_content = self._generate_workout_screen(config)
        with open(screens_dir / "workout_screen.dart", 'w', encoding='utf-8') as f:
            f.write(workout_screen_content)

        # 진행상황 화면
        progress_screen_content = self._generate_progress_screen(config)
        with open(screens_dir / "progress_screen.dart", 'w', encoding='utf-8') as f:
            f.write(progress_screen_content)

    def _apply_notification_system(self, app_path, config):
        """알림 시스템 적용"""
        print(f"🔔 알림 시스템 적용 중...")

        # 알림 서비스 복사 및 커스터마이징
        notification_template = self.templates_dir / "notification_service_template.dart"
        notification_target = app_path / "lib" / "services" / "notification_service.dart"

        if notification_template.exists():
            # 템플릿 읽기
            with open(notification_template, 'r', encoding='utf-8') as f:
                content = f.read()

            # 플레이스홀더 교체
            content = content.replace("{{APP_NAME}}", config['app_name'])
            content = content.replace("{{APP_TITLE}}", config['app_name'].upper())
            content = content.replace("{{CHANNEL_NAME}}", f"com.reaf.{config['package_name']}.notification_permissions")

            # 파일 저장
            notification_target.parent.mkdir(parents=True, exist_ok=True)
            with open(notification_target, 'w', encoding='utf-8') as f:
                f.write(content)

    def _finalize_app(self, app_path, config):
        """앱 설정 마무리"""
        print(f"⚙️ 앱 설정 마무리 중...")

        # main.dart 업데이트
        self._update_main_dart(app_path, config)

        # 안드로이드 설정 업데이트
        self._update_android_config(app_path, config)

        # 앱 정보 파일 생성
        self._create_app_info_file(app_path, config)

    def _generate_level_selection_screen(self, config):
        """레벨 선택 화면 생성"""
        exercise_type = config.get('exercise_type', 'exercise')
        app_name = config['app_name']
        primary_color = config['primary_color']

        return f'''import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../utils/universal_level_system.dart';

class LevelSelectionScreen extends StatefulWidget {{
  const LevelSelectionScreen({{super.key}});

  @override
  State<LevelSelectionScreen> createState() => _LevelSelectionScreenState();
}}

class _LevelSelectionScreenState extends State<LevelSelectionScreen> {{
  int? selectedLevel;

  final List<UniversalUserLevel> levels = [
    const UniversalUserLevel(
      id: 1,
      title: "🥺 완전 초보자",
      subtitle: "{exercise_type}를 처음 시작해요",
      description: "기본 동작도\\n어려워해요",
      primaryStat: "입문자",
      secondaryStat: "기초 동작",
      chadLevel: "☕ 베이비 차드",
      workoutType: "기초 체력 형성",
      trainingFocus: "올바른 자세 학습",
      imagePath: "assets/images/커피차드.png",
      color: Color(0xFF8D6E63),
    ),
    const UniversalUserLevel(
      id: 2,
      title: "💪 운동 경험자",
      subtitle: "기본적인 운동은 해봤어요",
      description: "꾸준히는 아니지만\\n경험이 있어요",
      primaryStat: "경험자",
      secondaryStat: "기본 동작",
      chadLevel: "🥉 브론즈 차드",
      workoutType: "기본 근력 강화",
      trainingFocus: "체계적인 프로그레션",
      imagePath: "assets/images/정면차드.jpg",
      color: Color(0xFFCD7F32),
    ),
    const UniversalUserLevel(
      id: 3,
      title: "🔥 중급 트레이너",
      subtitle: "운동을 꾸준히 하고 있어요",
      description: "일정 수준의\\n실력을 갖추고 있어요",
      primaryStat: "중급자",
      secondaryStat: "안정적 수행",
      chadLevel: "💯 라이징 차드",
      workoutType: "강도 높은 훈련",
      trainingFocus: "한계 돌파와 근력 향상",
      imagePath: "assets/images/썬글차드.jpg",
      color: Color(0xFFFF6B35),
    ),
    const UniversalUserLevel(
      id: 4,
      title: "🚀 상급 아스리트",
      subtitle: "운동이 내 일상이에요",
      description: "고급 동작도\\n무리없이 할 수 있어요",
      primaryStat: "상급자",
      secondaryStat: "고급 동작",
      chadLevel: "🦾 스틸 차드",
      workoutType: "전문가 수준 훈련",
      trainingFocus: "극한 도전과 마스터리",
      imagePath: "assets/images/눈빔차드.jpg",
      color: Color(0xFF4A90E2),
    ),
    const UniversalUserLevel(
      id: 5,
      title: "👑 LEGENDARY CHAD",
      subtitle: "나는 이미 전설이다",
      description: "모든 변형을\\n완벽하게 마스터했어요",
      primaryStat: "전설급",
      secondaryStat: "모든 변형",
      chadLevel: "👑 레전드 차드",
      workoutType: "극한 훈련 프로그램",
      trainingFocus: "불가능을 가능으로",
      imagePath: "assets/images/더블차드.jpg",
      color: Color({primary_color.replace('#', '0xFF')}),
    ),
  ];

  @override
  Widget build(BuildContext context) {{
    return UniversalLevelSelectionScreen(
      appName: "{app_name}",
      exerciseType: "{exercise_type}",
      levels: levels,
      primaryColor: Color({primary_color.replace('#', '0xFF')}),
    );
  }}
}}'''

    def _generate_workout_data(self, config):
        """운동 데이터 생성"""
        exercise_type = config.get('exercise_type', 'exercise')
        max_target = config['max_target']
        unit = config['exercise_unit']

        return f'''/// {config['app_name']} 과학적 프로그레션 시스템
/// 초보자부터 전문가까지 모든 레벨 지원
class Scientific{config['package_name'].title()}Program {{

  /// 레벨별 시작 값 설정
  static Map<int, Map<String, dynamic>> get levelConfigs => {{
    1: {{ // 완전 초보자
      'startValue': {max_target // 20},
      'weeklyIncrease': 1.2,
      'maxSets': 5,
      'restSeconds': 120,
    }},
    2: {{ // 운동 경험자
      'startValue': {max_target // 10},
      'weeklyIncrease': 1.3,
      'maxSets': 6,
      'restSeconds': 90,
    }},
    3: {{ // 중급 트레이너
      'startValue': {max_target // 5},
      'weeklyIncrease': 1.4,
      'maxSets': 7,
      'restSeconds': 75,
    }},
    4: {{ // 상급 아스리트
      'startValue': {max_target // 3},
      'weeklyIncrease': 1.5,
      'maxSets': 8,
      'restSeconds': 60,
    }},
    5: {{ // 레전드 차드
      'startValue': {max_target // 2},
      'weeklyIncrease': 1.6,
      'maxSets': 10,
      'restSeconds': 45,
    }},
  }};

  /// 레벨과 주차에 따른 운동 생성
  static {config['package_name'].title()}Workout getWorkoutForLevel(int level, int week, int day) {{
    final levelConfig = levelConfigs[level] ?? levelConfigs[1]!;
    final startValue = levelConfig['startValue'] as int;
    final weeklyIncrease = levelConfig['weeklyIncrease'] as double;
    final maxSets = levelConfig['maxSets'] as int;
    final restSeconds = levelConfig['restSeconds'] as int;

    // 주차별 강도 증가
    final weekMultiplier = pow(weeklyIncrease, week - 1);
    final dailyBase = (startValue * weekMultiplier).round();

    // 세트 생성 (일별로 약간씩 다르게)
    final sets = _generateSetsForDay(dailyBase, maxSets, day);

    return {config['package_name'].title()}Workout(
      sets: sets,
      restSeconds: restSeconds,
      notes: _getNotesForLevel(level, week),
      exerciseType: _getExerciseTypeForLevel(level),
      chadLevel: _getChadLevelForLevel(level),
    );
  }}

  static List<int> _generateSetsForDay(int baseValue, int maxSets, int day) {{
    final sets = <int>[];
    final baseReps = baseValue ~/ maxSets;

    for (int i = 0; i < maxSets; i++) {{
      // 요일별 변화와 세트별 변화 적용
      final dayVariation = (day % 3 == 0) ? 1.1 : (day % 2 == 0) ? 0.9 : 1.0;
      final setVariation = (i == 1) ? 1.3 : (i == maxSets - 1) ? 1.2 : 1.0;

      final reps = (baseReps * dayVariation * setVariation).round();
      sets.add(reps.clamp(1, {max_target}));
    }}

    return sets;
  }}

  static String _getNotesForLevel(int level, int week) {{
    final notes = [
      "완벽한 자세에 집중하세요",
      "호흡을 일정하게 유지하세요",
      "근육의 움직임을 느끼세요",
      "한계를 조금씩 늘려가세요",
      "완전한 가동범위로 수행하세요",
    ];

    return notes[week % notes.length];
  }}

  static String _getExerciseTypeForLevel(int level) {{
    switch (level) {{
      case 1: return "기초 {exercise_type}";
      case 2: return "표준 {exercise_type}";
      case 3: return "강화 {exercise_type}";
      case 4: return "고급 {exercise_type}";
      case 5: return "극한 {exercise_type}";
      default: return "기본 {exercise_type}";
    }}
  }}

  static String _getChadLevelForLevel(int level) {{
    switch (level) {{
      case 1: return "☕ 베이비 차드";
      case 2: return "🥉 브론즈 차드";
      case 3: return "💯 라이징 차드";
      case 4: return "🦾 스틸 차드";
      case 5: return "👑 레전드 차드";
      default: return "💪 차드";
    }}
  }}
}}

class {config['package_name'].title()}Workout {{
  final List<int> sets;
  final int restSeconds;
  final String notes;
  final String exerciseType;
  final String chadLevel;

  const {config['package_name'].title()}Workout({{
    required this.sets,
    required this.restSeconds,
    required this.notes,
    required this.exerciseType,
    required this.chadLevel,
  }});

  int get totalReps => sets.fold(0, (sum, reps) => sum + reps);
}}'''

    def _update_pubspec(self, app_path, config):
        """pubspec.yaml 업데이트"""
        pubspec_path = app_path / "pubspec.yaml"

        pubspec_content = f'''name: {config['package_name']}
description: "{config['description']}"
publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: ^3.8.0

dependencies:
  flutter:
    sdk: flutter

  # Core dependencies
  cupertino_icons: ^1.0.8

  # 상태관리
  provider: ^6.1.2

  # 로컬 데이터베이스
  sqflite: ^2.3.0
  path: ^1.8.3

  # 로컬 저장소
  shared_preferences: ^2.2.2

  # UI/UX
  google_fonts: ^6.1.0

  # 날짜 처리
  intl: ^0.20.2

  # 알림 시스템
  flutter_local_notifications: ^17.2.3
  permission_handler: ^11.3.1
  timezone: ^0.9.2

  # 광고 (수익화)
  google_mobile_ads: ^5.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0

flutter:
  uses-material-design: true

  assets:
    - assets/images/
    - assets/data/
    - assets/config/
'''

        with open(pubspec_path, 'w', encoding='utf-8') as f:
            f.write(pubspec_content)

    def generate_all_apps(self):
        """모든 운동 앱 일괄 생성"""
        print("🚀 모든 운동 앱 일괄 생성 시작...")

        success_count = 0
        total_count = len(self.exercise_configs)

        for exercise_type in self.exercise_configs:
            print(f"\\n{'='*50}")
            print(f"🏋️‍♂️ {exercise_type.upper()} 앱 생성 중...")
            print(f"{'='*50}")

            if self.create_complete_app(exercise_type):
                success_count += 1
                print(f"✅ {exercise_type} 앱 생성 완료!")
            else:
                print(f"❌ {exercise_type} 앱 생성 실패!")

        print(f"\\n🎉 전체 결과: {success_count}/{total_count}개 앱 생성 완료!")

        if success_count == total_count:
            print("🔥 모든 앱이 성공적으로 생성되었습니다! 만삣삐! 🔥")
        else:
            print(f"⚠️ {total_count - success_count}개 앱 생성 실패. 로그를 확인해주세요.")

    def _update_main_dart(self, app_path, config):
        """main.dart 업데이트"""
        main_content = f'''import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'package:provider/provider.dart';
import 'screens/level_selection_screen.dart';
import 'screens/main_screen.dart';
import 'services/notification_service.dart';

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();
  await MobileAds.instance.initialize();
  await NotificationService.initialize();
  runApp(const {config['package_name'].title()}App());
}}

class {config['package_name'].title()}App extends StatelessWidget {{
  const {config['package_name'].title()}App({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{config['app_name']}',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF1A1A1A),
        primaryColor: Color({config['primary_color'].replace('#', '0xFF')}),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF2A2A2A),
          foregroundColor: Color({config['primary_color'].replace('#', '0xFF')}),
        ),
      ),
      home: const LevelSelectionScreen(),
      routes: {{
        '/home': (context) => const MainScreen(),
        '/level_selection': (context) => const LevelSelectionScreen(),
      }},
    );
  }}
}}'''

        main_dart_path = app_path / "lib" / "main.dart"
        with open(main_dart_path, 'w', encoding='utf-8') as f:
            f.write(main_content)

    def _create_app_info_file(self, app_path, config):
        """앱 정보 파일 생성"""
        app_info = {
            "app_name": config['app_name'],
            "korean_name": config['korean_name'],
            "package_name": config['package_name'],
            "description": config['description'],
            "exercise_type": config.get('exercise_type', 'general'),
            "primary_color": config['primary_color'],
            "chad_theme": config['chad_theme'],
            "difficulty_levels": config['difficulty_levels'],
            "max_target": config['max_target'],
            "exercise_unit": config['exercise_unit'],
            "features": [
                "초보자부터 전문가까지 5단계 레벨 시스템",
                "과학적 근거 기반 프로그레션",
                "개인 맞춤형 운동 프로그램",
                "Chad 레벨 진화 시스템",
                "스마트 알림 시스템",
                "특수 챌린지 프로그램",
                "상세한 진행상황 추적",
                "AdMob 광고 수익화"
            ],
            "special_features": config['special_features'],
            "generated_date": datetime.now().isoformat(),
            "generator_version": "2.0_with_levels"
        }

        info_file_path = app_path / "APP_INFO.json"
        with open(info_file_path, 'w', encoding='utf-8') as f:
            json.dump(app_info, f, ensure_ascii=False, indent=2)

def main():
    """메인 실행 함수"""
    print("🏋️‍♂️ 고급 피트니스 앱 생성기 v2.0 - 레벨 시스템 통합")
    print("초보자부터 전문가까지 모든 사용자를 위한 완전한 운동 앱")
    print("="*60)

    generator = EnhancedFitnessAppGenerator()

    print("\\n선택하세요:")
    print("1. 모든 운동 앱 일괄 생성")
    print("2. 특정 운동 앱 생성")
    print("3. 지원 운동 목록 보기")

    choice = input("\\n선택 (1-3): ").strip()

    if choice == "1":
        generator.generate_all_apps()
    elif choice == "2":
        print("\\n🏋️‍♂️ 지원 운동 목록:")
        for i, exercise_type in enumerate(generator.exercise_configs.keys(), 1):
            config = generator.exercise_configs[exercise_type]
            print(f"{i}. {exercise_type} - {config['app_name']}")

        try:
            exercise_choice = int(input("\\n생성할 운동 번호: ")) - 1
            exercise_types = list(generator.exercise_configs.keys())

            if 0 <= exercise_choice < len(exercise_types):
                selected_exercise = exercise_types[exercise_choice]
                generator.create_complete_app(selected_exercise)
            else:
                print("❌ 잘못된 선택입니다.")
        except ValueError:
            print("❌ 올바른 번호를 입력해주세요.")

    elif choice == "3":
        print("\\n🏋️‍♂️ 지원 운동 앱 목록:")
        print("="*50)
        for exercise_type, config in generator.exercise_configs.items():
            print(f"📱 {config['app_name']} ({config['korean_name']})")
            print(f"   - {config['description']}")
            print(f"   - 레벨: {config['difficulty_levels']}단계")
            print(f"   - 목표: {config['max_target']}{config['exercise_unit']}")
            print(f"   - 테마: {config['chad_theme']} Chad")
            print(f"   - 특수 기능: {', '.join(config['special_features'])}")
            print()

    else:
        print("❌ 잘못된 선택입니다.")

if __name__ == "__main__":
    main()