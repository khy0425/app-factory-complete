# momento AdMob 설정 가이드

## AdMob 계정 설정 가이드: momento 앱 (com.reaf.momento)

이 가이드는 AdMob을 사용하여 Android 앱 "momento" (패키지명: com.reaf.momento)에 광고를 게재하는 방법을 단계별로 설명합니다.  초보자도 쉽게 따라할 수 있도록 자세히 설명하였습니다.

### 1단계: AdMob 계정 생성

1. **Google AdMob 콘솔 접속:** 웹 브라우저에서 `https://admob.google.com`으로 이동합니다.  Google 계정으로 로그인해야 합니다.  계정이 없다면 Google 계정을 먼저 생성해야 합니다.

2. **계정 생성 및 약관 동의:**  AdMob 콘솔에 처음 접속하면 계정 생성 안내를 따라 진행합니다.  개인 정보 및 결제 정보를 입력하고 AdMob 약관에 동의해야 합니다. (스크린샷 필요: 계정 생성 화면)

3. **결제 정보 설정:** AdMob은 수익이 발생해야 지급이 가능합니다.  계정 생성 과정에서 또는 나중에 **결제 정보** 탭에서 결제 수단 (은행 계좌 또는 PayPal)을 설정해야 합니다.  이 부분은 필수이며, 수익이 일정 금액 이상이 되어야 지급이 가능합니다. (스크린샷 필요: 결제 정보 설정 화면)


### 2단계: 앱 등록

1. **새 앱 추가:** AdMob 콘솔 상단 메뉴에서 "앱"을 클릭하고, "+ 앱 추가" 버튼을 클릭합니다. (스크린샷 필요: 앱 추가 버튼)

2. **플랫폼 선택:**  "플랫폼"에서 "Android"를 선택합니다.

3. **앱 정보 입력:**  다음 정보를 입력합니다.
    * **앱 이름:** momento
    * **패키지 이름:** com.reaf.momento
    * **앱의 SHA-1 서명 인증서 지문:**  Android Studio에서 찾을 수 있습니다.  `build.gradle` 파일을 열고 `signingConfigs` 블록 안에서 확인하거나,  Android Studio의 Build > Generate Signed Bundle / APK... 메뉴를 통해 확인할 수 있습니다. (스크린샷 필요: Android Studio에서 SHA-1 확인하는 방법)  정확한 SHA-1 지문을 입력해야 광고가 정상적으로 표시됩니다.
    * **해당 앱의 다운로드 링크 (선택 사항):** Google Play 스토어 링크를 입력할 수 있습니다.

4. **앱 등록 완료:** 모든 정보를 입력하고 "등록" 버튼을 클릭합니다.


### 3단계: 광고 단위 생성

각 광고 형식에 대한 광고 단위를 생성합니다.

1. **배너 광고 단위 생성:** "앱" 메뉴에서 momento 앱을 선택하고 "광고 단위" 탭을 클릭합니다.  "+ 광고 단위 추가" 버튼을 클릭하고, 광고 형식으로 "배너"를 선택합니다.  광고 단위 이름 (예: `momento_banner`)을 입력하고 "광고 단위 만들기"를 클릭합니다. (스크린샷 필요: 배너 광고 단위 생성 화면)

2. **전면 광고 단위 생성:**  위와 같은 과정을 반복하여 "전면" 광고 단위를 생성합니다. (예: `momento_interstitial`) (스크린샷 필요: 전면 광고 단위 생성 화면)

3. **보상형 광고 단위 생성:**  마찬가지로 "보상형" 광고 단위를 생성합니다. (예: `momento_rewarded`)  보상형 광고는 사용자가 광고를 시청한 후 보상을 제공해야 합니다.  보상 종류 및 양을 신중하게 설정해야 합니다. (스크린샷 필요: 보상형 광고 단위 생성 화면)

4. **각 광고 단위별 설정 옵션:** 각 광고 단위 생성 시, 추가적인 설정 옵션 (예: 광고 요청 타겟팅)을 확인하고 필요에 따라 설정할 수 있습니다.


### 4단계: 광고 ID 확인

1. **앱 ID:** AdMob 콘솔의 "앱" 섹션에서 momento 앱을 선택하면 앱 ID를 확인할 수 있습니다.

2. **광고 단위 ID:** 각 광고 단위를 선택하면 해당 광고 단위 ID를 확인할 수 있습니다.  각 광고 단위의 ID는 서로 다릅니다.

3. **ID 복사:** 각 ID를 복사하여 앱 코드에 붙여넣습니다.


### 5단계: 앱에 적용

이 단계는 앱의 프로그래밍 언어 (Flutter로 가정)에 따라 다릅니다.

1. **Android manifest 설정:**  AndroidManifest.xml에 인터넷 퍼미션을 추가해야 합니다.

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

2. **Flutter 코드 적용:**  Flutter의 AdMob 플러그인 (`google_mobile_ads`)을 사용하여 코드를 작성합니다.  아래는 예시 코드입니다. (실제 코드는 앱 구조에 따라 달라집니다.)

```dart
import 'package:google_mobile_ads/google_mobile_ads.dart';

// ... 다른 코드 ...

// 배너 광고
BannerAd myBanner = BannerAd(
  adUnitId: 'ca-app-pub-YOUR_AD_UNIT_ID/YOUR_BANNER_AD_UNIT_ID', // YOUR_AD_UNIT_ID와 YOUR_BANNER_AD_UNIT_ID를 실제 ID로 변경
  size: AdSize.banner,
  request: AdRequest(),
  listener: BannerAdListener(),
);

// ... 다른 코드 ...

// 전면 광고
InterstitialAd myInterstitial = InterstitialAd(
  adUnitId: 'ca-app-pub-YOUR_AD_UNIT_ID/YOUR_INTERSTITIAL_AD_UNIT_ID', // YOUR_AD_UNIT_ID와 YOUR_INTERSTITIAL_AD_UNIT_ID를 실제 ID로 변경
  request: AdRequest(),
  listener: InterstitialAdListener(),
);

// ... 다른 코드 ...

// 보상형 광고
RewardedAd myRewardedAd = RewardedAd(
  adUnitId: 'ca-app-pub-YOUR_AD_UNIT_ID/YOUR_REWARDED_AD_UNIT_ID', // YOUR_AD_UNIT_ID와 YOUR_REWARDED_AD_UNIT_ID를 실제 ID로 변경
  request: AdRequest(),
  listener: RewardedAdListener(),
);


// ... 광고 로드 및 표시 코드 ...
```

3. **테스트 방법:**  AdMob 테스트 광고 단위 ID를 사용하여 테스트합니다.  테스트 광고는 실제 광고와 다르게 표시되며, 실제 수익은 발생하지 않습니다. AdMob 콘솔에서 테스트 기기 ID를 추가하여 테스트 광고를 표시할 수 있습니다. (스크린샷 필요: AdMob 콘솔에서 테스트 기기 ID 추가 방법)


### 6단계: 정책 준수 사항

1. **AdMob 정책 요약:** AdMob 정책을 숙지하고 준수해야 합니다.  허용되지 않는 콘텐츠 (성인 콘텐츠, 불법 콘텐츠 등)를 포함해서는 안 됩니다.  자세한 내용은 AdMob 정책 페이지를 참조하십시오.

2. **주의사항:**  사용자에게 광고 표시 사실을 명확하게 알리고, 사용자 경험을 저해하지 않도록 광고를 배치해야 합니다.  강제적인 광고 표시는 피해야 합니다.

3. **승인 받기 위한 팁:**  앱이 AdMob 정책을 준수하고, 고품질의 사용자 경험을 제공한다면 승인 확률이 높아집니다.


### 7단계: 수익 최적화

1. **광고 배치 최적화:**  광고를 적절한 위치에 배치하여 사용자 경험을 저해하지 않으면서 수익을 최대화해야 합니다.  A/B 테스트를 통해 최적의 위치를 찾을 수 있습니다.

2. **사용자 경험 고려사항:**  광고는 사용자 경험을 고려하여 배치해야 합니다.  너무 많은 광고를 표시하거나, 광고가 앱 사용에 방해가 되는 경우 사용자 이탈로 이어질 수 있습니다.

3. **수익 향상 전략:**  다양한 광고 형식을 사용하고, 광고 요청 타겟팅을 최적화하여 수익을 높일 수 있습니다.  또한, 앱의 다운로드 수를 늘리는 것도 수익 증대에 중요합니다.


이 가이드를 통해 momento 앱에 AdMob을 성공적으로 설정하고 수익을 창출할 수 있기를 바랍니다.  모든 단계에서 스크린샷을 참조하면 더욱 쉽게 따라할 수 있을 것입니다.  AdMob 콘솔의 도움말과 자주 묻는 질문(FAQ)을 참조하여 추가적인 정보를 얻을 수 있습니다.  필요에 따라 Google AdMob 관련 문서를 참고하시기 바랍니다.
