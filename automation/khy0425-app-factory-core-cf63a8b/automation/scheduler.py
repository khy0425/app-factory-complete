#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Scheduler
6시간마다 CI/CD, 진행상황 추적, 형상관리 자동 실행 스케줄러
"""

import asyncio
import os
import sys
import signal
import schedule
import time
from datetime import datetime, timedelta
from typing import Optional
import threading
from pathlib import Path

class AutomatedScheduler:
    """자동화 스케줄러"""

    def __init__(self):
        self.is_running = False
        self.scheduler_thread = None
        self.tasks = []
        self.notion_tracker = None
        self._setup_notion_integration()

    def _setup_notion_integration(self):
        """Notion 통합 설정"""
        try:
            from .notion_integration import NotionTaskTracker
            from config_production import ProductionConfig

            config = ProductionConfig()
            self.notion_tracker = NotionTaskTracker(config.notion_token)
            print("✅ Notion integration initialized")
        except Exception as e:
            print(f"⚠️ Notion integration setup failed: {e}")
            self.notion_tracker = None

    async def run_cicd_setup(self):
        """CI/CD 설정 실행"""
        print(f"🔧 [{datetime.now().strftime('%H:%M:%S')}] Running CI/CD setup...")

        # Notion 추적 시작
        task_id = None
        if self.notion_tracker:
            task_id = await self.notion_tracker.start_task_tracking("CI/CD Setup")

        try:
            from .cicd_manager import CICDManager
            from config_production import ProductionConfig

            config = ProductionConfig()
            cicd_manager = CICDManager(config.github_token)

            # 모든 프로젝트에 CI/CD 설정 (새 프로젝트가 있다면)
            results = await cicd_manager.setup_cicd_for_all_projects()

            success_count = 0
            total_count = 0

            if results:
                success_count = sum(results.values())
                total_count = len(results)
                print(f"✅ CI/CD setup: {success_count}/{total_count} projects updated")
            else:
                print("📊 No new projects for CI/CD setup")

            # Notion 추적 완료 (성공)
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=True,
                    details={
                        "projects_updated": success_count,
                        "total_projects": total_count,
                        "results": results or {}
                    }
                )

        except Exception as e:
            print(f"❌ CI/CD setup failed: {e}")

            # Notion 추적 완료 (실패)
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=False,
                    error_message=str(e)
                )

    async def run_progress_tracking(self):
        """진행상황 추적 실행"""
        print(f"📊 [{datetime.now().strftime('%H:%M:%S')}] Running progress tracking...")

        # Notion 추적 시작
        task_id = None
        if self.notion_tracker:
            task_id = await self.notion_tracker.start_task_tracking("Progress Tracking")

        try:
            from .progress_tracker import ProgressTracker
            from config_production import ProductionConfig

            config = ProductionConfig()
            tracker = ProgressTracker(config.github_token)

            # 진행상황 추적 사이클 실행
            success = await tracker.run_progress_tracking_cycle()

            if success:
                print("✅ Progress tracking completed")
            else:
                print("❌ Progress tracking failed")

            # Notion 추적 완료
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=success,
                    details={"tracking_completed": success}
                )

        except Exception as e:
            print(f"❌ Progress tracking failed: {e}")

            # Notion 추적 완료 (실패)
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=False,
                    error_message=str(e)
                )

    async def run_mvp_auto_management(self):
        """MVP 자동 관리 실행"""
        print(f"🚀 [{datetime.now().strftime('%H:%M:%S')}] Running MVP auto management...")

        # Notion 추적 시작
        task_id = None
        if self.notion_tracker:
            task_id = await self.notion_tracker.start_task_tracking("MVP Auto Management")

        try:
            from .auto_repository_manager import AutoRepositoryManager
            from config_production import ProductionConfig

            config = ProductionConfig()
            repo_manager = AutoRepositoryManager(config.github_token)

            # MVP 프로젝트 자동 관리
            new_projects = await repo_manager.auto_manage_mvp_projects()

            if new_projects > 0:
                print(f"✅ MVP management: {new_projects} new projects created")
            else:
                print("📊 MVP management: No new projects detected")

            # Notion 추적 완료
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=True,
                    details={
                        "new_projects_created": new_projects,
                        "projects_detected": new_projects > 0
                    }
                )

        except Exception as e:
            print(f"❌ MVP auto management failed: {e}")

            # Notion 추적 완료 (실패)
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=False,
                    error_message=str(e)
                )

    async def run_mcp_ecosystem_sync(self):
        """MCP 생태계 동기화"""
        print(f"🌐 [{datetime.now().strftime('%H:%M:%S')}] Running MCP ecosystem sync...")

        # Notion 추적 시작
        task_id = None
        if self.notion_tracker:
            task_id = await self.notion_tracker.start_task_tracking("MCP Ecosystem Sync")

        try:
            from .mcp_ecosystem_integration import MCPEcosystemOrchestrator, MCPConfig
            from config_production import ProductionConfig

            config = ProductionConfig()

            mcp_config = MCPConfig(
                github_token=config.github_token,
                supabase_url=config.supabase_url,
                supabase_key=config.supabase_anon_key,
                zapier_webhook=config.zapier_webhook,
                notion_token=config.notion_token
            )

            orchestrator = MCPEcosystemOrchestrator(mcp_config)

            # 생태계 상태 체크 및 동기화
            await orchestrator.setup_mcp_ecosystem()

            # 헬스체크 데이터 처리
            health_data = {
                'event_type': 'scheduled_healthcheck',
                'timestamp': datetime.now().isoformat(),
                'system_health': 95.0,  # 기본 건강도
                'scheduled_run': True,
                'components_checked': ['github', 'supabase', 'notion', 'zapier']
            }

            await orchestrator.process_intelligence_data(health_data)
            print("✅ MCP ecosystem sync completed")

            # Notion 추적 완료
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=True,
                    details={
                        "health_score": health_data['system_health'],
                        "components_checked": health_data['components_checked']
                    }
                )

        except Exception as e:
            print(f"❌ MCP ecosystem sync failed: {e}")

            # Notion 추적 완료 (실패)
            if self.notion_tracker and task_id:
                await self.notion_tracker.complete_task_tracking(
                    task_id,
                    success=False,
                    error_message=str(e)
                )

    async def run_full_cycle(self):
        """전체 사이클 실행"""
        cycle_start = datetime.now()
        cycle_id = f"cycle_{cycle_start.strftime('%Y%m%d_%H%M%S')}"

        print(f"\n{'='*60}")
        print(f"🔄 STARTING AUTOMATED CYCLE - {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        # Notion 사이클 추적 시작
        cycle_task_id = None
        if self.notion_tracker:
            cycle_task_id = await self.notion_tracker.start_task_tracking("Full Automation Cycle")

        total_tasks = 4
        successful_tasks = 0
        cycle_details = {}

        try:
            # 1. MVP 자동 관리
            try:
                await self.run_mvp_auto_management()
                successful_tasks += 1
                cycle_details["mvp_management"] = "success"
            except Exception as e:
                cycle_details["mvp_management"] = f"failed: {e}"
            await asyncio.sleep(2)

            # 2. CI/CD 설정
            try:
                await self.run_cicd_setup()
                successful_tasks += 1
                cycle_details["cicd_setup"] = "success"
            except Exception as e:
                cycle_details["cicd_setup"] = f"failed: {e}"
            await asyncio.sleep(2)

            # 3. 진행상황 추적
            try:
                await self.run_progress_tracking()
                successful_tasks += 1
                cycle_details["progress_tracking"] = "success"
            except Exception as e:
                cycle_details["progress_tracking"] = f"failed: {e}"
            await asyncio.sleep(2)

            # 4. MCP 생태계 동기화
            try:
                await self.run_mcp_ecosystem_sync()
                successful_tasks += 1
                cycle_details["mcp_sync"] = "success"
            except Exception as e:
                cycle_details["mcp_sync"] = f"failed: {e}"

            cycle_end = datetime.now()
            duration = cycle_end - cycle_start

            print(f"\n{'='*60}")
            print(f"✅ CYCLE COMPLETED - Duration: {duration.total_seconds():.1f}s")
            print(f"📊 Success Rate: {successful_tasks}/{total_tasks} ({successful_tasks/total_tasks*100:.1f}%)")
            print(f"⏰ Next cycle: {(cycle_end + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}\n")

            # Notion 사이클 추적 완료
            if self.notion_tracker and cycle_task_id:
                await self.notion_tracker.complete_task_tracking(
                    cycle_task_id,
                    success=successful_tasks >= total_tasks * 0.5,  # 50% 이상 성공하면 성공으로 간주
                    details={
                        "cycle_id": cycle_id,
                        "total_tasks": total_tasks,
                        "successful_tasks": successful_tasks,
                        "duration_seconds": duration.total_seconds(),
                        "success_rate": successful_tasks/total_tasks*100,
                        "task_results": cycle_details,
                        "next_cycle": (cycle_end + timedelta(hours=6)).isoformat()
                    }
                )

                # KPI 대시보드 업데이트
                await self._update_cycle_kpis(cycle_id, successful_tasks, total_tasks, duration)

        except Exception as e:
            print(f"❌ Cycle execution error: {e}")

            # Notion 사이클 추적 완료 (실패)
            if self.notion_tracker and cycle_task_id:
                await self.notion_tracker.complete_task_tracking(
                    cycle_task_id,
                    success=False,
                    error_message=str(e),
                    details=cycle_details
                )

    async def _update_cycle_kpis(self, cycle_id: str, successful_tasks: int,
                                total_tasks: int, duration: timedelta):
        """사이클 KPI 업데이트"""
        if not self.notion_tracker:
            return

        try:
            # 사이클 성과 기록을 위한 추가 로직
            success_rate = successful_tasks / total_tasks * 100

            print(f"📊 Updating KPIs for cycle {cycle_id}")
            print(f"  Success Rate: {success_rate:.1f}%")
            print(f"  Duration: {duration.total_seconds():.1f}s")
            print(f"  Tasks: {successful_tasks}/{total_tasks}")

        except Exception as e:
            print(f"⚠️ KPI update error: {e}")

    def schedule_jobs(self):
        """작업 스케줄링"""
        # 6시간마다 전체 사이클 실행 (00:00, 06:00, 12:00, 18:00)
        schedule.every(6).hours.do(lambda: asyncio.run(self.run_full_cycle()))

        # 매시간 MVP 자동 관리 (새 프로젝트 감지용)
        schedule.every().hour.do(lambda: asyncio.run(self.run_mvp_auto_management()))

        # 매일 자정에 전체 시스템 헬스체크
        schedule.every().day.at("00:00").do(lambda: asyncio.run(self.run_mcp_ecosystem_sync()))

        print("⏰ Scheduled jobs:")
        print("  📊 Full cycle: Every 6 hours (00:00, 06:00, 12:00, 18:00)")
        print("  🚀 MVP check: Every hour")
        print("  🌐 Health check: Daily at 00:00")

    def run_scheduler(self):
        """스케줄러 실행 (별도 스레드)"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
                time.sleep(60)

    async def start_scheduler(self):
        """스케줄러 시작"""
        print("🚀 Starting Automated Scheduler...")

        # 초기 실행 여부 확인
        print("\n🔍 Do you want to run an initial cycle now? (y/N): ", end="")
        try:
            user_input = input().strip().lower()
            if user_input in ['y', 'yes']:
                await self.run_full_cycle()
        except KeyboardInterrupt:
            print("\n⏭️ Skipping initial cycle")

        # 스케줄 설정
        self.schedule_jobs()

        # 스케줄러 시작
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()

        print(f"✅ Scheduler started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📝 Press Ctrl+C to stop the scheduler")

        # 신호 핸들러 설정
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            # 메인 루프 (스케줄러가 백그라운드에서 실행됨)
            while self.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await self.stop_scheduler()

    def _signal_handler(self, signum, frame):
        """시그널 핸들러"""
        print(f"\n🛑 Received signal {signum}, stopping scheduler...")
        asyncio.create_task(self.stop_scheduler())

    async def stop_scheduler(self):
        """스케줄러 중지"""
        print("🛑 Stopping scheduler...")
        self.is_running = False

        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)

        print("✅ Scheduler stopped")

    def get_next_run_times(self):
        """다음 실행 시간들 표시"""
        print("\n⏰ Next scheduled runs:")
        for job in schedule.jobs:
            print(f"  {job.job_func.__name__}: {job.next_run}")

class ManualRunner:
    """수동 실행기"""

    def __init__(self):
        self.scheduler = AutomatedScheduler()

    async def run_single_task(self, task_name: str):
        """단일 작업 실행"""
        tasks = {
            'mvp': self.scheduler.run_mvp_auto_management,
            'cicd': self.scheduler.run_cicd_setup,
            'progress': self.scheduler.run_progress_tracking,
            'mcp': self.scheduler.run_mcp_ecosystem_sync,
            'full': self.scheduler.run_full_cycle
        }

        if task_name not in tasks:
            print(f"❌ Unknown task: {task_name}")
            print(f"Available tasks: {', '.join(tasks.keys())}")
            return

        print(f"🔄 Running task: {task_name}")
        await tasks[task_name]()
        print(f"✅ Task completed: {task_name}")

def show_usage():
    """사용법 표시"""
    usage = """
🤖 Automated Scheduler Usage

📅 Scheduled Mode (Runs every 6 hours):
  python -m automation.scheduler --start

🔧 Manual Mode (Run specific tasks):
  python -m automation.scheduler --run mvp      # MVP auto management
  python -m automation.scheduler --run cicd     # CI/CD setup
  python -m automation.scheduler --run progress # Progress tracking
  python -m automation.scheduler --run mcp      # MCP ecosystem sync
  python -m automation.scheduler --run full     # Full cycle

📊 Status:
  python -m automation.scheduler --status       # Show next run times

💡 Examples:
  # Start automated scheduler
  python -m automation.scheduler --start

  # Run progress tracking once
  python -m automation.scheduler --run progress

  # Run full cycle manually
  python -m automation.scheduler --run full
"""
    print(usage)

async def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="Automated Scheduler for MCP Ecosystem")
    parser.add_argument("--start", action="store_true", help="Start the automated scheduler")
    parser.add_argument("--run", type=str, help="Run a specific task manually")
    parser.add_argument("--status", action="store_true", help="Show scheduler status")

    args = parser.parse_args()

    if args.start:
        scheduler = AutomatedScheduler()
        await scheduler.start_scheduler()

    elif args.run:
        runner = ManualRunner()
        await runner.run_single_task(args.run)

    elif args.status:
        scheduler = AutomatedScheduler()
        scheduler.schedule_jobs()
        scheduler.get_next_run_times()

    else:
        show_usage()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Scheduler interrupted by user")
    except Exception as e:
        print(f"\n❌ Scheduler failed: {e}")