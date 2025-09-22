#!/usr/bin/env python3
"""
완전히 모듈화된 앱 팩토리 시스템
Mission100의 성공 요소들을 재사용 가능한 모듈로 분해
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

@dataclass
class AppConfig:
    """앱 설정 데이터 클래스"""
    app_name: str
    package_name: str
    exercise_type: str
    progression_type: str
    theme: Dict[str, Any]
    features: List[str]
    monetization: Dict[str, Any]
    scientific_basis: str
    target_goal: str

class ModularAppFactory:
    """모듈화된 앱 팩토리 메인 클래스"""

    def __init__(self):
        self.modules_dir = Path("modules")
        self.templates_dir = Path("templates")
        self.output_dir = Path("flutter_apps")
        self._ensure_directories()

    def _ensure_directories(self):
        """필요한 디렉토리 생성"""
        for dir_path in [self.modules_dir, self.templates_dir, self.output_dir]:
            dir_path.mkdir(exist_ok=True)

    def generate_app(self, config: AppConfig) -> bool:
        """설정 기반 앱 생성"""
        try:
            print(f"🚀 {config.app_name} 생성 시작...")

            # 1. 앱 디렉토리 생성
            app_dir = self._create_app_structure(config)

            # 2. 운동 데이터 모듈 생성
            self._generate_exercise_module(config, app_dir)

            # 3. 프로그레션 엔진 설정
            self._setup_progression_engine(config, app_dir)

            # 4. 테마 시스템 적용
            self._apply_theme_system(config, app_dir)

            # 5. UI 컴포넌트 조립
            self._assemble_ui_components(config, app_dir)

            # 6. 수익화 모듈 통합
            self._integrate_monetization(config, app_dir)

            # 7. 메인 앱 파일 생성
            self._generate_main_app(config, app_dir)

            # 8. pubspec.yaml 생성
            self._generate_pubspec(config, app_dir)

            print(f"✅ {config.app_name} 생성 완료!")
            return True

        except Exception as e:
            print(f"❌ {config.app_name} 생성 실패: {e}")
            return False

    def _create_app_structure(self, config: AppConfig) -> Path:
        """Flutter 앱 기본 구조 생성"""
        app_dir = self.output_dir / config.package_name.split('.')[-1]

        # 기본 Flutter 디렉토리 구조
        directories = [
            "lib", "lib/models", "lib/services", "lib/screens",
            "lib/widgets", "lib/utils", "lib/modules",
            "android/app/src/main", "assets/images", "test"
        ]

        for dir_name in directories:
            (app_dir / dir_name).mkdir(parents=True, exist_ok=True)

        return app_dir

    def _generate_exercise_module(self, config: AppConfig, app_dir: Path):
        """운동별 데이터 모듈 생성"""

        exercise_data = self._get_exercise_progression_data(config.exercise_type, config.progression_type)

        module_content = f'''import 'package:flutter/material.dart';
import '../models/user_profile.dart';

/// {config.app_name} 전용 운동 프로그레션 데이터
/// 과학적 근거: {config.scientific_basis}
class {config.exercise_type.title()}Data {{

  /// 레벨별 설명
  static Map<UserLevel, String> get levelDescriptions => {{
    UserLevel.rookie: '초보자 - 기본기 습득',
    UserLevel.rising: '중급자 - 실력 향상',
    UserLevel.alpha: '상급자 - 고급 기술',
    UserLevel.giga: '전문가 - 마스터 레벨',
  }};

  /// 6주 프로그레션 프로그램
  static Map<UserLevel, Map<int, Map<int, List<int>>>> get progressionPrograms => {{
{self._format_progression_data(exercise_data)}
  }};

  /// 레벨별 목표
  static Map<UserLevel, String> get goals => {{
    UserLevel.rookie: '{config.target_goal} (초보자)',
    UserLevel.rising: '{config.target_goal} (중급자)',
    UserLevel.alpha: '{config.target_goal} (상급자)',
    UserLevel.giga: '{config.target_goal} (전문가)',
  }};

  /// 휴식 시간 (초)
  static Map<UserLevel, int> get restTimeSeconds => {{
    UserLevel.rookie: 90,
    UserLevel.rising: 75,
    UserLevel.alpha: 60,
    UserLevel.giga: 45,
  }};

  /// 주간 포커스
  static Map<int, String> get weeklyFocus => {{
    1: '기본기 다지기',
    2: '자세 안정화',
    3: '볼륨 증가',
    4: '강도 상승',
    5: '고강도 적응',
    6: '최대 성능',
  }};
}}
''';

        exercise_file = app_dir / f"lib/utils/{config.exercise_type}_data.dart"
        with open(exercise_file, 'w', encoding='utf-8') as f:
            f.write(module_content)

    def _get_exercise_progression_data(self, exercise_type: str, progression_type: str) -> Dict:
        """운동 타입에 따른 프로그레션 데이터 생성"""

        base_progressions = {
            'plank': {
                'rookie': {
                    1: {1: [15, 20, 15, 15, 18], 2: [20, 25, 18, 18, 22], 3: [25, 30, 20, 20, 25]},
                    2: {1: [30, 40, 25, 25, 30], 2: [35, 45, 30, 30, 35], 3: [40, 50, 35, 35, 40]},
                    3: {1: [45, 60, 40, 40, 45], 2: [50, 65, 45, 45, 50], 3: [60, 75, 50, 50, 60]},
                    4: {1: [65, 85, 60, 60, 65], 2: [75, 95, 70, 70, 75], 3: [85, 105, 80, 80, 85]},
                    5: {1: [95, 120, 90, 90, 95], 2: [105, 135, 100, 100, 105], 3: [120, 150, 110, 110, 120]},
                    6: {1: [135, 180, 130, 130, 135], 2: [150, 200, 145, 145, 150], 3: [180, 240, 170, 170, 180]}
                }
            },
            'burpee': {
                'rookie': {
                    1: {1: [3, 5, 3, 3, 4], 2: [5, 8, 5, 5, 6], 3: [8, 12, 7, 7, 8]},
                    2: {1: [10, 15, 8, 8, 10], 2: [12, 18, 10, 10, 12], 3: [15, 20, 12, 12, 15]},
                    3: {1: [18, 25, 15, 15, 18], 2: [22, 30, 18, 18, 22], 3: [25, 35, 20, 20, 25]},
                    4: {1: [28, 40, 25, 25, 28], 2: [32, 45, 28, 28, 32], 3: [35, 50, 30, 30, 35]},
                    5: {1: [40, 55, 35, 35, 40], 2: [45, 60, 40, 40, 45], 3: [50, 65, 45, 45, 50]},
                    6: {1: [55, 75, 50, 50, 55], 2: [60, 80, 55, 55, 60], 3: [70, 90, 65, 65, 70]}
                }
            },
            'pullup': {
                'rookie': {
                    1: {1: [1, 2, 1, 1, 2], 2: [2, 3, 2, 2, 3], 3: [3, 5, 3, 3, 4]},
                    2: {1: [4, 6, 4, 4, 5], 2: [5, 7, 5, 5, 6], 3: [6, 8, 6, 6, 7]},
                    3: {1: [7, 10, 7, 7, 8], 2: [8, 12, 8, 8, 10], 3: [10, 14, 10, 10, 12]},
                    4: {1: [12, 16, 12, 12, 14], 2: [14, 18, 14, 14, 16], 3: [16, 20, 16, 16, 18]},
                    5: {1: [18, 24, 18, 18, 20], 2: [20, 26, 20, 20, 22], 3: [22, 28, 22, 22, 24]},
                    6: {1: [25, 32, 25, 25, 27], 2: [28, 35, 28, 28, 30], 3: [30, 40, 30, 30, 35]}
                }
            }
        }

        # 기본 데이터가 없으면 스쿼트 패턴 기반으로 생성
        if exercise_type not in base_progressions:
            return self._generate_default_progression(exercise_type)

        return base_progressions[exercise_type]

    def _generate_default_progression(self, exercise_type: str) -> Dict:
        """기본 프로그레션 패턴 생성"""
        # 스쿼트 패턴을 기반으로 다른 운동에 맞게 조정
        multiplier = {
            'lunge': 0.8,     # 런지는 스쿼트보다 약간 적게
            'jumping_jack': 2.0,  # 점핑잭은 더 많이
            'mountain_climber': 1.5,  # 마운틴 클라이머
        }.get(exercise_type, 1.0)

        base_data = {
            'rookie': {
                1: {1: [5, 8, 5, 5, 6], 2: [8, 12, 7, 7, 10], 3: [10, 15, 8, 8, 12]},
                2: {1: [12, 18, 10, 10, 14], 2: [15, 22, 12, 12, 16], 3: [18, 25, 15, 15, 20]},
                3: {1: [20, 30, 18, 18, 22], 2: [25, 35, 20, 20, 25], 3: [28, 40, 22, 22, 28]},
                4: {1: [30, 45, 25, 25, 30], 2: [35, 50, 28, 28, 35], 3: [40, 55, 30, 30, 40]},
                5: {1: [45, 65, 35, 35, 45], 2: [50, 70, 40, 40, 50], 3: [55, 75, 45, 45, 55]},
                6: {1: [60, 90, 50, 50, 60], 2: [65, 95, 55, 55, 65], 3: [70, 100, 60, 60, 70]}
            }
        }

        # multiplier 적용
        for level_data in base_data.values():
            for week_data in level_data.values():
                for day, sets in week_data.items():
                    week_data[day] = [int(rep * multiplier) for rep in sets]

        return base_data

    def _format_progression_data(self, data: Dict) -> str:
        """프로그레션 데이터를 Dart 코드 형식으로 포맷"""
        result = []

        for level, weeks in data.items():
            result.append(f"    UserLevel.{level}: {{")
            for week, days in weeks.items():
                result.append(f"      {week}: {{")
                for day, sets in days.items():
                    sets_str = str(sets).replace("'", "")
                    result.append(f"        {day}: {sets_str},")
                result.append("      },")
            result.append("    },")

        return '\n'.join(result)

    def _setup_progression_engine(self, config: AppConfig, app_dir: Path):
        """프로그레션 엔진 설정"""
        pass  # 이미 exercise module에서 처리됨

    def _apply_theme_system(self, config: AppConfig, app_dir: Path):
        """테마 시스템 적용"""

        theme_content = f'''import 'package:flutter/material.dart';

class {config.exercise_type.title()}Theme {{
  // {config.app_name} 전용 색상 팔레트
  static const Color primaryColor = Color({config.theme['primary_color_hex']});
  static const Color secondaryColor = Color({config.theme['secondary_color_hex']});
  static const Color backgroundColor = Color(0xFF1A1A1A);
  static const Color surfaceColor = Color(0xFF2A2A2A);

  static ThemeData get themeData => ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: backgroundColor,
    primaryColor: primaryColor,

    appBarTheme: AppBarTheme(
      backgroundColor: surfaceColor,
      foregroundColor: primaryColor,
      elevation: 0,
    ),

    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: primaryColor,
        foregroundColor: Colors.black,
        textStyle: TextStyle(fontWeight: FontWeight.bold),
      ),
    ),

    cardTheme: CardTheme(
      color: surfaceColor,
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
    ),
  );
}}
''';

        theme_file = app_dir / f"lib/utils/{config.exercise_type}_theme.dart"
        with open(theme_file, 'w', encoding='utf-8') as f:
            f.write(theme_content)

    def _assemble_ui_components(self, config: AppConfig, app_dir: Path):
        """UI 컴포넌트 조립"""
        pass  # 메인 앱에서 처리

    def _integrate_monetization(self, config: AppConfig, app_dir: Path):
        """수익화 모듈 통합"""
        pass  # 표준 AdMob 통합

    def _generate_main_app(self, config: AppConfig, app_dir: Path):
        """메인 앱 파일 생성"""

        main_content = f'''import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'utils/{config.exercise_type}_theme.dart';

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();
  await MobileAds.instance.initialize();
  runApp(const {config.exercise_type.title()}App());
}}

class {config.exercise_type.title()}App extends StatelessWidget {{
  const {config.exercise_type.title()}App({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{config.app_name}',
      debugShowCheckedModeBanner: false,
      theme: {config.exercise_type.title()}Theme.themeData,
      home: const {config.exercise_type.title()}HomeScreen(),
    );
  }}
}}

class {config.exercise_type.title()}HomeScreen extends StatefulWidget {{
  const {config.exercise_type.title()}HomeScreen({{super.key}});

  @override
  State<{config.exercise_type.title()}HomeScreen> createState() => _{config.exercise_type.title()}HomeScreenState();
}}

class _{config.exercise_type.title()}HomeScreenState extends State<{config.exercise_type.title()}HomeScreen> {{
  int currentWeek = 1;
  int currentDay = 1;

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('🏋️‍♂️ {config.app_name}'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    Text(
                      'Week $currentWeek - Day $currentDay',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: {config.exercise_type.title()}Theme.primaryColor,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      '{config.target_goal}을 향해!',
                      style: TextStyle(fontSize: 18),
                    ),
                  ],
                ),
              ),
            ),

            SizedBox(height: 20),

            Expanded(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      Text(
                        '오늘의 {config.exercise_type.title()} 프로그램',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 20),
                      Expanded(
                        child: Center(
                          child: Text(
                            '준비 중...',
                            style: TextStyle(fontSize: 18),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            SizedBox(height: 20),

            ElevatedButton(
              onPressed: () {{
                // TODO: 운동 시작 로직
              }},
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(horizontal: 48, vertical: 16),
              ),
              child: Text(
                '🔥 운동 시작하기',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      ),
    );
  }}
}}
''';

        main_file = app_dir / "lib/main.dart"
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_content)

    def _generate_pubspec(self, config: AppConfig, app_dir: Path):
        """pubspec.yaml 생성"""

        pubspec_content = f'''name: {config.package_name.split('.')[-1]}
description: {config.app_name} - 6주 프로그레션 챌린지

publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: ">=3.0.0"

dependencies:
  flutter:
    sdk: flutter
  google_mobile_ads: ^5.3.1
  shared_preferences: ^2.2.2
  sqflite: ^2.3.0
  fl_chart: ^0.66.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
''';

        pubspec_file = app_dir / "pubspec.yaml"
        with open(pubspec_file, 'w', encoding='utf-8') as f:
            f.write(pubspec_content)

def load_app_configs() -> List[AppConfig]:
    """앱 설정 파일들 로드"""

    configs = [
        AppConfig(
            app_name="Plank Champion",
            package_name="com.reaf.plankchampion",
            exercise_type="plank",
            progression_type="time_based",
            theme={"primary_color_hex": "0xFFFF6B35", "secondary_color_hex": "0xFF004E89"},
            features=["achievement_system", "progress_tracking"],
            monetization={"admob_strategy": "progressive_ads"},
            scientific_basis="core_strength_research",
            target_goal="5분 플랭크"
        ),

        AppConfig(
            app_name="Burpee Beast",
            package_name="com.reaf.burpeebeast",
            exercise_type="burpee",
            progression_type="rep_based",
            theme={"primary_color_hex": "0xFFE74C3C", "secondary_color_hex": "0xFF2C3E50"},
            features=["achievement_system", "progress_tracking"],
            monetization={"admob_strategy": "progressive_ads"},
            scientific_basis="hiit_cardio_research",
            target_goal="100개 버피"
        ),

        AppConfig(
            app_name="Pull-up Pro",
            package_name="com.reaf.pulluppro",
            exercise_type="pullup",
            progression_type="rep_based",
            theme={"primary_color_hex": "0xFF3498DB", "secondary_color_hex": "0xFF34495E"},
            features=["achievement_system", "progress_tracking"],
            monetization={"admob_strategy": "progressive_ads"},
            scientific_basis="upper_body_strength_research",
            target_goal="50개 턱걸이"
        ),

        AppConfig(
            app_name="Lunge Legend",
            package_name="com.reaf.lungelegend",
            exercise_type="lunge",
            progression_type="rep_based",
            theme={"primary_color_hex": "0xFF2ECC71", "secondary_color_hex": "0xFF27AE60"},
            features=["achievement_system", "progress_tracking"],
            monetization={"admob_strategy": "progressive_ads"},
            scientific_basis="lower_body_strength_research",
            target_goal="150개 런지"
        ),

        AppConfig(
            app_name="Jumping Jack Jedi",
            package_name="com.reaf.jumpingjackjedi",
            exercise_type="jumping_jack",
            progression_type="rep_based",
            theme={"primary_color_hex": "0xFF9B59B6", "secondary_color_hex": "0xFF8E44AD"},
            features=["achievement_system", "progress_tracking"],
            monetization={"admob_strategy": "progressive_ads"},
            scientific_basis="cardio_fitness_research",
            target_goal="500개 점핑잭"
        ),
    ]

    return configs

def main():
    """메인 실행 함수"""
    print("🏗️ 모듈화된 앱 팩토리 시작...")
    print("=" * 60)

    factory = ModularAppFactory()
    configs = load_app_configs()

    print(f"📱 {len(configs)}개 앱 생성 예정:")
    for config in configs:
        print(f"  • {config.app_name} ({config.exercise_type})")

    print("\n🚀 배치 생성 시작...")

    # 병렬 생성
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(factory.generate_app, config) for config in configs]
        results = [future.result() for future in futures]

    success_count = sum(results)
    print(f"\n" + "=" * 60)
    print(f"✅ {success_count}/{len(configs)}개 앱 생성 완료!")

    if success_count > 0:
        print("\n🔄 다음 단계:")
        print("1. cd flutter_apps/[앱이름]")
        print("2. flutter pub get")
        print("3. flutter run")

if __name__ == "__main__":
    main()