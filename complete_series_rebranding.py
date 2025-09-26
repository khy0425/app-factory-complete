#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100 시리즈 완성 - Squat Master → Squat100
Mission100, Run100, Squat100 시리즈 통일
"""

import os
from pathlib import Path

def update_squat_master_to_squat100():
    """Squat Master → Squat100 리브랜딩"""
    print("🏋️ Squat Master → Squat100 리브랜딩 시작...")

    app_path = Path("flutter_apps/squat_master")

    if not app_path.exists():
        print("❌ squat_master 폴더가 없습니다.")
        return False

    # 새 정보
    new_info = {
        "name": "squat100",
        "full_name": "Squat100 - 100일 스쿼트 마스터",
        "package": "com.reaf.squat100",
        "description": "100일 스쿼트 마스터 챌린지"
    }

    # 1. pubspec.yaml 업데이트
    pubspec_path = app_path / "pubspec.yaml"
    if pubspec_path.exists():
        try:
            with open(pubspec_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(pubspec_path, "r", encoding="cp949") as f:
                content = f.read()

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('name:'):
                lines[i] = f'name: {new_info["name"]}'
            elif line.startswith('description:'):
                lines[i] = f'description: "{new_info["description"]}"'

        with open(pubspec_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))

        print("  ✅ pubspec.yaml 업데이트 완료")

    # 2. Android 설정 업데이트
    build_gradle = app_path / "android" / "app" / "build.gradle.kts"
    if build_gradle.exists():
        try:
            with open(build_gradle, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(build_gradle, "r", encoding="cp949") as f:
                content = f.read()

        # namespace 및 applicationId 변경
        content = content.replace(
            'namespace = "com.reaf.squat_master"',
            f'namespace = "{new_info["package"]}"'
        )
        content = content.replace(
            'applicationId = "com.reaf.squat_master"',
            f'applicationId = "{new_info["package"]}"'
        )

        with open(build_gradle, "w", encoding="utf-8") as f:
            f.write(content)

        print("  ✅ Android 설정 업데이트 완료")

    # 3. README 업데이트
    readme_path = app_path / "README.md"
    if readme_path.exists():
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(readme_path, "r", encoding="cp949") as f:
                    content = f.read()
            except:
                content = "# Squat100\n\n100일 스쿼트 마스터 챌린지"

        content = content.replace("Squat Master", "Squat100")
        content = content.replace("squat_master", "squat100")

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("  ✅ README.md 업데이트 완료")

    return True

def create_series_summary():
    """100 시리즈 요약 생성"""
    series_info = {
        "series_name": "100 챌린지 시리즈",
        "concept": "100일 동안 꾸준히 운동하여 목표 달성",
        "apps": {
            "Mission100": {
                "full_name": "Mission100 - 푸쉬업 마스터",
                "package": "com.reaf.mission100",
                "status": "✅ 플레이스토어 출시 완료",
                "target": "100개 푸쉬업 달성"
            },
            "Run100": {
                "full_name": "Run100 - 100일 런닝 마스터",
                "package": "com.reaf.run100",
                "status": "⚡ 리브랜딩 완료, 빌드 준비중",
                "target": "100일 런닝 습관 완성"
            },
            "Squat100": {
                "full_name": "Squat100 - 100일 스쿼트 마스터",
                "package": "com.reaf.squat100",
                "status": "⚡ 리브랜딩 완료, 빌드 준비중",
                "target": "100개 스쿼트 달성"
            }
        },
        "branding_benefits": [
            "일관된 브랜딩으로 사용자 인식도 향상",
            "시리즈 효과로 교차 다운로드 유도",
            "숫자 기반 목표로 명확한 동기부여",
            "Mission100 성공 시 다른 앱도 연쇄 성공 가능"
        ]
    }

    return series_info

def main():
    print("🚀 100 시리즈 완성 작업 시작!")
    print("="*50)

    # 1. Squat Master → Squat100 리브랜딩
    squat_success = update_squat_master_to_squat100()

    # 2. 시리즈 요약 생성
    series_info = create_series_summary()

    # 3. 결과 출력
    print("\n📊 100 시리즈 완성 결과")
    print("="*50)

    if squat_success:
        print("✅ Squat Master → Squat100 리브랜딩 성공")
    else:
        print("❌ Squat100 리브랜딩 실패")

    print(f"\n🎯 100 챌린지 시리즈 완성:")
    for app_name, app_info in series_info["apps"].items():
        print(f"   • {app_name}: {app_info['status']}")

    print(f"\n💡 브랜딩 효과:")
    for benefit in series_info["branding_benefits"]:
        print(f"   • {benefit}")

    print(f"\n🚀 다음 단계:")
    print(f"   1. Run100, Squat100 APK 빌드 완료")
    print(f"   2. 세 앱 Google Play Console 등록")
    print(f"   3. Mission100 성과 기반 마케팅 전략 수립")

    return squat_success

if __name__ == "__main__":
    main()