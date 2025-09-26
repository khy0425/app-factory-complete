#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
단일 Feature Graphic 생성 테스트
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from automation.gemini_store_assets import GeminiStoreAssetGenerator

# .env 파일 로드
load_dotenv()

async def main():
    """메인 실행 함수"""

    print("🎨 Feature Graphic 단일 생성 테스트")
    print("=" * 60)

    # 기가차드 러너 앱 스펙
    gigachad_runner_spec = {
        "app_name": "기가차드 러너",
        "description": "100일 궁극의 러닝 챌린지. 평범한 인간에서 기가차드로의 진화",
        "tagline": "달린다... Yes.",
        "exercise_type": "running"
    }

    try:
        # Generator 초기화
        generator = GeminiStoreAssetGenerator()

        # 출력 디렉토리
        output_dir = Path("store_assets/기가차드_러너")
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"🎯 앱: {gigachad_runner_spec['app_name']}")
        print(f"📝 설명: {gigachad_runner_spec['description']}")
        print()

        # Feature Graphic만 생성
        print("🔥 Feature Graphic 생성 시작...")
        result = await generator.generate_feature_graphic(gigachad_runner_spec, output_dir)

        if result.get("status") == "success":
            print(f"✅ Feature Graphic 생성 성공!")
            print(f"📁 파일 위치: {result.get('file_path')}")
            print(f"📏 크기: {result.get('size_kb')}KB")
            print(f"💰 비용: ${result.get('cost')}")
        else:
            print(f"❌ Feature Graphic 생성 실패: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # UTF-8 인코딩 설정
    if os.name == 'nt':  # Windows
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    # 비동기 실행
    asyncio.run(main())