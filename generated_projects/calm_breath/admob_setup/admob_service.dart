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

  // AdMob 설정 (실제 ID로 교체 필요)
  final adMobConfig = {
    "app_name": "calm_breath",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~2459970125",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/24599701251",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/24599701252",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/24599701253"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~24599701254",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/24599701255",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/24599701256",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/24599701257"
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


  String get _appId {
    if (kDebugMode) {
      return Platform.isAndroid
          ? adMobConfig["test_ids"]["android_app_id"]
          : adMobConfig["test_ids"]["ios_app_id"];
    } else {
      return Platform.isAndroid
          ? adMobConfig["android"]["app_id"]
          : adMobConfig["ios"]["app_id"];
    }
  }

  String get _bannerAdUnitId {
    return kDebugMode
        ? Platform.isAndroid
            ? adMobConfig["test_ids"]["android_banner"]
            : adMobConfig["test_ids"]["ios_banner"]
        : Platform.isAndroid
            ? adMobConfig["android"]["banner_ad_unit"]
            : adMobConfig["ios"]["banner_ad_unit"];
  }

  String get _interstitialAdUnitId {
    return kDebugMode
        ? Platform.isAndroid
            ? adMobConfig["test_ids"]["android_interstitial"]
            : adMobConfig["test_ids"]["ios_interstitial"]
        : Platform.isAndroid
            ? adMobConfig["android"]["interstitial_ad_unit"]
            : adMobConfig["ios"]["interstitial_ad_unit"];
  }

  String get _rewardedAdUnitId {
    return kDebugMode
        ? Platform.isAndroid
            ? adMobConfig["test_ids"]["android_rewarded"]
            : adMobConfig["test_ids"]["ios_rewarded"]
        : Platform.isAndroid
            ? adMobConfig["android"]["rewarded_ad_unit"]
            : adMobConfig["ios"]["rewarded_ad_unit"];
  }


  // 광고 초기화
  Future<InitializationStatus> initializeAdMob() async {
    MobileAds.instance.initialize();
    return MobileAds.instance.initializationStatus;
  }


  // Banner 광고 로드 및 표시 (빈도 제한 추가)
  BannerAd? _bannerAd;
  bool _isBannerShowing = false;
  Future<void> showBannerAd() async {
    if (_isBannerShowing) return;
    _isBannerShowing = true;
    _bannerAd = BannerAd(
      adUnitId: _bannerAdUnitId,
      size: AdSize.banner,
      request: AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          _bannerAd?.show(anchorType: AnchorType.bottom);
        },
        onAdFailedToLoad: (ad, error) {
          print('BannerAd failed to load: $error');
          // 재시도 로직 추가 (예: 5초 후 재시도)
          Future.delayed(Duration(seconds: 5), showBannerAd);
          _isBannerShowing = false;
        },
        onAdOpened: (ad) {},
        onAdClosed: (ad) {},
        onAdWillDismissScreen: (ad) {},
        onAdImpression: (ad) {},
      ),
    );
    return _bannerAd?.load();
  }

  //Interstitial 광고 로드 및 표시
  InterstitialAd? _interstitialAd;
  bool _isInterstitialLoaded = false;
  Future<void> loadInterstitialAd() async {
    if (_isInterstitialLoaded) return;
    _interstitialAd = InterstitialAd(
      adUnitId: _interstitialAdUnitId,
      request: AdRequest(),
      listener: InterstitialAdListener(
        onAdLoaded: (ad) {
          _isInterstitialLoaded = true;
          print('InterstitialAd loaded');
        },
        onAdFailedToLoad: (ad, error) {
          print('InterstitialAd failed to load: $error');
          _isInterstitialLoaded = false;
          // 재시도 로직 추가
          Future.delayed(Duration(seconds: 5), loadInterstitialAd);
        },
        onAdOpened: (ad) {},
        onAdClosed: (ad) {
          _isInterstitialLoaded = false;
          loadInterstitialAd(); // 자동으로 다시 로드
        },
        onAdWillDismissScreen: (ad) {},
        onAdImpression: (ad) {},
      ),
    );
    return _interstitialAd?.load();
  }

  Future<void> showInterstitialAd() async {
    if (_isInterstitialLoaded && _interstitialAd != null) {
      _interstitialAd?.show();
    } else {
      print('InterstitialAd not loaded yet.');
    }
  }


  // Rewarded 광고 로드 및 표시
  RewardedAd? _rewardedAd;
  bool _isRewardedLoaded = false;
  Future<void> loadRewardedAd() async {
    if (_isRewardedLoaded) return;
    _rewardedAd = RewardedAd(
      adUnitId: _rewardedAdUnitId,
      request: AdRequest(),
      listener: RewardedAdListener(
        onAdLoaded: (ad) {
          _isRewardedLoaded = true;
          print('RewardedAd loaded');
        },
        onAdFailedToLoad: (ad, error) {
          print('RewardedAd failed to load: $error');
          _isRewardedLoaded = false;
          // 재시도 로직 추가
          Future.delayed(Duration(seconds: 5), loadRewardedAd);
        },
        onAdOpened: (ad) {},
        onAdClosed: (ad) {
          _isRewardedLoaded = false;
          loadRewardedAd(); // 자동으로 다시 로드
        },
        onUserEarnedReward: (ad, reward) {
          print('User earned reward: ${reward.amount} ${reward.type}');
          // 보상 처리 로직 추가
        },
        onAdImpression: (ad) {},
      ),
    );
    return _rewardedAd?.load();
  }

  Future<void> showRewardedAd() async {
    if (_isRewardedLoaded && _rewardedAd != null) {
      _rewardedAd?.show();
    } else {
      print('RewardedAd not loaded yet.');
    }
  }


  // 광고 제거 (메모리 관리)
  void dispose() {
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


void main() {
  WidgetsFlutterBinding.ensureInitialized();
  AdMobService().initializeAdMob(); // AdMob 초기화
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final adMobService = AdMobService();

  @override
  void initState() {
    super.initState();
    adMobService.loadInterstitialAd(); // 앱 시작시 Interstitial 광고 미리 로드
    adMobService.loadRewardedAd(); // 앱 시작시 Rewarded 광고 미리 로드
  }

  @override
  void dispose(){
    adMobService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Calm Breath')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(onPressed: () => adMobService.showBannerAd(), child: Text('Show Banner Ad')),
              ElevatedButton(onPressed: () => adMobService.showInterstitialAd(), child: Text('Show Interstitial Ad')),
              ElevatedButton(onPressed: () => adMobService.showRewardedAd(), child: Text('Show Rewarded Ad')),
            ],
          ),
        ),
      ),
    );
  }
}
```

**주의:**  실제 애플리케이션에서는  `adMobConfig` 에 있는  `XXXXXXXXXX`  플레이스홀더를  AdMob  콘솔에서 발급받은 실제 광고 단위 ID 로 바꿔야 합니다.  또한,  광고 표시 빈도 제한 및 수익 최적화 전략은  앱의 특성과 사용자 경험을 고려하여  더욱 세밀하게 조정해야 합니다.  예를 들어,  `showInterstitialAd()` 함수는 특정 이벤트(게임 레벨 클리어 등) 후에 호출하는 등의  조건을 추가할 수 있습니다.  `showRewardedAd()` 함수의 경우 사용자에게 보상을 제공하는  메커니즘을 구현해야 합니다.  마지막으로,  `google_mobile_ads` 패키지를 pubspec.yaml에 추가해야 합니다.


