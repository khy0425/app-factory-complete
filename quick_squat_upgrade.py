#!/usr/bin/env python3
"""
Squat Master 빠른 업그레이드 스크립트
"""

import os
import shutil
from pathlib import Path

def create_squat_main():
    """새로운 main.dart 생성"""
    main_content = '''import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await MobileAds.instance.initialize();
  runApp(const SquatMasterApp());
}

class SquatMasterApp extends StatelessWidget {
  const SquatMasterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Squat Master - 6주 스쿼트 챌린지',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF1A1A1A),
        primaryColor: const Color(0xFFFFD700), // 골드 옐로우
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF2A2A2A),
          foregroundColor: Color(0xFFFFD700),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFFFFD700),
            foregroundColor: Colors.black,
            textStyle: const TextStyle(fontWeight: FontWeight.bold),
          ),
        ),
      ),
      home: const SquatHomeScreen(),
    );
  }
}

class SquatHomeScreen extends StatefulWidget {
  const SquatHomeScreen({super.key});

  @override
  State<SquatHomeScreen> createState() => _SquatHomeScreenState();
}

class _SquatHomeScreenState extends State<SquatHomeScreen> {
  int currentWeek = 1;
  int currentDay = 1;

  // 6주 스쿼트 프로그레션 데이터
  final Map<int, Map<int, List<int>>> squatProgram = {
    1: { // Week 1
      1: [5, 8, 5, 5, 6],    // 29개
      2: [8, 12, 7, 7, 10],  // 44개
      3: [10, 15, 8, 8, 12], // 53개
    },
    2: { // Week 2
      1: [12, 18, 10, 10, 14],
      2: [15, 22, 12, 12, 16],
      3: [18, 25, 15, 15, 20],
    },
    3: { // Week 3
      1: [20, 30, 18, 18, 22],
      2: [25, 35, 20, 20, 25],
      3: [28, 40, 22, 22, 28],
    },
    4: { // Week 4
      1: [30, 45, 25, 25, 30],
      2: [35, 50, 28, 28, 35],
      3: [40, 55, 30, 30, 40],
    },
    5: { // Week 5
      1: [45, 65, 35, 35, 45],
      2: [50, 70, 40, 40, 50, 55],
      3: [55, 75, 45, 45, 55, 60],
    },
    6: { // Week 6 - 스쿼트 마스터!
      1: [60, 90, 50, 50, 60],
      2: [65, 95, 55, 55, 65, 70, 75],
      3: [70, 100, 60, 60, 70, 75, 80], // 총 515개!
    },
  };

  List<int> getCurrentWorkout() {
    return squatProgram[currentWeek]?[currentDay] ?? [5, 8, 5, 5, 6];
  }

  int getTotalReps() {
    return getCurrentWorkout().fold(0, (sum, reps) => sum + reps);
  }

  @override
  Widget build(BuildContext context) {
    final workout = getCurrentWorkout();
    final totalReps = getTotalReps();

    return Scaffold(
      appBar: AppBar(
        title: const Text('🏋️‍♀️ Squat Master'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // 주차 및 일차 표시
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    Text(
                      '주차 $currentWeek - 일차 $currentDay',
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFFFFD700),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '총 $totalReps개 스쿼트',
                      style: const TextStyle(fontSize: 18),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),

            // 운동 세트 표시
            Expanded(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '오늘의 스쿼트 세트:',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 16),

                      Expanded(
                        child: ListView.builder(
                          itemCount: workout.length,
                          itemBuilder: (context, index) {
                            return Container(
                              margin: const EdgeInsets.only(bottom: 12),
                              padding: const EdgeInsets.all(16),
                              decoration: BoxDecoration(
                                color: const Color(0xFF3A3A3A),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(
                                  color: const Color(0xFFFFD700),
                                  width: 2,
                                ),
                              ),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    '세트 ${index + 1}',
                                    style: const TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  Text(
                                    '${workout[index]}개',
                                    style: const TextStyle(
                                      fontSize: 24,
                                      fontWeight: FontWeight.bold,
                                      color: Color(0xFFFFD700),
                                    ),
                                  ),
                                ],
                              ),
                            );
                          },
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

            const SizedBox(height: 20),

            // 컨트롤 버튼들
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: currentDay > 1 ? () {
                      setState(() {
                        if (currentDay > 1) {
                          currentDay--;
                        } else if (currentWeek > 1) {
                          currentWeek--;
                          currentDay = 3;
                        }
                      });
                    } : null,
                    child: const Text('◀ 이전'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => WorkoutScreen(
                            week: currentWeek,
                            day: currentDay,
                            workout: workout,
                          ),
                        ),
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFFF6B00),
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: const Text(
                      '🔥 시작하기',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: ElevatedButton(
                    onPressed: (currentWeek < 6 || currentDay < 3) ? () {
                      setState(() {
                        if (currentDay < 3) {
                          currentDay++;
                        } else if (currentWeek < 6) {
                          currentWeek++;
                          currentDay = 1;
                        }
                      });
                    } : null,
                    child: const Text('다음 ▶'),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 20),

            // 진행 상황
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    const Text(
                      '6주 챌린지 진행상황',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    LinearProgressIndicator(
                      value: ((currentWeek - 1) * 3 + currentDay) / 18,
                      backgroundColor: Colors.grey[700],
                      valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFFFD700)),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${((currentWeek - 1) * 3 + currentDay)} / 18 일 완료',
                      style: const TextStyle(fontSize: 12),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class WorkoutScreen extends StatefulWidget {
  final int week;
  final int day;
  final List<int> workout;

  const WorkoutScreen({
    super.key,
    required this.week,
    required this.day,
    required this.workout,
  });

  @override
  State<WorkoutScreen> createState() => _WorkoutScreenState();
}

class _WorkoutScreenState extends State<WorkoutScreen> {
  int currentSet = 0;
  bool isResting = false;
  int restTime = 60;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.week}주차 ${widget.day}일차'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (currentSet < widget.workout.length) ...[
              Text(
                '세트 ${currentSet + 1}',
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              Text(
                '${widget.workout[currentSet]}',
                style: const TextStyle(
                  fontSize: 72,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFFFFD700),
                ),
              ),
              const Text(
                '개 스쿼트',
                style: TextStyle(fontSize: 24),
              ),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    if (currentSet < widget.workout.length - 1) {
                      currentSet++;
                      isResting = true;
                      // 여기서 휴식 타이머 시작 가능
                    } else {
                      // 운동 완료
                      Navigator.pop(context);
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('🎉 오늘 운동 완료! 수고하셨습니다!'),
                          backgroundColor: Color(0xFFFFD700),
                        ),
                      );
                    }
                  });
                },
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 16),
                  backgroundColor: const Color(0xFF4CAF50),
                ),
                child: Text(
                  currentSet < widget.workout.length - 1 ? '완료 ✅' : '마지막 세트 완료! 🎉',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ),
            ],

            if (isResting && currentSet < widget.workout.length) ...[
              const SizedBox(height: 40),
              const Text(
                '휴식 시간',
                style: TextStyle(fontSize: 20, color: Color(0xFFFF9800)),
              ),
              Text(
                '$restTime초',
                style: const TextStyle(fontSize: 48, color: Color(0xFFFF9800)),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    isResting = false;
                  });
                },
                child: const Text('휴식 완료'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
''';

    main_path = Path("flutter_apps/squat_master/lib/main.dart")
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(main_content)

    print(f"✅ Created new main.dart: {main_path}")

def main():
    print("🚀 Quick Squat Master upgrade starting...")

    try:
        create_squat_main()
        print("\n✅ Squat Master upgrade completed!")
        print("\nNext steps:")
        print("1. cd flutter_apps/squat_master")
        print("2. flutter pub get")
        print("3. flutter run")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()