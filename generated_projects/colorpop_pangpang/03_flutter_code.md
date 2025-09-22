# colorpop_pangpang Flutter 코드

```yaml
# pubspec.yaml
name: colorpop_pangpang
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
  firebase_core: ^2.14.0
  firebase_auth: ^4.6.3
  cloud_firestore: ^4.8.1
  google_mobile_ads: ^2.6.0
  shared_preferences: ^2.1.1
  path_provider: ^2.0.11
  sqflite: ^2.0.2+4
  provider: ^6.0.5
  get: ^4.6.5
  flutter_screenutil: ^5.6.1
  intl: ^0.18.1
  audioplayers: ^2.0.1 # 추가: 사운드 효과를 위한 패키지
  flutter_riverpod: ^2.3.6 # 추가: 더 나은 상태 관리를 위한 Riverpod 사용 (선택사항, provider 대체 가능)


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
```

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:colorpop_pangpang/ui/home_screen.dart';
import 'package:colorpop_pangpang/providers/user_provider.dart';
import 'package:provider/provider.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart'; //firebase_options.dart 파일 생성 후 경로 수정

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider()),
      ],
      child: ScreenUtilInit(
        designSize: const Size(375, 812), // 디자인 크기 설정
        minTextAdapt: true,
        splitScreenMode: true,
        builder: (context, child) {
          return MaterialApp(
            title: 'ColorPop PangPang',
            theme: ThemeData(
              useMaterial3: true,
              brightness: Brightness.light, // 밝은 테마
              primarySwatch: Colors.blue,
              fontFamily: 'NotoSansKR', // 한국어 폰트 적용 (설치 필요)
            ),
            darkTheme: ThemeData(
              useMaterial3: true,
              brightness: Brightness.dark, // 어두운 테마
              primarySwatch: Colors.blue,
              fontFamily: 'NotoSansKR', // 한국어 폰트 적용 (설치 필요)
            ),
            themeMode: ThemeMode.system, // 시스템 설정에 따른 테마 변경
            localizationsDelegates: const [
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            supportedLocales: const [
              Locale('ko', 'KR'), // 한국어 지원
            ],
            home: const HomeScreen(),
          );
        },
      ),
    );
  }
}
```

**중요:** 위 코드는 `main.dart` 파일의 기본 구조와 Firebase 초기화, 테마 설정, 언어 설정을 포함합니다.  `HomeScreen`을 비롯한 다른 파일들은  `lib/ui/` , `lib/models/`, `lib/services/` 등의 폴더에 각각의 기능에 맞게 구현해야 합니다.  또한,  `firebase_options.dart` 파일을 생성하고 Firebase 프로젝트 설정을 완료해야 합니다.  `NotoSansKR` 폰트를 pubspec.yaml에 추가하고 설치해야 한국어 폰트가 적용됩니다.  사운드 효과를 위해 `audioplayers` 패키지를 추가했고, 더욱 강력한 상태 관리를 위해 `flutter_riverpod` 를 추가 했습니다 (provider 대체 가능).  `flutter_riverpod` 를 사용하려면 `provider` 패키지를 제거하고 코드를 수정해야 합니다.  게임 로직과 각 화면의 세부 구현은  설계 문서의 세부 설명을 참고하여 직접 구현해야 합니다.  이 예시는 기본적인 틀을 제공하는 것에 불과하며,  실제 앱 개발에는 상당한 추가 작업이 필요합니다.
