#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter App Generator - 핵심 앱 생성 엔진
Mission100 템플릿 기반으로 새로운 Flutter 앱을 자동 생성
"""

import os
import json
import shutil
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import yaml

class FlutterAppGenerator:
    """Flutter 앱 자동 생성기"""

    def __init__(self, template_dir: str = "../templates/mission100"):
        self.template_dir = Path(template_dir)
        self.created_apps = []

    def create_app(self, app_config: Dict) -> Dict:
        """
        새 Flutter 앱 생성

        Args:
            app_config: 앱 설정 정보
                - name: 앱 이름
                - package_name: 패키지 이름 (com.example.app)
                - description: 앱 설명
                - target_audience: 타겟 고객층
                - language: 주 언어
                - features: 활성화할 기능 목록
        """
        print(f"🚀 Creating new Flutter app: {app_config['name']}")

        # 1. 프로젝트 디렉토리 생성
        app_dir = self._create_project_structure(app_config)

        # 2. 템플릿 파일 복사
        self._copy_template_files(app_dir, app_config)

        # 3. 앱 설정 적용
        self._apply_app_configuration(app_dir, app_config)

        # 4. 의존성 설치
        self._install_dependencies(app_dir)

        # 5. 초기 빌드
        self._initial_build(app_dir)

        # 6. 마케팅 자산 생성
        self._generate_marketing_assets(app_dir, app_config)

        result = {
            'app_name': app_config['name'],
            'app_dir': str(app_dir),
            'package_name': app_config['package_name'],
            'created_at': datetime.now().isoformat(),
            'status': 'success'
        }

        self.created_apps.append(result)
        return result

    def _create_project_structure(self, app_config: Dict) -> Path:
        """프로젝트 디렉토리 구조 생성"""
        app_name = app_config['name'].lower().replace(' ', '_')
        app_dir = Path(f"../../generated_apps/{app_name}")

        if app_dir.exists():
            shutil.rmtree(app_dir)

        app_dir.mkdir(parents=True, exist_ok=True)

        # Flutter 프로젝트 초기화
        subprocess.run([
            'flutter', 'create',
            '--org', app_config['package_name'].rsplit('.', 1)[0],
            '--project-name', app_name,
            str(app_dir)
        ], check=True)

        return app_dir

    def _copy_template_files(self, app_dir: Path, app_config: Dict):
        """템플릿 파일들을 새 프로젝트로 복사"""
        # lib 폴더 복사
        template_lib = self.template_dir / 'lib'
        if template_lib.exists():
            shutil.copytree(template_lib, app_dir / 'lib', dirs_exist_ok=True)

        # assets 폴더 복사
        template_assets = self.template_dir / 'assets'
        if template_assets.exists():
            shutil.copytree(template_assets, app_dir / 'assets', dirs_exist_ok=True)

        # 설정 파일들 복사
        for config_file in ['pubspec.yaml', 'analysis_options.yaml', 'l10n.yaml']:
            template_file = self.template_dir / config_file
            if template_file.exists():
                shutil.copy2(template_file, app_dir / config_file)

    def _apply_app_configuration(self, app_dir: Path, app_config: Dict):
        """앱 설정 적용"""
        # pubspec.yaml 수정
        pubspec_path = app_dir / 'pubspec.yaml'
        with open(pubspec_path, 'r', encoding='utf-8') as f:
            pubspec = yaml.safe_load(f)

        pubspec['name'] = app_config['name'].lower().replace(' ', '_')
        pubspec['description'] = app_config['description']

        with open(pubspec_path, 'w', encoding='utf-8') as f:
            yaml.dump(pubspec, f, allow_unicode=True)

        # 앱 설정 파일 생성
        config_file = app_dir / 'lib' / 'config' / 'app_config.dart'
        config_file.parent.mkdir(parents=True, exist_ok=True)

        config_content = f'''
class AppConfig {{
  static const String appName = '{app_config['name']}';
  static const String packageName = '{app_config['package_name']}';
  static const String description = '{app_config['description']}';
  static const String targetAudience = '{app_config.get('target_audience', 'general')}';
  static const String primaryLanguage = '{app_config.get('language', 'ko')}';

  static const List<String> enabledFeatures = {app_config.get('features', [])};
}}
'''
        config_file.write_text(config_content)

    def _install_dependencies(self, app_dir: Path):
        """Flutter 의존성 설치"""
        print("📦 Installing dependencies...")
        subprocess.run(['flutter', 'pub', 'get'], cwd=app_dir, check=True)

    def _initial_build(self, app_dir: Path):
        """초기 빌드 수행"""
        print("🔨 Running initial build...")
        # 코드 생성
        subprocess.run(['flutter', 'pub', 'run', 'build_runner', 'build', '--delete-conflicting-outputs'],
                      cwd=app_dir)

        # l10n 생성
        subprocess.run(['flutter', 'gen-l10n'], cwd=app_dir)

    def _generate_marketing_assets(self, app_dir: Path, app_config: Dict):
        """마케팅 자산 자동 생성"""
        marketing_dir = app_dir / 'marketing'
        marketing_dir.mkdir(exist_ok=True)

        # 앱 설명 생성
        description = {
            'short_description': f"{app_config['name']} - {app_config['description'][:80]}",
            'full_description': self._generate_full_description(app_config),
            'keywords': self._generate_keywords(app_config),
            'category': self._determine_category(app_config)
        }

        with open(marketing_dir / 'app_listing.json', 'w', encoding='utf-8') as f:
            json.dump(description, f, ensure_ascii=False, indent=2)

    def _generate_full_description(self, app_config: Dict) -> str:
        """전체 앱 설명 생성"""
        template = f"""
{app_config['name']}

{app_config['description']}

주요 기능:
• 100일 도전 시스템
• 일일 미션 및 추적
• 성취도 분석 및 통계
• 커뮤니티 및 공유 기능
• 맞춤형 알림 설정

{app_config.get('target_audience', '모든 연령층')}을 위한 완벽한 습관 형성 앱!

지금 바로 100일 도전을 시작하세요!
"""
        return template.strip()

    def _generate_keywords(self, app_config: Dict) -> List[str]:
        """ASO 키워드 생성"""
        base_keywords = ['100일', '챌린지', '습관', '목표', '도전', '자기계발']

        # 앱 이름에서 키워드 추출
        name_keywords = app_config['name'].lower().split()

        # 카테고리별 키워드 추가
        category_keywords = self._get_category_keywords(app_config)

        return list(set(base_keywords + name_keywords + category_keywords))

    def _determine_category(self, app_config: Dict) -> str:
        """앱 카테고리 결정"""
        name_lower = app_config['name'].lower()
        description_lower = app_config.get('description', '').lower()

        if any(word in name_lower + description_lower for word in ['운동', '헬스', '피트니스', 'fitness', 'workout']):
            return 'HEALTH_AND_FITNESS'
        elif any(word in name_lower + description_lower for word in ['교육', '학습', 'study', 'education']):
            return 'EDUCATION'
        elif any(word in name_lower + description_lower for word in ['생산성', 'productivity', '업무']):
            return 'PRODUCTIVITY'
        else:
            return 'LIFESTYLE'

    def _get_category_keywords(self, app_config: Dict) -> List[str]:
        """카테고리별 키워드 반환"""
        category = self._determine_category(app_config)

        keywords_map = {
            'HEALTH_AND_FITNESS': ['운동', '건강', '다이어트', '피트니스', '헬스'],
            'EDUCATION': ['학습', '교육', '공부', '독서', '암기'],
            'PRODUCTIVITY': ['생산성', '할일', '계획', '일정관리', '목표달성'],
            'LIFESTYLE': ['라이프스타일', '일상', '습관', '루틴', '자기관리']
        }

        return keywords_map.get(category, [])

    def batch_create_apps(self, app_configs: List[Dict]) -> List[Dict]:
        """여러 앱을 일괄 생성"""
        results = []
        for config in app_configs:
            try:
                result = self.create_app(config)
                results.append(result)
            except Exception as e:
                results.append({
                    'app_name': config['name'],
                    'status': 'failed',
                    'error': str(e)
                })

        return results

if __name__ == "__main__":
    # 테스트용 앱 생성
    generator = FlutterAppGenerator()

    test_config = {
        'name': 'Fitness Challenge 100',
        'package_name': 'com.appfactory.fitness100',
        'description': '100일 동안 운동 습관을 만들어가는 피트니스 챌린지 앱',
        'target_audience': '20-40대 직장인',
        'language': 'ko',
        'features': ['daily_mission', 'progress_tracking', 'social_sharing', 'achievements']
    }

    result = generator.create_app(test_config)
    print(f"✅ App created successfully: {result}")