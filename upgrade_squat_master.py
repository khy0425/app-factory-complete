#!/usr/bin/env python3
"""
Squat Master를 Mission100 스타일로 업그레이드하는 자동화 스크립트
"""

import os
import shutil
import re
from pathlib import Path

def copy_mission100_structure():
    """Mission100의 핵심 구조를 Squat Master에 복사"""

    mission100_path = Path("flutter_apps/mission100_v3")
    squat_master_path = Path("flutter_apps/squat_master")

    # 필수 디렉토리 생성
    required_dirs = [
        "lib/models",
        "lib/services",
        "lib/utils",
        "lib/widgets",
        "lib/screens",
        "lib/generated"
    ]

    for dir_path in required_dirs:
        full_path = squat_master_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {full_path}")

def copy_core_files():
    """핵심 파일들 복사 및 스쿼트에 맞게 수정"""

    mission100 = Path("flutter_apps/mission100_v3/lib")
    squat_master = Path("flutter_apps/squat_master/lib")

    # 복사할 파일 목록
    files_to_copy = [
        # Models
        ("models/user_profile.dart", "models/user_profile.dart"),
        ("models/workout_session.dart", "models/workout_session.dart"),
        ("models/achievement.dart", "models/achievement.dart"),
        ("models/workout_history.dart", "models/workout_history.dart"),

        # Services
        ("services/database_service.dart", "services/database_service.dart"),
        ("services/achievement_service.dart", "services/achievement_service.dart"),
        ("services/workout_program_service.dart", "services/workout_program_service.dart"),
        ("services/workout_history_service.dart", "services/workout_history_service.dart"),
        ("services/theme_service.dart", "services/theme_service.dart"),
        ("services/ad_service.dart", "services/ad_service.dart"),
        ("services/notification_service.dart", "services/notification_service.dart"),

        # Utils
        ("utils/constants.dart", "utils/constants.dart"),

        # Widgets
        ("widgets/ad_banner_widget.dart", "widgets/ad_banner_widget.dart"),
        ("widgets/achievement_badge.dart", "widgets/achievement_badge.dart"),
    ]

    for src, dst in files_to_copy:
        src_path = mission100 / src
        dst_path = squat_master / dst

        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"✅ Copied: {src} → {dst}")
        else:
            print(f"❌ Source file not found: {src_path}")

def create_squat_workout_data():
    """스쿼트 전용 워크아웃 데이터 생성"""

    squat_data_content = '''import 'package:flutter/material.dart';
import '../models/user_profile.dart';
import '../generated/app_localizations.dart';

class WorkoutData {
  // 6주 스쿼트 프로그램 데이터
  static Map<UserLevel, Map<int, Map<int, List<int>>>> get workoutPrograms => {
    // 초급 레벨 (Rookie Chad) - 스쿼트는 팔굽혀펴기보다 더 많이 가능
    UserLevel.rookie: {
      1: {
        // Week 1
        1: [5, 8, 5, 5, 6],    // Day 1: 29개
        2: [8, 12, 7, 7, 10],  // Day 2: 44개
        3: [10, 15, 8, 8, 12], // Day 3: 53개
      },
      2: {
        // Week 2
        1: [12, 18, 10, 10, 14],
        2: [15, 22, 12, 12, 16],
        3: [18, 25, 15, 15, 20],
      },
      3: {
        // Week 3
        1: [20, 30, 18, 18, 22],
        2: [25, 35, 20, 20, 25],
        3: [28, 40, 22, 22, 28],
      },
      4: {
        // Week 4
        1: [30, 45, 25, 25, 30],
        2: [35, 50, 28, 28, 35],
        3: [40, 55, 30, 30, 40],
      },
      5: {
        // Week 5
        1: [45, 65, 35, 35, 45],
        2: [50, 70, 40, 40, 50, 55], // 6세트
        3: [55, 75, 45, 45, 55, 60], // 6세트
      },
      6: {
        // Week 6 - 스쿼트 마스터 달성!
        1: [60, 90, 50, 50, 60],
        2: [65, 95, 55, 55, 65, 70, 75], // 7세트
        3: [70, 100, 60, 60, 70, 75, 80], // 7세트 (총 515개!)
      },
    },

    // 중급 레벨 (Rising Chad)
    UserLevel.rising: {
      1: {
        1: [10, 15, 8, 8, 12],   // 53개
        2: [15, 20, 12, 12, 16], // 75개
        3: [18, 25, 15, 15, 20], // 93개
      },
      2: {
        1: [20, 30, 18, 18, 22],
        2: [25, 35, 20, 20, 25],
        3: [30, 40, 25, 25, 30],
      },
      3: {
        1: [35, 50, 30, 30, 35],
        2: [40, 55, 35, 35, 40],
        3: [45, 60, 40, 40, 45],
      },
      4: {
        1: [50, 70, 45, 45, 50],
        2: [55, 75, 50, 50, 55],
        3: [60, 80, 55, 55, 60],
      },
      5: {
        1: [65, 90, 60, 60, 65],
        2: [70, 95, 65, 65, 70, 75],
        3: [75, 100, 70, 70, 75, 80],
      },
      6: {
        1: [80, 110, 75, 75, 80],
        2: [85, 115, 80, 80, 85, 90, 95],
        3: [90, 120, 85, 85, 90, 95, 100], // 총 665개!
      },
    },

    // 고급 레벨 (Alpha Chad)
    UserLevel.alpha: {
      1: {
        1: [20, 30, 15, 15, 20],  // 100개
        2: [25, 35, 20, 20, 25],  // 125개
        3: [30, 40, 25, 25, 30],  // 150개
      },
      2: {
        1: [35, 50, 30, 30, 35],
        2: [40, 55, 35, 35, 40],
        3: [45, 60, 40, 40, 45],
      },
      3: {
        1: [50, 70, 45, 45, 50],
        2: [55, 75, 50, 50, 55],
        3: [60, 80, 55, 55, 60],
      },
      4: {
        1: [65, 90, 60, 60, 65],
        2: [70, 95, 65, 65, 70],
        3: [75, 100, 70, 70, 75],
      },
      5: {
        1: [80, 110, 75, 75, 80],
        2: [85, 115, 80, 80, 85, 90],
        3: [90, 120, 85, 85, 90, 95],
      },
      6: {
        1: [100, 140, 95, 95, 100],
        2: [105, 145, 100, 100, 105, 110, 115],
        3: [110, 150, 105, 105, 110, 115, 120], // 총 815개!
      },
    },

    // 마스터 레벨 (Giga Chad)
    UserLevel.giga: {
      1: {
        1: [40, 60, 30, 30, 40],  // 200개
        2: [50, 70, 40, 40, 50],  // 250개
        3: [60, 80, 50, 50, 60],  // 300개
      },
      2: {
        1: [70, 90, 60, 60, 70],
        2: [80, 100, 70, 70, 80],
        3: [90, 110, 80, 80, 90],
      },
      3: {
        1: [100, 130, 90, 90, 100],
        2: [110, 140, 100, 100, 110],
        3: [120, 150, 110, 110, 120],
      },
      4: {
        1: [130, 170, 120, 120, 130],
        2: [140, 180, 130, 130, 140],
        3: [150, 190, 140, 140, 150],
      },
      5: {
        1: [160, 210, 150, 150, 160],
        2: [170, 220, 160, 160, 170, 180],
        3: [180, 230, 170, 170, 180, 190],
      },
      6: {
        1: [200, 270, 190, 190, 200],
        2: [210, 280, 200, 200, 210, 220, 230],
        3: [220, 290, 210, 210, 220, 230, 240], // 총 1620개!
      },
    },
  };

  // 레벨별 휴식 시간 (초)
  static Map<UserLevel, int> get restTimeSeconds => {
    UserLevel.rookie: 90,  // 스쿼트는 더 긴 휴식 필요
    UserLevel.rising: 75,
    UserLevel.alpha: 60,
    UserLevel.giga: 45,
  };

  // 워크아웃 가져오기
  static List<int>? getWorkout(UserLevel level, int week, int day) {
    return workoutPrograms[level]?[week]?[day];
  }

  // 총 횟수 계산
  static int getTotalReps(List<int> workout) {
    return workout.fold(0, (sum, reps) => sum + reps);
  }

  // 주간 총 운동량 계산
  static int getWeeklyTotal(UserLevel level, int week) {
    final weekData = workoutPrograms[level]?[week];
    if (weekData == null) return 0;

    int total = 0;
    for (int day = 1; day <= 3; day++) {
      final workout = weekData[day];
      if (workout != null) {
        total += getTotalReps(workout);
      }
    }
    return total;
  }

  // 전체 프로그램 총 운동량 계산
  static int getProgramTotal(UserLevel level) {
    int total = 0;
    for (int week = 1; week <= 6; week++) {
      total += getWeeklyTotal(level, week);
    }
    return total;
  }

  // 레벨별 목표 메시지
  static String getGoalMessage(UserLevel level, BuildContext context) {
    final isKorean = Localizations.localeOf(context).languageCode == 'ko';

    switch (level) {
      case UserLevel.rookie:
        return isKorean ? '6주 후 515개 스쿼트 마스터!' : 'Master 515 squats in 6 weeks!';
      case UserLevel.rising:
        return isKorean ? '6주 후 665개 스쿼트 챔피언!' : 'Champion 665 squats in 6 weeks!';
      case UserLevel.alpha:
        return isKorean ? '6주 후 815개 스쿼트 알파!' : 'Alpha 815 squats in 6 weeks!';
      case UserLevel.giga:
        return isKorean ? '6주 후 1620개 스쿼트 기가차드!' : 'GigaChad 1620 squats in 6 weeks!';
    }
  }
}
''';

    squat_data_path = Path("flutter_apps/squat_master/lib/utils/workout_data.dart")
    with open(squat_data_path, 'w', encoding='utf-8') as f:
        f.write(squat_data_content)

    print(f"✅ Created Squat workout data: {squat_data_path}")

def update_squat_theme():
    """스쿼트 전용 옐로우/블랙 테마 생성"""

    theme_content = '''import 'package:flutter/material.dart';

class SquatTheme {
  // 스쿼트 전용 색상 팔레트 (Yellow & Black)
  static const Color primaryYellow = Color(0xFFFFD700);    // 골드 옐로우
  static const Color accentYellow = Color(0xFFFFA500);     // 오렌지 옐로우
  static const Color darkBlack = Color(0xFF1A1A1A);        // 딥 블랙
  static const Color charcoalGray = Color(0xFF2A2A2A);     // 차콜 그레이
  static const Color lightGray = Color(0xFF3A3A3A);        // 라이트 그레이

  // 상태별 색상
  static const Color successGreen = Color(0xFF4CAF50);
  static const Color warningOrange = Color(0xFFFF9800);
  static const Color errorRed = Color(0xFFF44336);

  static ThemeData get themeData => ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: darkBlack,

    // AppBar 테마
    appBarTheme: AppBarTheme(
      backgroundColor: charcoalGray,
      foregroundColor: primaryYellow,
      elevation: 0,
      titleTextStyle: TextStyle(
        color: primaryYellow,
        fontSize: 20,
        fontWeight: FontWeight.bold,
      ),
      iconTheme: IconThemeData(color: primaryYellow),
    ),

    // 버튼 테마
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: primaryYellow,
        foregroundColor: darkBlack,
        textStyle: TextStyle(
          fontWeight: FontWeight.bold,
          fontSize: 16,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    ),

    // 카드 테마
    cardTheme: CardTheme(
      color: charcoalGray,
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
    ),

    // 텍스트 테마
    textTheme: TextTheme(
      headlineLarge: TextStyle(color: primaryYellow, fontWeight: FontWeight.bold),
      headlineMedium: TextStyle(color: primaryYellow, fontWeight: FontWeight.w600),
      bodyLarge: TextStyle(color: Colors.white),
      bodyMedium: TextStyle(color: Colors.white70),
    ),

    // 프로그레스 인디케이터
    progressIndicatorTheme: ProgressIndicatorThemeData(
      color: primaryYellow,
    ),

    // 아이콘 테마
    iconTheme: IconThemeData(
      color: primaryYellow,
    ),
  );

  // Chad 진화별 색상
  static Color getChadLevelColor(int level) {
    switch (level) {
      case 0: return Colors.grey;
      case 1: return accentYellow;
      case 2: return primaryYellow;
      case 3: return Color(0xFFFFE55C);
      case 4: return Color(0xFFFFEC8C);
      case 5: return Color(0xFFFFF3B8);
      case 6: return Color(0xFFFFFAE4);
      default: return primaryYellow;
    }
  }

  // 운동 강도별 색상
  static Color getIntensityColor(double intensity) {
    if (intensity >= 0.8) return errorRed;       // 고강도
    if (intensity >= 0.6) return warningOrange;  // 중강도
    if (intensity >= 0.4) return accentYellow;   // 중저강도
    return successGreen;                         // 저강도
  }
}
''';

    theme_path = Path("flutter_apps/squat_master/lib/utils/squat_theme.dart")
    with open(theme_path, 'w', encoding='utf-8') as f:
        f.write(theme_content)

    print(f"✅ Created Squat theme: {theme_path}")

def update_main_dart():
    """main.dart를 Mission100 스타일로 업데이트"""

    main_content = '''import 'package:flutter/material.dart';
import 'package:sqflite/sqflite.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'services/database_service.dart';
import 'services/ad_service.dart';
import 'services/theme_service.dart';
import 'utils/squat_theme.dart';
import 'screens/splash_screen.dart';
import 'screens/main_navigation_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // AdMob 초기화
  await MobileAds.instance.initialize();

  // 데이터베이스 초기화
  await DatabaseService().initDatabase();

  // 광고 미리 로드
  AdService().loadInterstitialAd();

  runApp(const SquatMasterApp());
}

class SquatMasterApp extends StatelessWidget {
  const SquatMasterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Squat Master - 6주 스쿼트 마스터',
      debugShowCheckedModeBanner: false,
      theme: SquatTheme.themeData,
      home: const SplashScreen(),
      routes: {
        '/main': (context) => const MainNavigationScreen(),
      },
    );
  }
}
''';

    main_path = Path("flutter_apps/squat_master/lib/main.dart")
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(main_content)

    print(f"✅ Updated main.dart: {main_path}")

def update_pubspec_yaml():
    """pubspec.yaml에 필요한 의존성 추가"""

    pubspec_path = Path("flutter_apps/squat_master/pubspec.yaml")

    if pubspec_path.exists():
        with open(pubspec_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 필요한 의존성들이 없으면 추가
        dependencies_to_add = [
            "sqflite: ^2.3.0",
            "google_mobile_ads: ^5.3.1",
            "shared_preferences: ^2.2.2",
            "fl_chart: ^0.66.2",
            "table_calendar: ^3.0.9",
            "confetti: ^0.7.0",
        ]

        for dep in dependencies_to_add:
            if dep.split(':')[0].strip() not in content:
                # dependencies 섹션 찾아서 추가
                if 'dependencies:' in content:
                    content = content.replace(
                        'dependencies:',
                        f'dependencies:\\n  {dep}'
                    )

        with open(pubspec_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated pubspec.yaml with dependencies")

def main():
    """메인 업그레이드 실행"""

    print("🚀 Starting Squat Master upgrade to Mission100 style...")
    print("=" * 60)

    try:
        # 1. 디렉토리 구조 생성
        print("\\n📁 Step 1: Creating directory structure...")
        copy_mission100_structure()

        # 2. 핵심 파일 복사
        print("\\n📋 Step 2: Copying core files...")
        copy_core_files()

        # 3. 스쿼트 전용 데이터 생성
        print("\\n🏋️‍♀️ Step 3: Creating squat workout data...")
        create_squat_workout_data()

        # 4. 테마 생성
        print("\\n🎨 Step 4: Creating squat theme...")
        update_squat_theme()

        # 5. main.dart 업데이트
        print("\\n🔧 Step 5: Updating main.dart...")
        update_main_dart()

        # 6. pubspec.yaml 업데이트
        print("\\n📦 Step 6: Updating dependencies...")
        update_pubspec_yaml()

        print("\\n" + "=" * 60)
        print("✅ Squat Master upgrade completed successfully!")
        print("\\n🔄 Next steps:")
        print("1. cd flutter_apps/squat_master")
        print("2. flutter pub get")
        print("3. flutter run")

    except Exception as e:
        print(f"\\n❌ Error during upgrade: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    main()
''';

if __name__ == "__main__":
    main()