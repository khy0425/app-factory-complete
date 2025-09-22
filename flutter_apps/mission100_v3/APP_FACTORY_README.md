# 🏭 Mission100 앱 공장 시스템

Mission100을 기반으로 한 앱 공장 시스템입니다. 하나의 코어 엔진으로 다양한 앱을 효율적으로 생성하고 관리할 수 있습니다.

## 🎯 목표

- **앱 1개 대박**보다 **앱 10개가 소소하게** 벌어들이는 총합으로 **월 3천만원** 달성
- 같은 노력으로 앱을 5개, 10개까지 확장 가능한 구조
- 노코드+코드 하이브리드 개념으로 빠른 앱 생성

## 🏗️ 시스템 구조

### 코어 엔진 모듈
```
lib/core/
├── ads/                    # 광고 관리 모듈
│   ├── ad_config.dart     # 광고 설정
│   └── core_ad_service.dart # 통합 광고 서비스
├── auth/                   # 인증/회원관리 (예정)
├── payment/               # 결제 시스템 (예정)
├── analytics/             # 분석/로깅 (예정)
└── common/
    └── config_manager.dart # 설정 관리자
```

### 설정 시스템
```
lib/config/
├── app_config.dart        # 메인 설정 클래스
└── themes/               # 테마 관리 (예정)

assets/config/
├── app_config.json           # Mission100 기본 설정
├── timer_app_template.json   # 타이머 앱 템플릿
└── habit_tracker_template.json # 습관 추적 앱 템플릿
```

### 앱 팩토리
```
lib/core/app_factory.dart  # 앱 초기화 및 관리 핵심 클래스
```

## 🚀 새로운 앱 생성 방법

### 1. 스크립트를 사용한 자동 생성

```powershell
# PowerShell에서 실행
cd scripts
.\create_new_app.ps1 -AppName "Focus Timer Pro" -PackageName "com.appfactory.focustimer" -ConfigTemplate "timer_app_template.json"
```

**매개변수:**
- `AppName`: 앱 이름 (필수)
- `PackageName`: 패키지 이름 (필수)
- `ConfigTemplate`: 사용할 템플릿 (선택, 기본값: timer_app_template.json)
- `Version`: 버전 (선택, 기본값: 1.0.0)
- `Description`: 앱 설명 (선택)
- `Author`: 개발자 이름 (선택)

### 2. 수동 생성 과정

1. **Flutter 프로젝트 생성**
   ```bash
   flutter create my_new_app
   cd my_new_app
   ```

2. **코어 파일 복사**
   ```bash
   # Mission100 프로젝트에서 코어 파일들 복사
   cp -r ../mission100/lib/core lib/
   cp -r ../mission100/lib/config lib/
   ```

3. **설정 파일 생성**
   ```bash
   mkdir assets/config
   # 템플릿 파일을 복사하고 앱에 맞게 수정
   cp ../mission100/assets/config/timer_app_template.json assets/config/app_config.json
   ```

4. **pubspec.yaml 업데이트**
   ```yaml
   dependencies:
     provider: ^6.1.1
     shared_preferences: ^2.2.2
     path_provider: ^2.1.1
     google_mobile_ads: ^5.3.0
   
   flutter:
     assets:
       - assets/config/
   ```

5. **main.dart 수정**
   ```dart
   import 'core/app_factory.dart';
   
   void main() async {
     WidgetsFlutterBinding.ensureInitialized();
     await AppFactory.instance.initialize();
     runApp(MyApp());
   }
   ```

## ⚙️ 설정 파일 구조

### app_config.json 예시
```json
{
  "app": {
    "name": "Focus Timer Pro",
    "package_name": "com.appfactory.focustimer",
    "version": "1.0.0",
    "description": "집중력 향상을 위한 포모도로 타이머",
    "author": "Timer Apps Team"
  },
  "theme": {
    "primary_color": "#FF5722",
    "secondary_color": "#4CAF50",
    "accent_color": "#FFC107",
    "font_family": "Roboto",
    "is_dark_mode": false
  },
  "features": {
    "timer_enabled": true,
    "habit_tracking_enabled": false,
    "statistics_enabled": true,
    "achievements_enabled": false,
    "social_sharing_enabled": true,
    "backup_enabled": true,
    "notifications_enabled": true
  },
  "ads": {
    "android_app_id": "YOUR_ANDROID_APP_ID",
    "android_banner_id": "YOUR_ANDROID_BANNER_ID",
    "android_interstitial_id": "YOUR_ANDROID_INTERSTITIAL_ID",
    "enable_banner_ads": true,
    "enable_interstitial_ads": false,
    "enable_rewarded_ads": true
  }
}
```

## 🎨 앱별 커스터마이징

### 테마 변경
```dart
// 설정에서 색상만 변경하면 자동으로 테마 적용
final themeConfig = ThemeConfig(
  primaryColor: Color(0xFF4CAF50),
  secondaryColor: Color(0xFF2196F3),
  accentColor: Color(0xFFFF9800),
);
```

### 기능 플래그로 기능 제어
```dart
// 특정 기능 활성화/비활성화
if (AppFactory.instance.isFeatureEnabled('timer')) {
  // 타이머 기능 표시
}

if (AppFactory.instance.isFeatureEnabled('achievements')) {
  // 업적 시스템 표시
}
```

### 광고 설정
```dart
// 광고 서비스 사용
final adService = CoreAdService.instance;

// 배너 광고 생성
final bannerAd = adService.createBannerAd(
  adSize: AdSize.banner,
  onAdLoaded: (ad) => print('광고 로드 완료'),
  onAdFailedToLoad: (ad, error) => print('광고 로드 실패'),
);

// 전면 광고 표시
await adService.showInterstitialAd();
```

## 📱 앱 아이디어 예시

### 1. 타이머 계열
- **Focus Timer Pro**: 포모도로 타이머
- **Meditation Timer**: 명상 타이머
- **Workout Timer**: 운동 타이머
- **Study Timer**: 공부 집중 타이머

### 2. 습관 관리 계열
- **Daily Habits**: 일일 습관 추적
- **Water Reminder**: 물 섭취 기록
- **Sleep Tracker**: 수면 패턴 관리
- **Mood Tracker**: 기분 일기

### 3. 생산성 도구 계열
- **Simple Todo**: 할 일 관리
- **Routine Manager**: 루틴 관리
- **Goal Tracker**: 목표 달성 추적
- **Progress Logger**: 진행 상황 기록

## 🤖 마케팅 자동화 시스템

### 구조
```
marketing_automation/
├── aso/                          # ASO 최적화
│   └── keyword_optimizer.py     # 키워드 분석 및 최적화
├── content_generator/            # 콘텐츠 자동 생성
│   └── blog_generator.py        # 블로그/유튜브 콘텐츠 생성
├── review_manager/               # 리뷰 관리
│   └── review_monitor.py         # 리뷰 모니터링 및 자동 응답
├── dashboard/                    # 성과 대시보드 (예정)
├── config/                       # 설정 파일
│   └── marketing_config.json     # 마케팅 자동화 설정
├── marketing_orchestrator.py     # 통합 관리자
└── run_marketing_automation.py   # 실행 스크립트
```

### 주요 기능

#### 1. ASO (앱스토어 최적화) 자동화
- 경쟁 앱 키워드 분석
- AI 기반 앱 설명 최적화
- 제목 변형 버전 생성 (A/B 테스트용)
- 정기적 키워드 업데이트

#### 2. 콘텐츠 자동 생성
- 앱 리뷰 블로그 포스트 생성
- 사용법 튜토리얼 작성
- 유튜브 리뷰 스크립트 생성
- 썸네일 이미지 자동 생성

#### 3. 리뷰 관리 자동화
- Play Store 리뷰 실시간 모니터링
- 감정 분석 기반 자동 분류
- AI 기반 맞춤형 응답 생성
- 리뷰 요약 리포트

### 사용 방법

#### 환경 설정
```bash
cd marketing_automation
pip install -r requirements.txt

# 환경 변수 설정
export OPENAI_API_KEY=your_openai_key
```

#### 1. 전체 마케팅 캠페인 실행
```bash
# 새 앱 출시 시 전체 마케팅 자동화
python run_marketing_automation.py full --app-config ../assets/config/timer_app_template.json
```

#### 2. 개별 기능 실행
```bash
# ASO 최적화만
python run_marketing_automation.py aso --app-config app_config.json

# 콘텐츠 생성만
python run_marketing_automation.py content --app-config app_config.json

# 리뷰 모니터링만
python run_marketing_automation.py review --app-config app_config.json
```

#### 3. 지속적 모니터링 (데몬 모드)
```bash
# 백그라운드에서 지속적 마케팅 자동화
python run_marketing_automation.py daemon
```

### 마케팅 자동화 워크플로우

1. **앱 출시 시 자동 실행**
   ```bash
   # 새 앱 생성 후
   cd scripts
   ./create_new_app.ps1 -AppName "Focus Timer" -PackageName "com.focus.timer"
   
   # 마케팅 자동화 실행
   cd ../marketing_automation
   python run_marketing_automation.py full --app-config ../focus_timer_app/assets/config/app_config.json
   ```

2. **자동화 결과**
   - ✅ ASO 키워드 최적화 완료
   - ✅ 블로그 포스트 및 유튜브 스크립트 생성
   - ✅ 리뷰 모니터링 시작
   - ✅ 일일 성과 리포트 생성

## 🔄 CI/CD 파이프라인

### GitHub Actions 워크플로우
```yaml
# .github/workflows/app_factory_pipeline.yml
name: App Factory Pipeline
on:
  push:
    paths:
      - 'assets/config/**'
      
jobs:
  build_and_market:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        config: [timer_app, habit_tracker, meditation_app]
    steps:
      - uses: actions/checkout@v2
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
      - name: Build App
        run: ./scripts/build_app.sh ${{ matrix.config }}
      - name: Run Marketing Automation
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          cd marketing_automation
          python run_marketing_automation.py full --app-config ../assets/config/${{ matrix.config }}.json
```

## 💰 수익화 전략

### 1. 광고 수익
- 배너 광고: 트래픽이 많은 앱에 적용
- 전면 광고: 적절한 타이밍에 표시
- 보상형 광고: 프리미엄 기능 잠금 해제

### 2. 구독/결제
- 프리미엄 구독: 고급 기능 제공
- 일회성 결제: 광고 제거, 추가 기능
- 제휴 마케팅: 관련 제품/서비스 연결

### 3. 목표 수익
- **1개월**: 코어 엔진 완성
- **2-4개월**: 앱 5개 출시, 월 100만원 달성
- **6개월**: 월 300만원 달성
- **18-24개월**: 월 3천만원 달성

## 🛠️ 개발 로드맵

### Phase 1 (완료)
- ✅ 코어 엔진 모듈화
- ✅ 설정 기반 시스템 구축
- ✅ 앱 팩토리 구현
- ✅ 자동 앱 생성 스크립트

### Phase 2 (진행 중)
- 🔄 인증/회원관리 모듈
- 🔄 결제 시스템 통합
- 🔄 분석/로깅 시스템
- 🔄 CI/CD 파이프라인

### Phase 3 (예정)
- 📋 운영 자동화 도구
- 📋 마케팅 자동화
- 📋 성과 분석 대시보드
- 📋 A/B 테스트 시스템

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

---

**Mission: 100팀이 만든 앱 공장으로 당신의 앱 제국을 건설하세요! 🏭✨**
