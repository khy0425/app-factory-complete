#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 App Factory CLI
앱 생성부터 마케팅, 배포까지 모든 것을 한 곳에서
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 Python path에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from core.integrated_generator import IntegratedAppGenerator
from marketing_orchestrator import MarketingOrchestrator
from deployment.deploy_manager import DeploymentManager

class UnifiedFactoryCLI:
    """통합 앱 팩토리 CLI"""

    def __init__(self):
        self.generator = IntegratedAppGenerator()
        self.marketing = MarketingOrchestrator()
        self.deployer = DeploymentManager()

    def create_gigachad_app(self, args):
        """GigaChad 스타일 앱 생성"""

        print("🗿 GigaChad App Factory")
        print("=" * 50)

        # 사전 정의된 템플릿
        gigachad_templates = {
            'runner': {
                'name': 'GigaChad Runner',
                'concept': 'running',
                'description': '100일 궁극의 러닝 챌린지로 기가차드 진화',
                'target_audience': '20-35세 남성 러너',
                'keywords': ['러닝', '기가차드', '100일챌린지', '시그마그라인드셋']
            },
            'gym': {
                'name': 'Alpha Gym Beast',
                'concept': 'fitness',
                'description': '헬스장에서 진짜 알파가 되는 100일 프로그램',
                'target_audience': '18-40세 남성 헬스인',
                'keywords': ['헬스', '근육', '알파', '비스트모드']
            },
            'study': {
                'name': 'Brain Chad Master',
                'concept': 'study',
                'description': '뇌근육을 키우는 시그마 학습 시스템',
                'target_audience': '15-30세 학생 직장인',
                'keywords': ['공부', '뇌차드', '학습', '자기계발']
            },
            'business': {
                'name': 'Sigma Entrepreneur',
                'concept': 'productivity',
                'description': '그라인드셋으로 사업 성공하는 100일',
                'target_audience': '25-45세 사업가',
                'keywords': ['창업', '사업', '시그마', '성공']
            }
        }

        # 템플릿 또는 커스텀 설정
        if args.template and args.template in gigachad_templates:
            config = gigachad_templates[args.template].copy()
            print(f"📱 Using GigaChad Template: {args.template.upper()}")
        else:
            config = {
                'name': args.name or 'Custom GigaChad App',
                'concept': args.concept or 'fitness',
                'description': args.description or 'A GigaChad transformation app',
                'target_audience': args.target_audience or '20-35세 남성',
                'keywords': args.keywords.split(',') if args.keywords else ['gigachad']
            }
            print(f"📱 Creating Custom App: {config['name']}")

        # 패키지 이름 생성
        safe_name = config['name'].lower().replace(' ', '_').replace('-', '_')
        config['package_name'] = args.package or f"com.chadtech.{safe_name}"
        config['marketing_budget'] = args.budget
        config['include_premium'] = args.premium
        config['auto_deploy'] = args.deploy

        print(f"📦 Package: {config['package_name']}")
        print(f"💰 Marketing Budget: ${config['marketing_budget']:,}")
        print()

        try:
            # 앱 생성
            print("🚀 Creating GigaChad App...")
            result = self.generator.create_gigachad_app(config)

            print("✅ App Generation Complete!")
            print(f"📱 App: {result['app_name']}")
            print(f"📂 Location: {result['app_dir']}")

            # 마케팅 자동화
            if result.get('marketing', {}).get('status') == 'success':
                print("📊 Marketing Automation: ✅ Active")
                print(f"🎯 Keywords: {len(result['marketing']['config']['keywords'])} optimized")
                print(f"📝 Content: Generated")
                print(f"📱 Social: Configured")

            # 자동 배포 (옵션)
            if args.deploy:
                print("\n🚀 Starting Auto Deployment...")
                deploy_result = self.deployer.deploy(
                    result['app_dir'],
                    platform='all',
                    track='internal'
                )
                print(f"📤 Deployment Status: {deploy_result.get('status', 'unknown')}")

            # 성공 메시지
            print("\n🗿 GIGACHAD APP FACTORY SUCCESS!")
            print("=" * 50)
            print("Next Steps:")
            print("1. cd " + result['app_dir'])
            print("2. flutter pub get")
            print("3. flutter run")
            print("4. Start dominating! 💪")

            # 결과 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"gigachad_app_{timestamp}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            print(f"💾 Results saved: {output_file}")

        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    def batch_create(self, args):
        """여러 앱을 배치로 생성"""

        print("🏭 GigaChad Batch Factory")
        print("=" * 30)

        concepts = args.concepts.split(',')
        results = []

        for i, concept in enumerate(concepts):
            print(f"\n📱 Creating App {i+1}/{len(concepts)}: {concept}")

            config = {
                'name': f'GigaChad {concept.title()}',
                'concept': concept.strip(),
                'package_name': f'com.chadtech.gigachad_{concept.strip()}',
                'description': f'GigaChad {concept} transformation app',
                'target_audience': '20-35세 남성',
                'marketing_budget': args.budget // len(concepts)  # 예산 분할
            }

            try:
                result = self.generator.create_gigachad_app(config)
                results.append(result)
                print(f"✅ {config['name']} created!")
            except Exception as e:
                print(f"❌ Failed to create {config['name']}: {e}")
                results.append({'error': str(e), 'config': config})

        print(f"\n🎉 Batch Creation Complete: {len(results)} apps")

        # 배치 결과 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        batch_file = f"batch_gigachad_{timestamp}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        print(f"💾 Batch results: {batch_file}")

    def launch_marketing(self, args):
        """마케팅 캠페인 시작"""

        print("📊 Marketing Campaign Launch")
        print("=" * 30)

        try:
            campaign_config = {
                'app_id': args.app_id,
                'strategy': args.strategy,
                'budget': args.budget,
                'duration': args.duration,
                'platforms': args.platforms.split(',') if args.platforms else ['all']
            }

            print(f"🎯 App ID: {campaign_config['app_id']}")
            print(f"📈 Strategy: {campaign_config['strategy']}")
            print(f"💰 Budget: ${campaign_config['budget']:,}")
            print(f"⏰ Duration: {campaign_config['duration']} days")

            result = self.marketing.run_campaign(args.app_id, 'all')

            print("✅ Marketing Campaign Started!")
            print(f"📊 Tasks: {len(result['tasks'])}")
            print(f"🚀 Status: {result.get('status', 'active')}")

        except Exception as e:
            print(f"❌ Marketing Error: {e}")

    def deploy_app(self, args):
        """앱 배포"""

        print("🚀 App Deployment")
        print("=" * 20)

        try:
            result = self.deployer.deploy(
                args.app_dir,
                platform=args.platform,
                track=args.track
            )

            print("✅ Deployment Complete!")
            print(f"📱 Platform: {args.platform}")
            print(f"🎯 Track: {args.track}")
            print(f"📊 Status: {result.get('status', 'unknown')}")

        except Exception as e:
            print(f"❌ Deployment Error: {e}")

    def start_dashboard(self, args):
        """대시보드 시작"""

        print("📈 Starting GigaChad Dashboard...")

        try:
            # start_dashboard.py 실행
            import subprocess
            dashboard_script = PROJECT_ROOT / 'start_dashboard.py'
            subprocess.run([sys.executable, str(dashboard_script)])
        except Exception as e:
            print(f"❌ Dashboard Error: {e}")

    def list_apps(self, args):
        """생성된 앱 목록"""

        print("📱 Generated GigaChad Apps")
        print("=" * 25)

        apps_dir = PROJECT_ROOT / 'generated_apps'
        if not apps_dir.exists():
            print("No apps generated yet.")
            return

        for app_dir in apps_dir.iterdir():
            if app_dir.is_dir():
                config_file = app_dir / 'app_config.json'
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        print(f"🗿 {config['name']}")
                        print(f"   📦 {config['package_name']}")
                        print(f"   📅 {config.get('created_at', 'Unknown')}")
                        print(f"   📂 {app_dir}")
                        print()
                    except:
                        print(f"📱 {app_dir.name} (config error)")
                else:
                    print(f"📱 {app_dir.name}")

def main():
    cli = UnifiedFactoryCLI()

    parser = argparse.ArgumentParser(
        description='🗿 GigaChad App Factory - Complete App Creation System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create from template
  python unified_factory_cli.py create --template runner --budget 15000

  # Create custom app
  python unified_factory_cli.py create --name "Beast Mode" --concept fitness

  # Batch create multiple apps
  python unified_factory_cli.py batch --concepts "runner,gym,study" --budget 30000

  # Launch marketing campaign
  python unified_factory_cli.py marketing --app-id com.chadtech.runner --budget 5000

  # Deploy to stores
  python unified_factory_cli.py deploy --app-dir ./apps/my_app --platform all

  # Start dashboard
  python unified_factory_cli.py dashboard
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create GigaChad app')
    create_parser.add_argument('--template', choices=['runner', 'gym', 'study', 'business'])
    create_parser.add_argument('--name', help='App name')
    create_parser.add_argument('--concept', choices=['fitness', 'running', 'study', 'productivity'])
    create_parser.add_argument('--package', help='Package name')
    create_parser.add_argument('--description', help='App description')
    create_parser.add_argument('--target-audience', help='Target audience')
    create_parser.add_argument('--keywords', help='Comma-separated keywords')
    create_parser.add_argument('--budget', type=int, default=10000, help='Marketing budget')
    create_parser.add_argument('--premium', action='store_true', help='Include premium features')
    create_parser.add_argument('--deploy', action='store_true', help='Auto deploy after creation')
    create_parser.set_defaults(func=cli.create_gigachad_app)

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch create multiple apps')
    batch_parser.add_argument('--concepts', required=True, help='Comma-separated concepts')
    batch_parser.add_argument('--budget', type=int, default=20000, help='Total budget to split')
    batch_parser.set_defaults(func=cli.batch_create)

    # Marketing command
    marketing_parser = subparsers.add_parser('marketing', help='Launch marketing campaign')
    marketing_parser.add_argument('--app-id', required=True, help='App package ID')
    marketing_parser.add_argument('--strategy', default='gigachad_aggressive', help='Marketing strategy')
    marketing_parser.add_argument('--budget', type=int, default=5000, help='Campaign budget')
    marketing_parser.add_argument('--duration', type=int, default=30, help='Campaign duration (days)')
    marketing_parser.add_argument('--platforms', help='Target platforms (comma-separated)')
    marketing_parser.set_defaults(func=cli.launch_marketing)

    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy app to stores')
    deploy_parser.add_argument('--app-dir', required=True, help='App directory path')
    deploy_parser.add_argument('--platform', default='all', choices=['google', 'apple', 'all'])
    deploy_parser.add_argument('--track', default='internal', choices=['internal', 'alpha', 'beta', 'production'])
    deploy_parser.set_defaults(func=cli.deploy_app)

    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Start analytics dashboard')
    dashboard_parser.set_defaults(func=cli.start_dashboard)

    # List command
    list_parser = subparsers.add_parser('list', help='List generated apps')
    list_parser.set_defaults(func=cli.list_apps)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()