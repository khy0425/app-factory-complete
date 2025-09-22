# momento 기술 명세서

## Flutter 프로젝트 구조

- **패키지명:** com.reaf.momento
- **필요한 dependencies:** (pubspec.yaml)

```yaml
name: momento
description: A minimal and beautiful diary app.
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
  sqflite: ^2.0.2
  path_provider: ^2.0.11
  image_picker: ^1.0.0
  cached_network_image: ^3.2.3
  flutter_staggered_grid_view: ^1.0.0 # 사진 그리드뷰
  provider: ^6.0.5 # 상태 관리 (Provider 사용 권장)
  intl: ^0.18.1 # 날짜/시간 국제화
  cupertino_icons: ^1.0.2
  flutter_datetime_picker: ^1.5.1 # 날짜 선택
  image_cropper: ^1.0.0 # 사진 자르기

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
├── models/
│   ├── diary_entry.dart
│   └── ...
├── screens/
│   ├── home_screen.dart
│   ├── diary_entry_screen.dart
│   ├── settings_screen.dart
│   └── ...
├── services/
│   ├── database_service.dart
│   └── ...
├── widgets/
│   ├── custom_app_bar.dart
│   ├── diary_card.dart
│   └── ...
├── utils/
│   ├── date_utils.dart
│   └── ...
└── ...
```


## 화면별 구현 상세

**1. 홈 화면 (HomeScreen):**

- **위젯 구조:** `Scaffold` + `CustomAppBar` + `CalendarView` (월별, 주별, 일별 보기 전환 기능 포함) + `DiaryEntryList` (각 날짜에 작성된 일기 요약 미리보기)
- **상태 관리 방식:** `Provider`를 이용하여 일기 목록과 현재 선택된 날짜를 관리.
- **필요한 패키지들:** `provider`, `flutter_calendar_carousel` (혹은 유사 패키지), `intl`


**2. 일기 작성 화면 (DiaryEntryScreen):**

- **위젯 구조:** `Scaffold` + `AppBar` + `TextField` (자동 저장 기능 구현) + `ImagePicker` + `ImageCropper` + `EmojiPicker` (이모티콘 선택 기능) + 키워드 제시 기능 (SuggestionChip)
- **상태 관리 방식:** `Provider`를 이용하여 입력 내용, 사진, 이모티콘 등을 관리.
- **필요한 패키지들:** `provider`, `image_picker`, `image_cropper`, `flutter_emoji`, `flutter_chips_input` (혹은 유사 패키지)


**3. 설정 화면 (SettingsScreen):**

- **위젯 구조:** `Scaffold` + `AppBar` + `SwitchListTile` (알림 설정) + `DropdownButton` (테마 변경)
- **상태 관리 방식:** `Provider` 또는 `setState`
- **필요한 패키지들:** `provider` (권장)


## 데이터 모델

- **DiaryEntry 클래스:**

```dart
import 'package:flutter/material.dart';

class DiaryEntry {
  final int id;
  final DateTime date;
  final String content;
  final List<String> imagePaths; // 사진 경로 리스트
  final List<String> emojis;     // 이모지 리스트

  DiaryEntry({
    required this.id,
    required this.date,
    required this.content,
    this.imagePaths = const [],
    this.emojis = const [],
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'date': date.toIso8601String(),
      'content': content,
      'imagePaths': imagePaths.join(','), // CSV 형식으로 저장
      'emojis': emojis.join(','),       // CSV 형식으로 저장
    };
  }

  factory DiaryEntry.fromMap(Map<String, dynamic> map) {
    return DiaryEntry(
      id: map['id'],
      date: DateTime.parse(map['date']),
      content: map['content'],
      imagePaths: map['imagePaths'].toString().split(','),
      emojis: map['emojis'].toString().split(','),
    );
  }
}
```

- **데이터베이스 스키마 (sqflite):**

```sql
CREATE TABLE diary_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  content TEXT,
  imagePaths TEXT,
  emojis TEXT
);
```

- **API 연동 방식:**  MVP 단계에서는 로컬 데이터베이스만 사용.


## 권한 및 설정

- **AndroidManifest.xml:**

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

- iOS 권한 설정:  Info.plist 파일에 카메라와 사진 접근 권한 추가.


## 핵심 기능 구현 방법

| 기능 | 사용할 Flutter 패키지 | 구현 난이도 (1-5) | 예상 개발 시간 |
|---|---|---|---|
| 일기 작성 | `provider`, `intl` | 2 | 2일 |
| 사진 첨부 | `image_picker`, `image_cropper` | 3 | 3일 |
| 달력 보기 | `table_calendar` (혹은 유사 패키지) | 2 | 2일 |
| SQLite 데이터베이스 연동 | `sqflite`, `path_provider` | 3 | 3일 |
| 자동 저장 | `provider`, `Timer` | 2 | 1일 |
| 키워드 제시 |  `flutter_chips_input` | 2 | 2일 |


## 테스트 계획

- **단위 테스트:**  `DiaryEntry` 클래스, 데이터베이스 관련 함수 등.
- **통합 테스트:**  각 화면의 기능 테스트 (일기 작성, 사진 첨부, 달력 보기 등).  UI 테스트 프레임워크 (Flutter Driver) 활용 고려.
- **사용자 테스트:** 베타 테스터 모집을 통해 실제 사용자 피드백 수집.


**참고:**  위 기술 명세서는 MVP 단계에 초점을 맞추었습니다. 프리미엄 기능 및 추가 기능들은 2, 3단계 개발 계획에 따라 세부적으로 기술 명세를 보완해야 합니다.  또한,  특정 패키지의 선택은 여러 대안이 있을 수 있으며, 프로젝트의 특성 및 개발자의 선호도에 따라 조정될 수 있습니다.  `provider` 외에 `riverpod`, `bloc` 등 다른 상태 관리 패키지를 사용할 수도 있습니다.  각 패키지에 대한 최신 버전 확인 및 사용법 숙지는 필수입니다.
