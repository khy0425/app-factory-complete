# meditation_app 기술 명세서

## Flutter 프로젝트 구조

- 패키지명: com.reaf.unsekotpida
- 필요한 dependencies: (pubspec.yaml용)

```yaml
name: unsekotpida
description: 운세꽃피다 앱

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  http: ^1.1.0
  shared_preferences: ^2.2.0
  sqflite: ^2.0.2+1
  firebase_core: ^2.14.0
  firebase_auth: ^4.6.3
  cloud_firestore: ^4.8.1
  intl: ^0.18.1
  provider: ^6.0.5
  flutter_local_notifications: ^10.0.0
  url_launcher: ^6.1.12
  google_mobile_ads: ^2.1.0 # 광고(수익화 단계)
  cached_network_image: ^3.2.3 # 이미지 캐싱
  flutter_screenutil: ^5.6.1 # 화면 크기 반응형 디자인

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0
```

- 폴더 구조: (lib 폴더 내부)

```
lib/
├── main.dart
├── models/             // 데이터 모델
│   ├── fortune.dart
│   ├── test.dart
│   └── user.dart
├── services/           // 서비스 로직 (API 호출, 데이터베이스 관리 등)
│   ├── fortune_service.dart
│   ├── test_service.dart
│   └── auth_service.dart (Firebase Auth)
├── ui/                 // UI 관련 코드
│   ├── screens/        // 각 화면
│   │   ├── home_screen.dart
│   │   ├── fortune_detail_screen.dart
│   │   ├── test_screen.dart
│   │   ├── result_screen.dart
│   │   └── settings_screen.dart
│   ├── widgets/       // 재사용 가능한 위젯
│   │   ├── fortune_card.dart
│   │   └── test_question.dart
│   └── themes/        // 테마 설정
├── utils/              // 유틸리티 함수
│   └── constants.dart
├── repositories/       // 데이터 접근 계층 (Repository Pattern)
│   ├── fortune_repository.dart
│   └── test_repository.dart
└── providers/         // Provider 상태 관리
    ├── fortune_provider.dart
    └── test_provider.dart

```


## 화면별 구현 상세

**1. 홈 화면 (home_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, body, bottomNavigationBar)  -> `CustomScrollView` (오늘의 운세 카드, 심리 테스트 추천 목록)
- **상태 관리 방식:** `Provider` (오늘의 운세, 추천 심리 테스트 목록 로딩 상태 관리)
- **필요한 패키지들:** `provider`, `cached_network_image`

**2. 운세 상세 화면 (fortune_detail_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, body) -> `SingleChildScrollView` (운세 이미지, 운세 내용)
- **상태 관리 방식:**  `Provider` (운세 데이터)
- **필요한 패키지들:** `provider`, `cached_network_image`

**3. 심리 테스트 화면 (test_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, body) -> `ListView` (테스트 질문 목록) - `test_question` Widget 사용
- **상태 관리 방식:** `Provider` (현재 질문, 응답 목록, 테스트 진행 상태)
- **필요한 패키지들:** `provider`, `flutter_screenutil`

**4. 결과 화면 (result_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, body) -> `Column` (결과 이미지, 결과 내용)
- **상태 관리 방식:** `Provider` (테스트 결과)
- **필요한 패키지들:** `provider`, `cached_network_image`

**5. 설정 화면 (settings_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, body) -> `ListView` (설정 항목 목록)
- **상태 관리 방식:** `Provider` (설정 값) -  알림 설정, 테마 변경 등
- **필요한 패키지들:** `provider`, `shared_preferences`, `flutter_local_notifications`


## 데이터 모델

- **fortune.dart:** `Fortune` 클래스 (운세 정보: 간지, 총운, 재물운, 애정운, 건강운, 이미지 URL 등)
- **test.dart:** `Test` 클래스 (심리 테스트 정보: 제목, 질문 목록, 답변, 결과 등)
- **user.dart:** `User` 클래스 (사용자 정보: UID, 구독 상태 등)  - Firebase Authentication과 연동


## 데이터베이스 스키마 (sqflite용)

- `fortunes` 테이블: `id` (INTEGER PRIMARY KEY), `zodiac` (TEXT), `total` (TEXT), `wealth` (TEXT), `love` (TEXT), `health` (TEXT), `imageUrl` (TEXT), `date` (TEXT)
- `tests` 테이블:  `id` (INTEGER PRIMARY KEY), `title` (TEXT), `questions` (TEXT), `answers` (TEXT), `results` (TEXT)
- `saved_fortunes` 테이블: `id` (INTEGER PRIMARY KEY), `fortuneId` (INTEGER), `userId` (TEXT)


## API 연동 방식

- 운세 API:  외부 API 사용 (Retrofit 또는 Dio 패키지 사용)  -  에러 핸들링 및 캐싱 구현
- Firebase Firestore: 심리 테스트 데이터, 사용자 데이터 저장 및 관리


## 권한 및 설정

- **AndroidManifest.xml:**
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.VIBRATE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />  <!-- 이미지 저장을 위한 권한 (Android 10 이상 필요시 Scoped Storage 고려)-->
```
- iOS 권한 설정:  Info.plist 파일에  Privacy - Vibrations usage description 추가


## 핵심 기능 구현 방법

| 기능                | 사용할 Flutter 패키지         | 구현 난이도 (1-5) | 예상 개발 시간 (시간) |
|---------------------|------------------------------|-------------------|-----------------------|
| 오늘의 운세          | `http`, `cached_network_image` | 3                 | 24                    |
| 심리 테스트          | `provider`, `shared_preferences` | 4                 | 48                    |
| 운세 저장/공유      | `shared_preferences`, `url_launcher` | 2                 | 16                    |
| 알림 기능           | `flutter_local_notifications` | 3                 | 24                    |
| Firebase 연동        | `firebase_core`, `cloud_firestore` | 4                 | 48                    |
| 프리미엄 구독 기능   |  (인앱 결제 플러그인 필요)  | 5                 | 72                    |


## 테스트 계획

- **단위 테스트:**  각 모델 클래스, 서비스 클래스에 대한 단위 테스트 (Flutter Test 사용)
- **통합 테스트:** API 연동, 데이터베이스 접근, UI 요소 간 상호 작용에 대한 통합 테스트 (Flutter Driver 또는 Integration Test 사용)
- **사용자 테스트:**  베타 테스터를 모집하여 사용성 테스트 및 피드백 수집


**참고:** 위 기술 명세서는  MVP 개발에 초점을 맞추고 있습니다.  정식 출시 및 기능 확장을 위해서는 더욱 상세한 설계와 구현이 필요합니다.  특히, 프리미엄 구독 기능 구현에는 추가적인 인앱 결제 플러그인 및 서버측 구현이 필요하며,  외부 운세 API 선택 및 안정적인 운영을 위한 에러 핸들링, 로딩 표시 등의 추가 작업이 요구됩니다.  또한, 이미지 자산 관리, 디자인 시스템 구축, 국제화/지역화 등도 고려해야 합니다.  성능 최적화를 위해서는 이미지 압축,  필요 없는 위젯 제거,  비동기 처리 등을 신경써야 합니다.
