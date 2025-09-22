# semsem_master AdMob 설정 가이드

## AdMob 계정 설정 가이드: semsem_master (com.reaf.semsem_master)

이 가이드는 Android 앱 `semsem_master` (패키지명: `com.reaf.semsem_master`)에 AdMob을 설정하는 방법을 단계별로 설명합니다. Flutter를 사용하는 것으로 가정하지만, 다른 Android 개발 환경에도 적용 가능한 부분이 많습니다.


### 1단계: AdMob 계정 생성

1. **Google AdMob 콘솔 접속:** 웹 브라우저에서 `https://apps.admob.com`을 입력하여 AdMob 콘솔에 접속합니다.  Google 계정으로 로그인해야 합니다.  계정이 없다면 Google 계정을 먼저 생성해야 합니다.

2. **계정 생성 및 약관 동의:**  처음 접속하면 계정 생성 또는 기존 계정 로그인을 선택하는 화면이 나타납니다.  계정 생성을 선택하고 지시에 따라 계정을 생성합니다.  AdMob의 약관에 동의해야 합니다.

3. **결제 정보 설정:**  계정 생성 후, AdMob에서 수익을 받기 위해 결제 정보를 설정해야 합니다.  이는 필수는 아니지만, 수익 지급을 받으려면 반드시 설정해야 합니다.  결제 정보 설정은 AdMob 콘솔의 설정 메뉴에서 찾을 수 있습니다.  (스크린샷 필요: 결제 정보 설정 화면)  자세한 내용은 AdMob의 도움말을 참조하세요.  여기서는 은행 계좌 정보 또는 Google Pay 계정을 연결하는 과정이 포함됩니다.


### 2단계: 앱 등록

1. **새 앱 추가:** AdMob 콘솔의 대시보드에서 "앱 추가" 버튼을 클릭합니다. (스크린샷 필요: AdMob 대시보드의 "앱 추가" 버튼)

2. **플랫폼 선택:** Android를 선택합니다.

3. **앱 정보 입력:** 다음 정보를 입력합니다.
    * **앱 이름:** semsem_master
    * **패키지 이름:** com.reaf.semsem_master
    * **앱의 SHA-1 서명 키 해시:**  이것은 Android 앱의 보안을 위해 매우 중요합니다.  Android Studio에서 찾을 수 있습니다.  `Build` > `Generated Signed Bundle / APK` > `Android App Bundle` 또는 `APK`를 선택하고, 키 저장소를 선택하고,  `SHA-1` 해시 값을 확인합니다. (스크린샷 필요: Android Studio에서 SHA-1 해시 값을 찾는 방법)  이 값을 정확하게 입력해야 합니다.  잘못된 값을 입력하면 광고가 표시되지 않습니다.
    * **앱의 SHA-256 서명 키 해시 (선택):** SHA-256 해시도 입력하는 것이 좋습니다.

4. **앱 등록 완료:** 모든 정보를 입력하고 "등록" 버튼을 클릭합니다.


### 3단계: 광고 단위 생성

1. **새 광고 단위 추가:**  앱이 등록되면 해당 앱을 선택하고, "광고 단위" 탭으로 이동하여 "광고 단위 추가" 버튼을 클릭합니다. (스크린샷 필요: 광고 단위 추가 버튼)

2. **광고 형식 선택 및 생성:** 각 광고 형식에 대해 다음을 수행합니다.
    * **배너 광고:** 배너 광고 단위를 생성하고, 광고 크기(예: 스마트 배너)와 광고 요청 옵션을 설정합니다.
    * **전면 광고:** 전면 광고 단위를 생성하고, 광고 표시 빈도 및 사용자 경험을 고려하여 설정합니다.  전면 광고는 사용자 경험을 저해할 수 있으므로 신중하게 사용해야 합니다.
    * **보상형 광고:** 보상형 광고 단위를 생성하고, 사용자가 보상으로 받을 보상 (예: 코인, 아이템)과 광고 시청에 대한 보상 규칙을 설정합니다.

    각 광고 단위마다 고유한 광고 단위 ID가 생성됩니다.  (스크린샷 필요: 각 광고 형식의 설정 화면)


### 4단계: 광고 ID 확인

1. **앱 ID:** AdMob 콘솔의 앱 설정에서 앱 ID를 찾을 수 있습니다.  (스크린샷 필요: AdMob 콘솔에서 앱 ID 확인 방법)

2. **광고 단위 ID:** 각 광고 단위별로 생성된 고유한 광고 단위 ID를 확인합니다. (스크린샷 필요: 각 광고 단위의 ID 확인 방법)

3. **ID 복사:** 각 ID를 안전하게 복사하여 앱에 적용할 준비를 합니다.


### 5단계: 앱에 적용

**Android Manifest 설정:**

앱의 `AndroidManifest.xml` 파일에 인터넷 권한을 추가합니다.

```xml
<uses-permission android:name="android.permission.INTERNET"/>
```

**Flutter 코드 적용 (예시):**

다음은 Flutter에서 AdMob을 사용하는 예시 코드입니다.  `google_mobile_ads` 패키지를 pubspec.yaml에 추가하고 설치해야 합니다.  아래 코드는 배너 광고를 추가하는 예시입니다.  전면 광고와 보상형 광고는 다른 메서드를 사용합니다.

```dart
import 'package:google_mobile_ads/google_mobile_ads.dart';

// ... 다른 코드 ...

BannerAd myBanner = BannerAd(
  adUnitId: 'ca-app-pub-YOUR_AD_UNIT_ID/YOUR_BANNER_AD_UNIT_ID', // YOUR_AD_UNIT_ID 와 YOUR_BANNER_AD_UNIT_ID 를 실제 ID 로 바꾸세요.
  size: AdSize.banner,
  request: AdRequest(),
  listener: BannerAdListener(),
);

@override
void initState() {
  super.initState();
  myBanner.load();
}

@override
Widget build(BuildContext context) {
  return Scaffold(
    body: Column(
      children: [
        // ... 다른 위젯 ...
        Container(
          alignment: Alignment.center,
          child: AdWidget(ad: myBanner),
        ),
        // ... 다른 위젯 ...
      ],
    ),
  );
}
```

**테스트:**  테스트 광고 단위 ID를 사용하여 테스트 광고를 표시합니다.  테스트 기기에서 광고가 제대로 표시되는지 확인합니다.


### 6단계: 정책 준수 사항

* **AdMob 정책 요약:** AdMob 정책을 숙지하고 준수해야 합니다.  정책 위반 시 계정 정지 또는 수익 지급 중단될 수 있습니다.  정책은 AdMob 콘솔에서 확인 가능합니다.

* **주의사항:**  사용자에게 광고가 지나치게 노출되지 않도록 주의하고, 사용자 경험을 저해하지 않도록 광고를 배치해야 합니다.  개인정보 보호 정책을 준수하고, 사용자 동의를 받아야 할 수 있습니다.

* **승인 받기 위한 팁:**  앱이 AdMob 정책을 준수하고, 양질의 콘텐츠를 제공하며, 사용자 경험을 고려하여 설계된 경우 승인 가능성이 높아집니다.


### 7단계: 수익 최적화

* **광고 배치 최적화:**  광고의 배치 위치와 형식을 실험하여 최적의 수익을 얻을 수 있는 위치를 찾아야 합니다.  A/B 테스트를 통해 효과적인 배치 전략을 찾을 수 있습니다.

* **사용자 경험 고려사항:**  광고는 사용자 경험을 저해하지 않도록 배치해야 합니다.  과도한 광고는 사용자 이탈을 초래할 수 있습니다.

* **수익 향상 전략:**  다양한 광고 형식을 사용하고, 광고 타겟팅을 최적화하여 수익을 향상시킬 수 있습니다.  AdMob의 보고서를 분석하여 수익 향상을 위한 전략을 수립할 수 있습니다.


이 가이드는 AdMob 설정에 대한 포괄적인 안내를 제공하지만, 모든 상황에 적용될 수 있는 것은 아닙니다.  AdMob 도움말 센터와 관련 문서를 참고하여 더 자세한 정보를 얻을 수 있습니다.  어려움이 있으면 AdMob 지원팀에 문의하십시오.
