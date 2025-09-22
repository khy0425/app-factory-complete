# calm_breath Flutter 코드

```yaml
# pubspec.yaml
name: maumsum
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
  provider: ^6.0.5
  path_provider: ^2.0.11
  sqflite: ^2.0.2
  just_audio: ^0.9.3
  audio_session: ^1.0.0
  flutter_svg: ^2.0.6
  intl: ^0.18.1
  shared_preferences: ^2.1.1
  flutter_screenutil: ^5.6.1
  flutter_local_notifications: ^10.0.0 # 알림 추가
  google_fonts: ^5.0.0 # 폰트 추가 (선택)

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/audio/
    - assets/images/

```

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:maumsum/ui/home_screen.dart';
import 'package:provider/provider.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart'; // 화면 크기 반응형 추가

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: const Size(360, 690),
      minTextAdapt: true,
      splitScreenMode: true,
      builder: (context, child) {
        return MaterialApp(
          title: '마음쉼',
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
            useMaterial3: true,
            brightness: Brightness.light, // 밝은 테마
          ),
          darkTheme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
            useMaterial3: true,
            brightness: Brightness.dark, // 어두운 테마
          ),
          themeMode: ThemeMode.system, // 시스템 테마 따라감
          localizationsDelegates: const [
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('ko', 'KR'), // 한국어 추가
          ],
          home: ChangeNotifierProvider(
              create: (context) => HomeScreenViewModel(), // ViewModel 추가
              child: const HomeScreen()),
        );
      },
    );
  }
}

// HomeScreenViewModel (예시)
class HomeScreenViewModel with ChangeNotifier {
  // HomeScreen에서 필요한 데이터나 기능 추가
}
```

**참고:** 위 코드는 `main.dart` 파일과 `pubspec.yaml` 파일의 기본 구조와 필요한 dependency들을 보여줍니다.  `home_screen.dart`, `meditation_list_screen.dart` 등 다른 화면 파일과 모델, 서비스, 위젯, 유틸리티 파일들은  설계 문서에 따라 별도로 구현해야 합니다.  특히,  `sqflite`를 이용한 데이터베이스 관리, `just_audio`를 이용한 오디오 재생, 알림 기능, 진동 기능 등은  각각의 패키지 문서를 참고하여 구현해야 합니다.  또한,  상세한 UI 구현은  Material Design 3 가이드라인을 참고하여 디자인해야 합니다.  이 코드는 완벽하게 작동하는 앱이 아니며,  프로젝트의 기본 구조를 제공하는 예시입니다.  상세한 기능 구현은 추가적인 코딩이 필요합니다.  특히,  `HomeScreenViewModel` 등의 ViewModel 클래스는 상태 관리를 위해 추가적으로 구현해야 합니다.  `flutter_local_notifications` 패키지를 이용한 알림 기능 구현도 추가로 필요합니다.  각 화면에서 필요한 ViewModel을 추가하고, 데이터 바인딩 및 이벤트 처리를 구현해야 합니다.  다크 테마는 `ThemeData`의 `darkTheme` 속성을 이용하여 구현했습니다.


이 답변은  기본적인 파일 구조와 코드를 제공하며,  실제 앱 개발에는  훨씬 많은 코드와 노력이 필요합니다.  각 기능에 대한 상세한 구현은  개발자가 직접 구현해야 합니다.  이 예시는 시작점으로 활용하고,  단계별로 기능을 추가하며 개발하는 것을 권장합니다.
