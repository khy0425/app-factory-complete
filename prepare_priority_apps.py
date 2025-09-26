#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
우선순위 앱 출시 준비 (Runner + Squat)
"""

import os
import subprocess
import shutil
from pathlib import Path

def update_package_name(app_path, package_name):
    """패키지명 업데이트"""
    print(f"  🔧 패키지명 변경: {package_name}")

    # Android build.gradle 수정
    build_gradle = app_path / "android" / "app" / "build.gradle"
    if build_gradle.exists():
        try:
            with open(build_gradle, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(build_gradle, "r", encoding="cp949") as f:
                content = f.read()

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'applicationId' in line:
                lines[i] = f'        applicationId "{package_name}"'
                break

        with open(build_gradle, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))

        print(f"    ✅ build.gradle 업데이트")
        return True
    else:
        print(f"    ❌ build.gradle 파일 없음")
        return False

def build_app(app_name, app_path):
    """앱 빌드"""
    print(f"  🔨 {app_name} APK 빌드 중...")

    try:
        # Flutter가 설치되어 있는지 확인
        flutter_check = subprocess.run(["flutter", "--version"],
                                     capture_output=True, text=True)

        if flutter_check.returncode != 0:
            print(f"    ❌ Flutter가 설치되지 않음")
            return False

        # Clean
        subprocess.run(["flutter", "clean"], cwd=app_path, check=True)

        # Pub get
        subprocess.run(["flutter", "pub", "get"], cwd=app_path, check=True)

        # Build APK
        result = subprocess.run(["flutter", "build", "apk", "--release"],
                              cwd=app_path, capture_output=True, text=True)

        if result.returncode == 0:
            # APK 파일 복사
            apk_source = app_path / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk"

            if apk_source.exists():
                output_dir = Path("priority_releases")
                output_dir.mkdir(exist_ok=True)

                apk_dest = output_dir / f"{app_name}-release.apk"
                shutil.copy2(apk_source, apk_dest)

                print(f"    ✅ APK 생성 완료: {apk_dest}")
                return True
            else:
                print(f"    ❌ APK 파일 생성 실패")
                return False
        else:
            print(f"    ❌ 빌드 실패: {result.stderr}")
            return False

    except Exception as e:
        print(f"    ❌ 빌드 오류: {e}")
        return False

def prepare_gigachad_runner():
    """GigaChad Runner 준비"""
    print("🏃 GigaChad Runner 출시 준비...")

    app_path = Path("flutter_apps/gigachad_runner")

    if not app_path.exists():
        print("  ❌ gigachad_runner 폴더 없음")
        return False

    # 패키지명 변경
    if update_package_name(app_path, "com.reaf.gigachadrunner"):
        # APK 빌드
        return build_app("gigachad_runner", app_path)

    return False

def prepare_squat_master():
    """Squat Master 준비"""
    print("🏋️ Squat Master 출시 준비...")

    app_path = Path("flutter_apps/squat_master")

    if not app_path.exists():
        print("  ❌ squat_master 폴더 없음")
        return False

    # 패키지명 변경
    if update_package_name(app_path, "com.reaf.squatmaster"):
        # APK 빌드
        return build_app("squat_master", app_path)

    return False

def main():
    print("🚀 우선순위 앱 출시 준비 시작!")
    print("="*50)

    results = {}

    # GigaChad Runner 준비
    results["runner"] = prepare_gigachad_runner()

    # Squat Master 준비
    results["squat"] = prepare_squat_master()

    # 결과 요약
    print("\n📊 출시 준비 결과")
    print("="*50)
    print(f"GigaChad Runner: {'✅ 성공' if results['runner'] else '❌ 실패'}")
    print(f"Squat Master: {'✅ 성공' if results['squat'] else '❌ 실패'}")

    if any(results.values()):
        print(f"\n📦 빌드 결과: priority_releases/ 폴더 확인")

    return results

if __name__ == "__main__":
    main()