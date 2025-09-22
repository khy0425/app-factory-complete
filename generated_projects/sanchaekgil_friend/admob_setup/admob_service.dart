```dart
// lib/services/admob_service.dart
import 'dart:async';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

class AdMobService {
  static final AdMobService _instance = AdMobService._internal();

  factory AdMobService() {
    return _instance;
  }

  AdMobService._internal();

  // AdMob 설정 (실제 ID로 교체 필요!)
  final Map<String, dynamic> _adMobConfig = {
    "app_name": "sanchaekgil_friend",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~7110397660",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/71103976601",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/71103976602",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/71103976603"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~71103976604",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/71103976605",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/71103976606",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/71103976607"
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

  String get _appId => kReleaseMode
      ? _getPlatformAppId()
      : _adMobConfig["test_ids"][Platform.isAndroid ? 'android_app_id' : 'ios_app_id'];

  String _getPlatformAppId() {
    return Platform.isAndroid
        ? _adMobConfig["android"]["app_id"]
        : _adMobConfig["ios"]["app_id"];
  }


  String get _bannerAdUnitId => kReleaseMode
      ? _getPlatformAdUnitId('banner')
      : _adMobConfig["test_ids"][Platform.isAndroid ? 'android_banner' : 'ios_banner'];

  String _getPlatformAdUnitId(String adType) {
    return Platform.isAndroid
        ? _adMobConfig["android"]['$adType\_ad\_unit']
        : _adMobConfig["ios"]['$adType\_ad\_unit'];
  }


  String get _interstitialAdUnitId => kReleaseMode
      ? _getPlatformAdUnitId('interstitial')
      : _adMobConfig["test_ids"][Platform.isAndroid ? 'android_interstitial' : 'ios_interstitial'];


  String get _rewardedAdUnitId => kReleaseMode
      ? _getPlatformAdUnitId('rewarded')
      : _adMobConfig["test_ids"][Platform.isAndroid ? 'android_rewarded' : 'ios_rewarded'];

  // 광고 초기화
  Future<InitializationStatus> initializeAdMob() async {
    MobileAds.instance.initialize();
    return MobileAds.instance.initializationStatus;
  }


  // Banner 광고 로드 및 표시
  BannerAd? _bannerAd;
  Future<void> showBannerAd(BuildContext context) async {
    if (_bannerAd != null && _bannerAd!.isLoading) return;
    if (_bannerAd != null && _bannerAd!.isValid) return;
    _bannerAd?.dispose();

    _bannerAd = BannerAd(
      adUnitId: _bannerAdUnitId,
      size: AdSize.banner,
      request: AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          print('BannerAd loaded.');
        },
        onAdFailedToLoad: (ad, error) {
          print('BannerAd failedToLoad: $error');
          // 재시도 로직 (예: 5초 후 재시도)
          Future.delayed(const Duration(seconds: 5), () => showBannerAd(context));
        },
        onAdOpened: (ad) => print('BannerAd opened.'),
        onAdClosed: (ad) => print('BannerAd closed.'),
        onAdImpression: (ad) => print('BannerAd impression.'),
      ),
    );

    _bannerAd!.load();
  }

  //Interstitial 광고
  InterstitialAd? _interstitialAd;
  Future<void> loadInterstitialAd() async {
    _interstitialAd?.dispose();
    InterstitialAd.load(
        adUnitId: _interstitialAdUnitId,
        request: AdRequest(),
        adLoadCallback: InterstitialAdLoadCallback(
          onAdLoaded: (InterstitialAd ad) {
            _interstitialAd = ad;
            print('InterstitialAd loaded');
            _interstitialAd?.show();
          },
          onAdFailedToLoad: (LoadAdError error) {
            print('InterstitialAd failed to load: $error');
          },
        ));
  }

  //Rewarded 광고
  RewardedAd? _rewardedAd;
  Future<void> loadRewardedAd() async {
    _rewardedAd?.dispose();
    RewardedAd.load(
        adUnitId: _rewardedAdUnitId,
        request: AdRequest(),
        rewardedAdLoadCallback: RewardedAdLoadCallback(
          onAdLoaded: (RewardedAd ad) {
            _rewardedAd = ad;
            print('RewardedAd loaded');
          },
          onAdFailedToLoad: (LoadAdError error) {
            print('RewardedAd failed to load: $error');
          },
        ));
  }

  Future<void> showRewardedAd() async {
    if (_rewardedAd == null) {
      print('RewardedAd not loaded');
      return;
    }
    _rewardedAd!.show(onUserEarnedReward: (ad, reward) {
      print('User earned reward');
    });
    _rewardedAd = null; // Showed, needs reloading.
  }


  // 광고 폐기
  void disposeAds() {
    _bannerAd?.dispose();
    _interstitialAd?.dispose();
    _rewardedAd?.dispose();
  }
}
```

**사용 예시:**

```dart
// main.dart or other widget
import 'package:flutter/material.dart';
import 'services/admob_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AdMobService().initializeAdMob();
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
    _adMobService.showBannerAd(context); // 앱 시작 시 배너 광고 표시
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Sanchaekgil Friend'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () {
                _adMobService.loadInterstitialAd();
              },
              child: Text('Interstitial 광고 표시'),
            ),
            ElevatedButton(
              onPressed: () {
                _adMobService.loadRewardedAd();
                _adMobService.showRewardedAd();
              },
              child: Text('보상형 광고 표시'),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _adMobService.disposeAds();
    super.dispose();
  }
}
```

**중요:** 위 코드는  `pubspec.yaml`에 `google_mobile_ads` 패키지를 추가해야 작동합니다.  `flutter pub get` 명령어를 실행하여 패키지를 설치하세요. 또한 실제 AdMob ID로  `_adMobConfig`  내용을 반드시 교체해야 합니다.  광고 표시 빈도 제한 및 수익 최적화 전략은 앱의 사용 패턴과 목표에 따라 추가적인 로직을 구현해야 합니다.  예를 들어, `SharedPreferences`를 사용하여 광고 표시 횟수를 추적하고 제한할 수 있습니다.  Interstitial 광고는 특정 이벤트 발생 시에만 표시하도록 하는 등의 전략이 필요합니다.