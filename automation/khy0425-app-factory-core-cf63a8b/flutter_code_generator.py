#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter 코드 자동 생성 및 프로젝트 빌드 시스템
AI가 생성한 기획서를 실제 Flutter 프로젝트로 변환
"""

import asyncio
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class FlutterCodeGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.flutter_apps_dir = Path("flutter_apps")
        self.flutter_apps_dir.mkdir(exist_ok=True)

    async def extract_flutter_code_from_plan(self, project_dir: Path):
        """기획서에서 Flutter 코드 추출 및 정리"""

        # Flutter 코드 파일 읽기
        flutter_code_file = project_dir / "03_flutter_code.md"
        if not flutter_code_file.exists():
            raise FileNotFoundError(f"Flutter 코드 파일이 없습니다: {flutter_code_file}")

        with open(flutter_code_file, "r", encoding="utf-8") as f:
            content = f.read()

        # pubspec.yaml 추출
        pubspec_match = re.search(r'```yaml\s*\n(.*?)\n```', content, re.DOTALL)
        pubspec_content = pubspec_match.group(1) if pubspec_match else None

        # main.dart 추출
        dart_match = re.search(r'```dart\s*\n(.*?)\n```', content, re.DOTALL)
        dart_content = dart_match.group(1) if dart_match else None

        return pubspec_content, dart_content

    async def create_flutter_project(self, app_name: str, project_dir: Path):
        """Flutter 프로젝트 생성"""

        # 안전한 프로젝트 이름 생성
        safe_name = re.sub(r'[^a-z0-9_]', '_', app_name.lower())
        safe_name = re.sub(r'_+', '_', safe_name).strip('_')

        if not safe_name or len(safe_name) < 3:
            safe_name = f"mvp_app_{int(time.time())}"

        flutter_project_dir = self.flutter_apps_dir / safe_name

        # 기존 프로젝트가 있으면 삭제
        if flutter_project_dir.exists():
            shutil.rmtree(flutter_project_dir)

        # Flutter 프로젝트 생성
        cmd = [
            "flutter", "create",
            "--project-name", safe_name,
            "--org", "com.reaf",
            str(flutter_project_dir)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.flutter_apps_dir)

        if result.returncode != 0:
            raise RuntimeError(f"Flutter 프로젝트 생성 실패: {result.stderr}")

        return flutter_project_dir, safe_name

    async def apply_generated_code(self, flutter_project_dir: Path, pubspec_content: str, dart_content: str):
        """생성된 코드를 Flutter 프로젝트에 적용"""

        # pubspec.yaml 업데이트
        if pubspec_content:
            pubspec_file = flutter_project_dir / "pubspec.yaml"

            # 기존 pubspec.yaml 읽기
            with open(pubspec_file, "r", encoding="utf-8") as f:
                original_pubspec = f.read()

            # AI가 생성한 dependencies만 추출하여 병합
            await self.merge_pubspec(pubspec_file, pubspec_content)

        # main.dart 업데이트
        if dart_content:
            main_dart_file = flutter_project_dir / "lib" / "main.dart"
            with open(main_dart_file, "w", encoding="utf-8") as f:
                f.write(dart_content)

        # AdMob 기본 설정 추가
        await self.add_basic_admob_config(flutter_project_dir)

    async def merge_pubspec(self, pubspec_file: Path, ai_pubspec_content: str):
        """AI 생성 dependencies를 기존 pubspec.yaml에 병합"""

        # 기존 pubspec.yaml 읽기
        with open(pubspec_file, "r", encoding="utf-8") as f:
            original_content = f.read()

        # AI가 생성한 dependencies 추출
        ai_deps = self.extract_dependencies(ai_pubspec_content)

        # 기본 dependencies에 추가
        basic_deps = """
  cupertino_icons: ^1.0.8
  provider: ^6.1.2
  shared_preferences: ^2.2.3
  google_mobile_ads: ^5.1.0
"""

        # dependencies 섹션 찾아서 업데이트
        updated_content = re.sub(
            r'(dependencies:\s*\n)(.*?)(\n\ndev_dependencies:)',
            lambda m: f"{m.group(1)}  flutter:\n    sdk: flutter{basic_deps}{ai_deps}{m.group(3)}",
            original_content,
            flags=re.DOTALL
        )

        with open(pubspec_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

    def extract_dependencies(self, pubspec_content: str):
        """pubspec 내용에서 dependencies만 추출"""

        # dependencies 섹션 추출
        deps_match = re.search(r'dependencies:\s*\n(.*?)(?=\n\S|\Z)', pubspec_content, re.DOTALL)
        if not deps_match:
            return ""

        deps_lines = deps_match.group(1).split('\n')
        ai_deps = []

        for line in deps_lines:
            line = line.strip()
            if line and not line.startswith('flutter:') and not line.startswith('cupertino_icons:'):
                if not line.startswith(' '):
                    ai_deps.append(f"  {line}")
                else:
                    ai_deps.append(line)

        return '\n' + '\n'.join(ai_deps) if ai_deps else ""

    async def add_basic_admob_config(self, flutter_project_dir: Path):
        """기본 AdMob 설정 추가"""

        # Android manifest 업데이트
        manifest_file = flutter_project_dir / "android" / "app" / "src" / "main" / "AndroidManifest.xml"

        if manifest_file.exists():
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest_content = f.read()

            # AdMob App ID 추가 (테스트용)
            admob_meta = '''
        <!-- Google AdMob App ID (테스트용) -->
        <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID"
                   android:value="ca-app-pub-3940256099942544~3347511713"/>'''

            if "com.google.android.gms.ads.APPLICATION_ID" not in manifest_content:
                manifest_content = manifest_content.replace(
                    '</application>',
                    f'{admob_meta}\n    </application>'
                )

                with open(manifest_file, "w", encoding="utf-8") as f:
                    f.write(manifest_content)

    async def build_apk(self, flutter_project_dir: Path):
        """Flutter APK 빌드"""

        print(f"🔨 APK 빌드 시작: {flutter_project_dir.name}")

        # flutter pub get 실행
        pub_get_cmd = ["flutter", "pub", "get"]
        result = subprocess.run(pub_get_cmd, capture_output=True, text=True, cwd=flutter_project_dir)

        if result.returncode != 0:
            raise RuntimeError(f"pub get 실패: {result.stderr}")

        # flutter build apk 실행
        build_cmd = ["flutter", "build", "apk", "--release"]
        result = subprocess.run(build_cmd, capture_output=True, text=True, cwd=flutter_project_dir)

        if result.returncode != 0:
            # 빌드 실패시 더 자세한 정보 제공
            print(f"❌ APK 빌드 실패: {flutter_project_dir.name}")
            print(f"Error: {result.stderr}")
            return None

        # APK 파일 경로 확인
        apk_path = flutter_project_dir / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk"

        if apk_path.exists():
            apk_size = apk_path.stat().st_size / 1024 / 1024  # MB
            print(f"✅ APK 빌드 완료: {flutter_project_dir.name} ({apk_size:.1f}MB)")
            return apk_path
        else:
            print(f"❌ APK 파일을 찾을 수 없음: {flutter_project_dir.name}")
            return None

    async def process_project(self, project_dir: Path):
        """단일 프로젝트를 Flutter 앱으로 변환"""

        try:
            print(f"\n🔄 프로젝트 처리 중: {project_dir.name}")

            # 1. Flutter 코드 추출
            pubspec_content, dart_content = await self.extract_flutter_code_from_plan(project_dir)

            if not dart_content:
                print(f"❌ Flutter 코드가 없습니다: {project_dir.name}")
                return None

            # 2. Flutter 프로젝트 생성
            flutter_project_dir, safe_name = await self.create_flutter_project(project_dir.name, project_dir)

            # 3. 생성된 코드 적용
            await self.apply_generated_code(flutter_project_dir, pubspec_content, dart_content)

            # 4. APK 빌드
            apk_path = await self.build_apk(flutter_project_dir)

            return {
                "project_name": project_dir.name,
                "flutter_project_dir": str(flutter_project_dir),
                "apk_path": str(apk_path) if apk_path else None,
                "status": "success" if apk_path else "build_failed"
            }

        except Exception as e:
            print(f"❌ 프로젝트 처리 실패: {project_dir.name} - {e}")
            return {
                "project_name": project_dir.name,
                "flutter_project_dir": None,
                "apk_path": None,
                "status": "failed",
                "error": str(e)
            }

    async def process_all_generated_projects(self):
        """모든 생성된 프로젝트를 Flutter 앱으로 변환"""

        generated_projects_dir = Path("generated_projects")

        if not generated_projects_dir.exists():
            print("❌ generated_projects 폴더가 없습니다.")
            return

        # 모든 프로젝트 폴더 찾기
        project_dirs = [d for d in generated_projects_dir.iterdir()
                       if d.is_dir() and d.name != "__pycache__"]

        if not project_dirs:
            print("❌ 처리할 프로젝트가 없습니다.")
            return

        print(f"🚀 총 {len(project_dirs)}개 프로젝트를 Flutter 앱으로 변환합니다.")

        results = []

        for project_dir in project_dirs:
            result = await self.process_project(project_dir)
            if result:
                results.append(result)

        # 결과 요약 저장
        await self.save_build_summary(results)

        return results

    async def save_build_summary(self, results):
        """빌드 결과 요약 저장"""

        summary = {
            "build_date": "2025-09-21",
            "total_projects": len(results),
            "successful_builds": len([r for r in results if r["status"] == "success"]),
            "failed_builds": len([r for r in results if r["status"] in ["failed", "build_failed"]]),
            "results": results
        }

        with open("build_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"\n📊 빌드 요약:")
        print(f"✅ 성공: {summary['successful_builds']}개")
        print(f"❌ 실패: {summary['failed_builds']}개")
        print(f"📁 요약 파일: build_summary.json")

async def main():
    """메인 실행 함수"""
    print("🤖 Flutter 코드 생성 및 APK 빌드 시스템")
    print("=" * 60)

    generator = FlutterCodeGenerator()
    await generator.process_all_generated_projects()

    print("\n🎉 모든 프로젝트 처리가 완료되었습니다!")

if __name__ == "__main__":
    import time
    asyncio.run(main())