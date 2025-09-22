# stepup Flutter 코드

```yaml
# pubspec.yaml
name: stepup
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
  intl: ^0.17.0
  sqflite: ^2.0.2+1
  path_provider: ^2.0.11
  charts_flutter: ^0.13.0
  permission_handler: ^10.0.0
  flutter_local_notifications: ^11.0.0
  provider: ^6.0.5
  sensors_plus: ^2.0.0 # 추가
  flutter_riverpod: ^2.0.0 # Riverpod 사용시 추가 (Provider와 함께 사용하지 마세요)

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
  generate: true
```

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart'; // Provider 사용
import 'package:stepup/main_app.dart';

void main() {
  runApp(
    ChangeNotifierProvider( // Provider 초기화
      create: (context) => MainAppState(), // MainAppState는 아래에 정의합니다.
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'StepUp',
      theme: ThemeData(
        useMaterial3: true, // Material Design 3 사용
        brightness: Brightness.light,
        primarySwatch: Colors.blue,
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        primarySwatch: Colors.blue,
      ),
      themeMode: ThemeMode.system, // 시스템 설정에 따른 다크 모드 적용
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('ko', 'KR'), // 한국어 지원
      ],
      home: const MainApp(),
    );
  }
}

// MainAppState 클래스 (상태 관리) - 필요한 데이터들을 추가하고 관리합니다.
class MainAppState extends ChangeNotifier {
  //여기에 필요한 변수들 추가 예시 (데이터베이스 연결, 사용자 프로필 등)
}
```

**중요:** 위 코드는 `main.dart` 파일의 기본 구조와 필요한 import 문, Provider 설정을 보여줍니다.  `main_app.dart`, `home_screen.dart`, `history_screen.dart`, `settings_screen.dart`,  그리고 각 서비스 및 모델 클래스를 구현해야 실제로 동작하는 앱이 됩니다.  특히, 계단 카운팅(`sensors_plus`), 데이터베이스(`sqflite`, `path_provider`), 알림(`flutter_local_notifications`) 기능은 상당한 분량의 코드가 필요하므로,  본 답변에서는 기본적인 프로젝트 구조와 상태 관리 부분만 제공합니다.  각 기능을 구현하려면 해당 패키지의 문서를 참조하고,  제공된 기술 명세서를 바탕으로 코드를 작성해야 합니다.  또한  `MainAppState` 클래스에 필요한 데이터들을 추가하고 관리해야 합니다.  Riverpod를 사용하려면 `provider` 패키지를 제거하고 `flutter_riverpod`를 추가하며,  Provider 사용 방식을 Riverpod 방식으로 변경해야 합니다.  각 화면(home, history, settings)도 각각 파일로 만들어서 구현해야 합니다.  이 예시는 단지 시작점일 뿐입니다.  실제 앱 개발에는 훨씬 많은 코드와 노력이 필요합니다.
