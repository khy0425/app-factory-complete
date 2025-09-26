#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Play Store 에셋 자동 생성 실행기
기가차드 러너 앱의 모든 Play Store 에셋을 자동 생성
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from automation.gemini_store_assets import GeminiStoreAssetGenerator
from automation.mission100_asset_adapter import Mission100AssetAdapter

# .env 파일 로드
load_dotenv()

async def main():
    """메인 실행 함수"""

    print("🎨 Google Play Store 에셋 자동 생성기")
    print("=" * 60)

    # 기가차드 러너 앱 스펙
    gigachad_runner_spec = {
        "app_name": "기가차드 러너",
        "description": "100일 궁극의 러닝 챌린지. 평범한 인간에서 기가차드로의 진화",
        "tagline": "달린다... Yes.",
        "exercise_type": "running",
        "category": "Health & Fitness",
        "target_audience": "운동 초보자부터 고수까지",
        "key_features": [
            "기가차드 캐릭터 진화 시스템",
            "100일 러닝 챌린지 프로그램",
            "한국어 맞춤 운동 가이드",
            "일일 챌린지 및 업적 시스템",
            "Sigma Mindset 동기부여 시스템",
            "진행률 추적 및 통계",
            "오프라인 모드 지원",
            "광고 없는 프리미엄 경험"
        ],
        "ui_theme": {
            "primary_color": "#FFD700",  # Alpha Gold
            "secondary_color": "#FF0000",  # Grindset Red
            "background_color": "#1A1A1A",  # Chad Black
            "style": "Dark, Bold, Chad Aesthetic"
        },
        "monetization": {
            "model": "Freemium",
            "premium_features": [
                "모든 Chad 캐릭터 언락",
                "고급 통계 및 분석",
                "맞춤형 운동 플랜",
                "광고 제거"
            ]
        }
    }

    try:
        # Gemini Store Asset Generator 초기화
        generator = GeminiStoreAssetGenerator()

        print(f"🎯 앱: {gigachad_runner_spec['app_name']}")
        print(f"📝 설명: {gigachad_runner_spec['description']}")
        print(f"🎨 테마: {gigachad_runner_spec['ui_theme']['style']}")
        print()

        # 모든 Play Store 에셋 생성
        print("🔥 Play Store 에셋 생성 시작...")
        assets_result = await generator.generate_all_assets_for_app(gigachad_runner_spec)

        if "error" not in assets_result:
            print("✅ 에셋 생성 완료!")
            print(f"📁 저장 위치: store_assets/{gigachad_runner_spec['app_name'].lower().replace(' ', '_')}")
            print()

            # 생성된 에셋 목록 출력
            assets = assets_result.get("assets", {})

            if "feature_graphic" in assets:
                fg = assets["feature_graphic"]
                print(f"🖼️  Feature Graphic: {fg.get('dimensions', 'N/A')} - {fg.get('status', 'Unknown')}")

            if "app_icon" in assets:
                icon = assets["app_icon"]
                print(f"📱 앱 아이콘: {icon.get('dimensions', 'N/A')} - {icon.get('status', 'Unknown')}")

            if "screenshots" in assets:
                screenshots = assets["screenshots"]
                print(f"📸 스크린샷: {screenshots.get('count', 0)}개 - {screenshots.get('status', 'Unknown')}")

            if "promo_images" in assets:
                promo = assets["promo_images"]
                print(f"📢 프로모션 이미지: {promo.get('count', 0)}개 - {promo.get('status', 'Unknown')}")

            # Store Listing 패키지 생성
            print("\n📦 Play Store 업로드 패키지 생성 중...")
            store_package = generator.create_store_listing_package(
                gigachad_runner_spec,
                assets_result
            )

            print("✅ Store Listing 패키지 생성 완료!")
            print()

            # 업로드 체크리스트 출력
            print("📋 Play Store 업로드 체크리스트:")
            checklist = store_package.get("upload_checklist", {})
            for item, status in checklist.items():
                print(f"  {status} {item}")

            print()
            print("🎉 모든 Play Store 에셋이 준비되었습니다!")
            print("📱 이제 Flutter APK를 빌드하고 Play Console에 업로드하세요!")

        else:
            print(f"❌ 에셋 생성 실패: {assets_result['error']}")
            return False

        return True

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    # UTF-8 인코딩 설정
    import os
    if os.name == 'nt':  # Windows
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    # 비동기 실행
    success = asyncio.run(main())

    if success:
        print("\n🚀 다음 단계:")
        print("1. APK 빌드: flutter build apk --release")
        print("2. Play Console에서 앱 생성")
        print("3. 생성된 에셋들을 업로드")
        print("4. 앱 심사 제출")
        sys.exit(0)
    else:
        sys.exit(1)