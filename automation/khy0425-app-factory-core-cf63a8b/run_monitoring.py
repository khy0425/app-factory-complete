#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 모니터링 실행기
- 오류 모니터링 시스템 실행
- 주기적 상태 체크
- 자동 수정 및 알림
"""

import asyncio
import schedule
import time
from datetime import datetime
from error_monitoring_system import ErrorMonitoringSystem

class MonitoringRunner:
    def __init__(self):
        self.monitoring_system = ErrorMonitoringSystem()
        self.is_running = False

    async def start_continuous_monitoring(self):
        """연속적인 모니터링 시작"""

        print("🤖 앱 팩토리 통합 모니터링 시작")
        print("- 실시간 오류 감지")
        print("- 자동 수정 시도")
        print("- Notion 자동 정리")
        print("- Slack 실시간 알림")
        print("=" * 60)

        self.is_running = True

        # 즉시 한 번 실행
        await self.monitoring_system.monitor_all_processes()

        # 주기적 실행 스케줄 설정
        schedule.every(10).minutes.do(self.schedule_monitoring)  # 10분마다 모니터링
        schedule.every().hour.do(self.schedule_health_check)     # 1시간마다 헬스체크
        schedule.every().day.at("09:00").do(self.schedule_daily_report)  # 매일 오전 9시 리포트

        # 스케줄러 실행
        while self.is_running:
            schedule.run_pending()
            await asyncio.sleep(60)  # 1분마다 스케줄 체크

    def schedule_monitoring(self):
        """스케줄된 모니터링 실행"""
        asyncio.create_task(self.monitoring_system.monitor_all_processes())

    def schedule_health_check(self):
        """헬스체크 실행"""
        print(f"🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 헬스체크 실행")
        asyncio.create_task(self.monitoring_system.check_dependency_issues())

    def schedule_daily_report(self):
        """일일 리포트 생성"""
        print(f"📊 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 일일 리포트 생성")
        asyncio.create_task(self.monitoring_system.generate_daily_report())

    def stop_monitoring(self):
        """모니터링 중지"""
        self.is_running = False
        print("🛑 모니터링 시스템 중지")

async def main():
    """메인 실행 함수"""

    runner = MonitoringRunner()

    try:
        await runner.start_continuous_monitoring()
    except KeyboardInterrupt:
        print("\n📋 사용자에 의해 중단됨")
        runner.stop_monitoring()
    except Exception as e:
        print(f"❌ 모니터링 시스템 오류: {e}")

if __name__ == "__main__":
    print("🚀 앱 팩토리 통합 모니터링 시스템")
    print("Ctrl+C로 중단할 수 있습니다")
    print()

    asyncio.run(main())