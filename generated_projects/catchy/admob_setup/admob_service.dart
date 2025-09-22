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

  // AdMob 설정 (실제 ID로 교체해야 함)
  final adMobConfig = {
    "app_name": "catchy",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~9243530066",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/92435300661",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/92435300662",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/92435300663"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~92435300664",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/92435300665",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/92435300666",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/92435300667"
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


  String get appId {
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

  String get bannerAdUnitId {
    return kDebugMode ? (Platform.isAndroid
        ? adMobConfig["test_ids"]["android_banner"]
        : adMobConfig["test_ids"]["ios_banner"]) : (Platform.isAndroid
            ? adMobConfig["android"]["banner_ad_unit"]
            : adMobConfig["ios"]["banner_ad_unit"]);
  }

  String get interstitialAdUnitId {
    return kDebugMode ? (Platform.isAndroid
        ? adMobConfig["test_ids"]["android_interstitial"]
        : adMobConfig["test_ids"]["ios_interstitial"]) : (Platform.isAndroid
            ? adMobConfig["android"]["interstitial_ad_unit"]
            : adMobConfig["ios"]["interstitial_ad_unit"]);
  }

  String get rewardedAdUnitId {
    return kDebugMode ? (Platform.isAndroid
        ? adMobConfig["test_ids"]["android_rewarded"]
        : adMobConfig["test_ids"]["ios_rewarded"]) : (Platform.isAndroid
            ? adMobConfig["android"]["rewarded_ad_unit"]
            : adMobConfig["ios"]["rewarded_ad_unit"]);
  }


  BannerAd? _bannerAd;
  InterstitialAd? _interstitialAd;
  RewardedAd? _rewardedAd;

  // 광고 로드 및 표시 함수들 (예시)
  Future<void> loadBannerAd() async {
    _bannerAd?.dispose();
    _bannerAd = BannerAd(
      adUnitId: bannerAdUnitId,
      size: AdSize.banner,
      request: AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          print('BannerAd loaded.');
        },
        onAdFailedToLoad: (ad, error) {
          print('BannerAd failed to load: $error');
          // 재시도 로직 추가 (예: 5초 후 재시도)
          Future.delayed(const Duration(seconds: 5), loadBannerAd);
        },
        onAdOpened: (ad) => print('BannerAd opened.'),
        onAdClosed: (ad) => print('BannerAd closed.'),
      ),
    );
    await _bannerAd?.load();
  }


  Future<void> showInterstitialAd() async {
    if (_interstitialAd == null) {
      await loadInterstitialAd();
    }
    if (_interstitialAd != null && _interstitialAd!.isLoaded) {
      _interstitialAd!.show();
    }
  }

  Future<void> loadInterstitialAd() async {
    _interstitialAd?.dispose();
    _interstitialAd = InterstitialAd(
      adUnitId: interstitialAdUnitId,
      request: AdRequest(),
      listener: InterstitialAdListener(
        onAdLoaded: (ad) => print('InterstitialAd loaded.'),
        onAdFailedToLoad: (ad, error) {
          print('InterstitialAd failed to load: $error');
          // 재시도 로직 추가
          Future.delayed(const Duration(seconds: 5), loadInterstitialAd);
        },
        onAdOpened: (ad) => print('InterstitialAd opened.'),
        onAdClosed: (ad) {
          print('InterstitialAd closed.');
          _interstitialAd = null; // 메모리 관리를 위해 null로 설정
        },
      ),
    );
    await _interstitialAd?.load();
  }

  Future<void> showRewardedAd() async {
    if (_rewardedAd == null) {
      await loadRewardedAd();
    }
    if (_rewardedAd != null && _rewardedAd!.isLoaded) {
      _rewardedAd!.show();
    }
  }

  Future<void> loadRewardedAd() async {
    _rewardedAd?.dispose();
    _rewardedAd = RewardedAd(
      adUnitId: rewardedAdUnitId,
      request: AdRequest(),
      listener: RewardedAdListener(
        onAdLoaded: (ad) => print('RewardedAd loaded.'),
        onAdFailedToLoad: (ad, error) {
          print('RewardedAd failed to load: $error');
          // 재시도 로직 추가
          Future.delayed(const Duration(seconds: 5), loadRewardedAd);
        },
        onAdOpened: (ad) => print('RewardedAd opened.'),
        onAdClosed: (ad) {
          print('RewardedAd closed.');
          _rewardedAd = null; // 메모리 관리를 위해 null로 설정
        },
        onUserEarnedReward: (ad, reward) {
          print('User earned reward: ${reward.amount} ${reward.type}');
        },
      ),
    );
    await _rewardedAd?.load();
  }


  // 광고 표시 빈도 제한을 위한 추가 로직 (예: SharedPreferences 사용)
  // ...

  // 수익 최적화를 위한 추가 로직 (예: A/B 테스트, 광고 배치 전략)
  // ...

  // 메모리 효율적인 광고 관리를 위해 dispose() 메소드 호출
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
  MobileAds.instance.initialize();
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
    adMobService.loadBannerAd(); // 앱 시작 시 배너 광고 로드
    adMobService.loadInterstitialAd(); // 앱 시작 시 전면 광고 로드 (필요시)
  }

  @override
  void dispose() {
    adMobService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Catchy App'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (adMobService._bannerAd != null && adMobService._bannerAd!.isLoading == false)
                Container(
                  alignment: Alignment.center,
                  child: AdWidget(ad: adMobService._bannerAd!),
                ),
              ElevatedButton(
                onPressed: () {
                  adMobService.showInterstitialAd();
                },
                child: const Text('Show Interstitial Ad'),
              ),
              ElevatedButton(
                onPressed: () {
                  adMobService.showRewardedAd();
                },
                child: const Text('Show Rewarded Ad'),
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

* 위 코드는 예시이며, 실제 앱에서는 광고 표시 빈도 제한, 수익 최적화 전략,  오류 처리를 더욱 세밀하게 구현해야 합니다.
* `google_mobile_ads` 플러그인을 pubspec.yaml에 추가해야 합니다.
* 실제 AdMob ID로 교체해야 합니다.  테스트 ID를 사용하여 테스트하고, 릴리즈 전에 실제 ID로 변경하는 것을 잊지 마세요.
* 광고 표시 빈도 제한을 위해서는 `SharedPreferences` 또는 다른 데이터 저장소를 사용하여 사용자가 마지막으로 광고를 본 시점을 기록하고 관리해야 합니다.
* 수익 최적화를 위해서는 다양한 광고 형식(네이티브 광고 등)을 테스트하고, 광고 배치 전략을 최적화해야 합니다.


이 코드는  AdMob 서비스를 더 효율적이고 안정적으로 관리하는 데 도움이 될 것입니다.  하지만  앱의 특성과 사용자 경험에 맞춰 추가적인 조정이 필요할 수 있습니다.  특히 광고 표시 빈도 제어와 수익 최적화 부분은 앱의 특성에 따라 세부적인 구현이 달라져야 합니다.
