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

  // AdMob 설정 - 실제 값으로 교체해야 합니다.
  final Map<String, dynamic> _adMobConfig = {
    "app_name": "meditation_app",
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~4236475790",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/42364757901",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/42364757902",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/42364757903"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~42364757904",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/42364757905",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/42364757906",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/42364757907"
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
      : _getPlatformTestAppId();

  String _getPlatformAppId() {
    if (Platform.isAndroid) {
      return _adMobConfig['android']['app_id'];
    } else if (Platform.isIOS) {
      return _adMobConfig['ios']['app_id'];
    } else {
      throw Exception('Unsupported platform');
    }
  }

  String _getPlatformTestAppId() {
    if (Platform.isAndroid) {
      return _adMobConfig['test_ids']['android_app_id'];
    } else if (Platform.isIOS) {
      return _adMobConfig['test_ids']['ios_app_id'];
    } else {
      throw Exception('Unsupported platform');
    }
  }


  String get _bannerAdUnitId => kReleaseMode
      ? _getPlatformAdUnitId('banner')
      : _getPlatformTestAdUnitId('banner');

  String _getPlatformAdUnitId(String adType) {
    if (Platform.isAndroid) {
      return _adMobConfig['android'][adType + '_ad_unit'];
    } else if (Platform.isIOS) {
      return _adMobConfig['ios'][adType + '_ad_unit'];
    } else {
      throw Exception('Unsupported platform');
    }
  }

  String _getPlatformTestAdUnitId(String adType) {
    if (Platform.isAndroid) {
      return _adMobConfig['test_ids']['android_' + adType];
    } else if (Platform.isIOS) {
      return _adMobConfig['test_ids']['ios_' + adType];
    } else {
      throw Exception('Unsupported platform');
    }
  }

  //Interstitial and Rewarded  methods are similar, omitted for brevity.  Follow the pattern of bannerAd

  Future<BannerAd?> loadBannerAd() async {
    try {
      return BannerAd(
        adUnitId: _bannerAdUnitId,
        size: AdSize.banner,
        request: AdRequest(),
        listener: BannerAdListener(
          onAdLoaded: (ad) => print('Banner ad loaded.'),
          onAdFailedToLoad: (ad, error) {
            print('Banner ad failed to load: $error');
            // 재시도 로직 추가
            Future.delayed(Duration(seconds: 5), () => loadBannerAd());
          },
          onAdOpened: (ad) => print('Banner ad opened.'),
          onAdClosed: (ad) => print('Banner ad closed.'),
        ),
      )..load();
    } catch (e) {
      print('Error loading banner ad: $e');
      return null;
    }
  }

  // ... other ad loading and showing methods for interstitial and rewarded ads ...

  // 광고 표시 빈도 제한 (예시 - 간단한 시간 기반 제한)
  DateTime? _lastInterstitialShown;
  Duration get interstitialShowInterval => const Duration(minutes: 10);

  bool canShowInterstitialAd() {
    return _lastInterstitialShown == null ||
        DateTime.now().difference(_lastInterstitialShown!) >= interstitialShowInterval;
  }

  void recordInterstitialAdShown() {
    _lastInterstitialShown = DateTime.now();
  }

  // Initialization method to be called once on app startup
  Future<InitializationStatus> initializeAdMob() async {
    MobileAds.instance.initialize();
    return MobileAds.instance.initializationStatus;
  }


}
```

**주의사항:**

* 위 코드는 완전한 예시이며, 실제 구현에는 추가적인 에러 처리와 광고 배치 전략(예: 특정 화면에서만 광고 표시, A/B 테스트 등)이 필요합니다.
* `interstitialAd`, `rewardedAd` 관련 메소드는 `bannerAd`와 유사하게 구현해야 합니다.  위 코드는 간결성을 위해 생략했습니다.
*  실제 앱 ID는  `_adMobConfig` 변수에  **실제 AdMob 콘솔에서 생성된 ID** 로 반드시 교체해야 합니다.
*  광고 표시 빈도 제한은  시간 기반의 간단한 예시이며, 더욱 정교한 로직이 필요할 수 있습니다. (예: 사용자 세션 기반, 앱 내 이벤트 기반 제한 등)
*  수익 최적화를 위해서는 다양한 광고 형식을 테스트하고, 광고 배치 전략을 지속적으로 개선해야 합니다.
* `initializeAdMob()` 함수는 앱 시작 시 한 번 호출하여 AdMob을 초기화해야 합니다.  `main()` 함수 또는 `runApp()` 전에 호출하는 것이 좋습니다.


이 코드는 AdMob 서비스를 싱글톤 패턴으로 구현하여 메모리 효율을 높였으며, 플랫폼별 ID 관리, 광고 로드 실패 시 재시도, 광고 표시 빈도 제한, 디버그/릴리즈 모드 관리 기능을 포함하고 있습니다.  하지만  실제 배포 전에는  더욱  세밀한 오류 처리와 최적화가 필요합니다.  특히 광고 배치 전략은 앱의 특성과 사용자 경험에 맞춰 신중하게 결정해야 합니다.
