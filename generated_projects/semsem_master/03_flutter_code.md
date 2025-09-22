# semsem_master Flutter 코드

```yaml
# pubspec.yaml
name: semsem_master
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
  intl: ^0.17.0
  sqflite: ^2.0.2+1
  path_provider: ^2.0.11
  provider: ^6.0.5
  flutter_test:
    sdk: flutter
  flutter_svg: ^2.0.6
  google_fonts: ^5.2.0
  shared_preferences: ^2.1.1
  vibration: ^1.0.1
  flutter_riverpod: ^2.3.6 # 상태 관리 추가 (Provider와 함께 사용 가능)
  cupertino_icons: ^1.0.2 # cupertino 아이콘 사용을 위한 추가


dev_dependencies:
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
```

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';
import 'package:semsem_master/screens/home_screen.dart'; // 홈 화면 import
import 'package:semsem_master/screens/practice_screen.dart'; // 연습 화면 import
import 'package:semsem_master/screens/game_screen.dart'; // 게임 화면 import
import 'package:semsem_master/screens/settings_screen.dart'; // 설정 화면 import
import 'package:semsem_master/services/database_service.dart'; // 데이터베이스 서비스 import
import 'package:flutter_riverpod/flutter_riverpod.dart'; // Riverpod 추가


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Provider<DatabaseService>(
      create: (context) => DatabaseService(), // 데이터베이스 서비스 생성
      child: ChangeNotifierProvider(
        create: (context) => DatabaseService(),
        child: MaterialApp(
          title: '셈셈 마스터',
          theme: ThemeData(
            brightness: Brightness.light,
            primarySwatch: Colors.blue,
            fontFamily: 'NotoSansKR', // 또는 원하는 폰트 지정
          ),
          darkTheme: ThemeData(
            brightness: Brightness.dark,
            primarySwatch: Colors.blue,
            fontFamily: 'NotoSansKR', // 또는 원하는 폰트 지정
          ),
          themeMode: ThemeMode.system, // 시스템 기본값 따라감.
          localizationsDelegates: const [
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('ko', 'KR'), // 한국어 지원
          ],
          home: const HomeScreen(), // 홈 화면으로 시작
          routes: {
            '/practice': (context) => const PracticeScreen(),
            '/game': (context) => const GameScreen(),
            '/settings': (context) => const SettingsScreen(),
          },
        ),
      ),
    );
  }
}

```

**주의:** 위 코드는 기본적인 구조만 제공하며, 실제 작동하는 앱을 만들기 위해서는 `home_screen.dart`, `practice_screen.dart`, `game_screen.dart`, `settings_screen.dart`, `database_service.dart`,  모델 클래스 (`user.dart`, `exercise_record.dart`, `game_record.dart`) 등의 파일을 추가로 구현해야 합니다.  데이터베이스 생성 및 연동,  상태 관리 로직,  UI 디자인 등 많은 부분을 추가로 구현해야 완전한 앱이 됩니다.  특히 데이터베이스 관련 부분은 에러 처리 및 최적화가 필요합니다.  또한,  진동 권한 처리도 추가해야 합니다.  이 예제는  MVP 수준의 기본적인 구조를 제공하는 것에 불과하다는 점을 유의하십시오.  실제 개발은 이 예제를 기반으로 더욱 확장해야 합니다.  `flutter_riverpod`는 추가적인 상태 관리를 위해 포함되었지만,  `provider`와 함께 사용하거나 `provider`만 사용하도록 선택할 수 있습니다.
