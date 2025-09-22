```dart
import 'dart:async';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

// lib/services/admob_service.dart
class AdMobService {
  static final AdMobService _instance = AdMobService._internal();

  factory AdMobService() {
    return _instance;
  }

  AdMobService._internal();

  static const String _appName = "semsem_master";
  final Map<String, dynamic> _adMobConfig = {
    "app_name": _appName,
    "note": "⚠️ 실제 사용시 AdMob 콘솔에서 생성된 ID로 교체 필요",
    "android": {
      "app_id": "ca-app-pub-XXXXXXXXXX~1870150220",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/18701502201",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/18701502202",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/18701502203"
    },
    "ios": {
      "app_id": "ca-app-pub-XXXXXXXXXX~18701502204",
      "banner_ad_unit": "ca-app-pub-XXXXXXXXXX/18701502205",
      "interstitial_ad_unit": "ca-app-pub-XXXXXXXXXX/18701502206",
      "rewarded_ad_unit": "ca-app-pub-XXXXXXXXXX/18701502207"
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
    if (kReleaseMode) {
      return Platform.isAndroid
          ? _adMobConfig["android"]["app_id"]
          : _adMobConfig["ios"]["app_id"];
    } else {
      return Platform.isAndroid
          ? _adMobConfig["test_ids"]["android_app_id"]
          : _adMobConfig["test_ids"]["ios_app_id"];
    }
  }

  String get bannerAdUnitId {
    return kReleaseMode ? getAdUnitId("banner") : getAdUnitId("banner", test: true);
  }

  String get interstitialAdUnitId {
    return kReleaseMode ? getAdUnitId("interstitial") : getAdUnitId("interstitial", test: true);
  }

  String get rewardedAdUnitId {
    return kReleaseMode ? getAdUnitId("rewarded") : getAdUnitId("rewarded", test: true);
  }


  String getAdUnitId(String adType, {bool test = false}) {
    final platform = Platform.isAndroid ? "android" : "ios";
    if(test){
      return _adMobConfig["test_ids"]["${platform}_${adType}"];
    } else {
      return _adMobConfig[platform]["${adType}_ad_unit"];
    }
  }


  // 광고 로드 및 표시 메서드 (예시)
  Future<void> loadBannerAd(BannerAd bannerAd, {required BuildContext context}) async {
    try {
      await bannerAd.load();
    } catch (e) {
      print("Banner Ad Load Error: $e");
      // 재시도 로직 추가 (예: 지연 후 재시도)
      await Future.delayed(Duration(seconds: 3));
      await loadBannerAd(bannerAd, context: context);
    }
  }


  // ... (InterstitialAd, RewardedAd 로드 및 표시 메서드 추가)


  // 광고 표시 빈도 제한 및 수익 최적화 로직 추가 (필요에 따라 구현)

  // 예시: 최근 광고 표시 시간 기록
  DateTime? _lastAdShownTime;
  final int _adShowIntervalSeconds = 60; // 60초 간격으로 광고 표시

  bool canShowAd() {
    if (_lastAdShownTime == null) return true;
    final diff = DateTime.now().difference(_lastAdShownTime!);
    return diff.inSeconds >= _adShowIntervalSeconds;
  }


  void recordAdShown() {
    _lastAdShownTime = DateTime.now();
  }

  // 오류 처리 및 로깅 (예시)
  void handleAdError(AdError error) {
    print("Ad Error: ${error.code} - ${error.message}");
    // 필요에 따라 오류 보고 기능 추가
  }
}
```

**사용 예시:**

```dart
// main.dart 또는 다른 위젯에서
final adMobService = AdMobService();

// 앱 시작 시 초기화 (appId 설정 필요)
MobileAds.instance.initialize();

// 배너 광고 로드 및 표시
BannerAd myBanner = BannerAd(
  adUnitId: adMobService.bannerAdUnitId,
  size: AdSize.banner,
  request: AdRequest(),
  listener: BannerAdListener(
    onAdLoaded: (ad) => print('Ad loaded.'),
    onAdFailedToLoad: (ad, error) => adMobService.handleAdError(error),
  ),
);

adMobService.loadBannerAd(myBanner, context: context); // context 필요

// ... (InterstitialAd, RewardedAd 사용 예시 추가)
```

**추가 설명:**

* 위 코드는 기본적인 AdMob 서비스 클래스 구현 예시입니다. 실제 프로젝트에서는 더욱 복잡한 로직과 기능이 필요할 수 있습니다.
* 광고 표시 빈도 제한 및 수익 최적화 로직은 프로젝트의 특성에 따라 다르게 구현해야 합니다.  예시로 `canShowAd()`와 `recordAdShown()` 메서드가 추가되었지만, 더욱 정교한 알고리즘이 필요할 수 있습니다.
* `_adShowIntervalSeconds` 변수를 통해 광고 표시 간격을 조절할 수 있습니다.
* 오류 처리 및 로깅 부분은 실제 환경에 맞춰 자세하게 구현해야 합니다.  예를 들어, Firebase Crashlytics와 같은 오류 보고 서비스를 사용하는 것이 좋습니다.
* `context` 매개변수는 `loadBannerAd` 함수에 추가되었으며, 이는 광고를 표시하기 위해 필요한 Flutter context를 전달하기 위함입니다.


이 코드를 사용하기 전에 `pubspec.yaml`에 `google_mobile_ads` 패키지를 추가하고,  `flutter pub get` 명령어를 실행해야 합니다. 또한, AdMob 계정을 설정하고 앱에 AdMob ID를 정확하게 입력해야 합니다.  `XXXXXXXXXX` 부분은 실제 AdMob ID로 대체해야 합니다.  릴리즈 전에 테스트 광고 ID를 실제 광고 ID로 변경하는 것을 잊지 마세요.  그리고, AndroidManifest.xml과 iOS의 Info.plist 파일에 필요한 설정을 추가해야 합니다.  Google Mobile Ads SDK 문서를 참조하세요.
