# 📱 Slack 알림 시스템 설정 가이드

서버리스 앱 팩토리의 실시간 모니터링을 위한 Slack 알림 시스템 설정 방법입니다.

## 🚀 빠른 설정 (5분)

### 1단계: Slack 웹훅 URL 발급

1. **Slack 워크스페이스**에서 [Incoming Webhooks 앱](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 설치
2. **"Add to Slack"** 클릭
3. 알림을 받을 **채널 선택** (예: `#app-factory`)
4. **웹훅 URL 복사** (예: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`)

### 2단계: 앱 팩토리에 설정

```bash
# 대화형 설정
python automation/slack_notifier.py --setup

# 또는 직접 입력
python automation/slack_notifier.py --setup --webhook "https://hooks.slack.com/services/..."
```

### 3단계: 테스트

```bash
python automation/slack_notifier.py --test
```

✅ **"Slack 알림 테스트 성공!"** 메시지가 나타나면 설정 완료!

## 📊 알림 유형

### 🎉 성공 알림
```
✅ App Generation Success
새 앱이 성공적으로 생성되었습니다!

📱 앱 이름: Premium Fitness Timer Pro
💸 비용: $0.665
⭐ 품질 점수: 87/100
🏪 스토어 준비: ✅ 완료
```

### ⚠️ 예산 경고
```
⚠️ Budget Warning
예산 사용률이 85.0%에 도달했습니다.

💰 사용량: $8.50 / $10.00
📱 생성된 앱: 12개
📊 남은 예산: $1.50
```

### 🚨 긴급 상황
```
🚨 CRITICAL: Budget Almost Exhausted
예산이 거의 소진되었습니다!

💰 사용량: $9.80 / $10.00 (98.0%)
📱 생성된 앱: 14개
⚠️ 즉시 확인이 필요합니다!
```

### ❌ 에러 알림
```
❌ App Factory Error
앱 팩토리에서 오류가 발생했습니다.

🔥 오류 유형: API Rate Limit
📱 앱 이름: Smart Todo App
📝 오류 메시지: Rate limit exceeded
```

## ⚙️ 고급 설정

### 알림 임계값 조정

`automation/slack_notifier.py` 파일에서 수정:

```python
self.notification_config = {
    "budget_threshold": 0.8,    # 80% → 70%로 변경
    "critical_threshold": 0.95, # 95% → 90%로 변경
    "error_cooldown": 300,      # 5분 → 10분으로 변경
}
```

### 환경변수로 설정

`.env` 파일에 추가:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

또는 시스템 환경변수:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

## 📱 실제 사용 예시

### 월간 앱 생성 시나리오

```bash
python run_app_factory.py --generate "Fitness Timer Pro"
```

**Slack에서 받는 알림들:**
1. `✅ App Generation Success` - 앱 생성 성공
2. `💰 Budget Alert` - 예산 50% 사용 (필요시)
3. `🚀 Store Deployment` - 스토어 배포 완료

### 에러 발생 시나리오

```bash
# API 키가 만료된 경우
python run_app_factory.py --generate "Todo App"
```

**Slack 알림:**
```
❌ App Factory Error
앱 팩토리에서 오류가 발생했습니다.

🔥 오류 유형: API Authentication Failed
📱 앱 이름: Todo App
📝 오류 메시지: Invalid API key

즉시 확인이 필요합니다!
```

## 🔧 문제 해결

### Q: 알림이 오지 않아요
```bash
# 1. 웹훅 URL 확인
python automation/slack_notifier.py --test

# 2. 설정 파일 확인
cat ~/.config/app-factory/slack.json

# 3. 로그 확인
tail -f serverless_app_factory.log | grep -i slack
```

### Q: 너무 많은 알림이 와요
```python
# 에러 쿨다운 시간 늘리기
"error_cooldown": 600,  # 10분

# 예산 경고 임계값 높이기
"budget_threshold": 0.9,  # 90%
```

### Q: 특정 알림만 받고 싶어요

`SlackNotifier` 클래스에서 조건부 알림 설정:

```python
async def notify_app_generation_success(self, ...):
    # 고품질 앱만 알림
    if quality_score >= 85:
        await self.send_notification(...)
```

## 📈 운영 팁

### 1. 채널 분리
- `#app-factory-success`: 성공 알림만
- `#app-factory-alerts`: 에러/경고만
- `#app-factory-daily`: 일간 요약만

### 2. 멘션 설정
```python
# 긴급 상황 시 특정 사용자 태그
message = f"<@U1234567> {message}"
```

### 3. 시간 필터링
```python
# 근무시간에만 알림
if 9 <= datetime.now().hour <= 18:
    await self.send_notification(...)
```

---

## 🎯 완료 체크리스트

- [ ] Slack 워크스페이스에 Incoming Webhooks 설치
- [ ] 웹훅 URL 발급 및 복사
- [ ] `python automation/slack_notifier.py --setup` 실행
- [ ] `python automation/slack_notifier.py --test` 테스트
- [ ] 첫 번째 앱 생성으로 실제 알림 확인

✅ **설정 완료 후 30초 안에 실시간 모니터링 시작!**