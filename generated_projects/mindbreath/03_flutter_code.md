# mindbreath Flutter 코드

```yaml
# pubspec.yaml
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
  intl: ^0.17.0
  sqflite: ^2.0.2+1
  path_provider: ^2.0.11
  audioplayers: ^1.0.0
  vibration: ^1.0.0
  flutter_svg: ^2.0.5
  provider: ^6.0.5
  charts_flutter: ^0.13.0
  google_fonts: ^5.0.0
  flutter_riverpod: ^2.0.0 # 추가: Riverpod 상태 관리 (Provider 대신 사용 가능)


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0


flutter:
  uses-material-design: true
  assets:
    - assets/audios/
    - assets/images/
```

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:mindbreath/app_theme.dart';
import 'package:mindbreath/routes.dart';
import 'package:mindbreath/ui/screens/home/home_screen.dart';
import 'package:provider/provider.dart'; // Provider 사용
import 'package:flutter_riverpod/flutter_riverpod.dart'; // Riverpod 사용 (Provider 대신)

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => AppTheme(), // AppTheme Provider 추가
      child:  ProviderScope( // Riverpod 사용시 ProviderScope 사용
          child: MaterialApp(
        title: 'MindBreath',
        theme: Provider.of<AppTheme>(context).lightTheme, // 테마 적용
        darkTheme: Provider.of<AppTheme>(context).darkTheme, // 다크 테마 적용
        themeMode: ThemeMode.system, // 시스템 테마 모드 따라감
        debugShowCheckedModeBanner: false,
        localizationsDelegates: const [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        supportedLocales: const [
          Locale('ko', 'KR'), // 한국어 지원
        ],
        initialRoute: '/',
        routes: routes,
        home: const HomeScreen(),
      ),
    ));
  }
}
```

**참고:** 위 코드는 `main.dart` 파일의 기본 구조와 앱 실행을 위한 필수 부분만 포함하고 있습니다.  `routes.dart`, `app_theme.dart`,  `ui` 폴더 안의 화면 위젯들(HomeScreen, MeditationScreen, BreathingScreen, RecordScreen, SettingsScreen)과 모델, 서비스 클래스들은  설계된 구조에 따라 별도로 구현해야 합니다.  데이터베이스 연동, 오디오 재생, 진동 등 기능 구현은  각 패키지의 문서를 참고하여 코드를 작성해야 합니다.  특히, 데이터베이스 스키마 생성 및 데이터 관리 부분은  `sqflite` 패키지 사용법을 숙지하고 구현해야 합니다.  상태관리 방식은 Provider를 기본으로 하였지만, Riverpod로 변경하여 사용할 수 있습니다.  (Riverpod 사용 시, `provider` dependency는 제거하고 `flutter_riverpod` dependency를 추가해야 합니다.  그리고 `ChangeNotifierProvider` 대신 `ProviderScope` 위젯을 사용하고, Provider 사용 방식을 Riverpod 방식으로 변경해야 합니다.)  이 예제는 완전한 앱 코드가 아니며, 각 기능을 구현하기 위한 기본 틀을 제공합니다.  실제 앱 개발에는 더 많은 코드와 세부적인 구현이 필요합니다.  각 화면과 기능에 대한 상세한 위젯 구성과 로직은  기술 명세서에 제시된 내용을 바탕으로 구현해야 합니다.


이 답변은  기술 명세서에 명시된 요구사항을 충족하는 `main.dart` 파일의 기본 틀을 제공합니다.  실제로 작동하는 완전한 앱을 구현하려면,  각 화면과 기능에 대한  상세한 코드 구현이 필요합니다.  각 기능에 대한 구현은  제공된 기술 명세서와 사용할 패키지의 문서를 참고하여 개발해야 합니다.
