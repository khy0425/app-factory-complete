# sanchaekgil_friend 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** com.reaf.sanchaekgilfriend
- **필요한 dependencies:** (pubspec.yaml)

```yaml
name: sanchaekgilfriend
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
  google_maps_flutter: ^2.4.0 # 또는 다른 지도 API 패키지
  geolocator: ^9.0.0
  shared_preferences: ^2.0.15 # 로컬 저장용
  cloud_firestore: ^4.8.3 # Firebase Firestore
  firebase_core: ^2.14.0 # Firebase Core
  firebase_auth: ^4.6.3 # Firebase Authentication (추후 로그인 기능 추가시)
  image_picker: ^1.0.0 # 이미지 선택
  path_provider: ^2.0.11 # 파일 저장 경로
  intl: ^0.18.1 # 날짜/시간 국제화
  provider: ^6.0.5 # 상태 관리 (Provider 패턴)
  cached_network_image: ^3.2.3 # 이미지 캐싱
  url_launcher: ^6.1.12 # URL 열기 (SNS 공유)


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0


flutter:
  uses-material-design: true
  assets:
    - assets/images/ # 이미지 파일 위치
```

- **폴더 구조:** (lib 폴더 내부)

```
lib/
├── models/          # 데이터 모델
│   ├── course.dart
│   ├── user.dart
│   └── ...
├── services/        # 서비스 로직 (API, 데이터베이스 접근)
│   ├── location_service.dart
│   ├── database_service.dart
│   ├── map_service.dart
│   └── ...
├── ui/              # UI 구성요소
│   ├── screens/     # 화면
│   │   ├── home_screen.dart
│   │   ├── course_create_screen.dart
│   │   ├── course_detail_screen.dart
│   │   ├── mypage_screen.dart
│   │   └── ...
│   ├── widgets/    # 재사용 가능한 위젯
│   │   ├── custom_button.dart
│   │   └── ...
│   └── styles.dart # 스타일 정의
├── main.dart
├── app.dart        # 앱의 루트 위젯
└── ...
```


## 화면별 구현 상세

**1. 홈 화면 (home_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, Body, BottomNavigationBar)  -> `ListView` (근처 코스 추천, 나의 산책 기록 요약, 인기 코스 목록)
- **상태 관리 방식:** `Provider`를 사용하여 코스 데이터 관리.  `FutureBuilder`를 사용하여 비동기 데이터 로딩 처리.
- **필요한 패키지들:** `provider`, `google_maps_flutter`, `cached_network_image`

**2. 코스 생성 화면 (course_create_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, Body) -> `GoogleMap` (경로 기록),  `TextField` (설명, 해시태그), `ElevatedButton` (저장)
- **상태 관리 방식:** `Provider`를 사용하여 코스 데이터 관리.  `geolocator` 패키지를 사용하여 위치 정보 획득.
- **필요한 패키지들:** `provider`, `google_maps_flutter`, `geolocator`, `image_picker`

**3. 코스 상세 화면 (course_detail_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, Body) -> `Column` (코스 정보, 사진, 설명, 리뷰)
- **상태 관리 방식:** `Provider`를 사용하여 코스 데이터 관리.
- **필요한 패키지들:** `provider`, `cached_network_image`

**4. 마이페이지 화면 (mypage_screen.dart):**

- **위젯 구조:** `Scaffold` (AppBar, Body) -> `ListView` (나의 산책 기록, 내가 생성한 코스 목록)
- **상태 관리 방식:** `Provider`를 사용하여 사용자 데이터 및 코스 데이터 관리.
- **필요한 패키지들:** `provider`


## 데이터 모델

- **Course:** `courseId`, `userId`, `title`, `description`, `hashtags`, `difficulty`, `distance`, `duration`, `caloriesBurned`, `createdAt`, `path`(List<LatLng>), `images`(List<String>)
- **User:** `userId`, `userName`, `profileImage` (Firebase Authentication과 연동)

- **데이터베이스 스키마 (Firestore):**
    - Collection: `courses`
        - Document:  Course 객체의 JSON 표현
    - Collection: `users`
        - Document: User 객체의 JSON 표현


- **API 연동 방식:** Firebase Firestore를 사용하여 데이터 저장 및 관리.  지도 API는 Google Maps Platform 또는 Naver Maps Platform을 사용. 날씨 API는 필요에 따라 추가.


## 권한 및 설정

- **AndroidManifest.xml:**
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
```

- iOS 권한 설정: Info.plist 파일에  `Privacy - Location Always Usage Description` , `Privacy - Camera Usage Description`, `Privacy - Photo Library Usage Description` 추가.


## 핵심 기능 구현 방법

| 기능                     | 사용할 Flutter 패키지            | 구현 난이도 (1-5) | 예상 개발 시간 (시간) |
|--------------------------|---------------------------------|--------------------|-----------------------|
| 산책 코스 생성 및 저장     | `geolocator`, `google_maps_flutter`, `cloud_firestore`, `image_picker` | 4                 | 40                     |
| 산책 코스 검색 및 추천     | `cloud_firestore`, `google_maps_flutter` | 3                 | 30                     |
| 산책 기록 관리            | `shared_preferences`, `cloud_firestore` | 2                 | 20                     |
| 산책 코스 공유             | `url_launcher`, `share`           | 2                 | 15                     |
| 마이페이지 기능            |                                 | 1                 | 10                     |
| 사용자 리뷰 및 평점 기능   | `cloud_firestore`                | 2                 | 20                     |
| 알림 기능 (Firebase Cloud Messaging) | `firebase_messaging`       | 3                 | 25                     |


## 테스트 계획

- **단위 테스트 대상:**  데이터 모델, 서비스 로직 (location_service, database_service)
- **통합 테스트 시나리오:**  각 화면의 기능 테스트,  데이터 저장 및 불러오기 테스트,  지도 API 연동 테스트,  공유 기능 테스트.
- **사용자 테스트 계획:**  베타 테스터를 모집하여 사용성 테스트, 버그 수정.


**추가 고려사항:**

* **배터리 최적화:**  GPS 사용 최소화,  배경 위치 업데이트 간격 조절,  필요 없는 서비스 중지.
* **성능 최적화:**  데이터 로딩 최적화,  리스트 뷰 최적화,  이미지 캐싱 활용.
* **오프라인 기능:**  로컬 데이터베이스 (SQLite)를 사용하여 오프라인에서도 코스 정보를 일부 접근 가능하도록 구현하는 것은 MVP 이후 단계에서 고려.
* **에러 핸들링:**  네트워크 에러,  GPS 에러,  권한 에러 등 다양한 에러 상황에 대한 처리 로직 구현.
* **UI/UX 디자인:**  앱 디자인 가이드라인을 준수하고 사용자 친화적인 인터페이스를 구현.


본 기술 명세서는 MVP 개발에 초점을 맞추고 있으며,  프리미엄 기능 및 추가 기능들은  향후 단계에서 구현될 수 있습니다.  필요에 따라  Google Maps Platform 또는 Naver Maps Platform 중 하나를 선택하여 사용해야 합니다.  또한,  Firebase Authentication을 사용하여 사용자 인증 및 관리 기능을 구현할 수 있습니다.  모든 기능을 완벽하게 구현하는 것은 어려우므로, 우선순위를 정하여 개발해야 합니다.
