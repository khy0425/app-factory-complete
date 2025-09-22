#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slack Notification System
앱 팩토리 운영 상태 실시간 알림 시스템
"""

import json
import asyncio
import requests
from typing import Dict, Optional
from datetime import datetime
import logging
from pathlib import Path

class SlackNotifier:
    """Slack 웹훅 알림 시스템"""

    def __init__(self, config_manager=None, webhook_url: Optional[str] = None):
        self.logger = logging.getLogger(__name__)

        # 설정 관리자 통합
        if config_manager:
            self.config_manager = config_manager
            self.webhook_url = self.config_manager.get_api_key("SLACK_WEBHOOK_URL")
        else:
            # 기존 방식 호환성 유지
            self.webhook_url = webhook_url or self._load_webhook_url()

        # 알림 설정
        self.notification_config = {
            "budget_threshold": 0.8,  # 예산 80% 사용 시 경고
            "critical_threshold": 0.95,  # 예산 95% 사용 시 긴급
            "error_cooldown": 300,  # 같은 에러 5분 쿨다운
            "enabled": bool(self.webhook_url)
        }

        # 에러 쿨다운 추적
        self.error_history = {}

    def _load_webhook_url(self) -> Optional[str]:
        """Slack 웹훅 URL 로드"""
        try:
            # 환경변수에서 로드
            import os
            webhook = os.getenv("SLACK_WEBHOOK_URL")
            if webhook:
                return webhook

            # 설정 파일에서 로드
            config_file = Path.home() / ".config/app-factory/slack.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("webhook_url")

        except Exception as e:
            self.logger.warning(f"⚠️ Slack 웹훅 URL 로드 실패: {e}")

        return None

    def send_notification(self, message: str, level: str = "info",
                              title: str = "App Factory Alert") -> bool:
        """Slack 알림 전송"""

        if not self.notification_config["enabled"]:
            self.logger.debug("Slack 알림이 비활성화됨")
            return False

        # 이모지 및 색상 설정
        emoji_map = {
            "success": "✅",
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨",
            "budget": "💰"
        }

        color_map = {
            "success": "good",
            "info": "#36a64f",
            "warning": "warning",
            "error": "danger",
            "critical": "danger",
            "budget": "#ffaa00"
        }

        # Slack 페이로드 구성
        payload = {
            "text": f"{emoji_map.get(level, 'ℹ️')} {title}",
            "attachments": [
                {
                    "color": color_map.get(level, "#36a64f"),
                    "fields": [
                        {
                            "title": "Message",
                            "value": message,
                            "short": False
                        },
                        {
                            "title": "Timestamp",
                            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "short": True
                        },
                        {
                            "title": "Level",
                            "value": level.upper(),
                            "short": True
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                self.logger.info(f"📱 Slack 알림 전송 성공: {level}")
                return True
            else:
                self.logger.error(f"❌ Slack 알림 실패: {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Slack 알림 전송 오류: {e}")
            return False

    def notify_budget_alert(self, spent: float, budget: float, apps_generated: int):
        """예산 관련 알림"""
        usage_percentage = (spent / budget) * 100 if budget > 0 else 0

        if usage_percentage >= self.notification_config["critical_threshold"] * 100:
            level = "critical"
            title = "🚨 CRITICAL: Budget Almost Exhausted"
            message = f"""
예산이 거의 소진되었습니다!

💰 사용량: ${spent:.2f} / ${budget:.2f} ({usage_percentage:.1f}%)
📱 생성된 앱: {apps_generated}개
⚠️ 즉시 확인이 필요합니다!
"""
        elif usage_percentage >= self.notification_config["budget_threshold"] * 100:
            level = "warning"
            title = "⚠️ Budget Warning"
            message = f"""
예산 사용률이 {usage_percentage:.1f}%에 도달했습니다.

💰 사용량: ${spent:.2f} / ${budget:.2f}
📱 생성된 앱: {apps_generated}개
📊 남은 예산: ${budget - spent:.2f}
"""
        else:
            return  # 알림 필요 없음

        self.send_notification(message, level, title)

    def notify_app_generation_success(self, app_name: str, cost: float,
                                          quality_score: int, store_ready: bool):
        """앱 생성 성공 알림"""
        message = f"""
새 앱이 성공적으로 생성되었습니다! 🎉

📱 앱 이름: {app_name}
💸 비용: ${cost:.3f}
⭐ 품질 점수: {quality_score}/100
🏪 스토어 준비: {'✅ 완료' if store_ready else '⚠️ 추가 작업 필요'}
"""
        self.send_notification(message, "success", "App Generation Success")

    def notify_error(self, error_type: str, error_message: str, app_name: str = None):
        """에러 발생 알림 (쿨다운 적용)"""

        # 에러 키 생성 (중복 방지용)
        error_key = f"{error_type}_{hash(error_message) % 10000}"
        current_time = datetime.now().timestamp()

        # 쿨다운 체크
        if error_key in self.error_history:
            last_sent = self.error_history[error_key]
            if current_time - last_sent < self.notification_config["error_cooldown"]:
                self.logger.debug(f"에러 알림 쿨다운: {error_key}")
                return

        # 에러 알림 전송
        message = f"""
앱 팩토리에서 오류가 발생했습니다.

🔥 오류 유형: {error_type}
📱 앱 이름: {app_name or 'N/A'}
📝 오류 메시지: {error_message}

즉시 확인이 필요합니다!
"""

        self.send_notification(message, "error", "App Factory Error")

        # 쿨다운 기록 업데이트
        self.error_history[error_key] = current_time

    def notify_system_status(self, status_data: Dict):
        """시스템 상태 요약 알림"""

        current_month = status_data.get("current_month", {})
        performance = status_data.get("performance_metrics", {})

        message = f"""
📊 월간 팩토리 상태 리포트

💰 예산: {current_month.get('budget_spent', 'N/A')} / {current_month.get('budget_remaining', 'N/A')}
📱 앱 생성: {current_month.get('apps_generated', 0)}개
⭐ 평균 품질: {performance.get('avg_quality_score', 0):.1f}/100
🏪 스토어 배포율: {performance.get('store_deployment_rate', '0%')}
✅ 규정 준수율: {performance.get('compliance_success_rate', '0%')}

시스템이 정상 작동 중입니다! 🚀
"""

        self.send_notification(message, "info", "Factory Status Report")

    def notify_daily_summary(self, apps_today: int, cost_today: float,
                                 successful_deployments: int):
        """일간 요약 알림"""
        message = f"""
📅 오늘의 팩토리 성과

📱 생성된 앱: {apps_today}개
💸 사용된 예산: ${cost_today:.2f}
🚀 스토어 배포: {successful_deployments}개
📈 성공률: {(successful_deployments/apps_today*100):.1f}% (앱당)

훌륭한 하루였습니다! 🎉
"""
        self.send_notification(message, "success", "Daily Summary")

    def setup_webhook_url(self, webhook_url: str) -> bool:
        """Slack 웹훅 URL 설정"""
        try:
            # 설정 디렉토리 생성
            config_dir = Path.home() / ".config/app-factory"
            config_dir.mkdir(parents=True, exist_ok=True)

            # 설정 파일 저장
            config_file = config_dir / "slack.json"
            config = {
                "webhook_url": webhook_url,
                "setup_date": datetime.now().isoformat(),
                "enabled": True
            }

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            self.webhook_url = webhook_url
            self.notification_config["enabled"] = True

            self.logger.info("✅ Slack 웹훅 URL 설정 완료")
            return True

        except Exception as e:
            self.logger.error(f"❌ Slack 웹훅 설정 실패: {e}")
            return False

    def test_notification(self) -> bool:
        """알림 시스템 테스트"""
        if not self.notification_config["enabled"]:
            print("❌ Slack 웹훅이 설정되지 않았습니다.")
            print("💡 python automation/slack_notifier.py --setup 을 실행하여 설정하세요.")
            return False

        test_message = """
🧪 Slack 알림 시스템 테스트

이 메시지가 보인다면 알림 시스템이 정상 작동합니다!

📅 테스트 시간: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        success = self.send_notification(
            test_message,
            "info",
            "🧪 Notification Test"
        )

        if success:
            print("✅ Slack 알림 테스트 성공!")
        else:
            print("❌ Slack 알림 테스트 실패")

        return success

def main():
    """CLI 인터페이스"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description="Slack 알림 시스템 관리")
    parser.add_argument("--setup", action="store_true", help="Slack 웹훅 URL 설정")
    parser.add_argument("--test", action="store_true", help="알림 시스템 테스트")
    parser.add_argument("--webhook", type=str, help="Slack 웹훅 URL (--setup과 함께 사용)")

    args = parser.parse_args()

    notifier = SlackNotifier()

    if args.setup:
        webhook_url = args.webhook
        if not webhook_url:
            print("Slack 웹훅 URL을 입력하세요:")
            print("1. Slack에서 Incoming Webhook 앱 설치")
            print("2. 웹훅 URL 복사 (https://hooks.slack.com/services/...)")
            webhook_url = input("웹훅 URL: ").strip()

        if webhook_url:
            success = notifier.setup_webhook_url(webhook_url)
            if success:
                print("✅ Slack 알림 설정 완료!")
                print("💡 python automation/slack_notifier.py --test 로 테스트하세요.")
            else:
                print("❌ 설정 실패")
        else:
            print("❌ 웹훅 URL이 필요합니다.")

    elif args.test:
        notifier.test_notification()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()