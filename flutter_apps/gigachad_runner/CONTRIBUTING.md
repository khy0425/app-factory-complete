# 💪 Contributing to GigaChad Runner

> **"강한 코드는 강한 앱을 만들고, 강한 앱은 강한 Chad를 만든다!"**

GigaChad Runner에 기여해주셔서 감사합니다! 이 문서는 프로젝트에 기여하는 방법을 안내합니다.

## 🎯 기여 방식

### 🐛 버그 리포트
- [Bug Report Template](https://github.com/your-username/gigachad-runner/issues/new?template=bug_report.yml) 사용
- 재현 가능한 단계 제공
- 스크린샷 또는 로그 첨부

### ✨ 기능 제안
- [Feature Request Template](https://github.com/your-username/gigachad-runner/issues/new?template=feature_request.yml) 사용
- Chad 테마와의 일관성 고려
- 구체적인 사용 사례 설명

### 🔧 코드 기여
1. 저장소 Fork
2. Feature 브랜치 생성
3. 변경사항 구현
4. 테스트 작성 및 실행
5. Pull Request 생성

## 🛠️ 개발 환경 설정

### 전제 조건
- Flutter 3.32.0+
- Dart 3.0+
- Android Studio / VS Code
- Git

### 초기 설정
```bash
# 1. 저장소 클론
git clone https://github.com/your-username/gigachad-runner.git
cd gigachad-runner/flutter_apps/gigachad_runner

# 2. 의존성 설치
flutter pub get

# 3. 코드 분석
flutter analyze

# 4. 테스트 실행
flutter test

# 5. 포맷 확인
dart format --output=none --set-exit-if-changed .
```

## 📋 코딩 가이드라인

### 🎨 코드 스타일
- **Dart 공식 스타일 가이드** 준수
- **80자 줄 길이** 제한
- **camelCase** 변수명 사용
- **PascalCase** 클래스명 사용

### 🏗️ 아키텍처 원칙
- **MVC 패턴** 유지
- **Provider 패턴** 상태 관리
- **단일 책임 원칙** 준수
- **의존성 주입** 활용

### 📱 UI/UX 가이드라인
- **검정/금색 테마** 일관성 유지
- **Material Design 3** 원칙 준수
- **Chad 밈 요소** 적절히 활용
- **접근성** 고려

### 🧪 테스트 가이드라인
- **모든 새 기능**에 테스트 작성
- **최소 80% 코드 커버리지** 유지
- **단위 테스트** 우선 작성
- **통합 테스트** 핵심 기능 커버

## 🌲 브랜치 전략

### 브랜치 네이밍
```
feature/chad-level-improvements
fix/gps-tracking-bug
docs/update-readme
refactor/workout-provider
```

### 브랜치 유형
- `feature/` - 새로운 기능
- `fix/` - 버그 수정
- `docs/` - 문서 업데이트
- `refactor/` - 코드 리팩토링
- `test/` - 테스트 추가/수정
- `style/` - UI/스타일 변경

## 📝 커밋 메시지 컨벤션

### 형식
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### 타입
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 스타일 변경
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드 프로세스/도구 변경

### 예시
```bash
feat(workout): add real-time pace calculation

Implement GPS-based pace tracking with Chad level determination.
- Add GPSService for location tracking
- Update WorkoutProvider with pace calculation
- Add vibration feedback for level changes

Closes #123
```

## 🔍 Pull Request 가이드라인

### PR 체크리스트
- [ ] 관련 이슈 링크
- [ ] 명확한 설명과 스크린샷
- [ ] 테스트 추가/업데이트
- [ ] 문서 업데이트 (필요시)
- [ ] 코드 리뷰 준비 완료

### PR 크기
- **작은 PR** 선호 (300줄 이하)
- **단일 기능/버그** 수정에 집중
- **큰 변경사항**은 여러 PR로 분할

### 리뷰 프로세스
1. **자동 검사** 통과 (CI/CD)
2. **코드 리뷰** 요청
3. **테스트 결과** 확인
4. **승인 후 머지**

## 🧪 테스트 가이드

### 테스트 실행
```bash
# 모든 테스트
flutter test

# 커버리지 포함
flutter test --coverage

# 특정 테스트
flutter test test/models/chad_level_test.dart
```

### 테스트 작성 원칙
- **Given-When-Then** 패턴 사용
- **명확한 테스트명** 작성
- **독립적인 테스트** 보장
- **모든 경우의 수** 커버

### 예시
```dart
group('ChadLevel', () {
  test('should return Ultra Chad for pace under 5 min/km', () {
    // Given
    final pace = 4.5;

    // When
    final level = ChadLevel.getChadLevelByPace(pace);

    // Then
    expect(level.type, ChadLevelType.ultraChad);
    expect(level.name, 'Ultra Chad');
  });
});
```

## 🎨 UI/UX 기여 가이드

### 디자인 시스템
- **AppColors** 클래스 활용
- **일관된 간격** (8dp 단위)
- **Google Fonts** 사용
- **Chad 테마** 유지

### 색상 팔레트
```dart
// 메인 색상
AppColors.chadGold        // #FFD700
AppColors.pureBlack       // #000000
AppColors.cardBackground  // #1C1C1C

// Chad 레벨 색상
AppColors.ultraChad       // #FFD700
AppColors.sigmaChad       // #DAA520
AppColors.alphaChad       // #B8860B
```

## 🌍 국제화 (i18n)

### 현재 지원 언어
- 한국어 (기본)

### 새 언어 추가
1. `lib/l10n/` 폴더에 번역 파일 추가
2. `pubspec.yaml`에 로케일 설정
3. 모든 하드코딩된 문자열 교체

## 🚀 릴리즈 프로세스

### 버전 관리
- **Semantic Versioning** 사용
- `MAJOR.MINOR.PATCH` 형식
- `pubspec.yaml`에서 버전 관리

### 릴리즈 단계
1. **버전 태그** 생성
2. **릴리즈 노트** 작성
3. **자동 빌드** 실행 (GitHub Actions)
4. **APK/AAB** 아티팩트 생성

## 🤝 커뮤니티 가이드라인

### 행동 강령
- **존중과 배려** 우선
- **건설적인 피드백** 제공
- **Chad 정신** 유지 (긍정적이고 동기부여적)
- **영어/한국어** 모두 환영

### 소통 채널
- **GitHub Issues** - 버그 리포트, 기능 제안
- **GitHub Discussions** - 일반적인 질문, 아이디어
- **Pull Request Reviews** - 코드 리뷰

## 📋 FAQ

### Q: 첫 기여는 어떻게 시작하나요?
A: [Good First Issue](https://github.com/your-username/gigachad-runner/labels/good%20first%20issue) 라벨이 붙은 이슈부터 시작하세요!

### Q: Chad 테마를 벗어나도 되나요?
A: Chad 테마는 앱의 정체성이므로 유지해주세요. 대신 창의적인 Chad 해석은 환영합니다!

### Q: 새로운 의존성을 추가해도 되나요?
A: 꼭 필요한 경우에만 추가하고, PR에서 이유를 설명해주세요.

### Q: iOS 지원은 언제 시작하나요?
A: 현재는 Android 우선이지만, v2.0.0에서 iOS 지원을 계획하고 있습니다.

## 🏆 인정과 감사

모든 기여자는 프로젝트의 **Contributors** 섹션에 기록됩니다. 작은 기여라도 소중히 여깁니다!

---

**함께 만들어가는 GigaChad Runner! 💪**

*"기여하는 자는 Chad, 리뷰하는 자는 더 큰 Chad, 함께 만들어가는 우리는 모두 GigaChad!"*