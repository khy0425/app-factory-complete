#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 나머지 앱들 플레이스토어 업로드 준비 자동화
com.reaf.XXX 패키지명으로 일괄 설정
"""

import os
import json
import shutil
from pathlib import Path
import subprocess

class BatchUploadPreparation:
    def __init__(self):
        # 이미 업로드된 앱 (제외)
        self.uploaded_apps = ["mission100_v3"]

        # Flutter Apps (수동 개발) - 업로드 대기
        self.flutter_apps = {
            "burpeebeast": "com.reaf.burpeebeast",
            "gigachad_runner": "com.reaf.gigachadrunner",
            "jumpingjackjedi": "com.reaf.jumpingjackjedi",
            "lungelegend": "com.reaf.lungelegend",
            "plankchampion": "com.reaf.plankchampion",
            "pulluppro": "com.reaf.pulluppro",
            "squat_master": "com.reaf.squatmaster"
        }

        # Generated Projects (AI 생성) - 업로드 대기
        self.generated_apps = {
            "calm_breath": "com.reaf.calmbreath",
            "catchy": "com.reaf.catchy",
            "colorpop_pangpang": "com.reaf.colorpop",
            "meditation_app": "com.reaf.meditation",
            "mindbreath": "com.reaf.mindbreath",
            "momento": "com.reaf.momento",
            "sanchaekgil_friend": "com.reaf.sanchaekgil",
            "semsem_master": "com.reaf.semsem",
            "stepup": "com.reaf.stepup"
        }

        # 모든 앱 통합
        self.all_apps = {**self.flutter_apps, **self.generated_apps}

    def update_package_name(self, app_name, new_package_name):
        """앱의 패키지명을 com.reaf.XXX로 변경"""
        # Flutter Apps 경로
        flutter_path = Path(f"flutter_apps/{app_name}")
        generated_path = Path(f"generated_projects/{app_name}")

        app_path = flutter_path if flutter_path.exists() else generated_path

        if not app_path.exists():
            print(f"❌ {app_name} 폴더를 찾을 수 없습니다.")
            return False

        print(f"🔧 {app_name} 패키지명 변경: {new_package_name}")

        # 1. Android build.gradle 수정
        android_build_gradle = app_path / "android" / "app" / "build.gradle"
        if android_build_gradle.exists():
            self.update_android_package(android_build_gradle, new_package_name)

        # 2. AndroidManifest.xml 수정
        manifest_path = app_path / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
        if manifest_path.exists():
            self.update_android_manifest(manifest_path, new_package_name)

        # 3. MainActivity.kt 수정 (있는 경우)
        main_activity_path = app_path / "android" / "app" / "src" / "main" / "kotlin"
        if main_activity_path.exists():
            self.update_main_activity(main_activity_path, new_package_name)

        # 4. pubspec.yaml에서 앱 이름 확인
        pubspec_path = app_path / "pubspec.yaml"
        if pubspec_path.exists():
            self.check_pubspec(pubspec_path, app_name)

        return True

    def update_android_package(self, build_gradle_path, new_package_name):
        """Android build.gradle 패키지명 변경"""
        try:
            with open(build_gradle_path, "r", encoding="utf-8") as f:
                content = f.read()

            # applicationId 변경
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'applicationId' in line:
                    lines[i] = f'        applicationId "{new_package_name}"'
                    break

            with open(build_gradle_path, "w", encoding="utf-8") as f:
                f.write('\n'.join(lines))

            print(f"  ✅ build.gradle 업데이트 완료")

        except Exception as e:
            print(f"  ❌ build.gradle 업데이트 실패: {e}")

    def update_android_manifest(self, manifest_path, new_package_name):
        """AndroidManifest.xml 패키지명 변경"""
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                content = f.read()

            # package 속성 변경
            import re
            content = re.sub(r'package="[^"]*"', f'package="{new_package_name}"', content)

            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  ✅ AndroidManifest.xml 업데이트 완료")

        except Exception as e:
            print(f"  ❌ AndroidManifest.xml 업데이트 실패: {e}")

    def update_main_activity(self, kotlin_path, new_package_name):
        """MainActivity.kt 패키지명 변경"""
        try:
            # 새로운 패키지 구조로 폴더 이동
            package_parts = new_package_name.split('.')
            new_path = kotlin_path
            for part in package_parts:
                new_path = new_path / part

            new_path.mkdir(parents=True, exist_ok=True)

            # MainActivity.kt 파일 찾기 및 이동
            for kotlin_file in kotlin_path.rglob("MainActivity.kt"):
                # 패키지 선언 변경
                with open(kotlin_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # package 선언 변경
                import re
                content = re.sub(r'package [^\n]*', f'package {new_package_name}', content)

                # 새 위치에 저장
                new_file_path = new_path / "MainActivity.kt"
                with open(new_file_path, "w", encoding="utf-8") as f:
                    f.write(content)

                # 기존 파일 삭제
                kotlin_file.unlink()

                print(f"  ✅ MainActivity.kt 업데이트 완료")
                break

        except Exception as e:
            print(f"  ❌ MainActivity.kt 업데이트 실패: {e}")

    def check_pubspec(self, pubspec_path, app_name):
        """pubspec.yaml 확인"""
        try:
            with open(pubspec_path, "r", encoding="utf-8") as f:
                content = f.read()

            if f"name: {app_name}" in content:
                print(f"  ✅ pubspec.yaml 확인됨")
            else:
                print(f"  ⚠️ pubspec.yaml 앱 이름 확인 필요")

        except Exception as e:
            print(f"  ❌ pubspec.yaml 확인 실패: {e}")

    def build_apk(self, app_name):
        """APK 빌드"""
        # Flutter Apps 경로
        flutter_path = Path(f"flutter_apps/{app_name}")
        generated_path = Path(f"generated_projects/{app_name}")

        app_path = flutter_path if flutter_path.exists() else generated_path

        if not app_path.exists():
            print(f"❌ {app_name} 폴더를 찾을 수 없습니다.")
            return False

        print(f"🔨 {app_name} APK 빌드 중...")

        try:
            # Flutter clean
            subprocess.run(["flutter", "clean"], cwd=app_path, check=True)

            # Flutter pub get
            subprocess.run(["flutter", "pub", "get"], cwd=app_path, check=True)

            # Flutter build apk
            subprocess.run(["flutter", "build", "apk", "--release"], cwd=app_path, check=True)

            print(f"  ✅ {app_name} APK 빌드 완료")

            # APK 파일 복사
            apk_source = app_path / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk"
            apk_dest = Path("build_outputs") / f"{app_name}-release.apk"
            apk_dest.parent.mkdir(exist_ok=True)

            if apk_source.exists():
                shutil.copy2(apk_source, apk_dest)
                print(f"  📦 APK 저장: {apk_dest}")
                return True
            else:
                print(f"  ❌ APK 파일을 찾을 수 없음")
                return False

        except subprocess.CalledProcessError as e:
            print(f"  ❌ {app_name} 빌드 실패: {e}")
            return False

    def create_upload_checklist(self):
        """업로드 체크리스트 생성"""
        checklist = {
            "업로드_준비_상태": {
                "총_앱_수": len(self.all_apps),
                "Flutter_Apps": len(self.flutter_apps),
                "Generated_Apps": len(self.generated_apps),
                "이미_업로드된_앱": self.uploaded_apps
            },
            "업로드_대기_앱목록": {},
            "필요한_작업": [
                "Google Play Console에서 새 앱 생성",
                "앱 아이콘 및 스크린샷 준비",
                "앱 설명 및 키워드 최적화",
                "연령 등급 설정",
                "개인정보 처리방침 URL 등록",
                "APK 업로드 및 출시"
            ]
        }

        for app_name, package_name in self.all_apps.items():
            category = "Flutter_App" if app_name in self.flutter_apps else "Generated_App"
            checklist["업로드_대기_앱목록"][app_name] = {
                "패키지명": package_name,
                "카테고리": category,
                "APK_경로": f"build_outputs/{app_name}-release.apk",
                "준비상태": "대기중"
            }

        with open("upload_checklist.json", "w", encoding="utf-8") as f:
            json.dump(checklist, f, ensure_ascii=False, indent=2)

        print("📋 업로드 체크리스트 생성: upload_checklist.json")
        return checklist

    def run_batch_preparation(self):
        """일괄 업로드 준비 실행"""
        print("🚀 나머지 앱들 플레이스토어 업로드 준비 시작!")
        print("="*60)

        print(f"\n📱 총 {len(self.all_apps)}개 앱 업로드 준비:")
        print(f"   • Flutter Apps: {len(self.flutter_apps)}개")
        print(f"   • Generated Apps: {len(self.generated_apps)}개")
        print(f"   • 이미 업로드됨: {len(self.uploaded_apps)}개 (Mission100)")

        success_count = 0
        failed_apps = []

        for app_name, package_name in self.all_apps.items():
            print(f"\n🔧 {app_name} 준비 중...")

            # 1. 패키지명 변경
            if self.update_package_name(app_name, package_name):
                # 2. APK 빌드
                if self.build_apk(app_name):
                    success_count += 1
                    print(f"  ✅ {app_name} 준비 완료!")
                else:
                    failed_apps.append(app_name)
                    print(f"  ❌ {app_name} 빌드 실패")
            else:
                failed_apps.append(app_name)
                print(f"  ❌ {app_name} 패키지명 변경 실패")

        # 3. 체크리스트 생성
        checklist = self.create_upload_checklist()

        # 4. 결과 요약
        self.print_preparation_summary(success_count, failed_apps)

        return {
            "성공": success_count,
            "실패": failed_apps,
            "체크리스트": checklist
        }

    def print_preparation_summary(self, success_count, failed_apps):
        """준비 결과 요약"""
        print("\n" + "="*60)
        print("📊 업로드 준비 결과")
        print("="*60)

        print(f"\n✅ 성공: {success_count}개 앱")
        print(f"❌ 실패: {len(failed_apps)}개 앱")

        if failed_apps:
            print(f"\n실패한 앱들:")
            for app in failed_apps:
                print(f"   • {app}")

        print(f"\n📦 빌드된 APK 위치: build_outputs/ 폴더")
        print(f"📋 업로드 체크리스트: upload_checklist.json")

        print(f"\n🚀 다음 단계:")
        print("1. Google Play Console에서 각 앱별로 새 애플리케이션 생성")
        print("2. 앱 아이콘, 스크린샷, 설명 등 Store Listing 준비")
        print("3. build_outputs/ 폴더의 APK 파일들을 각각 업로드")
        print("4. 내부 테스트 → 비공개 테스트 → 프로덕션 순으로 출시")

        print(f"\n💡 업로드 성과 예상:")
        print("• Flutter Apps가 Generated Apps보다 높은 다운로드 예상")
        print("• 일관된 패키지명(com.reaf.XXX)으로 브랜딩 효과")
        print("• 자동 모니터링으로 성과 비교 가능")

if __name__ == "__main__":
    prep = BatchUploadPreparation()
    prep.run_batch_preparation()