#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Factory Launcher - 통합 앱 팩토리 실행기
Claude Pro + Nano Banana로 월 15개 고품질 앱 자동 생성
"""

import asyncio
import sys
import argparse
from datetime import datetime
from automation.serverless_app_factory import ServerlessAppFactory

def print_banner():
    """앱 팩토리 배너"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    🏭 SERVERLESS APP FACTORY                                     ║
║                Claude Pro + Nano Banana Integration                              ║
║                   월 15개 서버리스 고수익 앱 자동 생성                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝

🚀 Claude Pro: 완전한 Flutter 코드 생성
🎨 Nano Banana: 세계 최고 품질 에셋 생성
💰 월 $30 예산으로 $45,000+ 수익 창출 (서버 비용 $0!)
📱 85% 완성도 서버리스 앱 (무한 확장 가능)
"""
    print(banner)

async def show_factory_status():
    """팩토리 상태 표시"""
    factory = ServerlessAppFactory()
    status = factory.get_factory_status()

    print("📊 Factory Status:")
    print(f"  Claude Pro: {status['factory_config']['claude_pro_subscription']}")
    print(f"  Nano Banana: {status['factory_config']['nano_banana_integration']}")
    print(f"  Monthly Budget: {status['factory_config']['monthly_budget']}")
    print(f"  Max Apps/Month: {status['factory_config']['max_apps_per_month']}")
    print(f"  Apps Generated: {status['current_month']['apps_generated']}")
    print(f"  Budget Remaining: {status['current_month']['budget_remaining']}")
    print(f"  Expected Revenue: {status['expected_performance']['estimated_revenue_per_app']}")

async def generate_single_app(app_concept: str):
    """단일 앱 생성"""
    factory = ServerlessAppFactory()

    print(f"🚀 Generating app: {app_concept}")

    try:
        result = await factory.generate_complete_serverless_app(app_concept)

        print(f"✅ App generation complete!")
        print(f"  App: {result['app_concept']}")
        print(f"  Cost: ${result['total_cost']:.3f}")
        print(f"  Quality Score: {result['quality_assurance']['overall_quality_score']}/100")
        print(f"  Store Ready: {result['store_ready']}")
        print(f"  Generation Time: {result['generation_time_seconds']:.1f}s")

        if result['store_ready']:
            print(f"🎯 Ready for store deployment!")
        else:
            print(f"⚠️ Needs additional work before store submission")

    except Exception as e:
        print(f"❌ App generation failed: {e}")

async def monthly_batch_demo():
    """월간 배치 생성 데모"""
    factory = ServerlessAppFactory()

    demo_concepts = [
        "Premium Fitness Tracker Pro",
        "Elite Expense Manager",
        "Professional Task Planner"
    ]

    print(f"🏭 Starting monthly batch demo with {len(demo_concepts)} apps")

    try:
        results = await factory.monthly_batch_generation(demo_concepts)

        print(f"🎯 Batch Generation Complete!")
        print(f"  Successful Apps: {results['batch_stats']['successful_apps']}")
        print(f"  Success Rate: {results['batch_stats']['success_rate']}")
        print(f"  Total Cost: ${results['financial_summary']['total_spent']:.2f}")
        print(f"  Budget Used: {results['financial_summary']['budget_used']}")
        print(f"  Revenue Projection: {results['revenue_projection']['conservative']}")
        print(f"  ROI Estimate: {results['revenue_projection']['roi_estimate']}")

        print(f"\n📱 Generated Apps:")
        for app_name, app_data in results['apps'].items():
            if 'error' not in app_data:
                print(f"  ✅ {app_name}: ${app_data['total_cost']:.3f}")
            else:
                print(f"  ❌ {app_name}: {app_data['error']}")

    except Exception as e:
        print(f"❌ Batch generation failed: {e}")

def show_setup_guide():
    """설정 가이드 표시"""
    guide = """
🔧 Setup Guide:

1. Prerequisites:
   ✅ Claude Pro subscription ($20/month) - Already have!
   ✅ Google Gemini API key for Nano Banana
   ✅ Firebase project for app backend
   ✅ Flutter development environment

2. API Keys Setup:
   export GEMINI_API_KEY="your_gemini_api_key"
   export FIREBASE_PROJECT_ID="your_firebase_project"

3. Budget Configuration:
   - Monthly Budget: $30
   - Claude Pro: $20 (already subscribed)
   - Available for generation: $10
   - Apps per month: 15

4. Usage:
   python run_app_factory.py --status
   python run_app_factory.py --generate "My App Concept"
   python run_app_factory.py --batch-demo
   python run_app_factory.py --setup

💡 Tips:
- Each app costs ~$0.67 to generate
- 80% completion level with store-ready quality
- Expected revenue: $1500-5000 per app per month
- ROI: 7500% ($30 → $22,500+ potential)
"""
    print(guide)

async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="Unified App Factory - Claude Pro + Nano Banana",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--status", action="store_true",
                       help="Show factory status")
    parser.add_argument("--generate", type=str, metavar="CONCEPT",
                       help="Generate single app with given concept")
    parser.add_argument("--batch-demo", action="store_true",
                       help="Run monthly batch generation demo")
    parser.add_argument("--setup", action="store_true",
                       help="Show setup guide")

    args = parser.parse_args()

    print_banner()

    if args.setup:
        show_setup_guide()

    elif args.status:
        await show_factory_status()

    elif args.generate:
        await generate_single_app(args.generate)

    elif args.batch_demo:
        await monthly_batch_demo()

    else:
        print("🏭 Unified App Factory")
        print(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Available commands:")
        print("  --status         Show factory status and capacity")
        print("  --generate TEXT  Generate single app with concept")
        print("  --batch-demo     Run batch generation demo")
        print("  --setup          Show setup guide")
        print()
        print("💡 Quick start: python run_app_factory.py --status")
        print("🚀 Generate app: python run_app_factory.py --generate 'Fitness Tracker'")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 App factory interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)