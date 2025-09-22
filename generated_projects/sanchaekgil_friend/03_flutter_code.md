# sanchaekgil_friend Flutter 코드

```yaml
# pubspec.yaml
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
  google_maps_flutter: ^2.4.0
  geolocator: ^9.0.0
  shared_preferences: ^2.0.15
  cloud_firestore: ^4.8.3
  firebase_core: ^2.14.0
  firebase_auth: ^4.6.3
  image_picker: ^1.0.0
  path_provider: ^2.0.11
  intl: ^0.18.1
  provider: ^6.0.5
  cached_network_image: ^3.2.3
  url_launcher: ^6.1.12
  flutter_riverpod: ^2.3.6 #추가: Riverpod 상태 관리 (Provider 대신 사용 권장)


dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0


flutter:
  uses-material-design: true
  assets:
    - assets/images/

```

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:sanchaekgilfriend/app.dart'; // app.dart 파일 import
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart'; // firebase_options.dart 파일 생성 후 import


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}


//app.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:sanchaekgilfriend/ui/screens/home_screen.dart';
import 'package:sanchaekgilfriend/ui/screens/course_create_screen.dart';
import 'package:sanchaekgilfriend/ui/screens/course_detail_screen.dart';
import 'package:sanchaekgilfriend/ui/screens/mypage_screen.dart';
// 추가 import 필요에 따라 추가

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '산책길 친구',
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.light,
        primarySwatch: Colors.blue,
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        primarySwatch: Colors.blue,
      ),
      themeMode: ThemeMode.system, // 시스템 설정에 따라 다크 모드/라이트 모드 변경
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
        '/createCourse': (context) => const CourseCreateScreen(),
        '/courseDetail': (context) => const CourseDetailScreen(),
        '/mypage': (context) => const MyPageScreen(),
      },
    );
  }
}

```

**중요:** 위 코드는 기본적인 `main.dart` 와 `app.dart` 파일의 구조만 제공합니다.  `HomeScreen`, `CourseCreateScreen`, `CourseDetailScreen`, `MyPageScreen`  등의 UI 파일과  `models`, `services` 폴더 내부의 파일들은  기술 명세서에 따라 별도로 구현해야 합니다.  또한 Firebase 프로젝트 설정 및  `firebase_options.dart` 파일 생성도 필요합니다.  위 코드를 실행하려면 모든 필요한 파일들이 제대로 구현되어 있어야 합니다.  특히  `google_maps_flutter` 의 API 키 설정을 잊지 마세요.  이 예제는  `provider` 대신  `flutter_riverpod` 를 사용하는 것이 더욱 효율적이고 관리하기 쉬우므로,  `flutter_riverpod` 를 추가하였습니다.  `provider`를 사용하시려면 `flutter_riverpod` 관련 부분을 제거하고 `provider` 를 사용하는 코드로 변경해야 합니다.  또한,  실제 데이터베이스 연동 및 지도 API 연동을 위해서는 추가적인 코드가 필요합니다.  이 코드는 기본적인 틀을 제공하며,  실제 개발에는 많은 추가 작업이 필요합니다.
