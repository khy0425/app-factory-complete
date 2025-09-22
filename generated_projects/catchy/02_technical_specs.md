# catchy 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** com.reaf.tajawang
- **필요한 dependencies:** (pubspec.yaml용)

```yaml
name: tajawang
description: 한글 타이핑 게임 앱

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  get: ^4.6.5 # 상태 관리
  sqflite: ^2.0.2+1 # 로컬 데이터베이스
  path_provider: ^2.0.11 # 파일 경로 접근
  google_fonts: ^5.2.0 # 폰트
  vibration: ^1.0.0+1 # 진동
  cached_network_image: ^3.2.3 # 이미지 캐싱
  flutter_screenutil: ^5.8.0 # 화면 크기 적응
  shared_preferences: ^2.0.15 # 간단한 데이터 저장
  intl: ^0.18.1 # 국제화


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0
```

- **폴더 구조:** (lib 폴더 내부)

```
lib/
├── main.dart
├── models/             # 데이터 모델
│   ├── user.dart
│   ├── game_data.dart
│   └── achievement.dart
├── screens/            # 화면 위젯
│   ├── home_screen.dart
│   ├── game_screen.dart
│   ├── practice_screen.dart
│   ├── achievement_screen.dart
│   └── settings_screen.dart
├── widgets/            # 재사용 가능한 위젯
│   ├── custom_button.dart
│   └── typing_field.dart
├── services/           # 데이터베이스, 설정 등 서비스
│   ├── database_helper.dart
│   └── settings_service.dart
├── utils/              # 유틸리티 함수
│   ├── game_logic.dart
│   └── helper_functions.dart
└── constants.dart       # 상수 정의
```

## 화면별 구현 상세

**1. 홈 화면 (home_screen.dart):**

- **위젯 구조:**  `Scaffold`  -> `Column` (게임 시작 버튼, 연습 시작 버튼, 성취도 확인 버튼, 설정 버튼)
- **상태 관리 방식:** `GetBuilder` (Get 패키지 사용)
- **필요한 패키지들:** `flutter`, `get`, `google_fonts`, `flutter_screenutil`

**2. 게임 화면 (game_screen.dart):**

- **위젯 구조:** `Scaffold` -> `Column` (게임 진행 영역, 점수 표시, 타이머, 남은 시간) + `GestureDetector` (키보드 입력 감지)
- **상태 관리 방식:** `GetxController` (게임 로직, 점수, 시간 관리)
- **필요한 패키지들:** `flutter`, `get`, `vibration`, `google_fonts`, `flutter_screenutil`

**3. 연습 화면 (practice_screen.dart):**

- **위젯 구조:** `Scaffold` -> `Column` (입력 필드, 타이핑 결과 표시, 오타 분석)
- **상태 관리 방식:** `GetxController` (입력 내용, 타이핑 속도, 정확도 관리)
- **필요한 패키지들:** `flutter`, `get`, `google_fonts`, `flutter_screenutil`

**4. 성취도 관리 화면 (achievement_screen.dart):**

- **위젯 구조:** `Scaffold` -> `Column` (그래프, 목표 설정, 기록 목록)
- **상태 관리 방식:** `GetBuilder`
- **필요한 패키지들:** `flutter`, `get`, `charts_flutter` (차트 라이브러리), `google_fonts`, `flutter_screenutil`

**5. 설정 화면 (settings_screen.dart):**

- **위젯 구조:** `Scaffold` -> `ListView` (설정 항목들: 사운드, 진동, 배경 설정 등)
- **상태 관리 방식:** `GetxController` (설정 값 저장 및 불러오기)
- **필요한 패키지들:** `flutter`, `get`, `shared_preferences`, `google_fonts`, `flutter_screenutil`


## 데이터 모델

- **User.dart:** 사용자 정보 (ID, 이름, 레벨, 점수 등)
- **GameData.dart:** 게임 데이터 (문제, 정답, 레벨 등)
- **Achievement.dart:** 성취도 데이터 (날짜, 점수, 속도, 정확도 등)

**데이터베이스 스키마 (sqflite용):**

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  level INTEGER,
  score INTEGER
);

CREATE TABLE game_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  level INTEGER,
  question TEXT,
  answer TEXT
);

CREATE TABLE achievements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  date TEXT,
  score INTEGER,
  speed REAL,
  accuracy REAL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

- **API 연동 방식:** 없음 (MVP 단계)


## 권한 및 설정

- **android/app/src/main/AndroidManifest.xml:**

```xml
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.VIBRATE" />
```

- iOS 권한 설정:  Info.plist 파일에 `NSLocationWhenInUseUsageDescription` 추가 (필요시)


## 핵심 기능 구현 방법

| 기능             | 사용할 Flutter 패키지       | 구현 난이도 (1-5) | 예상 개발 시간 (시간) |
|-----------------|---------------------------|-----------------|-------------------|
| 게임 모드         | `get`, `vibration`, `google_fonts` | 4                 | 120                |
| 연습 모드         | `get`, `google_fonts`       | 3                 | 80                 |
| 성취도 관리       | `get`, `charts_flutter`    | 3                 | 60                 |
| 로컬 데이터베이스 | `sqflite`, `path_provider` | 3                 | 40                 |
| 진동 기능         | `vibration`                | 1                 | 10                 |
| 설정 저장         | `shared_preferences`       | 1                 | 10                 |
| UI 구현           | `flutter`, `google_fonts`, `flutter_screenutil` | 4                 | 100                |


## 테스트 계획

- **단위 테스트 대상:** 각 위젯, 데이터 모델, 게임 로직 함수
- **통합 테스트 시나리오:** 각 화면의 기능 테스트, 데이터베이스 연동 테스트, 게임 플레이 테스트
- **사용자 테스트 계획:**  베타 테스터 모집을 통해 사용성 및 버그 검출 (초등학생 대상 테스트 포함)


**참고:**  상기 개발 시간은 추정치이며, 실제 개발 시간은 개발자의 숙련도,  요구사항 변경 등에 따라 달라질 수 있습니다.  또한,  `charts_flutter` 패키지는 차트 기능에 필요하며,  필요에 따라 다른 차트 라이브러리를 사용할 수 있습니다.  이미지 캐싱을 위해 `cached_network_image`를 사용하여 네트워크 요청 횟수를 줄이고,  `flutter_screenutil`을 사용하여 다양한 기기 크기에 대한 반응형 디자인을 구현합니다.  Getx 패키지는 상태 관리를 효율적으로 처리하는 데 도움이 됩니다.  `intl` 패키지를 사용하여 다국어 지원을 위한 기반을 마련합니다.  하지만 MVP 단계에서는 우선 한국어만 지원하는 것이 좋습니다.
