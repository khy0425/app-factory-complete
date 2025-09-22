# calm_breath 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** `com.reaf.maumsum`
- **필요한 dependencies:** (pubspec.yaml)

```yaml
name: maumsum
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
  provider: ^6.0.5 # 상태 관리
  path_provider: ^2.0.11 # 로컬 파일 저장
  sqflite: ^2.0.2 # 로컬 데이터베이스
  just_audio: ^0.9.3 # 오디오 재생
  audio_session: ^1.0.0 # 오디오 세션 관리
  flutter_svg: ^2.0.6 # SVG 이미지 사용 (선택)
  intl: ^0.18.1 # 다국어 지원 (향후)
  shared_preferences: ^2.1.1 # 간단한 설정 저장
  flutter_screenutil: ^5.6.1 # 화면 크기 반응형 UI

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/audio/ # 명상 오디오 파일
    - assets/images/ # 이미지 파일

```

- **폴더 구조:** (lib 폴더 내부)

```
lib/
├── main.dart
├── models/
│   ├── meditation.dart
│   ├── breathing.dart
│   └── user.dart
├── services/
│   ├── database_helper.dart
│   ├── audio_player.dart
│   └── notification_service.dart
├── ui/
│   ├── home_screen.dart
│   ├── meditation_list_screen.dart
│   ├── breathing_list_screen.dart
│   ├── meditation_detail_screen.dart
│   ├── breathing_detail_screen.dart
│   ├── mypage_screen.dart
│   └── settings_screen.dart
├── widgets/
│   ├── custom_button.dart
│   ├── progress_indicator.dart
│   └── ...  (다른 공통 위젯들)
├── utils/
│   ├── constants.dart
│   └── helper_functions.dart
└── ...
```


## 화면별 구현 상세

**1. 홈 화면 (home_screen.dart):**

- **위젯 구조:** `Scaffold`  > `AppBar` > `ListView` (오늘의 추천 명상, 최근 활동)
- **상태 관리 방식:** `Provider`
- **필요한 패키지들:** `provider`, `flutter_svg` (선택), `intl`


**2. 명상 목록 화면 (meditation_list_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `GridView` 또는 `ListView` (명상 목록)
- **상태 관리 방식:** `Provider`
- **필요한 패키지들:** `provider`, `flutter_svg`


**3. 호흡 연습 목록 화면 (breathing_list_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `GridView` 또는 `ListView` (호흡 연습 목록)
- **상태 관리 방식:** `Provider`
- **필요한 패키지들:** `provider`, `flutter_svg`


**4. 명상 상세 화면 (meditation_detail_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `Column` (명상 제목, 설명, 플레이어, 진행바)
- **상태 관리 방식:** `Provider`, `just_audio`
- **필요한 패키지들:** `provider`, `just_audio`, `audio_session`


**5. 호흡 연습 상세 화면 (breathing_detail_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `Column` (호흡법 설명, 애니메이션, 진행바, 진동 제어)
- **상태 관리 방식:** `Provider`
- **필요한 패키지들:** `provider`


**6. 마이페이지 화면 (mypage_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `Column` (사용자 정보, 명상/호흡 기록, 목표 설정)
- **상태 관리 방식:** `Provider` , `shared_preferences`
- **필요한 패키지들:** `provider`, `shared_preferences`


**7. 설정 화면 (settings_screen.dart):**

- **위젯 구조:** `Scaffold` > `AppBar` > `ListView` (알림 설정, 배경 음악, 프리미엄 구독)
- **상태 관리 방식:** `Provider`, `shared_preferences`
- **필요한 패키지들:** `provider`, `shared_preferences`



## 데이터 모델

- **meditation.dart:** `Meditation` 클래스 (id, title, description, audioPath, duration, theme, level)
- **breathing.dart:** `Breathing` 클래스 (id, title, description, animation, steps, duration)
- **user.dart:** `User` 클래스 (id, weeklyGoal,  completedMeditations, completedBreathings)

- **데이터베이스 스키마 (sqflite):**

```sql
CREATE TABLE meditations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  audioPath TEXT NOT NULL,
  duration INTEGER NOT NULL,
  theme TEXT,
  level INTEGER
);

CREATE TABLE breathings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  animation TEXT, -- 애니메이션 파일 경로 또는 데이터
  steps TEXT, -- 각 단계에 대한 정보
  duration INTEGER NOT NULL
);

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  weeklyGoal INTEGER,
  completedMeditations TEXT, -- JSON 형태로 저장
  completedBreathings TEXT -- JSON 형태로 저장
);
```

- **API 연동 방식:**  MVP 단계에서는 로컬 DB만 사용. 향후 음성 합성 API(추가 기능) 연동 고려.


## 권한 및 설정

- **AndroidManifest.xml:**

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.VIBRATE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
```

- iOS 권한 설정:  `info.plist`에 필요한 권한 추가 (진동, 저장공간)


## 핵심 기능 구현 방법

| 기능 | 사용할 Flutter 패키지 | 구현 난이도 (1-5점) | 예상 개발 시간 |
|---|---|---|---|
| 가이드 명상 재생 | `just_audio`, `audio_session` | 3 | 2일 |
| 호흡 연습 애니메이션 | `AnimatedBuilder`, `CustomPainter` (혹은 애니메이션 라이브러리) | 4 | 3일 |
| 로컬 데이터베이스 관리 | `sqflite` | 3 | 2일 |
| 알림 기능 | `flutter_local_notifications` | 3 | 2일 |
| 사용자 데이터 저장 | `shared_preferences` | 2 | 1일 |
| 진동 기능 |  플랫폼 채널 | 2 | 1일 |


## 테스트 계획

- **단위 테스트 대상:**  각 모델 클래스, 데이터베이스 헬퍼 함수, 오디오 플레이어 기능
- **통합 테스트 시나리오:**  명상 재생, 호흡 연습 진행, 데이터 저장 및 로딩, 알림 기능 동작 확인
- **사용자 테스트 계획:**  베타 테스터를 통해 UI/UX 평가, 기능 사용성 평가, 성능 및 안정성 검증


**참고:**  상기 개발 시간은 대략적인 예상치이며, 실제 개발 시간은 개발자의 숙련도 및 기능의 복잡성에 따라 달라질 수 있습니다.  또한,  MVP 이후 기능 추가 및 개선에 따른 시간이 추가적으로 소요될 것입니다.  애니메이션 구현은  `flutter_animation`과 같은 라이브러리를 활용하여 효율성을 높일 수 있습니다. 다국어 지원은 `intl` 패키지를 사용하여 구현할 수 있습니다.  추후 기능 구현(개인 맞춤형 추천, 커뮤니티 기능 등)은  머신러닝 모델 연동이나  Firebase와 같은 백엔드 서비스를 필요로 할 수 있습니다.  이 경우 추가적인 기술 스택 및 개발 시간이 필요합니다.
