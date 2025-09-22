#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
배치 앱 생성 시스템
10개의 MVP 앱을 자동으로 기획 및 생성
"""

import asyncio
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from automated_app_planner import AutomatedAppPlanner

load_dotenv()

class BatchAppGenerator:
    def __init__(self):
        self.planner = AutomatedAppPlanner()
        self.app_ideas = [
            "명상과 호흡 연습 앱",
            "한글 타이핑 연습 게임",
            "물 마시기 알림 앱",
            "간단한 가계부 앱",
            "색깔 맞추기 퍼즐 게임",
            "계단 카운터 앱",
            "미니 다이어리 앱",
            "동네 산책로 추천 앱",
            "오늘의 운세 앱",
            "간단한 암산 연습 앱"
        ]

    async def generate_all_apps(self):
        """모든 앱 아이디어를 배치로 생성"""

        print("🚀 배치 앱 생성 시작!")
        print(f"총 {len(self.app_ideas)}개의 앱을 생성합니다.")
        print("=" * 60)

        generated_projects = []

        for i, idea in enumerate(self.app_ideas, 1):
            print(f"\n🎯 [{i}/{len(self.app_ideas)}] 현재 앱: {idea}")
            print("-" * 40)

            try:
                # 1단계: 앱 기획서 생성
                print("📋 앱 기획서 생성 중...")
                app_plan = await self.planner.create_full_app_plan(idea)

                # 2단계: 기술 명세서 생성
                print("🔧 기술 명세서 생성 중...")
                tech_specs = await self.planner.create_technical_specs(app_plan)

                # 3단계: Flutter 코드 구조 생성
                print("💻 Flutter 코드 구조 생성 중...")
                flutter_code = await self.planner.create_flutter_code_structure(tech_specs)

                # 4단계: 마케팅 에셋 기획
                print("🎨 마케팅 에셋 기획 중...")
                marketing_assets = await self.planner.generate_marketing_assets(app_plan)

                # 5단계: 프로젝트 저장
                print("💾 프로젝트 파일 저장 중...")
                project_dir = await self.planner.save_complete_project(
                    idea, app_plan, tech_specs, flutter_code, marketing_assets
                )

                generated_projects.append({
                    "idea": idea,
                    "project_dir": str(project_dir),
                    "status": "success"
                })

                print(f"✅ 완료! 저장 위치: {project_dir}")

                # API 호출 제한을 위한 대기
                print("⏳ API 제한을 위해 3초 대기...")
                await asyncio.sleep(3)

            except Exception as e:
                print(f"❌ 실패: {e}")
                generated_projects.append({
                    "idea": idea,
                    "project_dir": None,
                    "status": "failed",
                    "error": str(e)
                })
                continue

        # 배치 생성 결과 저장
        await self.save_batch_summary(generated_projects)
        return generated_projects

    async def save_batch_summary(self, generated_projects):
        """배치 생성 결과 요약 저장"""

        summary = {
            "batch_date": "2025-09-21",
            "total_apps": len(self.app_ideas),
            "successful": len([p for p in generated_projects if p["status"] == "success"]),
            "failed": len([p for p in generated_projects if p["status"] == "failed"]),
            "projects": generated_projects,
            "next_steps": [
                "각 프로젝트의 Flutter 코드 구현",
                "배치 APK 빌드 시스템 구축",
                "Play Store 에셋 자동 생성",
                "마케팅 자동화 설정"
            ]
        }

        batch_dir = Path("generated_projects")
        batch_dir.mkdir(exist_ok=True)

        with open(batch_dir / "batch_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"\n📊 배치 생성 완료!")
        print(f"✅ 성공: {summary['successful']}개")
        print(f"❌ 실패: {summary['failed']}개")
        print(f"📁 요약 파일: {batch_dir / 'batch_summary.json'}")

async def main():
    """메인 실행 함수"""
    print("🤖 배치 앱 생성 시스템")
    print("80% MVP 전략으로 10개 앱을 자동 생성합니다")
    print("=" * 60)

    generator = BatchAppGenerator()
    await generator.generate_all_apps()

    print("\n🎉 모든 앱 생성이 완료되었습니다!")
    print("📁 generated_projects 폴더를 확인하세요.")

if __name__ == "__main__":
    asyncio.run(main())