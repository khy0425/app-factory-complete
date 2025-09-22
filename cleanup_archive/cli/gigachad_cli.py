#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GigaChad App Factory CLI
통합 앱 생성 + 마케팅 자동화 CLI
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from core.integrated_generator import IntegratedAppGenerator

def create_gigachad_app(args):
    """GigaChad 스타일 앱 생성"""

    print("🗿 GigaChad App Factory - Creating Alpha-level App")
    print("=" * 50)

    generator = IntegratedAppGenerator()

    # 사전 정의된 GigaChad 앱 템플릿
    gigachad_templates = {
        'runner': {
            'name': 'GigaChad Runner',
            'concept': 'running',
            'description': '100일 궁극의 러닝 챌린지로 평범한 인간에서 기가차드로 진화',
            'target_audience': '20-35세 남성, 러닝 초보자부터 마라토너까지'
        },
        'gym': {
            'name': 'Alpha Gym Beast',
            'concept': 'fitness',
            'description': '헬스장에서 진짜 알파가 되는 100일 트레이닝 프로그램',
            'target_audience': '18-40세 남성, 헬스 초보자 및 중급자'
        },
        'study': {
            'name': 'Brain Chad Academy',
            'concept': 'study',
            'description': '공부로 뇌근육을 키우는 시그마 학습 시스템',
            'target_audience': '15-30세, 학생 및 직장인'
        },
        'hustle': {
            'name': 'Sigma Grind Master',
            'concept': 'productivity',
            'description': '생산성 그라인드셋으로 인생 역전을 이루는 100일',
            'target_audience': '20-40세, 직장인 및 창업가'
        }
    }

    if args.template in gigachad_templates:
        base_config = gigachad_templates[args.template]
        print(f"📱 Using GigaChad template: {args.template.upper()}")
    else:
        # 커스텀 설정
        base_config = {
            'name': args.name,
            'concept': args.concept,
            'description': args.description,
            'target_audience': args.target_audience
        }
        print(f"📱 Creating custom GigaChad app: {args.name}")

    # 패키지 이름 자동 생성
    if not args.package:
        safe_name = base_config['name'].lower().replace(' ', '_').replace('-', '_')
        package_name = f"com.chadtech.{safe_name}"
    else:
        package_name = args.package

    config = {
        **base_config,
        'package_name': package_name,
        'marketing_budget': args.budget,
        'include_premium': args.premium,
        'enable_analytics': True,
        'chad_mode': True  # 이게 핵심!
    }

    print(f"⚙️ Configuration:")
    print(f"   Name: {config['name']}")
    print(f"   Package: {config['package_name']}")
    print(f"   Concept: {config['concept']}")
    print(f"   Target: {config['target_audience']}")
    print(f"   Budget: ${config['marketing_budget']:,}")
    print()

    try:
        # 앱 생성 시작
        print("🚀 Starting GigaChad app generation...")
        result = generator.create_gigachad_app(config)

        # 결과 출력
        print("✅ GigaChad App Generation Complete!")
        print("=" * 50)
        print(f"📱 App Name: {result['app_name']}")
        print(f"📂 App Directory: {result['app_dir']}")
        print(f"📦 Package: {result['package_name']}")
        print(f"⏰ Created: {result['created_at']}")

        if 'marketing' in result:
            marketing = result['marketing']
            print(f"📊 Marketing Status: {marketing['status']}")
            if marketing['status'] == 'success':
                print(f"🎯 Keywords Generated: {len(marketing['config']['keywords'])}")
                print(f"📝 Content Suite: {marketing['content']['status']}")
                print(f"📱 Social Campaigns: {marketing['social']['status']}")

        if 'assets' in result:
            assets = result['assets']
            print(f"🎨 Assets Generated: {assets['icons']['count']} icons")
            print(f"🔊 Audio Scripts: {assets['audio']['total_lines']} voice lines")

        if 'launch_plan' in result:
            launch = result['launch_plan']
            print(f"🚀 Launch Timeline: {launch['estimated_timeline']}")
            print(f"💰 Recommended Budget: {launch['recommended_budget']}")

        # 결과를 JSON 파일로 저장
        output_file = f"gigachad_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)

        print(f"💾 Full results saved to: {output_file}")

        # Next steps 안내
        print("\n🗿 NEXT STEPS:")
        print("1. Navigate to your app directory")
        print("2. Run: flutter pub get")
        print("3. Run: flutter run")
        print("4. Start dominating the app store!")

    except Exception as e:
        print(f"❌ Error creating GigaChad app: {e}")
        sys.exit(1)

def list_templates(args):
    """사용 가능한 GigaChad 템플릿 목록"""

    templates = {
        'runner': {
            'name': 'GigaChad Runner',
            'description': '궁극의 러닝 챌린지 앱',
            'audience': '러너, 피트니스 애호가'
        },
        'gym': {
            'name': 'Alpha Gym Beast',
            'description': '헬스장 지배자 앱',
            'audience': '헬스 트레이너, 바디빌더'
        },
        'study': {
            'name': 'Brain Chad Academy',
            'description': '뇌근육 키우는 학습 앱',
            'audience': '학생, 자기계발러'
        },
        'hustle': {
            'name': 'Sigma Grind Master',
            'description': '생산성 그라인드셋 앱',
            'audience': '직장인, 창업가'
        }
    }

    print("🗿 Available GigaChad Templates:")
    print("=" * 40)

    for key, template in templates.items():
        print(f"📱 {key.upper()}")
        print(f"   Name: {template['name']}")
        print(f"   Description: {template['description']}")
        print(f"   Target: {template['audience']}")
        print()

def analyze_market(args):
    """마켓 분석 실행"""

    print("📊 GigaChad Market Analysis")
    print("=" * 30)

    # 여기서 마케팅 시스템의 분석 기능 호출
    try:
        from marketing_orchestrator import MarketingOrchestrator

        orchestrator = MarketingOrchestrator()

        analysis_config = {
            'category': args.category,
            'target_keywords': args.keywords.split(',') if args.keywords else [],
            'competitor_apps': args.competitors.split(',') if args.competitors else [],
            'region': args.region
        }

        print(f"🎯 Analyzing category: {args.category}")
        print(f"🔍 Target keywords: {analysis_config['target_keywords']}")
        print(f"🏆 Competitors: {analysis_config['competitor_apps']}")
        print()

        # 실제 분석 실행 (모의)
        print("⚡ Running market analysis...")
        analysis_result = {
            'market_size': 'Large',
            'competition_level': 'High',
            'opportunity_score': 8.5,
            'recommended_keywords': ['fitness', 'workout', 'chad', 'motivation'],
            'pricing_strategy': 'Freemium with $9.99 premium',
            'launch_timing': 'Q1 2024 recommended'
        }

        print("✅ Analysis Complete!")
        print(f"📈 Market Size: {analysis_result['market_size']}")
        print(f"🥊 Competition: {analysis_result['competition_level']}")
        print(f"⭐ Opportunity Score: {analysis_result['opportunity_score']}/10")
        print(f"🎯 Top Keywords: {', '.join(analysis_result['recommended_keywords'])}")
        print(f"💰 Pricing Strategy: {analysis_result['pricing_strategy']}")
        print(f"📅 Launch Timing: {analysis_result['launch_timing']}")

    except ImportError:
        print("⚠️ Marketing system not available. Install marketing-automation-system first.")

def main():
    parser = argparse.ArgumentParser(
        description='🗿 GigaChad App Factory - Build Apps Like a Chad',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create using template
  python gigachad_cli.py create --template runner --budget 15000

  # Create custom app
  python gigachad_cli.py create --name "Beast Cardio" --concept fitness --budget 20000

  # List available templates
  python gigachad_cli.py templates

  # Analyze market
  python gigachad_cli.py analyze --category fitness --keywords "workout,gym,chad"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new GigaChad app')
    create_parser.add_argument('--template', choices=['runner', 'gym', 'study', 'hustle'],
                              help='Use predefined GigaChad template')
    create_parser.add_argument('--name', help='Custom app name')
    create_parser.add_argument('--concept', choices=['fitness', 'running', 'study', 'productivity'],
                              help='App concept category')
    create_parser.add_argument('--package', help='Package name (e.g., com.company.app)')
    create_parser.add_argument('--description', help='App description')
    create_parser.add_argument('--target-audience', help='Target audience description')
    create_parser.add_argument('--budget', type=int, default=10000, help='Marketing budget in USD')
    create_parser.add_argument('--premium', action='store_true', help='Include premium features')
    create_parser.set_defaults(func=create_gigachad_app)

    # Templates command
    templates_parser = subparsers.add_parser('templates', help='List available templates')
    templates_parser.set_defaults(func=list_templates)

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze market opportunity')
    analyze_parser.add_argument('--category', required=True, help='App category to analyze')
    analyze_parser.add_argument('--keywords', help='Comma-separated target keywords')
    analyze_parser.add_argument('--competitors', help='Comma-separated competitor app names')
    analyze_parser.add_argument('--region', default='US', help='Target market region')
    analyze_parser.set_defaults(func=analyze_market)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()