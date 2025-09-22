# colorpop_pangpang 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** com.reaf.colorpop_pangpang
- **필요한 dependencies:** (pubspec.yaml용)

```yaml
name: colorpop_pangpang
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
  firebase_core: ^2.14.0
  firebase_auth: ^4.6.3
  firebase_database: ^10.2.0 #or firebase_firestore for better scalability
  cloud_firestore: ^4.8.1
  google_mobile_ads: ^2.6.0
  shared_preferences: ^2.1.1
  path_provider: ^2.0.11
  sqflite: ^2.0.2+4
  provider: ^6.0.5
  get: ^4.6.5
  flutter_screenutil: ^5.6.1 #For responsive design
  intl: ^0.18.1 #For localization

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
```

- **폴더 구조:** (lib 폴더 내부)

```
lib/
├── main.dart
├── models/               // 데이터 모델
│   ├── game_data.dart
│   ├── user_data.dart
│   └── level_data.dart
├── services/            // 서비스 및 API 연동
│   ├── firebase_service.dart
│   ├── local_db_service.dart
│   └── ad_service.dart
├── ui/                  // 화면 위젯들
│   ├── home_screen.dart
│   ├── game_screen.dart
│   ├── settings_screen.dart
│   └── ranking_screen.dart
├── widgets/             // 재사용 가능한 위젯들
│   ├── game_board.dart
│   ├── custom_button.dart
│   └── ...
├── utils/               // 유틸리티 함수들
│   ├── game_logic.dart
│   └── ...
└── providers/           // 상태 관리 (provider 사용)
    ├── game_provider.dart
    ├── user_provider.dart
    └── ...

```


## 화면별 구현 상세

**1. 홈 화면 (HomeScreen):**

- **위젯 구조:** Scaffold, Column, Row, ElevatedButton, Image, Text, FutureBuilder (데이터 로딩 표시)
- **상태 관리 방식:** Provider 패키지를 사용하여 `UserProvider` 에서 사용자 데이터 및 일일 미션 정보 관리.
- **필요한 패키지들:** provider, flutter_screenutil


**2. 게임 화면 (GameScreen):**

- **위젯 구조:** Stack (게임 보드, 점수, 시간 표시 위젯 배치), CustomPainter (게임 보드 그리기), AnimatedBuilder (애니메이션 효과), GestureDetector (블록 터치 이벤트 처리)
- **상태 관리 방식:** Provider 패키지를 사용하여 `GameProvider` 에서 게임 상태 (보드, 점수, 남은 시간 등) 관리.
- **필요한 패키지들:** provider, flutter_screenutil


**3. 설정 화면 (SettingsScreen):**

- **위젯 구조:** Scaffold, ListView, SwitchListTile, ListTile
- **상태 관리 방식:**  `SharedPreferences` 를 사용하여 설정 값 저장.
- **필요한 패키지들:** shared_preferences, flutter_screenutil


**4. 랭킹 화면 (RankingScreen):**

- **위젯 구조:** Scaffold, ListView, StreamBuilder (실시간 랭킹 업데이트)
- **상태 관리 방식:** Firebase Database 또는 Firestore 사용.
- **필요한 패키지들:** firebase_database or cloud_firestore, flutter_screenutil


## 데이터 모델

- **`GameData`:** 레벨 정보 (레벨 번호, 목표, 블록 배치, 제한 시간), 현재 게임 상태 (점수, 남은 시간, 보드 상태) 등을 저장
- **`UserData`:** 사용자 ID, 점수, 아이템 정보 등을 저장
- **`LevelData`:** 각 레벨의 상세 정보를 담는 클래스 (블록 배열, 목표 점수, 시간 제한 등)
- **`DailyMission`:** 일일 미션 정보 (미션 내용, 보상)를 저장

- **데이터베이스 스키마 (sqflite용):**  `GameData` 는 로컬 DB(sqflite)에 저장. 테이블 이름: `game_data`.  필드는 `GameData` 클래스의 변수에 따라 생성.
- **API 연동 방식:** Firebase Realtime Database 또는 Cloud Firestore를 사용하여 사용자 데이터와 랭킹 데이터를 관리.


## 권한 및 설정

- **android/app/src/main/AndroidManifest.xml:**

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.VIBRATE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>  <!--For saving game data, if needed -->
```

- iOS 권한 설정:  Vibrate 권한 설정 필요 (Info.plist 수정). 저장공간 권한은 필요시 추가.


## 핵심 기능 구현 방법

**1. 퍼즐 게임:**

- **사용할 Flutter 패키지:**  `provider`, `flutter_screenutil`
- **구현 난이도:** 4/5
- **예상 개발 시간:** 3주

**2. 레벨 시스템:**

- **사용할 Flutter 패키지:**  `shared_preferences` 또는 `sqflite`,  `provider`
- **구현 난이도:** 3/5
- **예상 개발 시간:** 2주

**3. 일일 미션 & 보상:**

- **사용할 Flutter 패키지:** `shared_preferences` 또는 `sqflite`, `provider` , `firebase_database` or `cloud_firestore` (서버측 미션 정보 저장 및 관리에 사용)
- **구현 난이도:** 3/5
- **예상 개발 시간:** 1주


**4. 랭킹 시스템:**

- **사용할 Flutter 패키지:** `firebase_database` or `cloud_firestore`
- **구현 난이도:** 3/5
- **예상 개발 시간:** 1주


**5. 광고 시스템:**

- **사용할 Flutter 패키지:** `google_mobile_ads`
- **구현 난이도:** 2/5
- **예상 개발 시간:** 1주


**6. 진동 기능:**

- **사용할 Flutter 패키지:**  내장 기능 사용
- **구현 난이도:** 1/5
- **예상 개발 시간:** 0.5주


**7. 사운드 효과:**

- **사용할 Flutter 패키지:** `audioplayers` (권장) or `assets_audio_player`
- **구현 난이도:** 2/5
- **예상 개발 시간:** 0.5주


## 테스트 계획

- **단위 테스트 대상:** 게임 로직 (점수 계산, 블록 제거 알고리즘 등), 데이터 모델, API 연동 부분
- **통합 테스트 시나리오:**  각 기능 간의 연동 테스트,  다양한 레벨에서의 게임 플레이 테스트,  랭킹 시스템 테스트,  광고 표시 테스트
- **사용자 테스트 계획:**  베타 테스터 모집,  피드백 수렴,  버그 수정 및 기능 개선


**참고:**  위 예상 개발 시간은 대략적인 수치이며, 실제 개발 시간은 개발자의 숙련도 및 기능 복잡도에 따라 달라질 수 있습니다.  Firebase Realtime Database 보다는 Cloud Firestore를 사용하는 것이 장기적인 유지보수 및 확장성 측면에서 더욱 효율적입니다.  또한,  Getx와 같은 다른 상태 관리 패키지를 사용할 수도 있습니다.  성능 최적화를 위해서는 필요에 따라 위젯의 재구성을 최소화하고,  메모리 관리 및 애니메이션 최적화에 신경 써야 합니다.
