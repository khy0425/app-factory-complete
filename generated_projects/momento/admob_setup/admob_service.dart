```dart
// lib/services/admob_service.dart
import 'dart:async';
import 'dart:io' show Platform;

import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'package:flutter/foundation.dart' show kDebugMode;

class AdMobService {
  static final AdMobService _instance = AdMobService._internal();

  factory AdMobService() {
    return _instance;
  }

  AdMobService._internal();

  // AdMob 설정 (실제 값으로 변경 필요)
  final Map<String, dynamic> _adMobConfig = {
    "app_name": "momento",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~7113724946",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/71137249461",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/71137249462",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/71137249463"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~71137249464",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/71137249465",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/71137249466",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/71137249467"
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

  String get _appId => kDebugMode
      ? Platform.isAndroid
          ? _adMobConfig["test_ids"]["android_app_id"]
          : _adMobConfig["test_ids"]["ios_app_id"]
      : Platform.isAndroid
          ? _adMobConfig["android"]["app_id"]
          : _adMobConfig["ios"]["app_id"];

  String get _bannerAdUnitId => kDebugMode
      ? Platform.isAndroid
          ? _adMobConfig["test_ids"]["android_banner"]
          : _adMobConfig["test_ids"]["ios_banner"]
      : Platform.isAndroid
          ? _adMobConfig["android"]["banner_ad_unit"]
          : _adMobConfig["ios"]["banner_ad_unit"];

  String get _interstitialAdUnitId => kDebugMode
      ? Platform.isAndroid
          ? _adMobConfig["test_ids"]["android_interstitial"]
          : _adMobConfig["test_ids"]["ios_interstitial"]
      : Platform.isAndroid
          ? _adMobConfig["android"]["interstitial_ad_unit"]
          : _adMobConfig["ios"]["interstitial_ad_unit"];

  String get _rewardedAdUnitId => kDebugMode
      ? Platform.isAndroid
          ? _adMobConfig["test_ids"]["android_rewarded"]
          : _adMobConfig["test_ids"]["ios_rewarded"]
      : Platform.isAndroid
          ? _adMobConfig["android"]["rewarded_ad_unit"]
          : _adMobConfig["ios"]["rewarded_ad_unit"];


  // 광고 초기화
  Future<InitializationStatus> initializeAdMob() async {
    MobileAds.instance.initialize();
    return MobileAds.instance.initializationStatus;
  }


  // Banner 광고 로드 및 표시 (최적화를 위해 필요시 수정)
  BannerAd? _bannerAd;
  Future<void> showBannerAd() async {
      _bannerAd?.dispose();
      _bannerAd = BannerAd(
          adUnitId: _bannerAdUnitId,
          size: AdSize.banner,
          request: AdRequest(),
          listener: BannerAdListener(
              onAdLoaded: (ad) => print('Ad loaded.'),
              onAdFailedToLoad: (ad, error) {
                print('Ad failed to load: $error');
                // 재시도 로직 추가 (예: 5초 후 재시도)
                Future.delayed(Duration(seconds: 5), showBannerAd);
              }
          )
      );
      _bannerAd?.load();
  }

  void disposeBannerAd(){
    _bannerAd?.dispose();
  }


  // Interstitial 광고 로드 및 표시
  InterstitialAd? _interstitialAd;
  Future<void> loadInterstitialAd() async {
    _interstitialAd?.dispose();
    _interstitialAd = InterstitialAd(
      adUnitId: _interstitialAdUnitId,
      request: AdRequest(),
      listener: InterstitialAdListener(
        onAdLoaded: (ad) => print('Interstitial ad loaded.'),
        onAdFailedToLoad: (ad, error) {
          print('Interstitial ad failed to load: $error');
          // 재시도 로직 추가
          Future.delayed(Duration(seconds: 5), loadInterstitialAd);
        },
        onAdOpened: (ad) => print('Interstitial ad opened.'),
        onAdClosed: (ad) {
          print('Interstitial ad closed.');
          loadInterstitialAd(); // 자동으로 재로드
        },
      ),
    );
    return _interstitialAd?.load();
  }

  Future<void> showInterstitialAd() async {
    if (_interstitialAd != null && _interstitialAd!.isLoaded) {
      _interstitialAd!.show();
    } else {
      print('Interstitial ad is not loaded.');
    }
  }

  // Rewarded 광고 로드 및 표시
  RewardedAd? _rewardedAd;
  Future<void> loadRewardedAd() async {
    _rewardedAd?.dispose();
    _rewardedAd = RewardedAd(
      adUnitId: _rewardedAdUnitId,
      request: AdRequest(),
      listener: RewardedAdListener(
        onAdLoaded: (ad) => print('Rewarded ad loaded.'),
        onAdFailedToLoad: (ad, error) {
          print('Rewarded ad failed to load: $error');
          // 재시도 로직 추가
          Future.delayed(Duration(seconds: 5), loadRewardedAd);
        },
        onAdOpened: (ad) => print('Rewarded ad opened.'),
        onAdClosed: (ad) {
          print('Rewarded ad closed.');
          loadRewardedAd(); // 자동으로 재로드
        },
        onUserEarnedReward: (ad, reward) {
          print(
              'User earned reward: ${reward.amount}, type: ${reward.type}');
          // 보상 처리 로직 추가
        },
      ),
    );
    return _rewardedAd?.load();
  }

  Future<void> showRewardedAd() async {
    if (_rewardedAd != null && _rewardedAd!.isLoaded) {
      _rewardedAd!.show();
    } else {
      print('Rewarded ad is not loaded.');
    }
  }


  // 광고 표시 빈도 제한 (예시 - 필요에 따라 수정)
  DateTime? _lastInterstitialShown;
  DateTime? _lastRewardedShown;

  bool canShowInterstitial() {
    return _lastInterstitialShown == null ||
        DateTime.now().difference(_lastInterstitialShown!) >=
            Duration(minutes: 10); // 10분 간격
  }

  bool canShowRewarded() {
    return _lastRewardedShown == null ||
        DateTime.now().difference(_lastRewardedShown!) >=
            Duration(minutes: 30); // 30분 간격
  }

  void recordInterstitialShown() {
    _lastInterstitialShown = DateTime.now();
  }

  void recordRewardedShown() {
    _lastRewardedShown = DateTime.now();
  }
}
```

**사용 예시:**

```dart
import 'package:flutter/material.dart';
// ... other imports
import 'services/admob_service.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final adMobService = AdMobService();
  await adMobService.initializeAdMob(); // AdMob 초기화
  runApp(MyApp());
}


class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final adMobService = AdMobService();

  @override
  void initState() {
    super.initState();
    adMobService.showBannerAd();
    adMobService.loadInterstitialAd();
    adMobService.loadRewardedAd();
  }

  @override
  void dispose() {
    adMobService.disposeBannerAd();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Momento App')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: () {
                  if (adMobService.canShowInterstitial()) {
                    adMobService.showInterstitialAd();
                    adMobService.recordInterstitialShown();
                  } else {
                    print('Interstitial ad cannot be shown yet.');
                  }
                },
                child: Text('Show Interstitial Ad'),
              ),
              ElevatedButton(
                onPressed: () {
                  if (adMobService.canShowRewarded()) {
                    adMobService.showRewardedAd();
                    adMobService.recordRewardedShown();
                  } else {
                    print('Rewarded ad cannot be shown yet.');
                  }
                },
                child: Text('Show Rewarded Ad'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

**주의사항:**

* 위 코드는 예시이며, 실제 앱에 적용하기 전에 광고 배치 전략, 표시 빈도, 재시도 로직 등을  앱의 특성에 맞게 조정해야 합니다.
* `google_mobile_ads` 패키지를 `pubspec.yaml`에 추가해야 합니다.
* 실제 AdMob ID로 교체해야 합니다.  `XXXXXXXXXX` 부분을 실제 ID로 바꾸세요.
* 광고 표시 빈도 제한은 사용자 경험을 고려하여 적절하게 설정해야 합니다.  너무 잦은 광고 표시는 사용자 이탈을 야기할 수 있습니다.
*  `initializeAdMob()` 함수는 앱 실행 시 한 번만 호출해야 합니다. 보통 `main` 함수에서 `initState`를 이용하는 것이 좋습니다.
*  `dispose` 함수를 이용하여 광고 리소스를 해제하여 메모리 누수를 방지하는 것이 중요합니다. 특히 `BannerAd`는 `dispose`를 호출하지 않으면 메모리 누수가 발생할 수 있습니다.


이 코드를 사용하여 Momento 앱에서 AdMob 광고를 효율적으로 관리할 수 있습니다.  필요에 따라 추가적인 기능(예:  광고 수익 추적, A/B 테스트)을 구현할 수 있습니다.  항상 Google AdMob 정책을 준수해야 합니다.
