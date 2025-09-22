```dart
// lib/services/admob_service.dart
import 'dart:async';
import 'dart:io' show Platform;

import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

class AdMobService {
  // 싱글톤 패턴
  static final AdMobService _instance = AdMobService._internal();
  factory AdMobService() => _instance;
  AdMobService._internal();

  // AdMob 설정
  final Map<String, dynamic> _adMobConfig = {
    "app_name": "mindbreath",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~8408921719",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/84089217191",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/84089217192",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/84089217193"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~84089217194",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/84089217195",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/84089217196",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/84089217197"
    },
    "test_ids": {
      "android_app_id": "ca-app-pub-3940256099942544~3347511713",
      "android_banner": "ca-app-pub-3940256099942544/6300978111",
      "android_interstitial": "ca-app-pub-3940256099942544/1033173712",
      "android_rewarded": "ca-app-pub-3940256099942544/5224354917",
      "ios_app_id": "ca-app-pub-3940256099942544~1458002511",
      "ios_banner": "ca-app-pub-3940256099942544/2934735716",
      "ios_interstitial": "ca-app-pub-3940256099942544/4411468910",
      "ios_rewarded": "ca-app-pub-3940256099942544/1712485313"
    },
    "setup_required": true
  };

  // 플랫폼별 ID 관리
  String get _appId => kReleaseMode
      ? Platform.isAndroid
          ? _adMobConfig['android']['app_id']
          : _adMobConfig['ios']['app_id']
      : Platform.isAndroid
          ? _adMobConfig['test_ids']['android_app_id']
          : _adMobConfig['test_ids']['ios_app_id'];

  String get _bannerAdUnitId => kReleaseMode
      ? Platform.isAndroid
          ? _adMobConfig['android']['banner_ad_unit']
          : _adMobConfig['ios']['banner_ad_unit']
      : Platform.isAndroid
          ? _adMobConfig['test_ids']['android_banner']
          : _adMobConfig['test_ids']['ios_banner'];

  String get _interstitialAdUnitId => kReleaseMode
      ? Platform.isAndroid
          ? _adMobConfig['android']['interstitial_ad_unit']
          : _adMobConfig['ios']['interstitial_ad_unit']
      : Platform.isAndroid
          ? _adMobConfig['test_ids']['android_interstitial']
          : _adMobConfig['test_ids']['ios_interstitial'];

  String get _rewardedAdUnitId => kReleaseMode
      ? Platform.isAndroid
          ? _adMobConfig['android']['rewarded_ad_unit']
          : _adMobConfig['ios']['rewarded_ad_unit']
      : Platform.isAndroid
          ? _adMobConfig['test_ids']['android_rewarded']
          : _adMobConfig['test_ids']['ios_rewarded'];


  // 광고 초기화
  Future<InitializationStatus> initializeAdMob() async {
    MobileAds.instance.initialize();
    return MobileAds.instance.initializationStatus;
  }


  // Banner 광고 로드 및 표시 (수익 최적화를 위해 적절한 위치에 배치)
  BannerAd? _bannerAd;
  Future<void> showBannerAd() async {
    if (_bannerAd != null && _bannerAd!.isLoading) return;
    _bannerAd?.dispose();
    _bannerAd = BannerAd(
      adUnitId: _bannerAdUnitId,
      size: AdSize.banner,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          print('BannerAd loaded.');
        },
        onAdFailedToLoad: (ad, error) {
          print('BannerAd failedToLoad: $error');
          // 재시도 로직 추가 (예: 5초 후 재시도)
          Future.delayed(const Duration(seconds: 5), showBannerAd);
        },
        onAdOpened: (ad) => print('BannerAd opened.'),
        onAdClosed: (ad) => print('BannerAd closed.'),
        onAdImpression: (ad) => print('BannerAd impression.'),
      ),
    );
    await _bannerAd!.load();
  }


  // Interstitial 광고 로드 및 표시 (사용자 경험 고려, 적절한 시점에 표시)
  InterstitialAd? _interstitialAd;
  Future<void> showInterstitialAd() async {
    if (_interstitialAd != null && _interstitialAd!.isLoading) return;
    _interstitialAd?.dispose();
    _interstitialAd = InterstitialAd(
      adUnitId: _interstitialAdUnitId,
      request: const AdRequest(),
      listener: InterstitialAdListener(
        onAdLoaded: (ad) {
          print('InterstitialAd loaded.');
          ad.show();
        },
        onAdFailedToLoad: (ad, error) {
          print('InterstitialAd failedToLoad: $error');
          // 재시도 로직 추가 (예: 5초 후 재시도)
          Future.delayed(const Duration(seconds: 5), showInterstitialAd);
        },
        onAdOpened: (ad) => print('InterstitialAd opened.'),
        onAdClosed: (ad) => print('InterstitialAd closed.'),
        onAdImpression: (ad) => print('InterstitialAd impression.'),
      ),
    );
    await _interstitialAd!.load();
  }


  // Rewarded 광고 로드 및 표시 (보상형 광고, 사용자에게 보상 제공)
  RewardedAd? _rewardedAd;
  Future<void> showRewardedAd() async {
    if (_rewardedAd != null && _rewardedAd!.isLoading) return;
    _rewardedAd?.dispose();
    _rewardedAd = RewardedAd(
      adUnitId: _rewardedAdUnitId,
      request: const AdRequest(),
      listener: RewardedAdListener(
        onAdLoaded: (ad) {
          print('RewardedAd loaded.');
          ad.show();
        },
        onAdFailedToLoad: (ad, error) {
          print('RewardedAd failedToLoad: $error');
          // 재시도 로직 추가 (예: 5초 후 재시도)
          Future.delayed(const Duration(seconds: 5), showRewardedAd);
        },
        onAdOpened: (ad) => print('RewardedAd opened.'),
        onAdClosed: (ad) {
          print('RewardedAd closed.');
          // 보상 지급 로직 추가
        },
        onAdImpression: (ad) => print('RewardedAd impression.'),
        onUserEarnedReward: (ad, reward) {
          print(
              'User earned reward: ${reward.amount} ${reward.type}'); // 보상 처리
        },
      ),
    );
    await _rewardedAd!.load();
  }


  // 광고 제거 (메모리 효율)
  void disposeAds() {
    _bannerAd?.dispose();
    _interstitialAd?.dispose();
    _rewardedAd?.dispose();
  }
}
```

**사용 예시:**

```dart
import 'package:flutter/material.dart';
import 'services/admob_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AdMobService().initializeAdMob(); // AdMob 초기화
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final AdMobService _adMobService = AdMobService();

  @override
  void initState() {
    super.initState();
    _adMobService.showBannerAd(); // Banner 광고 표시
  }

  @override
  void dispose() {
    _adMobService.disposeAds(); // 광고 제거
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mindbreath')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _adMobService.showInterstitialAd(), // Interstitial 광고 표시
              child: const Text('Show Interstitial Ad'),
            ),
            ElevatedButton(
              onPressed: () => _adMobService.showRewardedAd(), // Rewarded 광고 표시
              child: const Text('Show Rewarded Ad'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**중요:**  `XXXXXXXXXX` 부분을 실제 AdMob ID로 바꿔야 합니다.  `pubspec.yaml`에 `google_mobile_ads` 패키지를 추가하고,  Android 및 iOS 설정을 올바르게 구성해야 합니다.  또한,  앱에서 광고 표시 빈도를 조절하여 사용자 경험을 최적화해야 합니다.  예를 들어, 인터스티셜 광고는 게임 레벨을 완료하거나 특정 이벤트 발생 시에만 표시하는 것이 좋습니다.  Rewarded 광고는 사용자가 원하는 경우에만 표시하는 것이 좋습니다.  그리고 항상 AdMob 정책을 준수해야 합니다.
