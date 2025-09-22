# mindbreath 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** com.reaf.mindbreath
- **필요한 dependencies:** (pubspec.yaml)

```yaml
name: mindbreath
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
  intl: ^0.17.0 # 국제화
  sqflite: ^2.0.2+1 # 로컬 데이터베이스
  path_provider: ^2.0.11 # 로컬 저장소 경로 접근
  audioplayers: ^1.0.0 # 오디오 재생
  vibration: ^1.0.0 # 진동 피드백
  flutter_svg: ^2.0.5 # SVG 아이콘 사용 (선택)
  provider: ^6.0.5 # 상태 관리 (Provider 패턴)
  charts_flutter: ^0.13.0 # 차트 그래프 표시 (선택, 다른 차트 라이브러리 사용 가능)
  google_fonts: ^5.0.0 # 구글 폰트 (선택)


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0


flutter:
  uses-material-design: true
  assets:
    - assets/audios/ # 명상 오디오 파일
    - assets/images/ # 이미지 파일
```

- **폴더 구조:** (lib 폴더 내부)

```
lib/
├── models/       # 데이터 모델
├── services/     # 데이터베이스, API 연동 등 서비스 로직
├── ui/          # UI 관련 위젯 및 화면
│   ├── screens/  # 각 화면별 위젯
│   │   ├── home/
│   │   ├── meditation/
│   │   ├── breathing/
│   │   ├── record/
│   │   └── settings/
│   └── widgets/  # 공통적으로 사용하는 위젯
├── main.dart     # 메인 함수
├── app_theme.dart # 앱 테마
├── routes.dart   # 라우팅 관리
└── ...
```


## 화면별 구현 상세

**1. 홈 화면 (Home Screen):**

- **위젯 구조:** `Scaffold` - `AppBar` - `Column` (오늘의 추천, 일일 기록 요약, 프리미엄 기능 안내)
- **상태 관리 방식:** `Provider` 를 이용하여 오늘의 추천 명상/호흡 연습 데이터 관리
- **필요한 패키지들:** `flutter`, `provider`, `flutter_svg` (아이콘 사용 시)

**2. 명상 화면 (Meditation Screen):**

- **위젯 구조:** `Scaffold` - `AppBar` - `Column` (오디오 플레이어, 타이머, 배경음악 조절 슬라이더)
- **상태 관리 방식:** `Provider` 를 이용하여 재생 상태, 타이머, 볼륨 관리
- **필요한 패키지들:** `flutter`, `provider`, `audioplayers`

**3. 호흡 연습 화면 (Breathing Screen):**

- **위젯 구조:** `Scaffold` - `AppBar` - `Column` (호흡법 선택, 진동 피드백 토글, 타이머, 애니메이션)
- **상태 관리 방식:** `Provider` 를 이용하여 호흡 속도, 시간, 진동 설정, 타이머 관리
- **필요한 패키지들:** `flutter`, `provider`, `vibration`

**4. 기록 화면 (Record Screen):**

- **위젯 구조:** `Scaffold` - `AppBar` - `Column` (차트, 통계 정보)
- **상태 관리 방식:** `Provider` 를 이용하여 데이터 로딩 및 표시
- **필요한 패키지들:** `flutter`, `provider`, `charts_flutter` (또는 다른 차트 라이브러리)

**5. 설정 화면 (Settings Screen):**

- **위젯 구조:** `Scaffold` - `AppBar` - `ListView` (설정 항목들)
- **상태 관리 방식:** `Provider` 또는 `StatefulWidget`
- **필요한 패키지들:** `flutter`, `provider`


## 데이터 모델

- **Meditation:** `id`, `title`, `description`, `duration`, `audioPath`, `theme`
- **BreathingExercise:** `id`, `title`, `description`, `inhaleDuration`, `holdDuration`, `exhaleDuration`
- **Record:** `date`, `meditationId`, `breathingExerciseId`, `duration`

- **데이터베이스 스키마 (sqflite):**

```sql
CREATE TABLE meditations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  duration INTEGER NOT NULL,
  audioPath TEXT NOT NULL,
  theme TEXT
);

CREATE TABLE breathingExercises (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  inhaleDuration INTEGER NOT NULL,
  holdDuration INTEGER NOT NULL,
  exhaleDuration INTEGER NOT NULL
);

CREATE TABLE records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date INTEGER NOT NULL,
  meditationId INTEGER,
  breathingExerciseId INTEGER,
  duration INTEGER NOT NULL,
  FOREIGN KEY (meditationId) REFERENCES meditations(id),
  FOREIGN KEY (breathingExerciseId) REFERENCES breathingExercises(id)
);
```

- **API 연동 방식:**  (필요시) HTTP 패키지를 사용하여 음악 스트리밍 API와 통신.


## 권한 및 설정

- **AndroidManifest.xml:**

```xml
<uses-permission android:name="android.permission.VIBRATE" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" /> # 오디오 저장시 필요
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/> # 오디오 저장시 필요 (Android 10 이상)
```

- **iOS 권한 설정:**  Info.plist에 진동 및 저장 공간 접근 권한 추가.


## 핵심 기능 구현 방법

| 기능           | 사용할 Flutter 패키지 | 구현 난이도 (1-5) | 예상 개발 시간 (일) |
|-----------------|----------------------|-------------------|---------------------|
| 가이드 명상       | audioplayers          | 3                   | 7                    |
| 호흡 연습       | vibration             | 2                   | 5                    |
| 일일 기록        | sqflite, provider     | 3                   | 7                    |
| 진동 피드백     | vibration             | 1                   | 2                    |
| 오디오 재생      | audioplayers          | 2                   | 3                    |
| 차트 그래프 표시 | charts_flutter        | 3                   | 5                    |
| 데이터베이스 관리 | sqflite, path_provider | 3                   | 7                    |
| 사용자 계정 시스템 | Firebase Auth (선택) | 4                   | 10                   |
| 프리미엄 구독 기능 | In-app purchase       | 5                   | 14                   |


## 테스트 계획

- **단위 테스트 대상:** 각 모델 클래스, 데이터베이스 액세스 함수, API 연동 함수
- **통합 테스트 시나리오:** 각 화면의 기능 테스트, 데이터베이스 연동 테스트, API 연동 테스트, 진동 피드백 테스트
- **사용자 테스트 계획:** 베타 테스트를 통해 사용자 피드백 수집, UI/UX 개선


**참고:** 위 기술 명세서는 MVP 개발에 초점을 맞추고 있습니다.  프리미엄 기능, 개인 맞춤형 추천 알고리즘, 커뮤니티 기능 등은  2단계, 3단계 개발에서 자세히 설계 및 구현해야 합니다.  Firebase, AWS Amplify 와 같은 백엔드 서비스 사용을 고려할 수 있습니다. 또한, 성능 최적화를 위해 이미지, 오디오 파일 최적화 및 필요 없는 위젯 제거 등을 고려해야 합니다.  애니메이션 효과는 성능에 영향을 미칠 수 있으므로 최적화된 방식으로 구현해야 합니다.
