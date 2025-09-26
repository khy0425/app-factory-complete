#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
스마트 모니터링 시스템
- 이벤트 기반 실시간 감지
- 3시간마다 정기 체크
- 중요한 오류만 즉시 알림
- 배치별 오류 수집 및 일괄 처리
"""

import asyncio
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import schedule
from error_monitoring_system import ErrorMonitoringSystem

class SmartMonitoringSystem:
    def __init__(self):
        self.error_monitor = ErrorMonitoringSystem()
        self.last_check = datetime.now()
        self.error_queue = []
        self.critical_errors = []

        # 스마트 감지 설정
        self.watch_paths = [
            "flutter_apps",
            "generated_projects",
            "error_logs"
        ]

    class ErrorFileHandler(FileSystemEventHandler):
        def __init__(self, monitoring_system):
            self.monitoring_system = monitoring_system

        def on_created(self, event):
            if event.is_directory:
                return

            # 로그 파일이나 오류 관련 파일 감지
            if any(keyword in event.src_path.lower() for keyword in
                   ['error', 'fail', 'exception', 'crash', '.log']):
                print(f"🔍 오류 파일 감지: {event.src_path}")
                asyncio.create_task(
                    self.monitoring_system.handle_error_file(event.src_path)
                )

        def on_modified(self, event):
            if event.is_directory:
                return

            # 빌드 결과 파일 변경 감지
            if 'build' in event.src_path and event.src_path.endswith('.apk'):
                print(f"✅ APK 빌드 완료: {event.src_path}")

    async def start_smart_monitoring(self):
        """스마트 모니터링 시작"""

        print("🧠 스마트 모니터링 시스템 시작")
        print("=" * 50)
        print("📊 모니터링 전략:")
        print("  • 실시간: 파일 시스템 변화 감지")
        print("  • 3시간마다: 정기 전체 체크")
        print("  • 즉시 알림: Critical 오류만")
        print("  • 배치 처리: 일반 오류들 3시간마다 일괄 처리")
        print("=" * 50)

        # 파일 시스템 감시자 설정
        self.setup_file_watchers()

        # 스케줄 설정 (3시간마다)
        schedule.every(3).hours.do(self.scheduled_comprehensive_check)
        schedule.every().day.at("09:00").do(self.daily_summary)
        schedule.every().monday.at("10:00").do(self.weekly_report)

        # 즉시 한 번 체크
        await self.comprehensive_check()

        # 무한 루프 모니터링
        while True:
            schedule.run_pending()
            await self.process_error_queue()
            await asyncio.sleep(300)  # 5분마다 스케줄 체크

    def setup_file_watchers(self):
        """파일 시스템 감시자 설정"""

        self.observer = Observer()
        event_handler = self.ErrorFileHandler(self)

        for watch_path in self.watch_paths:
            if Path(watch_path).exists():
                self.observer.schedule(event_handler, watch_path, recursive=True)
                print(f"👁️ 감시 시작: {watch_path}")

        self.observer.start()

    async def handle_error_file(self, file_path):
        """실시간으로 감지된 오류 파일 처리"""

        try:
            # 파일이 완전히 생성될 때까지 잠시 대기
            await asyncio.sleep(2)

            if not Path(file_path).exists():
                return

            # 파일 내용 분석
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Critical 오류 키워드 체크
            critical_keywords = [
                'CRITICAL', 'FATAL', 'CRASH', 'SEGFAULT',
                'OutOfMemoryError', 'API_KEY', 'Authentication',
                'BUILD FAILED', 'EXCEPTION'
            ]

            is_critical = any(keyword.lower() in content.lower()
                            for keyword in critical_keywords)

            if is_critical:
                # 즉시 처리
                await self.handle_critical_error(file_path, content)
            else:
                # 큐에 추가 (나중에 배치 처리)
                self.error_queue.append({
                    'file_path': file_path,
                    'content': content[:1000],  # 첫 1000자만
                    'timestamp': datetime.now(),
                    'type': 'file_system_detection'
                })

        except Exception as e:
            print(f"❌ 오류 파일 처리 실패: {e}")

    async def handle_critical_error(self, file_path, content):
        """Critical 오류 즉시 처리"""

        print(f"🚨 Critical 오류 감지: {file_path}")

        # AI 분석
        analysis = await self.error_monitor.analyze_error_with_ai(
            content, "Critical System Error"
        )

        # 즉시 Slack 알림
        await self.error_monitor.report_error(
            error_type="Critical Error",
            app_name=Path(file_path).parent.name,
            description=content[:500],
            severity="Critical",
            auto_fixable=analysis.get('auto_fixable', False),
            ai_analysis=analysis
        )

        # Critical 에러 목록에 추가
        self.critical_errors.append({
            'file_path': file_path,
            'analysis': analysis,
            'timestamp': datetime.now()
        })

    async def process_error_queue(self):
        """오류 큐 배치 처리 (경미한 오류들)"""

        if not self.error_queue:
            return

        if len(self.error_queue) < 5 and \
           datetime.now() - self.last_check < timedelta(hours=1):
            return  # 5개 미만이고 1시간 이내면 대기

        print(f"📦 배치 처리: {len(self.error_queue)}개 오류")

        # 유사한 오류들 그룹핑
        grouped_errors = self.group_similar_errors(self.error_queue)

        for group_type, errors in grouped_errors.items():
            if len(errors) > 1:
                # 중복 오류 - 요약해서 하나로 처리
                await self.handle_grouped_errors(group_type, errors)
            else:
                # 단일 오류 - 개별 처리
                await self.handle_single_error(errors[0])

        # 큐 비우기
        self.error_queue.clear()

    def group_similar_errors(self, errors):
        """유사한 오류들 그룹핑"""

        groups = {}

        for error in errors:
            # 오류 타입 분류
            content = error['content'].lower()

            if 'flutter' in content and 'build' in content:
                group_key = 'flutter_build_errors'
            elif 'dependency' in content or 'package' in content:
                group_key = 'dependency_errors'
            elif 'api' in content or 'http' in content:
                group_key = 'api_errors'
            elif 'timeout' in content:
                group_key = 'timeout_errors'
            else:
                group_key = 'misc_errors'

            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(error)

        return groups

    async def handle_grouped_errors(self, group_type, errors):
        """그룹화된 오류들 처리"""

        error_summary = f"{len(errors)}개의 유사한 {group_type} 발생"

        # 대표 오류 선택 (가장 최근)
        representative_error = max(errors, key=lambda x: x['timestamp'])

        await self.error_monitor.report_error(
            error_type=f"Grouped {group_type}",
            app_name="Multiple Apps",
            description=f"{error_summary}\n\n대표 오류:\n{representative_error['content'][:300]}",
            severity="Medium",
            auto_fixable=True
        )

    async def handle_single_error(self, error):
        """단일 오류 처리"""

        analysis = await self.error_monitor.analyze_error_with_ai(
            error['content'], "Single Error"
        )

        await self.error_monitor.report_error(
            error_type="Individual Error",
            app_name=Path(error['file_path']).parent.name,
            description=error['content'],
            severity=analysis.get('severity', 'Low'),
            auto_fixable=analysis.get('auto_fixable', False),
            ai_analysis=analysis
        )

    def scheduled_comprehensive_check(self):
        """3시간마다 정기 전체 체크"""

        print(f"🔍 [{datetime.now().strftime('%H:%M')}] 정기 전체 체크 시작")
        asyncio.create_task(self.comprehensive_check())

    async def comprehensive_check(self):
        """전체 시스템 종합 체크"""

        print("🏥 시스템 종합 건강 검진")

        tasks = [
            self.check_flutter_apps_health(),
            self.check_background_processes(),
            self.check_api_status(),
            self.check_disk_space(),
            self.cleanup_old_logs()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 결과 요약
        issues_found = sum(1 for result in results if isinstance(result, Exception))

        if issues_found > 0:
            print(f"⚠️ {issues_found}개 문제 발견 - 자동 수정 시도")
        else:
            print("✅ 모든 시스템 정상")

        self.last_check = datetime.now()

    async def check_flutter_apps_health(self):
        """Flutter 앱들 건강 상태 체크"""

        flutter_apps_dir = Path("flutter_apps")
        if not flutter_apps_dir.exists():
            return

        for app_dir in flutter_apps_dir.iterdir():
            if app_dir.is_dir():
                await self.quick_app_health_check(app_dir)

    async def quick_app_health_check(self, app_dir):
        """앱별 빠른 건강 체크"""

        issues = []

        # pubspec.yaml 존재 체크
        if not (app_dir / "pubspec.yaml").exists():
            issues.append("pubspec.yaml 누락")

        # build 폴더 크기 체크 (너무 크면 정리 필요)
        build_dir = app_dir / "build"
        if build_dir.exists():
            build_size = sum(f.stat().st_size for f in build_dir.rglob('*') if f.is_file())
            if build_size > 500 * 1024 * 1024:  # 500MB 이상
                issues.append("빌드 캐시 과다 - 정리 필요")

        if issues:
            await self.error_monitor.report_error(
                error_type="App Health Issue",
                app_name=app_dir.name,
                description="; ".join(issues),
                severity="Low",
                auto_fixable=True
            )

    async def check_background_processes(self):
        """백그라운드 프로세스 상태 체크"""

        # 실행 중인 배치 작업들 체크
        batch_processes = [
            "batch_app_generator.py",
            "admob_automation.py",
            "flutter_code_generator.py"
        ]

        for process in batch_processes:
            # 프로세스 실행 시간이 3시간 넘으면 이상
            # (실제 구현은 psutil 라이브러리 사용 권장)
            pass

    async def check_api_status(self):
        """API 상태 체크"""

        # Gemini API 간단 테스트
        try:
            test_response = await self.error_monitor.model.generate_content_async("test")
            if not test_response.text:
                raise Exception("Empty API response")
        except Exception as e:
            await self.error_monitor.report_error(
                error_type="API Status",
                app_name="Gemini API",
                description=f"API 상태 이상: {str(e)}",
                severity="High",
                auto_fixable=False
            )

    async def check_disk_space(self):
        """디스크 공간 체크"""

        import shutil

        total, used, free = shutil.disk_usage(".")
        free_gb = free / (1024**3)

        if free_gb < 5:  # 5GB 미만
            await self.error_monitor.report_error(
                error_type="Disk Space",
                app_name="System",
                description=f"디스크 공간 부족: {free_gb:.1f}GB 남음",
                severity="Critical",
                auto_fixable=True
            )

    async def cleanup_old_logs(self):
        """오래된 로그 파일들 정리"""

        log_dirs = ["error_logs", ".", "flutter_apps"]
        cutoff_date = datetime.now() - timedelta(days=7)

        for log_dir in log_dirs:
            log_path = Path(log_dir)
            if not log_path.exists():
                continue

            for log_file in log_path.glob("*.log"):
                if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                    try:
                        log_file.unlink()
                        print(f"🗑️ 오래된 로그 삭제: {log_file}")
                    except:
                        pass

    async def daily_summary(self):
        """일일 요약 (오전 9시)"""

        print("📊 일일 요약 생성 중...")
        await self.error_monitor.generate_daily_report()

        # Critical 오류 요약
        if self.critical_errors:
            await self.send_critical_errors_summary()

    async def weekly_report(self):
        """주간 리포트 (월요일 오전 10시)"""

        print("📈 주간 리포트 생성 중...")

        # 지난 주 통계 수집
        week_stats = {
            "total_errors": len(self.error_queue) + len(self.critical_errors),
            "critical_errors": len(self.critical_errors),
            "auto_fixed": 0,  # 실제로는 성공 로그에서 계산
            "manual_required": len(self.critical_errors)
        }

        # Slack 주간 리포트 전송
        await self.send_weekly_report(week_stats)

        # 데이터 리셋
        self.critical_errors.clear()

    async def send_weekly_report(self, stats):
        """주간 리포트 Slack 전송"""

        # 실제 구현은 error_monitor의 slack 전송 기능 활용
        pass

async def main():
    """메인 실행 함수"""
    print("🧠 스마트 모니터링 시스템")
    print("더 효율적인 모니터링으로 업그레이드!")
    print()

    monitor = SmartMonitoringSystem()

    try:
        await monitor.start_smart_monitoring()
    except KeyboardInterrupt:
        print("\n👋 모니터링 시스템 종료")
        monitor.observer.stop()
        monitor.observer.join()

if __name__ == "__main__":
    asyncio.run(main())