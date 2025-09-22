# meditation_app Flutter 코드

```yaml
# pubspec.yaml
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
  flutter_riverpod: ^2.3.6 # 상태 관리 추가 (Provider 대신 Riverpod 사용 권장)
  material_design_3: ^0.1.1 # Material Design 3


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0
  build_runner: ^2.4.1 # Riverpod 빌드용
```

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:unsekotpida/ui/screens/home_screen.dart';
import 'package:unsekotpida/ui/themes/app_theme.dart';

void main() {
  runApp(const ProviderScope(child: UnsekOtpidaApp()));
}

class UnsekOtpidaApp extends StatelessWidget {
  const UnsekOtpidaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '운세꽃피다',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system, // 시스템 설정에 따라 테마 변경
      home: const HomeScreen(),
    );
  }
}

// 나머지 파일 (models, services, ui, utils, repositories, providers)은  본문에 명시된 구조와 기능에 맞춰 구현해야 합니다.
// 아래는 각 파일의 간략한 예시이며, 실제 구현에는 많은 코드가 필요합니다.

// lib/models/fortune.dart
class Fortune {
  final String zodiac;
  final String total;
  // ... other properties
  Fortune({required this.zodiac, required this.total, /* ... */});
}

// lib/services/fortune_service.dart
// 운세 API 호출 로직 구현 (http 패키지 사용)

// lib/ui/screens/home_screen.dart
// HomeScreen 위젯 구현 (Provider 사용) -  오늘의 운세, 심리 테스트 추천 목록 표시

// lib/ui/screens/fortune_detail_screen.dart
// 운세 상세 화면 위젯 구현 (Provider 사용)

// lib/ui/screens/test_screen.dart
// 심리 테스트 화면 위젯 구현 (Provider, flutter_screenutil 사용)

// lib/ui/screens/result_screen.dart
// 결과 화면 위젯 구현 (Provider 사용)

// lib/ui/screens/settings_screen.dart
// 설정 화면 위젯 구현 (Provider, shared_preferences, flutter_local_notifications 사용)

// lib/ui/widgets/fortune_card.dart
// 운세 카드 위젯 구현

// lib/ui/widgets/test_question.dart
// 심리 테스트 질문 위젯 구현

// lib/ui/themes/app_theme.dart
// 어플리케이션 테마 정의 (다크 모드 지원)

// lib/utils/constants.dart
// 상수 정의

// lib/repositories/fortune_repository.dart
// 운세 데이터 접근 로직 구현 (API 또는 데이터베이스)

// lib/repositories/test_repository.dart
// 심리 테스트 데이터 접근 로직 구현 (데이터베이스 또는 Firestore)

// lib/providers/fortune_provider.dart
// Riverpod를 사용한 운세 데이터 상태 관리

// lib/providers/test_provider.dart
// Riverpod를 사용한 심리 테스트 데이터 상태 관리


//  위에 간략하게 작성된 파일들을 실제로 구현해야 완전한 애플리케이션이 됩니다.  각 파일은 복잡한 로직과 코드를 포함하게 될 것입니다.
//  이 예시는  main.dart 파일과  필요한 import 문, 그리고 각 파일의 목적을 보여주기 위한 것입니다.  상세한 구현은  기술 명세서에 따라 개발자가 직접 작성해야 합니다.
```

**중요:** 위 코드는 `main.dart` 파일의 기본 구조와 몇 가지 모델 클래스의 예시만 제공합니다.  실제 앱을 구현하려면  기술 명세서에 따라  나머지 파일들을 모두 구현해야 합니다.  특히,  Firebase 연동, API 호출, 데이터베이스 관리,  상태 관리,  위젯 구현 등은 상당한 시간과 노력을 필요로 하는 작업입니다.  Riverpod를 사용하여 Provider보다 더 효율적인 상태 관리를 권장합니다.  각 위젯의 디자인과 기능은 Material Design 3 가이드라인을 따르도록 구현해야 합니다.  또한, 에러 핸들링과 로딩 표시를 적절히 구현하여 사용자 경험을 향상시켜야 합니다.  이 코드는  완성된 앱이 아니며,  개발자가 직접 구현해야 하는 부분이 매우 많습니다.
