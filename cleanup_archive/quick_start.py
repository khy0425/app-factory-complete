#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start Script
원클릭 배포 및 실행 스크립트
"""

import asyncio
import os
import sys
import subprocess
from datetime import datetime

def print_banner():
    """시작 배너"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    🚀 MCP ECOSYSTEM QUICK START                                  ║
║                          원클릭 배포 및 실행                                       ║
╚══════════════════════════════════════════════════════════════════════════════════╝

💰 월 $30 예산으로 $50,000+ 가치 창출
🧠 Ultra Intelligence • 📊 Real-time Analytics • 🤖 Full Automation
"""
    print(banner)

def check_dependencies():
    """의존성 체크"""
    print("📦 Checking dependencies...")

    required_packages = [
        'supabase',
        'requests',
        'asyncio'  # 내장 모듈
    ]

    missing_packages = []

    for package in required_packages:
        if package == 'asyncio':
            continue  # 내장 모듈
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")

    if missing_packages:
        print(f"\n📥 Installing missing packages...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"  ✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"  ❌ Failed to install {package}")
                return False

    print("✅ All dependencies ready")
    return True

async def quick_setup():
    """빠른 설정"""
    print("\n⚙️ Quick setup...")

    # 1. 환경 변수 설정
    from config_production import setup_environment_variables
    config = setup_environment_variables()
    print("✅ Environment variables configured")

    # 2. Supabase 스키마 설정
    print("\n📊 Setting up Supabase schema...")
    try:
        from setup_supabase_schema import setup_supabase_complete
        schema_success = await setup_supabase_complete()
        if schema_success:
            print("✅ Supabase schema ready")
        else:
            print("⚠️ Supabase schema setup had issues")
    except Exception as e:
        print(f"❌ Supabase setup failed: {e}")

    # 3. 연결 테스트
    print("\n🔍 Testing connections...")
    try:
        from test_mcp_connections import run_complete_connection_test
        test_success = await run_complete_connection_test()
        if test_success:
            print("✅ All connections working")
        else:
            print("⚠️ Some connections failed")
    except Exception as e:
        print(f"❌ Connection test failed: {e}")

    return True

async def run_demo():
    """데모 실행"""
    print("\n🎬 Running ecosystem demo...")

    try:
        from run_complete_ecosystem import run_complete_ecosystem_demo
        demo_success = await run_complete_ecosystem_demo()
        return demo_success
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def show_next_steps():
    """다음 단계 안내"""
    print(f"\n{'='*60}")
    print("🎯 NEXT STEPS")
    print(f"{'='*60}")

    print("\n1️⃣ MVP 프로젝트 자동 관리:")
    print("  python run_auto_mvp_manager.py --detect     # 자동 감지 & 레포 생성")
    print("  python run_auto_mvp_manager.py --status     # 프로젝트 상태 확인")

    print("\n2️⃣ CI/CD 자동화 설정:")
    print("  python run_cicd_automation.py --setup-all   # 모든 프로젝트 CI/CD 설정")
    print("  python run_cicd_automation.py --status      # CI/CD 상태 확인")

    print("\n3️⃣ Notion 대시보드 설정:")
    print("  python run_notion_dashboard.py --setup         # Notion 추적 설정")
    print("  python run_notion_dashboard.py --test          # 연결 테스트")

    print("\n4️⃣ 자동화 시스템 시작:")
    print("  python run_cicd_automation.py --start-scheduler  # 6시간마다 자동 실행 (Notion 추적 포함)")

    print("\n5️⃣ 추가 설정 (선택사항):")
    print("  • Zapier 웹훅 설정: https://zapier.com")
    print("  • Notion Integration 권한 설정")

    print("\n6️⃣ 프로덕션 실행:")
    print("  python run_complete_ecosystem.py --production")

    print("\n7️⃣ 모니터링 대시보드:")
    print("  • Supabase: https://supabase.com/dashboard/project/pbktfaimqoxmnxpkvdpm")
    print("  • GitHub: 자동 생성된 이슈들 & MVP 레포들 & CI/CD Actions")
    print("  • Notion: 실시간 Task 추적 & KPI 대시보드")

    print("\n8️⃣ 지원:")
    print("  • 배포 가이드: DEPLOYMENT_GUIDE.md")
    print("  • 추가 테스트: python test_mcp_connections.py")
    print("  • MVP 관리: python run_auto_mvp_manager.py --setup")
    print("  • CI/CD 가이드: python run_cicd_automation.py --examples")
    print("  • Notion 설정: python run_notion_dashboard.py --guide")

async def main():
    """메인 실행 함수"""
    print_banner()

    # 단계별 실행
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 의존성 체크
    if not check_dependencies():
        print("❌ Dependency check failed. Please install required packages manually.")
        return

    # 2. 빠른 설정
    setup_success = await quick_setup()
    if not setup_success:
        print("❌ Setup failed. Check configuration.")
        return

    # 3. 데모 실행
    demo_success = await run_demo()

    # 4. 결과 및 다음 단계
    if demo_success:
        print(f"\n🎉 SUCCESS! MCP Ecosystem is ready!")
        show_next_steps()
    else:
        print(f"\n⚠️ Demo completed with issues. Check logs above.")

    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Quick start interrupted by user")
    except Exception as e:
        print(f"\n❌ Quick start failed: {e}")
        print("💡 Try manual setup with DEPLOYMENT_GUIDE.md")