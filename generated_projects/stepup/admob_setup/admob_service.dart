```dart
// lib/services/admob_service.dart
import 'dart:async';
import 'dart:io' show Platform;

import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

class AdMobService {
  static final AdMobService _instance = AdMobService._internal();

  factory AdMobService() {
    return _instance;
  }

  AdMobService._internal();

  // AdMob 설정 (실제 값으로 교체해야 함)
  final adMobConfig = {
    "app_name": "stepup",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~7249420389",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/72494203891",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/72494203892",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/72494203893"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~72494203894",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/72494203895",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/72494203896",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/72494203897"
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
      ? (Platform.isAndroid
          ? adMobConfig["android"]["app_id"]
          : adMobConfig["ios"]["app_id"])
      : (Platform.isAndroid
          ? adMobConfig["test_ids"]["android_app_id"]
          : adMobConfig["test_ids"]["ios_app_id"]);

  String get _bannerAdUnitId => kReleaseMode
      ? (Platform.isAndroid
          ? adMobConfig["android"]["banner_ad_unit"]
          : adMobConfig["ios"]["banner_ad_unit"])
      : (Platform.isAndroid
          ? adMobConfig["test_ids"]["android_banner"]
          : adMobConfig["test_ids"]["ios_banner"]);

  String get _interstitialAdUnitId => kReleaseMode
      ? (Platform.isAndroid
          ? adMobConfig["android"]["interstitial_ad_unit"]
          : adMobConfig["ios"]["interstitial_ad_unit"])
      : (Platform.isAndroid
          ? adMobConfig["test_ids"]["android_interstitial"]
          : adMobConfig["test_ids"]["ios_interstitial"]);

  String get _rewardedAdUnitId => kReleaseMode
      ? (Platform.isAndroid
          ? adMobConfig["android"]["rewarded_ad_unit"]
          : adMobConfig["ios"]["rewarded_ad_unit"])
      : (Platform.isAndroid
          ? adMobConfig["test_ids"]["android_rewarded"]
          : adMobConfig["test_ids"]["ios_rewarded"]);


  Future<InitializationStatus> initializeAdMob() async {
    MobileAds.instance.initialize();
    return MobileAds.instance.initializationStatus;
  }


  BannerAd? _bannerAd;
  InterstitialAd? _interstitialAd;
  RewardedAd? _rewardedAd;

  Future<void> loadBannerAd() async {
    _bannerAd?.dispose();
    _bannerAd = BannerAd(
      adUnitId: _bannerAdUnitId,
      size: AdSize.banner,
      request: AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) => print('Banner ad loaded.'),
        onAdFailedToLoad: (ad, error) {
          print('Banner ad failed to load: $error');
          // 재시도 로직 추가 (예: 5초 후 재시도)
          Future.delayed(const Duration(seconds: 5), loadBannerAd);
        },
        onAdOpened: (ad) => print('Banner ad opened.'),
        onAdClosed: (ad) => print('Banner ad closed.'),
      ),
    );
    await _bannerAd!.load();
  }

  Future<void> showBannerAd() async {
    if (_bannerAd != null && _bannerAd!.isLoading == false) {
      _bannerAd!.show(anchorType: AnchorType.bottom);
    }
  }


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
          Future.delayed(const Duration(seconds: 5), loadInterstitialAd);
        },
        onAdOpened: (ad) => print('Interstitial ad opened.'),
        onAdClosed: (ad) => print('Interstitial ad closed.'),
      ),
    );
    await _interstitialAd!.load();
  }

  Future<void> showInterstitialAd() async {
    if (_interstitialAd != null && _interstitialAd!.isLoading == false) {
      _interstitialAd!.show();
    }
  }

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
          Future.delayed(const Duration(seconds: 5), loadRewardedAd);
        },
        onAdOpened: (ad) => print('Rewarded ad opened.'),
        onAdClosed: (ad) {
          print('Rewarded ad closed.');
          loadRewardedAd(); // 광고 재로드
        },
        onUserEarnedReward: (ad, reward) {
          print('User earned reward: ${reward.amount}, type: ${reward.type}');
          // 보상 처리 로직
        },
      ),
    );
    await _rewardedAd!.load();
  }

  Future<void> showRewardedAd() async {
    if (_rewardedAd != null && _rewardedAd!.isLoading == false) {
      _rewardedAd!.show();
    }
  }

  // 광고 표시 빈도 제한 및 수익 최적화 로직은 별도 구현 필요 (예: SharedPreferences 사용)
}
```

**추가 설명:**

* **싱글톤 패턴:** `_instance` 변수와 `_internal` 생성자를 사용하여 싱글톤 패턴을 구현했습니다.
* **플랫폼별 ID 관리:** `kReleaseMode`와 `Platform.isAndroid`를 사용하여 플랫폼별 및 빌드 모드별 AdMob ID를 자동으로 선택합니다.  실제 AdMob ID로  `adMobConfig`  내용을 반드시 교체해야 합니다.
* **광고 로드 실패시 재시도 로직:**  `loadBannerAd`, `loadInterstitialAd`, `loadRewardedAd` 함수에서 광고 로드 실패 시 5초 후 재시도하는 로직을 추가했습니다.  재시도 횟수 제한 등을 추가로 구현할 수 있습니다.
* **광고 표시 빈도 제한:** 이 부분은  `SharedPreferences`  등을 사용하여 사용자가 광고를 본 횟수나 시간을 기록하고, 제한을 설정하는 로직을 추가해야 합니다.  코드에는 구현되어 있지 않으므로 별도로 구현해야 합니다.
* **수익 최적화를 위한 광고 배치 전략:**  광고 배치 전략은 앱의 특성과 사용자 경험에 따라 다르게 설계해야 합니다.  예를 들어, 게임의 레벨 클리어 시점이나 앱의 특정 기능 사용 후에 광고를 표시하는 등의 전략을 고려해야 합니다.
* **메모리 효율적인 광고 관리:** 광고 객체를 `_bannerAd`, `_interstitialAd`, `_rewardedAd` 변수에 저장하고 사용 후 `dispose()` 메서드를 호출하여 메모리 누수를 방지합니다.
* **상세한 주석과 오류 처리:** 각 함수에 주석을 추가하고, 광고 로드 실패 시 에러 메시지를 출력하여 디버깅을 용이하게 했습니다.

**사용 방법:**

1. `pubspec.yaml` 에 `google_mobile_ads` 패키지를 추가하고 pub get을 실행합니다.
2.  `adMobConfig` 에 실제 AdMob ID를 입력합니다.
3.  `AdMobService`  클래스의 메서드를 사용하여 광고를 로드하고 표시합니다.  예를 들어,  `AdMobService().initializeAdMob();`  을 호출하여 AdMob을 초기화하고, `AdMobService().loadBannerAd();` 와 `AdMobService().showBannerAd();` 를 사용하여 배너 광고를 로드하고 표시합니다.
4.  광고 표시 빈도 제한 및 수익 최적화 로직을 추가 구현합니다.


이 코드는 기본적인 AdMob 서비스 클래스의 구현이며, 실제 앱에 적용하기 위해서는 앱의 특성에 맞게 추가적인 기능과 로직을 구현해야 합니다.  특히 광고 표시 빈도 제어와 수익 최적화는 중요한 부분이므로 신중하게 설계해야 합니다.
