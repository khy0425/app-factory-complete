# stepup 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** com.reaf.stepup
- **필요한 dependencies:** (pubspec.yaml)

```yaml
name: stepup
description: A new Flutter project.
publish_to: 'none' # Remove this line if you wish to publish to pub.dev

version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.17.0
  sqflite: ^2.0.2+1
  path_provider: ^2.0.11
  charts_flutter: ^0.13.0
  permission_handler: ^10.0.0
  flutter_local_notifications: ^11.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
  generate: true
```

- **폴더 구조:** (lib 폴더 내부)

```
lib/
├── main.dart
├── models/
│   ├── step_data.dart
│   └── user_profile.dart
├── services/
│   ├── database_helper.dart
│   ├── step_counter.dart
│   └── notification_service.dart
├── ui/
│   ├── home_screen.dart
│   ├── history_screen.dart
│   ├── settings_screen.dart
│   └── widgets/  // 공통 위젯들
├── utils/
│   ├── constants.dart
│   └── helpers.dart
└── main_app.dart
```


## 화면별 구현 상세

**1. 홈 화면 (home_screen.dart):**

- **위젯 구조:** `Scaffold`  > `AppBar` > `Column` (오늘의 계단 수, 목표 달성률, 칼로리, 거리 표시) > `ElevatedButton` (목표 설정, 기록 확인) > `charts_flutter` (차트)
- **상태 관리 방식:** `Provider` 또는 `Riverpod` (데이터 변경 감지 및 업데이트 용이)
- **필요한 패키지들:** `flutter`, `provider` (or `riverpod`), `charts_flutter`

**2. 기록 화면 (history_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `charts_flutter` (일별, 주별, 월별 차트) > `ListView` (상세 기록)
- **상태 관리 방식:** `Provider` 또는 `Riverpod`
- **필요한 패키지들:** `flutter`, `provider` (or `riverpod`), `charts_flutter`, `intl` (날짜 포맷)

**3. 설정 화면 (settings_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `ListView` (키, 몸무게 입력 필드, 알림 설정 토글, 단위 선택, 앱 정보)
- **상태 관리 방식:** `Provider` 또는 `Riverpod`
- **필요한 패키지들:** `flutter`, `provider` (or `riverpod`)


## 데이터 모델

- **step_data.dart:**
```dart
class StepData {
  final DateTime date;
  final int steps;
  final double calories;
  final double distance;

  StepData({required this.date, required this.steps, required this.calories, required this.distance});

  Map<String, dynamic> toMap() {
    return {
      'date': date.toIso8601String(),
      'steps': steps,
      'calories': calories,
      'distance': distance,
    };
  }

  factory StepData.fromMap(Map<String, dynamic> map) {
    return StepData(
      date: DateTime.parse(map['date']),
      steps: map['steps'],
      calories: map['calories'],
      distance: map['distance'],
    );
  }
}
```

- **user_profile.dart:**
```dart
class UserProfile {
  double height;
  double weight;
  int dailyGoal; // 추가

  UserProfile({this.height = 0, this.weight = 0, this.dailyGoal = 10000});

  Map<String, dynamic> toMap() {
    return {
      'height': height,
      'weight': weight,
      'dailyGoal': dailyGoal,
    };
  }

  factory UserProfile.fromMap(Map<String, dynamic> map) {
    return UserProfile(
      height: map['height'],
      weight: map['weight'],
      dailyGoal: map['dailyGoal'],
    );
  }
}
```

- **데이터베이스 스키마 (sqflite):**

```sql
CREATE TABLE step_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  steps INTEGER NOT NULL,
  calories REAL NOT NULL,
  distance REAL NOT NULL
);

CREATE TABLE user_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  height REAL NOT NULL,
  weight REAL NOT NULL,
  dailyGoal INTEGER NOT NULL
);
```

- **API 연동 방식:**  MVP는 로컬 DB만 사용.


## 권한 및 설정

- **android/app/src/main/AndroidManifest.xml:**

```xml
<uses-permission android:name="android.permission.ACTIVITY_RECOGNITION" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/> <!-- 백그라운드 계측을 위한 권한 -->
```

- **iOS 권한 설정:**  Info.plist에 `NSMotionUsageDescription` 추가 (사용자에게 가속도계 사용 이유 설명).


## 핵심 기능 구현 방법

**1. 계단 수 자동 카운팅:**

- **사용할 Flutter 패키지:** `sensors_plus` (권장)
- **구현 난이도:** 4/5 (정확도 향상 알고리즘 구현이 어려움)
- **예상 개발 시간:** 40시간 (알고리즘 개발 및 테스트 포함)

**2. 목표 설정 및 관리:**

- **사용할 Flutter 패키지:**  `flutter` (내장 위젯 사용)
- **구현 난이도:** 2/5
- **예상 개발 시간:** 16시간

**3. 칼로리 및 거리 계산:**

- **사용할 Flutter 패키지:**  `flutter` (내장 계산 기능 사용)
- **구현 난이도:** 2/5
- **예상 개발 시간:** 8시간

**4. 로컬 데이터베이스:**

- **사용할 Flutter 패키지:** `sqflite`, `path_provider`
- **구현 난이도:** 3/5
- **예상 개발 시간:** 24시간

**5. 알림 기능:**

- **사용할 Flutter 패키지:** `flutter_local_notifications`
- **구현 난이도:** 3/5
- **예상 개발 시간:** 16시간


## 테스트 계획

- **단위 테스트 대상:**  `StepCounter` 클래스, 데이터 모델 클래스들,  데이터베이스 헬퍼 클래스
- **통합 테스트 시나리오:**  계단 카운팅 정확도 테스트,  목표 달성 알림 테스트,  데이터 저장 및 로딩 테스트
- **사용자 테스트 계획:**  다양한 사용 환경(계단 높이, 걷는 속도)에서의 계단 카운팅 정확도 검증, UI/UX 사용성 테스트


**참고:**  계단 카운팅 알고리즘은 정확도를 높이기 위해 머신러닝 기반 접근 방식을 고려할 수 있습니다.  하지만 MVP 단계에서는 간단한 가속도 변화 감지 알고리즘을 먼저 구현하고,  사용자 피드백을 바탕으로 개선하는 것이 좋습니다.  배터리 최적화를 위해  백그라운드 계산은 최소화하고,  필요시만 가속도 센서를 사용하도록 설계해야 합니다.  또한,  사용자에게 데이터 사용량을 알리고,  필요시 데이터 수집 빈도를 조절할 수 있는 설정을 제공하는 것이 좋습니다.
