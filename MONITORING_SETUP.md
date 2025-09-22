# 🤖 완전 자동화 오류 모니터링 시스템 설정 가이드

## 📋 시스템 개요

**완전 자동화된 오류 감지 → AI 분석 → 자동 수정 → Notion 정리 → Slack 알림** 시스템

### ✨ 핵심 기능
- 🔍 **실시간 오류 감지**: Flutter 빌드, Python 스크립트, API 오류 자동 감지
- 🤖 **AI 기반 분석**: Gemini AI로 오류 원인 분석 및 해결책 제시
- 🔧 **자동 수정 시도**: 일반적인 오류는 자동으로 수정 시도
- 📊 **Notion 자동 정리**: 모든 오류를 Notion 데이터베이스에 체계적으로 기록
- 📱 **Slack 실시간 알림**: 오류 발생시 즉시 Slack으로 알림
- 📈 **일일 리포트**: 매일 자동으로 오류 통계 리포트 생성

## 🚀 빠른 설정

### 1단계: 필수 패키지 설치
```bash
pip install schedule requests
```

### 2단계: 환경 변수 설정
```bash
# .env 파일에 추가
NOTION_API_TOKEN=your_notion_token
NOTION_DATABASE_ID=your_notion_database_id
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

### 3단계: 모니터링 시스템 실행
```bash
# 백그라운드에서 연속 모니터링
python run_monitoring.py

# 또는 일회성 체크
python error_monitoring_system.py
```

## 📊 Notion 데이터베이스 설정

### 1. Notion 통합 생성
1. [Notion Integrations](https://www.notion.so/my-integrations) 접속
2. "New integration" 클릭
3. 이름: "App Factory Monitor"
4. 워크스페이스 선택 후 "Submit"
5. **Internal Integration Token** 복사 → `NOTION_API_TOKEN`

### 2. 오류 추적 데이터베이스 생성
Notion에서 새 데이터베이스 생성 후 다음 속성 추가:

| 속성명 | 타입 | 설명 |
|--------|------|------|
| 제목 | Title | 오류 제목 |
| 타입 | Select | 오류 유형 (Flutter Error, API Error, 등) |
| 앱 | Rich Text | 앱 이름 |
| 심각도 | Select | Low, Medium, High, Critical |
| 자동수정가능 | Checkbox | AI가 자동 수정 가능한지 여부 |
| 상태 | Select | New, In Progress, Resolved, Manual Required |
| 발생시간 | Date | 오류 발생 시간 |

### 3. 데이터베이스 연결
1. 생성한 데이터베이스에서 "Share" 클릭
2. "App Factory Monitor" 통합을 "Can edit"으로 초대
3. 데이터베이스 URL에서 ID 복사 → `NOTION_DATABASE_ID`

## 📱 Slack 웹훅 설정

### 1. Slack 앱 생성
1. [Slack API](https://api.slack.com/apps) 접속
2. "Create New App" → "From scratch"
3. 앱 이름: "App Factory Monitor"
4. 워크스페이스 선택

### 2. 웹훅 활성화
1. "Incoming Webhooks" 메뉴
2. "Activate Incoming Webhooks" 토글 활성화
3. "Add New Webhook to Workspace"
4. 알림받을 채널 선택
5. **Webhook URL** 복사 → `SLACK_WEBHOOK_URL`

## 🔧 자동 수정 기능

### 자동 수정 가능한 오류들
- ✅ Flutter 의존성 오류 (`flutter clean`, `flutter pub get`)
- ✅ 패키지 버전 충돌 (`flutter pub upgrade`)
- ✅ 빌드 캐시 문제 (`flutter clean`)
- ✅ Python 패키지 누락 (`pip install`)

### 수동 수정 필요한 오류들
- ❌ 소스 코드 문법 오류
- ❌ API 키 누락/만료
- ❌ 네트워크 연결 문제
- ❌ 시스템 환경 설정 오류

## 📈 알림 유형

### 🔴 즉시 알림 (High/Critical)
- API 키 오류
- 빌드 실패
- 시스템 오류

### 🟠 중요 알림 (Medium)
- 의존성 문제
- 성능 이슈
- 자동 수정 실패

### 🟡 일반 알림 (Low)
- 자동 수정 성공
- 일일 통계 리포트

## 🎯 실제 사용 예시

### 시나리오 1: Flutter 빌드 오류
1. **감지**: `flutter build apk` 실패 감지
2. **분석**: AI가 오류 로그 분석
3. **수정**: `flutter clean && flutter pub get` 자동 실행
4. **성공 시**: ✅ Slack에 "자동 수정 완료" 알림
5. **실패 시**: 🔴 Slack에 "수동 수정 필요" + Notion에 상세 기록

### 시나리오 2: API 호출 실패
1. **감지**: Gemini API 호출 오류 감지
2. **분석**: API 키 만료 또는 할당량 초과 판단
3. **알림**: 🔴 즉시 Slack 알림 "API 키 확인 필요"
4. **기록**: Notion에 상세 오류 로그 및 해결 방법 기록

## 📊 일일 리포트 예시

매일 오전 9시에 Slack으로 전송:
```
📊 앱 팩토리 일일 리포트 (2025-09-21)

총 오류: 5개
자동 수정: 3개
수동 필요: 2개

심각도별 분포:
🟡 Low: 2개
🟠 Medium: 2개
🔴 High: 1개

오류 유형별:
• Flutter Dependency: 2개
• API Error: 1개
• Build Error: 2개
```

## 🔄 모니터링 주기

- **실시간**: 오류 발생시 즉시 감지
- **10분마다**: 전체 시스템 상태 체크
- **1시간마다**: 헬스체크 및 의존성 확인
- **매일 오전 9시**: 일일 리포트 생성

## 🛠️ 고급 설정

### 커스텀 오류 패턴 추가
`error_monitoring_system.py`의 `error_patterns` 수정:
```python
error_patterns = [
    r"ERROR:.*",
    r"Traceback.*",
    r"Exception:.*",
    r"Failed.*",
    r"TimeoutError.*",
    r"Your custom pattern.*"  # 추가
]
```

### 알림 필터링
심각도별 알림 설정:
```python
# High/Critical만 즉시 알림
if error_data['severity'] in ['High', 'Critical']:
    await self.send_slack_notification(error_data)
```

## 🚀 실행 명령어 요약

```bash
# 연속 모니터링 (권장)
python run_monitoring.py

# 일회성 체크
python error_monitoring_system.py

# 테스트 알림 (설정 확인용)
python -c "
import asyncio
from error_monitoring_system import ErrorMonitoringSystem
async def test():
    monitor = ErrorMonitoringSystem()
    await monitor.send_slack_notification({
        'app_name': 'Test',
        'error_type': 'Test Alert',
        'severity': 'Low',
        'description': 'Slack 연동 테스트',
        'auto_fixable': False
    })
asyncio.run(test())
"
```

---

💡 **팁**: 처음 설정할 때는 테스트 알림부터 보내서 Slack과 Notion 연동이 제대로 되는지 확인하세요!

🎉 **이제 완전 자동화된 오류 모니터링 시스템이 24/7로 앱 팩토리를 지켜드립니다!**