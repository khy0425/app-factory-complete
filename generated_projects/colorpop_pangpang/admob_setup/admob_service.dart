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

  // AdMob 설정 (실제 ID로 교체)
  final Map<String, dynamic> _adMobConfig = {
    "app_name": "colorpop_pangpang",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~4078092620",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/40780926201",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/40780926202",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/40780926203"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~40780926204",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/40780926205",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/40780926206",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/40780926207"
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
      ? _getPlatformId(_adMobConfig, "app_id")
      : _getPlatformId(_adMobConfig["test_ids"], "android_app_id");

  String _getPlatformId(Map<String, dynamic> config, String key) {
    return Platform.isAndroid ? config["android"][key] : config["ios"][key];
  }


  BannerAd? _bannerAd;
  InterstitialAd? _interstitialAd;
  RewardedAd? _rewardedAd;

  Future<void> initializeAdMob() async {
    MobileAds.instance.initialize();
  }

  Future<InitializationStatus> initialize() async {
    return MobileAds.instance.initialize();
  }

  Future<void> loadBannerAd({required BuildContext context}) async {
    if (_bannerAd != null && _bannerAd!.isLoading) return;
    final adUnitId = _getPlatformAdUnitId(_adMobConfig, "banner_ad_unit");
    _bannerAd = BannerAd(
      adUnitId: adUnitId,
      size: AdSize.banner,
      request: AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          print('BannerAd loaded.');
          //  여기서 BannerAd를 UI에 추가합니다.
        },
        onAdFailedToLoad: (ad, error) {
          print('BannerAd failedToLoad: $error');
          _retryLoadAd(_bannerAd, adUnitId, context); // 재시도 로직
        },
        onAdOpened: (ad) => print('BannerAd opened.'),
        onAdClosed: (ad) => print('BannerAd closed.'),
      ),
    );
    await _bannerAd!.load();
  }


  Future<void> showInterstitialAd(BuildContext context) async {
    if (_interstitialAd == null || _interstitialAd!.isLoading) {
      await loadInterstitialAd(context);
      // 광고 로드 실패 시 처리
    }
    if (_interstitialAd != null && _interstitialAd!.isLoaded) {
      _interstitialAd!.fullScreenContentCallback = FullScreenContentCallback(
        onAdShowedFullScreenContent: (ad) => print('ad showed'),
        onAdDismissedFullScreenContent: (ad) {
          print('$ad dismissed fullscreen content.');
          _interstitialAd!.dispose();
          _interstitialAd = null;
        },
        onAdFailedToShowFullScreenContent: (ad, error) {
          print('ad failed to show fullscreen content.');
          _interstitialAd!.dispose();
          _interstitialAd = null;
        },
      );
      _interstitialAd!.show();
    }
  }

  Future<void> loadInterstitialAd(BuildContext context) async {
    if (_interstitialAd != null && _interstitialAd!.isLoading) return;
    final adUnitId = _getPlatformAdUnitId(_adMobConfig, "interstitial_ad_unit");
    _interstitialAd = InterstitialAd(
      adUnitId: adUnitId,
      request: AdRequest(),
      listener: InterstitialAdListener(
        onAdLoaded: (ad) => print('InterstitialAd loaded.'),
        onAdFailedToLoad: (ad, error) {
          print('InterstitialAd failedToLoad: $error');
          _retryLoadAd(_interstitialAd, adUnitId, context);
        },
        onAdOpened: (ad) => print('InterstitialAd opened.'),
        onAdClosed: (ad) {
          print('InterstitialAd closed.');
          _interstitialAd!.dispose();
          _interstitialAd = null;
        },
      ),
    );
    await _interstitialAd!.load();
  }


  Future<void> showRewardedAd(BuildContext context) async {
    if (_rewardedAd == null || _rewardedAd!.isLoading) {
      await loadRewardedAd(context);
    }
    if (_rewardedAd != null && _rewardedAd!.isLoaded) {
      _rewardedAd!.fullScreenContentCallback = FullScreenContentCallback(
        onAdShowedFullScreenContent: (ad) => print('ad showed'),
        onAdDismissedFullScreenContent: (ad) {
          print('$ad dismissed fullscreen content.');
          _rewardedAd!.dispose();
          _rewardedAd = null;
        },
        onAdFailedToShowFullScreenContent: (ad, error) {
          print('ad failed to show fullscreen content.');
          _rewardedAd!.dispose();
          _rewardedAd = null;
        },
      );
      _rewardedAd!.show();
    }
  }

  Future<void> loadRewardedAd(BuildContext context) async {
      if (_rewardedAd != null && _rewardedAd!.isLoading) return;
      final adUnitId = _getPlatformAdUnitId(_adMobConfig, "rewarded_ad_unit");
      _rewardedAd = RewardedAd(
        adUnitId: adUnitId,
        request: AdRequest(),
        listener: RewardedAdListener(
          onAdLoaded: (ad) => print('RewardedAd loaded.'),
          onAdFailedToLoad: (ad, error) {
            print('RewardedAd failedToLoad: $error');
            _retryLoadAd(_rewardedAd, adUnitId, context);
          },
          onAdOpened: (ad) => print('RewardedAd opened.'),
          onAdClosed: (ad) {
            print('RewardedAd closed.');
            _rewardedAd!.dispose();
            _rewardedAd = null;
          },
          onUserEarnedReward: (ad, reward) {
            print('User earned reward: ${reward.amount} ${reward.type}');
            // 보상 처리
          },
        ),
      );
      await _rewardedAd!.load();
  }

  String _getPlatformAdUnitId(Map<String, dynamic> config, String key) {
    return kReleaseMode
        ? _getPlatformId(config, key)
        : _getPlatformId(config["test_ids"], key.replaceAll("ad_unit", ""));
  }


  Future<void> _retryLoadAd(Ad? ad, String adUnitId, BuildContext context) async {
    // 재시도 로직 -  3회 재시도 후 실패 처리
    int retryCount = 0;
    const maxRetries = 3;
    while (retryCount < maxRetries) {
      try {
        await Future.delayed(Duration(seconds: 2)); // 2초 후 재시도
        print("Retry loading ad: $adUnitId, attempt: ${retryCount + 1}");
        if (ad is BannerAd) await loadBannerAd(context: context);
        else if (ad is InterstitialAd) await loadInterstitialAd(context);
        else if (ad is RewardedAd) await loadRewardedAd(context);
        break; // 성공 시 반복문 종료
      } catch (e) {
        retryCount++;
        print("Ad load retry failed: $e");
        if (retryCount == maxRetries) {
          print("Ad load failed after multiple retries: $adUnitId");
          // 실패 처리 (예: 사용자에게 알림 표시)
        }
      }
    }
  }

  void dispose(){
    _bannerAd?.dispose();
    _interstitialAd?.dispose();
    _rewardedAd?.dispose();
  }
}
```

**사용 예시 (main.dart):**

```dart
import 'package:flutter/material.dart';
import 'services/admob_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AdMobService().initialize();
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final AdMobService _adMobService = AdMobService();

  @override
  void initState() {
    super.initState();
    _adMobService.loadBannerAd(context: context); // 앱 시작 시 배너 광고 로드
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('AdMob Example')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (_adMobService._bannerAd != null && _adMobService._bannerAd!.isLoading == false)
                Container(
                    alignment: Alignment.center,
                    child: AdWidget(ad: _adMobService._bannerAd!)),
              ElevatedButton(
                onPressed: () => _adMobService.showInterstitialAd(context),
                child: Text('Show Interstitial Ad'),
              ),
              ElevatedButton(
                onPressed: () => _adMobService.showRewardedAd(context),
                child: Text('Show Rewarded Ad'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _adMobService.dispose();
    super.dispose();
  }
}
```

**중요:**  위 코드에서 `XXXXXXXXXX` 부분을 실제 AdMob ID로 바꿔야 합니다.  `pubspec.yaml`에 `google_mobile_ads` 패키지를 추가하고 `flutter pub get`을 실행해야 합니다.  또한, Android와 iOS 프로젝트 설정에서 AdMob ID를 올바르게 설정해야 합니다.  광고 표시 빈도 제한 및 수익 최적화 전략은 앱의 사용 패턴과 목표에 따라 추가적인 코드 구현이 필요할 수 있습니다.  예를 들어,  `showInterstitialAd` 함수에  `SharedPreferences`를 이용하여 광고 표시 횟수를 제한하는 로직을 추가할 수 있습니다.