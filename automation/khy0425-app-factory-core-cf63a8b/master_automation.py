#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마스터 자동화 시스템
전체 앱 팩토리 파이프라인을 한번에 실행

1. 10개 MVP 앱 기획 생성
2. Flutter 프로젝트 변환
3. APK 빌드
4. 마케팅 에셋 생성 (향후)
5. 배포 자동화 (향후)
"""

import asyncio
import json
import os
import time
from pathlib import Path
from batch_app_generator import BatchAppGenerator
from flutter_code_generator import FlutterCodeGenerator

class MasterAutomation:
    def __init__(self):
        self.batch_generator = BatchAppGenerator()
        self.flutter_generator = FlutterCodeGenerator()

    async def run_complete_pipeline(self):
        """전체 파이프라인 실행"""

        print("🚀 마스터 자동화 시스템 시작!")
        print("80% MVP 전략으로 완전 자동화된 앱 팩토리")
        print("=" * 60)

        # 1단계: 10개 MVP 앱 기획 생성
        print("\n📋 1단계: 10개 MVP 앱 기획 생성")
        print("-" * 40)
        generated_projects = await self.batch_generator.generate_all_apps()

        success_count = len([p for p in generated_projects if p["status"] == "success"])
        print(f"✅ {success_count}개 앱 기획 완료")

        if success_count == 0:
            print("❌ 기획 생성 실패로 프로세스 중단")
            return

        # 2단계: Flutter 프로젝트 변환 및 APK 빌드
        print("\n🔨 2단계: Flutter 프로젝트 변환 및 APK 빌드")
        print("-" * 40)
        build_results = await self.flutter_generator.process_all_generated_projects()

        apk_count = len([r for r in build_results if r["status"] == "success"])
        print(f"✅ {apk_count}개 APK 빌드 완료")

        # 3단계: 전체 결과 요약
        await self.create_final_summary(generated_projects, build_results)

        print("\n🎉 마스터 자동화 완료!")
        print(f"📱 총 {apk_count}개의 배포 가능한 앱이 생성되었습니다.")

    async def create_final_summary(self, planning_results, build_results):
        """최종 요약 보고서 생성"""

        summary = {
            "master_automation_date": "2025-09-21",
            "strategy": "80% MVP 앱 팩토리",
            "total_planned_apps": len(planning_results),
            "successful_plans": len([p for p in planning_results if p["status"] == "success"]),
            "total_built_apps": len(build_results),
            "successful_builds": len([r for r in build_results if r["status"] == "success"]),
            "planning_results": planning_results,
            "build_results": build_results,
            "next_steps": [
                "생성된 APK들을 Play Store에 업로드",
                "각 앱별 마케팅 에셋 이미지 생성",
                "소셜 미디어 자동 홍보 시스템 구축",
                "수익 분석 및 최적화"
            ],
            "revenue_strategy": {
                "monetization": "AdMob 광고 (테스트 ID 적용)",
                "target_revenue": "앱당 월 $50-200 (광고 기반)",
                "scaling_plan": "성공 앱 기반으로 유사 앱 대량 생산"
            }
        }

        with open("master_automation_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print("\n📊 최종 요약:")
        print(f"📋 기획 완료: {summary['successful_plans']}개")
        print(f"🔨 빌드 완료: {summary['successful_builds']}개")
        print(f"💰 예상 수익: ${summary['successful_builds'] * 50}-${summary['successful_builds'] * 200}/월")
        print(f"📁 요약 파일: master_automation_summary.json")

    async def quick_status_check(self):
        """현재 상태 빠른 확인"""

        print("📊 현재 앱 팩토리 상태")
        print("=" * 40)

        # Generated projects 확인
        generated_dir = Path("generated_projects")
        if generated_dir.exists():
            projects = [d for d in generated_dir.iterdir() if d.is_dir()]
            print(f"📋 기획 완료: {len(projects)}개")

            for project in projects:
                print(f"  - {project.name}")
        else:
            print("📋 기획 완료: 0개")

        # Flutter apps 확인
        flutter_dir = Path("flutter_apps")
        if flutter_dir.exists():
            flutter_projects = [d for d in flutter_dir.iterdir() if d.is_dir()]
            print(f"🔨 Flutter 프로젝트: {len(flutter_projects)}개")

            # APK 확인
            apk_count = 0
            for project in flutter_projects:
                apk_path = project / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk"
                if apk_path.exists():
                    apk_count += 1

            print(f"📱 APK 빌드 완료: {apk_count}개")
        else:
            print("🔨 Flutter 프로젝트: 0개")

async def main():
    """메인 실행 함수"""
    automation = MasterAutomation()

    # 현재 상태 확인
    await automation.quick_status_check()

    print("\n" + "=" * 60)
    choice = input("전체 파이프라인을 실행하시겠습니까? (y/N): ").lower().strip()

    if choice == 'y':
        await automation.run_complete_pipeline()
    else:
        print("실행이 취소되었습니다.")

if __name__ == "__main__":
    asyncio.run(main())