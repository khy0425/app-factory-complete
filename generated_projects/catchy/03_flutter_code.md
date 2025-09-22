# catchy Flutter 코드

## pubspec.yaml

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
  provider: ^6.0.5 # 상태 관리 (Provider 패턴 사용)
  flutter_riverpod: ^2.3.6 # 상태 관리 (Riverpod 패턴 사용 - 선택사항)


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0
  build_runner: ^2.2.0
  json_serializable: ^6.4.4 # json 데이터 처리를 위한 라이브러리 (추가)


```

## main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:tajawang/screens/home_screen.dart';
import 'package:tajawang/theme/app_theme.dart'; // 추가: 테마 파일 import


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider( // Provider를 사용하여 상태 관리 시작
      providers: [
        // 여기에 필요한 Provider들을 추가합니다. 예:
        // ChangeNotifierProvider(create: (_) => GameData()),
        // ChangeNotifierProvider(create: (_) => SettingsData()),
      ],
      child: GetMaterialApp( // GetX 사용
        title: '타자왕',
        theme: AppTheme.lightTheme, // 라이트 테마 설정 (AppTheme.dart에서 정의)
        darkTheme: AppTheme.darkTheme, // 다크 테마 설정 (AppTheme.dart에서 정의)
        themeMode: ThemeMode.system, // 시스템 테마 모드 사용
        localizationsDelegates: const [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        supportedLocales: const [
          Locale('ko', 'KR'), // 한국어 지원
        ],
        home: const HomeScreen(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}

```

**주의:** 위 코드는 `main.dart` 파일의 기본 구조와 Provider 패턴을 사용하는 예시입니다.  `home_screen.dart` 와 다른 화면 파일들,  데이터 모델(`models` 폴더),  서비스(`services` 폴더),  그리고 `AppTheme.dart` 파일은  직접 구현해야 합니다.  `AppTheme.dart` 파일에서는 Material Design 3 스타일을 적용한 밝은 테마와 어두운 테마를 정의해야 합니다. 또한,  `provider` 패키지를 사용하여 상태 관리를 구현하도록 모든 화면의 상태 관리 로직을 수정해야 합니다. `json_serializable` 패키지를 사용하여 json 데이터 처리를 위한 작업도 추가로 필요합니다.  데이터베이스 연결 및 다른 기능들은  각 파일의 구현 내용에 따라 달라집니다.  이 예시는 기본적인 구조를 제공하며,  실제 구현은  제공된 명세서를 바탕으로  개발자가 직접 완성해야 합니다.  특히,  각 화면의 위젯 구성과 상태 관리 구현에 대한 자세한 코드는 생략되어 있습니다.  Riverpod를 사용하는 경우, `provider` 대신 `flutter_riverpod`를 사용하고, provider 설정을 Riverpod 방식으로 변경해야 합니다.


이 응답은  제공된 명세서를 충족하는  `main.dart` 파일의 템플릿을 제공합니다.  실제 앱을 개발하려면  각 화면, 서비스, 모델, 유틸리티 함수 등을  개발자가 직접 구현해야 합니다.  이 템플릿을 기반으로  개발을 진행하고,  문제가 발생하면  추가적인 질문을 주시면 도와드리겠습니다.
