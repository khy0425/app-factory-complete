#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 앱 생성기 - App Factory + Marketing Automation 연동
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Marketing Automation System 경로 추가
MARKETING_SYSTEM_PATH = Path("../../../../marketing-automation-system")
sys.path.append(str(MARKETING_SYSTEM_PATH))

from app_generator import FlutterAppGenerator

try:
    from marketing_orchestrator import MarketingOrchestrator
    MARKETING_AVAILABLE = True
except ImportError:
    print("⚠️ Marketing Automation System not available")
    MARKETING_AVAILABLE = False

class IntegratedAppGenerator(FlutterAppGenerator):
    """앱 생성 + 마케팅 자동화 통합 시스템"""

    def __init__(self, template_dir: str = "../templates/mission100"):
        super().__init__(template_dir)
        self.marketing_orchestrator = None

        if MARKETING_AVAILABLE:
            try:
                self.marketing_orchestrator = MarketingOrchestrator()
                print("✅ Marketing Automation System connected")
            except Exception as e:
                print(f"⚠️ Marketing system connection failed: {e}")

    def create_gigachad_app(self, app_config: Dict) -> Dict:
        """
        GigaChad Runner 스타일 앱 생성 + 마케팅 자동화

        Args:
            app_config: 앱 설정
                - name: 앱 이름
                - concept: 앱 컨셉 (fitness, study, productivity 등)
                - target_audience: 타겟 고객층
                - marketing_budget: 마케팅 예산 (선택)
        """
        print(f"🗿 Creating GigaChad-style app: {app_config['name']}")

        # 1. GigaChad 브랜딩 적용
        enhanced_config = self._apply_gigachad_branding(app_config)

        # 2. 앱 생성
        app_result = self.create_app(enhanced_config)

        # 3. 마케팅 자동화 설정
        if MARKETING_AVAILABLE and self.marketing_orchestrator:
            marketing_result = self._setup_marketing_automation(enhanced_config, app_result)
            app_result['marketing'] = marketing_result

        # 4. GigaChad 전용 에셋 생성
        asset_result = self._generate_gigachad_assets(enhanced_config, app_result)
        app_result['assets'] = asset_result

        # 5. 런칭 플랜 생성
        launch_plan = self._create_launch_plan(enhanced_config)
        app_result['launch_plan'] = launch_plan

        return app_result

    def _apply_gigachad_branding(self, app_config: Dict) -> Dict:
        """GigaChad 브랜딩 스타일 적용"""

        # Chad-style 이름 변환
        chad_name = self._chadify_app_name(app_config['name'], app_config.get('concept', 'fitness'))

        # GigaChad 컬러 팔레트 적용
        gigachad_config = {
            **app_config,
            'name': chad_name,
            'branding': {
                'style': 'gigachad',
                'colors': {
                    'primary': '#1A1A1A',  # Chad Black
                    'secondary': '#FFD700',  # Alpha Gold
                    'accent': '#FF0000',    # Grindset Red
                    'background': '#0A0A0A' # Sigma Dark
                },
                'fonts': {
                    'heading': 'Bebas Neue',
                    'body': 'Roboto Condensed'
                },
                'voice': 'aggressive_motivational'
            },
            'features': [
                'daily_missions',
                'level_system',
                'leaderboards',
                'voice_coaching',
                'streak_tracking',
                'transformation_photos'
            ]
        }

        return gigachad_config

    def _chadify_app_name(self, original_name: str, concept: str) -> str:
        """앱 이름을 Chad 스타일로 변환"""

        chad_prefixes = {
            'fitness': ['GigaChad', 'Alpha', 'Sigma', 'Beast Mode'],
            'running': ['Chad Runner', 'Sigma Sprint', 'Alpha Marathon'],
            'study': ['Brain Chad', 'Study Beast', 'Knowledge Alpha'],
            'productivity': ['Grind Master', 'Sigma Hustle', 'Chad Productivity']
        }

        chad_suffixes = {
            'fitness': ['Beast', 'Machine', 'Warrior', 'Champion'],
            'running': ['Runner', 'Sprinter', 'Marathoner', 'Racer'],
            'study': ['Brain', 'Scholar', 'Genius', 'Master'],
            'productivity': ['Grind', 'Hustle', 'Machine', 'Pro']
        }

        import random

        if concept in chad_prefixes:
            prefix = random.choice(chad_prefixes[concept])
            suffix = random.choice(chad_suffixes[concept])
            return f"{prefix} {suffix}"
        else:
            return f"GigaChad {original_name}"

    def _setup_marketing_automation(self, app_config: Dict, app_result: Dict) -> Dict:
        """마케팅 자동화 시스템 설정"""

        if not self.marketing_orchestrator:
            return {'status': 'skipped', 'reason': 'Marketing system not available'}

        try:
            # 마케팅 설정 생성
            marketing_config = {
                'app_id': app_config['package_name'],
                'app_name': app_config['name'],
                'category': self._determine_app_category(app_config),
                'target_audience': app_config.get('target_audience', '20-35세 남성'),
                'brand_voice': 'gigachad_motivational',
                'keywords': self._generate_chad_keywords(app_config),
                'content_themes': [
                    'transformation',
                    'motivation',
                    'challenge',
                    'grindset',
                    'alpha_mindset'
                ]
            }

            # ASO 최적화 시작
            print("📊 Starting ASO optimization...")
            aso_result = self.marketing_orchestrator.optimize_aso(
                app_config['package_name'],
                marketing_config
            )

            # 콘텐츠 생성 파이프라인 시작
            print("✍️ Generating marketing content...")
            content_result = self.marketing_orchestrator.generate_content_suite(
                marketing_config
            )

            # 소셜 미디어 캠페인 설정
            print("📱 Setting up social media campaigns...")
            social_result = self.marketing_orchestrator.setup_social_campaigns(
                marketing_config
            )

            return {
                'status': 'success',
                'aso': aso_result,
                'content': content_result,
                'social': social_result,
                'config': marketing_config
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _generate_chad_keywords(self, app_config: Dict) -> List[str]:
        """Chad 스타일 키워드 생성"""

        base_keywords = ['기가차드', 'gigachad', '시그마', 'sigma', '그라인드셋', 'grindset']

        concept_keywords = {
            'fitness': ['운동', '헬스', '피트니스', '근육', '다이어트', 'workout', 'gym'],
            'running': ['러닝', '달리기', '마라톤', '조깅', 'running', 'marathon'],
            'study': ['공부', '학습', '교육', '독서', 'study', 'education'],
            'productivity': ['생산성', '목표', '습관', '계획', 'productivity', 'goals']
        }

        concept = app_config.get('concept', 'fitness')
        keywords = base_keywords + concept_keywords.get(concept, [])

        # Chad-specific motivational keywords
        motivational_keywords = [
            '100일챌린지', '습관형성', '자기계발', '동기부여',
            'motivation', 'challenge', 'transformation', 'mindset'
        ]

        return keywords + motivational_keywords

    def _generate_gigachad_assets(self, app_config: Dict, app_result: Dict) -> Dict:
        """GigaChad 전용 에셋 생성"""

        app_dir = Path(app_result['app_dir'])
        assets_dir = app_dir / 'assets' / 'gigachad'
        assets_dir.mkdir(parents=True, exist_ok=True)

        # Chad 아이콘 생성 (텍스트 기반)
        icon_result = self._generate_chad_icons(assets_dir, app_config)

        # 동기부여 사운드 설정
        audio_result = self._setup_motivational_audio(assets_dir, app_config)

        # Chad 배경화면 생성
        wallpaper_result = self._generate_chad_wallpapers(assets_dir, app_config)

        return {
            'icons': icon_result,
            'audio': audio_result,
            'wallpapers': wallpaper_result,
            'assets_path': str(assets_dir)
        }

    def _generate_chad_icons(self, assets_dir: Path, app_config: Dict) -> Dict:
        """Chad 스타일 아이콘 생성 (플레이스홀더)"""

        icons_dir = assets_dir / 'icons'
        icons_dir.mkdir(exist_ok=True)

        # 텍스트 기반 아이콘 설명 생성
        icon_specs = {
            'app_icon': 'Muscular silhouette with gold accent, black background',
            'achievement_icons': [
                '💪 First Victory',
                '🔥 Streak Master',
                '🗿 Chad Ascension',
                '👑 Ultra Chad'
            ],
            'level_badges': [
                '🥺 Virgin Runner',
                '💪 Brad Apprentice',
                '😎 Chad',
                '🗿 GigaChad',
                '👑 Ultra Chad'
            ]
        }

        # 아이콘 사양을 JSON으로 저장
        with open(icons_dir / 'icon_specifications.json', 'w', encoding='utf-8') as f:
            json.dump(icon_specs, f, ensure_ascii=False, indent=2)

        return {
            'status': 'generated',
            'specs_file': str(icons_dir / 'icon_specifications.json'),
            'count': len(icon_specs['achievement_icons']) + len(icon_specs['level_badges'])
        }

    def _setup_motivational_audio(self, assets_dir: Path, app_config: Dict) -> Dict:
        """동기부여 오디오 설정"""

        audio_dir = assets_dir / 'audio'
        audio_dir.mkdir(exist_ok=True)

        # Chad 보이스 라인 스크립트
        voice_scripts = {
            'start_workout': [
                "Time to activate beast mode!",
                "Let's make weakness cry!",
                "Chad energy: ACTIVATED!"
            ],
            'mid_workout': [
                "You're not tired, you're getting stronger!",
                "Pain is temporary, Chad is forever!",
                "Push through! GigaChad awaits!"
            ],
            'finish_workout': [
                "Another W for the Chad!",
                "You just leveled up in real life!",
                "Built different, built better!"
            ],
            'motivational_quotes': [
                "Rest? I don't know her.",
                "Pain is just weakness leaving the body.",
                "While they sleep, I grind.",
                "Comfort is the enemy of greatness."
            ]
        }

        # 스크립트를 JSON으로 저장
        with open(audio_dir / 'voice_scripts.json', 'w', encoding='utf-8') as f:
            json.dump(voice_scripts, f, ensure_ascii=False, indent=2)

        return {
            'status': 'configured',
            'scripts_file': str(audio_dir / 'voice_scripts.json'),
            'total_lines': sum(len(lines) for lines in voice_scripts.values())
        }

    def _generate_chad_wallpapers(self, assets_dir: Path, app_config: Dict) -> Dict:
        """Chad 배경화면 사양 생성"""

        wallpapers_dir = assets_dir / 'wallpapers'
        wallpapers_dir.mkdir(exist_ok=True)

        wallpaper_specs = {
            'main_background': {
                'style': 'Dark gradient with subtle geometric patterns',
                'colors': ['#0A0A0A', '#1A1A1A'],
                'elements': ['Subtle Chad silhouette', 'Gold accent lines']
            },
            'level_backgrounds': {
                'virgin': 'Soft gray tones with upward arrow',
                'brad': 'Blue to purple gradient with strength symbols',
                'chad': 'Gold and black with confidence imagery',
                'gigachad': 'Bold red and gold with power symbols',
                'ultra_chad': 'Royal purple with crown elements'
            }
        }

        with open(wallpapers_dir / 'wallpaper_specs.json', 'w', encoding='utf-8') as f:
            json.dump(wallpaper_specs, f, ensure_ascii=False, indent=2)

        return {
            'status': 'specified',
            'specs_file': str(wallpapers_dir / 'wallpaper_specs.json')
        }

    def _create_launch_plan(self, app_config: Dict) -> Dict:
        """앱 런칭 플랜 생성"""

        launch_phases = {
            'pre_launch': {
                'duration': '2 weeks',
                'tasks': [
                    'App Store listing optimization',
                    'Social media account setup',
                    'Influencer outreach preparation',
                    'Press kit creation',
                    'Beta testing with Chad community'
                ]
            },
            'launch_week': {
                'duration': '1 week',
                'tasks': [
                    'Coordinated social media campaign',
                    'Press release distribution',
                    'App Store featuring push',
                    'Community engagement activation',
                    'User feedback monitoring'
                ]
            },
            'post_launch': {
                'duration': '4 weeks',
                'tasks': [
                    'Performance analytics review',
                    'User feedback implementation',
                    'Content marketing expansion',
                    'Partnership development',
                    'Feature iteration planning'
                ]
            }
        }

        success_metrics = {
            'week_1': {
                'downloads': 1000,
                'rating': 4.0,
                'retention_day_1': 70,
                'social_mentions': 100
            },
            'month_1': {
                'downloads': 10000,
                'rating': 4.5,
                'retention_day_7': 40,
                'retention_day_30': 20,
                'revenue': 5000
            }
        }

        return {
            'phases': launch_phases,
            'success_metrics': success_metrics,
            'estimated_timeline': '7 weeks total',
            'recommended_budget': '$10,000 - $25,000'
        }

    def _determine_app_category(self, app_config: Dict) -> str:
        """앱 카테고리 결정"""
        concept = app_config.get('concept', 'fitness').lower()

        category_map = {
            'fitness': 'Health & Fitness',
            'running': 'Health & Fitness',
            'study': 'Education',
            'productivity': 'Productivity',
            'lifestyle': 'Lifestyle'
        }

        return category_map.get(concept, 'Health & Fitness')

if __name__ == "__main__":
    # GigaChad Runner 생성 테스트
    generator = IntegratedAppGenerator()

    gigachad_config = {
        'name': 'Ultimate Runner',
        'concept': 'running',
        'package_name': 'com.chadtech.ultimate_runner',
        'description': '100일 만에 평범한 러너에서 기가차드로 변신하는 궁극의 러닝 챌린지',
        'target_audience': '20-35세 남성, 피트니스 애호가',
        'marketing_budget': 15000
    }

    result = generator.create_gigachad_app(gigachad_config)
    print(f"🎉 GigaChad app created: {json.dumps(result, indent=2, ensure_ascii=False)}")