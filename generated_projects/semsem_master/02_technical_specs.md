# semsem_master 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** com.reaf.semsemmaster
- **필요한 dependencies:** (pubspec.yaml)

```yaml
name: semsem_master
description: A new Flutter project.
publish_to: none

version: 1.0.0+1

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.17.0
  sqflite: ^2.0.2+1
  path_provider: ^2.0.11
  provider: ^6.0.5
  flutter_test:
    sdk: flutter
  flutter_svg: ^2.0.6 # 필요시 SVG 아이콘 사용
  google_fonts: ^5.2.0 # 원하는 폰트 사용시
  shared_preferences: ^2.1.1 # 설정 저장
  vibration: ^1.0.1 # 진동 기능

dev_dependencies:
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
```

- **폴더 구조:** (lib 폴더 내부)

```
lib/
├── main.dart
├── models/
│   ├── user.dart
│   ├── exercise_record.dart
│   ├── game_record.dart
│   └── ...
├── screens/
│   ├── home_screen.dart
│   ├── practice_screen.dart
│   ├── game_screen.dart
│   ├── settings_screen.dart
│   └── ...
├── services/
│   ├── database_service.dart
│   └── ...
├── widgets/
│   ├── custom_button.dart
│   ├── result_chart.dart
│   └── ...
├── utils/
│   ├── constants.dart
│   └── ...
└── ...
```


## 화면별 구현 상세

**1. 홈 화면 (home_screen.dart):**

- **위젯 구조:** `Scaffold`  -> `AppBar` -> `Column` (최근 기록, 연습 모드 버튼, 미니 게임 모드 버튼, 설정 버튼)
- **상태 관리 방식:** `Provider` 패키지를 사용하여 최근 기록 데이터 관리.
- **필요한 패키지들:** `flutter`, `provider`, `intl` (날짜/시간 포맷), `google_fonts` (원하는 폰트 사용시)

**2. 연습 모드 화면 (practice_screen.dart):**

- **위젯 구조:** `Scaffold` -> `AppBar` -> `Column` (문제 표시, 정답 입력, 점수/시간 표시, 다음 문제/결과 버튼)
- **상태 관리 방식:** `ChangeNotifier`를 상속받은 클래스를 사용하여 문제, 정답, 점수, 시간 등의 상태 관리.  `Provider`로 상태 공유.
- **필요한 패키지들:** `flutter`, `provider`, `intl`, `vibration` (정답/오답 진동 피드백)

**3. 미니 게임 화면 (game_screen.dart):**  (게임 종류에 따라 구조 다름)

- **위젯 구조:**  게임 종류에 따라 다르게 구현 (예: `Stack`, `AnimatedBuilder` 등 사용)
- **상태 관리 방식:** `ChangeNotifier`를 상속받은 클래스 사용. `Provider`로 상태 공유.
- **필요한 패키지들:** `flutter`, `provider`, `vibration`

**4. 설정 화면 (settings_screen.dart):**

- **위젯 구조:** `Scaffold` -> `AppBar` -> `ListView` (사용자 프로필, 연산 설정, 알림 설정, 테마 설정)
- **상태 관리 방식:** `Provider` 또는 `SharedPreferences`를 사용하여 설정 값 저장 및 관리.
- **필요한 패키지들:** `flutter`, `provider`, `shared_preferences`


## 데이터 모델

- **User.dart:**  `String username`, `DateTime registeredDate` 등
- **ExerciseRecord.dart:**  `int id`, `DateTime date`, `String operationType`, `int difficulty`, `int correctCount`, `int totalCount`, `int timeTaken` 등
- **GameRecord.dart:**  `int id`, `DateTime date`, `String gameType`, `int score`, `int rank` 등


- **데이터베이스 스키마 (sqflite):**

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  registeredDate INTEGER NOT NULL
);

CREATE TABLE exercise_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER NOT NULL,
  date INTEGER NOT NULL,
  operationType TEXT NOT NULL,
  difficulty INTEGER NOT NULL,
  correctCount INTEGER NOT NULL,
  totalCount INTEGER NOT NULL,
  timeTaken INTEGER NOT NULL,
  FOREIGN KEY (userId) REFERENCES users(id)
);

CREATE TABLE game_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER NOT NULL,
  date INTEGER NOT NULL,
  gameType TEXT NOT NULL,
  score INTEGER NOT NULL,
  rank INTEGER
  FOREIGN KEY (userId) REFERENCES users(id)
);
```

- **API 연동 방식:** 없음 (로컬 데이터베이스만 사용)


## 권한 및 설정

- **android/app/src/main/AndroidManifest.xml:**  진동 권한 필요시 추가. `<uses-permission android:name="android.permission.VIBRATE" />`

- **iOS 권한 설정:** 진동 권한 필요시 설정 (Info.plist).


## 핵심 기능 구현 방법

**1. 암산 연습 모드:**

- **사용할 Flutter 패키지:** `flutter`, `provider`, `intl`, `vibration`
- **구현 난이도:** 3/5
- **예상 개발 시간:** 2주

**2. 미니 게임 모드 (1종류):** (예: 숫자 맞추기)

- **사용할 Flutter 패키지:** `flutter`, `provider`, `vibration`
- **구현 난이도:** 2/5
- **예상 개발 시간:** 1주

**3. 설정:**

- **사용할 Flutter 패키지:** `flutter`, `shared_preferences`, `provider`
- **구현 난이도:** 2/5
- **예상 개발 시간:** 1주

**4. 데이터베이스:**

- **사용할 Flutter 패키지:** `sqflite`, `path_provider`
- **구현 난이도:** 3/5
- **예상 개발 시간:** 2주


## 테스트 계획

- **단위 테스트 대상:** 각 모델 클래스, 연산 함수, 데이터베이스 쿼리 함수 등
- **통합 테스트 시나리오:**  각 기능 간의 상호 작용 테스트, 데이터베이스 연동 테스트, 다양한 입력값에 대한 테스트
- **사용자 테스트 계획:** 베타 테스터 모집을 통해 실제 사용자 환경에서의 테스트 진행, 사용자 피드백 수렴 및 반영


**참고:** 위 명세서는 MVP 개발에 집중하여 작성되었습니다.  프리미엄 기능 및 추가 미니 게임들은 2단계, 3단계 개발 계획에 따라 추가될 것입니다.  난이도 및 개발 시간은 예상치이며, 실제 개발 과정에서 변동될 수 있습니다.  또한,  UI 디자인 및 구체적인 게임 로직은 별도로 설계되어야 합니다.  성능 최적화를 위해서는 필요시 코드 분석 및 프로파일링 도구를 사용하여 병목 지점을 찾고 개선해야 합니다.
