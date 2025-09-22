#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자동 기가차드 앱 생성기
Mission100 에셋을 활용하여 한국어 기가차드 스타일 운동 앱을 자동 생성하고
노션과 슬랙으로 실시간 보고
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from automation.serverless_app_factory import ServerlessAppFactory
from automation.mission100_asset_adapter import Mission100AssetAdapter

class ChadAppAutoGenerator:
    """기가차드 앱 자동 생성기"""

    def __init__(self):
        self.factory = ServerlessAppFactory()
        self.mission100_adapter = Mission100AssetAdapter()

    async def generate_random_chad_app(self):
        """랜덤한 기가차드 앱 자동 생성"""

        print("🔥 기가차드 앱 자동 생성 시작...")
        print("=" * 80)

        try:
            # 1. 랜덤 앱 컨셉 선택
            app_concept = self.mission100_adapter.get_random_chad_app_concept()
            app_spec = self.mission100_adapter.generate_chad_app_spec(app_concept)

            print(f"🎯 선택된 앱: {app_spec['app_name']}")
            print(f"📝 태그라인: {app_spec['tagline']}")
            print(f"🏋️ 운동 타입: {app_spec['technical_specs']['platform']}")

            # 2. 노션에 프로젝트 시작 보고
            if self.factory.notion_dashboard:
                await self.report_to_notion_start(app_spec)

            # 3. 슬랙에 시작 알림
            if self.factory.slack_notifier:
                await self.report_to_slack_start(app_spec)

            # 4. 실제 앱 생성
            print(f"\n🚀 앱 생성 중: {app_spec['description']}")

            result = await self.factory.generate_complete_serverless_app(
                f"{app_spec['app_name']} - {app_spec['description']}"
            )

            # 5. 생성 완료 보고
            await self.report_completion(app_spec, result)

            print(f"\n✅ 앱 생성 완료!")
            print(f"📱 앱명: {result.get('app_concept', app_spec['app_name'])}")
            print(f"💰 비용: ${result.get('total_cost', 0):.3f}")
            print(f"🏆 품질점수: {result.get('quality_assurance', {}).get('overall_quality_score', 0)}/100")
            print(f"🎯 스토어 준비: {result.get('store_ready', False)}")

            return result

        except Exception as e:
            print(f"❌ 앱 생성 실패: {e}")

            # 에러 보고
            if self.factory.slack_notifier:
                self.factory.slack_notifier.notify_error(
                    "Chad App Generation Failed",
                    str(e),
                    app_concept.get('app_name', 'Unknown App')
                )

            raise e

    async def report_to_notion_start(self, app_spec: Dict):
        """노션에 프로젝트 시작 보고"""
        try:
            notion_data = {
                "title": f"🔥 {app_spec['app_name']} 생성 시작",
                "status": "진행중",
                "project_type": "기가차드 운동 앱",
                "description": app_spec['description'],
                "tagline": app_spec['tagline'],
                "target_audience": app_spec['target_audience'],
                "platform": app_spec['technical_specs']['platform'],
                "expected_revenue": app_spec['monetization']['expected_revenue'],
                "start_time": datetime.now().isoformat(),
                "key_features": "\\n".join(app_spec['key_features'])
            }

            await self.factory.notion_dashboard.create_project_entry(notion_data)
            print("📊 노션에 프로젝트 시작 보고 완료")

        except Exception as e:
            print(f"⚠️ 노션 보고 실패: {e}")

    async def report_to_slack_start(self, app_spec: Dict):
        """슬랙에 시작 알림"""
        try:
            message = f"""
🔥 **기가차드 앱 생성 시작!**

📱 **앱명**: {app_spec['app_name']}
💬 **태그라인**: {app_spec['tagline']}
🎯 **타겟**: {app_spec['target_audience']}
💰 **예상 수익**: {app_spec['monetization']['expected_revenue']}

🚀 Mission100 에셋 재활용으로 비용 50% 절감!
"""

            self.factory.slack_notifier.notify_app_generation_start(
                app_spec['app_name'],
                app_spec['description'],
                {"estimated_cost": "$0.35", "asset_reuse": "50% 절감"}
            )
            print("💬 슬랙에 시작 알림 전송 완료")

        except Exception as e:
            print(f"⚠️ 슬랙 알림 실패: {e}")

    async def report_completion(self, app_spec: Dict, result: Dict):
        """완료 보고"""
        try:
            # 노션 완료 업데이트
            if self.factory.notion_dashboard:
                completion_data = {
                    "status": "완료" if result.get('store_ready') else "검토 필요",
                    "actual_cost": result.get('total_cost', 0),
                    "quality_score": result.get('quality_assurance', {}).get('overall_quality_score', 0),
                    "completion_time": datetime.now().isoformat(),
                    "store_ready": result.get('store_ready', False),
                    "generation_time": result.get('generation_time_seconds', 0)
                }

                await self.factory.notion_dashboard.update_project_completion(
                    app_spec['app_name'],
                    completion_data
                )

            # 슬랙 완료 알림
            if self.factory.slack_notifier:
                success_message = f"""
✅ **{app_spec['app_name']} 생성 완료!**

💰 **실제 비용**: ${result.get('total_cost', 0):.3f}
🏆 **품질 점수**: {result.get('quality_assurance', {}).get('overall_quality_score', 0)}/100
⏱️ **생성 시간**: {result.get('generation_time_seconds', 0):.1f}초
🎯 **스토어 준비**: {"✅ 준비완료" if result.get('store_ready') else "❌ 추가 작업 필요"}

{app_spec['tagline']} 🔥
"""

                self.factory.slack_notifier.notify_app_generation_complete(
                    app_spec['app_name'],
                    result.get('total_cost', 0),
                    result.get('quality_assurance', {}).get('overall_quality_score', 0),
                    result.get('store_ready', False)
                )

            print("📊 완료 보고 전송 완료")

        except Exception as e:
            print(f"⚠️ 완료 보고 실패: {e}")

async def main():
    """메인 실행 함수"""

    print("🔥 자동 기가차드 앱 생성기")
    print("Mission100 에셋 재활용 + 노션/슬랙 자동 보고")
    print("=" * 60)

    generator = ChadAppAutoGenerator()

    try:
        # 자동 앱 생성
        result = await generator.generate_random_chad_app()

        print(f"\n🎉 성공! 새로운 기가차드 앱이 생성되었습니다!")
        print(f"📊 노션과 슬랙에서 진행상황을 확인하세요.")

        return result

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        return None

if __name__ == "__main__":
    import sys
    import os

    # UTF-8 인코딩 설정
    if os.name == 'nt':  # Windows
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    # 비동기 실행
    result = asyncio.run(main())

    if result:
        sys.exit(0)
    else:
        sys.exit(1)