#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마케팅 자동화 오케스트레이터
모든 마케팅 자동화 모듈을 통합 관리하는 중앙 컨트롤러
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio
import logging

# 로컬 모듈 import
from aso.keyword_optimizer import PlayStoreASO
from content_generator.blog_generator import ContentGenerator
from review_manager.review_monitor import ReviewMonitor

@dataclass
class MarketingTask:
    task_id: str
    task_type: str  # 'aso', 'content', 'review'
    app_config: Dict
    status: str  # 'pending', 'running', 'completed', 'failed'
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error_message: Optional[str] = None

class MarketingOrchestrator:
    def __init__(self, config_file: str = "config/marketing_config.json"):
        """마케팅 오케스트레이터 초기화"""
        self.config_file = config_file
        self.config = self._load_config()
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('marketing_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 모듈 초기화
        self.aso_optimizer = PlayStoreASO(self.config.get('openai_api_key', ''))
        self.content_generator = ContentGenerator(self.config.get('openai_api_key', ''))
        self.review_monitor = ReviewMonitor(self.config.get('openai_api_key', ''))
        
        self.tasks_queue = []
        self.completed_tasks = []
    
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"설정 파일 없음: {self.config_file}, 기본 설정 사용")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """기본 설정 생성"""
        default_config = {
            "openai_api_key": os.getenv('OPENAI_API_KEY', ''),
            "automation_schedule": {
                "aso_update_interval_days": 14,
                "content_generation_enabled": True,
                "review_monitoring_interval_hours": 6
            },
            "content_settings": {
                "blog_platforms": ["wordpress", "blogger"],
                "youtube_enabled": True,
                "auto_posting": False  # 안전을 위해 기본값 false
            },
            "notification_settings": {
                "slack_webhook": "",
                "email_notifications": True,
                "daily_reports": True
            },
            "apps_to_monitor": []
        }
        
        # 기본 설정 파일 생성
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def add_app_to_monitoring(self, app_config_path: str):
        """앱을 마케팅 모니터링에 추가"""
        with open(app_config_path, 'r', encoding='utf-8') as f:
            app_config = json.load(f)
        
        if app_config_path not in self.config['apps_to_monitor']:
            self.config['apps_to_monitor'].append(app_config_path)
            self._save_config()
            self.logger.info(f"앱 모니터링 추가: {app_config['app']['name']}")
    
    def _save_config(self):
        """설정 파일 저장"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def create_marketing_campaign(self, app_config_path: str, campaign_type: str = "full"):
        """새 앱을 위한 마케팅 캠페인 생성"""
        with open(app_config_path, 'r', encoding='utf-8') as f:
            app_config = json.load(f)
        
        app_name = app_config['app']['name']
        self.logger.info(f"마케팅 캠페인 시작: {app_name}")
        
        tasks = []
        
        if campaign_type in ["full", "aso"]:
            # ASO 최적화 태스크
            tasks.append(MarketingTask(
                task_id=f"aso_{app_name}_{int(time.time())}",
                task_type="aso",
                app_config=app_config,
                status="pending",
                created_at=datetime.now()
            ))
        
        if campaign_type in ["full", "content"]:
            # 콘텐츠 생성 태스크들
            content_types = ["review", "tutorial"]
            for content_type in content_types:
                tasks.append(MarketingTask(
                    task_id=f"content_{content_type}_{app_name}_{int(time.time())}",
                    task_type="content",
                    app_config=app_config,
                    status="pending",
                    created_at=datetime.now()
                ))
        
        if campaign_type in ["full", "review"]:
            # 리뷰 모니터링 태스크
            tasks.append(MarketingTask(
                task_id=f"review_{app_name}_{int(time.time())}",
                task_type="review",
                app_config=app_config,
                status="pending",
                created_at=datetime.now()
            ))
        
        self.tasks_queue.extend(tasks)
        self.logger.info(f"{len(tasks)}개 마케팅 태스크 생성 완료")
        
        return tasks
    
    async def execute_task(self, task: MarketingTask):
        """개별 태스크 실행"""
        self.logger.info(f"태스크 실행 시작: {task.task_id}")
        task.status = "running"
        
        try:
            if task.task_type == "aso":
                result = await self._execute_aso_task(task)
            elif task.task_type == "content":
                result = await self._execute_content_task(task)
            elif task.task_type == "review":
                result = await self._execute_review_task(task)
            else:
                raise ValueError(f"알 수 없는 태스크 타입: {task.task_type}")
            
            task.status = "completed"
            task.completed_at = datetime.now()
            task.result = result
            
            self.logger.info(f"태스크 완료: {task.task_id}")
            
        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            self.logger.error(f"태스크 실패: {task.task_id} - {e}")
        
        self.completed_tasks.append(task)
    
    async def _execute_aso_task(self, task: MarketingTask) -> Dict:
        """ASO 최적화 태스크 실행"""
        app_config = task.app_config
        
        # ASO 최적화 실행
        optimized_config = self.aso_optimizer.update_app_config_with_aso(
            "", # config path는 메모리에서 처리
            self._determine_app_type(app_config)
        )
        
        # 최적화된 설정을 앱 설정에 병합
        app_config.update(optimized_config)
        
        return {
            "keywords_updated": True,
            "description_optimized": True,
            "title_variants_generated": len(optimized_config.get('marketing', {}).get('title_variants', [])),
            "optimization_date": datetime.now().isoformat()
        }
    
    async def _execute_content_task(self, task: MarketingTask) -> Dict:
        """콘텐츠 생성 태스크 실행"""
        app_config = task.app_config
        
        # 블로그 포스트 생성
        blog_post = self.content_generator.generate_blog_post(app_config, "review")
        
        # 유튜브 스크립트 생성
        youtube_script = self.content_generator.generate_youtube_script(app_config)
        
        # 콘텐츠 저장 (실제로는 자동 포스팅 API 사용)
        content_dir = f"generated_content/{app_config['app']['name']}"
        os.makedirs(content_dir, exist_ok=True)
        
        # 블로그 포스트 저장
        with open(f"{content_dir}/blog_post.md", 'w', encoding='utf-8') as f:
            f.write(f"# {blog_post.title}\n\n{blog_post.content}")
        
        # 유튜브 스크립트 저장
        with open(f"{content_dir}/youtube_script.txt", 'w', encoding='utf-8') as f:
            f.write(youtube_script)
        
        return {
            "blog_post_generated": True,
            "youtube_script_generated": True,
            "content_saved_to": content_dir,
            "generation_date": datetime.now().isoformat()
        }
    
    async def _execute_review_task(self, task: MarketingTask) -> Dict:
        """리뷰 모니터링 태스크 실행"""
        app_config = task.app_config
        package_name = app_config['app']['package_name']
        app_name = app_config['app']['name']
        
        # 리뷰 처리
        processed_count = self.review_monitor.process_reviews_batch(package_name, app_name)
        
        # 리뷰 요약 리포트 생성
        summary_report = self.review_monitor.generate_review_summary_report(package_name, 7)
        
        return {
            "reviews_processed": processed_count,
            "summary_report": summary_report,
            "monitoring_date": datetime.now().isoformat()
        }
    
    def _determine_app_type(self, app_config: Dict) -> str:
        """앱 타입 자동 결정"""
        app_name = app_config['app']['name'].lower()
        description = app_config['app']['description'].lower()
        
        if any(keyword in app_name + description for keyword in ['timer', '타이머', 'focus', '집중']):
            return "timer"
        elif any(keyword in app_name + description for keyword in ['habit', '습관', 'routine', '루틴']):
            return "habit"
        else:
            return "productivity"
    
    async def run_automation_cycle(self):
        """자동화 사이클 실행"""
        self.logger.info("마케팅 자동화 사이클 시작")
        
        # 대기 중인 태스크들 실행
        pending_tasks = [task for task in self.tasks_queue if task.status == "pending"]
        
        if not pending_tasks:
            self.logger.info("실행할 태스크 없음")
            return
        
        # 태스크들을 병렬로 실행 (최대 3개씩)
        semaphore = asyncio.Semaphore(3)
        
        async def execute_with_semaphore(task):
            async with semaphore:
                await self.execute_task(task)
        
        tasks_coroutines = [execute_with_semaphore(task) for task in pending_tasks]
        await asyncio.gather(*tasks_coroutines)
        
        # 완료된 태스크들을 큐에서 제거
        self.tasks_queue = [task for task in self.tasks_queue if task.status == "pending"]
        
        self.logger.info(f"자동화 사이클 완료: {len(pending_tasks)}개 태스크 처리")
    
    def generate_daily_report(self) -> Dict:
        """일일 리포트 생성"""
        today = datetime.now().date()
        today_tasks = [task for task in self.completed_tasks 
                      if task.completed_at and task.completed_at.date() == today]
        
        report = {
            "date": today.isoformat(),
            "total_tasks_completed": len(today_tasks),
            "tasks_by_type": {},
            "success_rate": 0,
            "apps_processed": set()
        }
        
        for task in today_tasks:
            task_type = task.task_type
            report["tasks_by_type"][task_type] = report["tasks_by_type"].get(task_type, 0) + 1
            report["apps_processed"].add(task.app_config['app']['name'])
        
        report["apps_processed"] = list(report["apps_processed"])
        
        successful_tasks = [task for task in today_tasks if task.status == "completed"]
        if today_tasks:
            report["success_rate"] = len(successful_tasks) / len(today_tasks) * 100
        
        return report
    
    def start_scheduler(self):
        """스케줄러 시작 (실제로는 백그라운드 서비스로 구현)"""
        self.logger.info("마케팅 자동화 스케줄러 시작")
        
        # TODO: APScheduler나 Celery로 실제 스케줄링 구현
        print("스케줄러 설정:")
        print(f"- ASO 업데이트: {self.config['automation_schedule']['aso_update_interval_days']}일마다")
        print(f"- 리뷰 모니터링: {self.config['automation_schedule']['review_monitoring_interval_hours']}시간마다")
        print(f"- 콘텐츠 생성: {'활성화' if self.config['automation_schedule']['content_generation_enabled'] else '비활성화'}")

def main():
    """테스트 실행"""
    orchestrator = MarketingOrchestrator()
    
    # 테스트 앱 설정 생성
    test_app_config = {
        'app': {
            'name': 'Focus Timer Pro',
            'package_name': 'com.appfactory.focustimer',
            'description': '집중력 향상을 위한 포모도로 타이머'
        }
    }
    
    # 임시 설정 파일 생성
    test_config_path = "test_app_config.json"
    with open(test_config_path, 'w', encoding='utf-8') as f:
        json.dump(test_app_config, f, indent=2, ensure_ascii=False)
    
    # 마케팅 캠페인 생성
    tasks = orchestrator.create_marketing_campaign(test_config_path, "full")
    print(f"생성된 태스크 수: {len(tasks)}")
    
    # 자동화 사이클 실행 (비동기)
    asyncio.run(orchestrator.run_automation_cycle())
    
    # 일일 리포트 생성
    report = orchestrator.generate_daily_report()
    print(f"일일 리포트: {json.dumps(report, indent=2, ensure_ascii=False)}")
    
    # 정리
    os.remove(test_config_path)

if __name__ == "__main__":
    main()
