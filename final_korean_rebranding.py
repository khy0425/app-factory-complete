#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 한국 시장 맞춤 리브랜딩 실행
스쿼트PT (SquatPT) & 런스타트 (RunStart)
"""

import os
import json
from pathlib import Path
from datetime import datetime

class FinalKoreanRebranding:
    def __init__(self):
        self.apps_to_rebrand = {
            "squat": {
                "current_folder": "squat_master",
                "new_name": "squatpt",
                "display_name": "스쿼트PT",
                "full_name": "스쿼트PT - AI 개인 트레이너",
                "package": "com.reaf.squatpt",
                "description": "헬스장 PT 안 받아도 완벽한 스쿼트 마스터",
                "keywords": ["스쿼트", "PT", "개인트레이너", "하체운동", "홈트레이닝"]
            },
            "runner": {
                "current_folder": "gigachad_runner",
                "new_name": "runstart",
                "display_name": "런스타트",
                "full_name": "런스타트 - 12주 런닝 시작 프로그램",
                "package": "com.reaf.runstart",
                "description": "러닝 한번도 못해본 사람도 12주면 러너",
                "keywords": ["런닝", "러닝시작", "초보러닝", "12주프로그램", "달리기"]
            }
        }

    def update_squat_to_squatpt(self):
        """Squat Master → 스쿼트PT 리브랜딩"""
        print("🏋️ 스쿼트PT 리브랜딩 시작...")

        app_info = self.apps_to_rebrand["squat"]
        app_path = Path(f"flutter_apps/{app_info['current_folder']}")

        if not app_path.exists():
            print(f"❌ {app_path} 폴더가 없습니다.")
            return False

        # 1. pubspec.yaml 업데이트
        pubspec_path = app_path / "pubspec.yaml"
        if pubspec_path.exists():
            self.update_pubspec(pubspec_path, app_info)
            print("  ✅ pubspec.yaml 업데이트 완료")

        # 2. Android 설정 업데이트
        build_gradle = app_path / "android" / "app" / "build.gradle.kts"
        if build_gradle.exists():
            self.update_android_config(build_gradle, app_info)
            print("  ✅ Android 설정 업데이트 완료")

        # 3. 앱 설명 파일 생성
        self.create_app_description(app_path, app_info)
        print("  ✅ 앱 설명 파일 생성 완료")

        return True

    def update_runner_to_runstart(self):
        """GigaChad Runner → 런스타트 리브랜딩"""
        print("🏃 런스타트 리브랜딩 시작...")

        app_info = self.apps_to_rebrand["runner"]
        app_path = Path(f"flutter_apps/{app_info['current_folder']}")

        if not app_path.exists():
            print(f"❌ {app_path} 폴더가 없습니다.")
            return False

        # 1. pubspec.yaml 업데이트
        pubspec_path = app_path / "pubspec.yaml"
        if pubspec_path.exists():
            self.update_pubspec(pubspec_path, app_info)
            print("  ✅ pubspec.yaml 업데이트 완료")

        # 2. Android 설정 업데이트
        build_gradle = app_path / "android" / "app" / "build.gradle.kts"
        if build_gradle.exists():
            self.update_android_config(build_gradle, app_info)
            print("  ✅ Android 설정 업데이트 완료")

        # 3. 앱 설명 파일 생성
        self.create_app_description(app_path, app_info)
        print("  ✅ 앱 설명 파일 생성 완료")

        return True

    def update_pubspec(self, pubspec_path, app_info):
        """pubspec.yaml 파일 업데이트"""
        try:
            with open(pubspec_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(pubspec_path, "r", encoding="cp949") as f:
                content = f.read()

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('name:'):
                lines[i] = f'name: {app_info["new_name"]}'
            elif line.startswith('description:'):
                lines[i] = f'description: "{app_info["description"]}"'

        with open(pubspec_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))

    def update_android_config(self, build_gradle, app_info):
        """Android build.gradle.kts 업데이트"""
        try:
            with open(build_gradle, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(build_gradle, "r", encoding="cp949") as f:
                content = f.read()

        # namespace와 applicationId 변경
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'namespace = ' in line:
                lines[i] = f'    namespace = "{app_info["package"]}"'
            elif 'applicationId = ' in line:
                lines[i] = f'        applicationId = "{app_info["package"]}"'

        with open(build_gradle, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))

    def create_app_description(self, app_path, app_info):
        """앱 스토어 설명 파일 생성"""
        store_desc = f"""# {app_info['display_name']} - {app_info['full_name']}

## 한 줄 설명
{app_info['description']}

## 스토어 설명 (한글)
{'스쿼트PT와 함께라면 누구나 완벽한 스쿼트 마스터가 될 수 있습니다!' if '스쿼트' in app_info['display_name'] else '런스타트와 함께 12주만 투자하면 진짜 러너가 됩니다!'}

### 주요 기능
{'• 2023년 Scientific Reports 연구 기반 4단계 프로그램' if '스쿼트' in app_info['display_name'] else '• None to Run (N2R) 12주 과학적 프로그램'}
{'• Assisted → Bodyweight → Bulgarian → Pistol 단계별 진화' if '스쿼트' in app_info['display_name'] else '• 부상 방지를 위한 체계적 시간 기반 인터벌'}
{'• 10단계 차드 레벨 시스템으로 동기부여' if '스쿼트' in app_info['display_name'] else '• 매일 5분부터 시작하는 점진적 프로그램'}
{'• Progressive Overload 원칙으로 안전한 발전' if '스쿼트' in app_info['display_name'] else '• 강화 운동 포함된 종합 프로그램'}

### 이런 분들께 추천
{'• PT비가 부담스러운 분' if '스쿼트' in app_info['display_name'] else '• 러닝을 시작하고 싶지만 어떻게 해야 할지 모르는 분'}
{'• 정확한 스쿼트 자세를 배우고 싶은 분' if '스쿼트' in app_info['display_name'] else '• 작심삼일로 끝났던 분'}
{'• 무릎 부상 없이 하체 운동하고 싶은 분' if '스쿼트' in app_info['display_name'] else '• 무릎 부상이 걱정되는 분'}
{'• 체계적으로 운동하고 싶은 분' if '스쿼트' in app_info['display_name'] else '• 12주 후 5km 완주를 목표로 하는 분'}

### 과학적 근거
{'2023년 Scientific Reports 발표 연구 기반' if '스쿼트' in app_info['display_name'] else 'None to Run - C25K의 과학적 개선 프로그램'}

## 키워드
{', '.join(app_info['keywords'])}

## 패키지명
{app_info['package']}
"""

        store_file = app_path / "STORE_DESCRIPTION.md"
        with open(store_file, "w", encoding="utf-8") as f:
            f.write(store_desc)

    def create_final_series_summary(self):
        """최종 시리즈 요약 생성"""
        series = {
            "series_name": "K-Fitness 마스터 시리즈",
            "launch_date": datetime.now().isoformat(),
            "apps": {
                "Mission100": {
                    "status": "✅ 플레이스토어 출시 완료",
                    "package": "com.reaf.mission100",
                    "target": "푸쉬업 100개 달성",
                    "marketing": "6주 만에 푸쉬업 100개"
                },
                "스쿼트PT": {
                    "status": "🔄 리브랜딩 완료",
                    "package": "com.reaf.squatpt",
                    "target": "완벽한 스쿼트 마스터",
                    "marketing": "헬스장 PT 안 받아도 완벽한 스쿼트"
                },
                "런스타트": {
                    "status": "🔄 리브랜딩 완료",
                    "package": "com.reaf.runstart",
                    "target": "12주 런닝 마스터",
                    "marketing": "러닝 못해본 사람도 12주면 러너"
                }
            },
            "marketing_strategy": {
                "공통_메시지": "과학적 연구 기반 + 무료 + 체계적 프로그램",
                "타겟": "2030 운동 입문자 및 홈트족",
                "차별화": "PT/코칭 비용 절감 + 과학적 검증"
            }
        }

        return series

    def run_final_rebranding(self):
        """최종 리브랜딩 실행"""
        print("🚀 한국 시장 맞춤 최종 리브랜딩 시작!")
        print("="*60)

        results = {
            "timestamp": datetime.now().isoformat(),
            "rebranding_results": {}
        }

        # 1. 스쿼트PT 리브랜딩
        squat_success = self.update_squat_to_squatpt()
        results["rebranding_results"]["스쿼트PT"] = "✅ 성공" if squat_success else "❌ 실패"

        # 2. 런스타트 리브랜딩
        runner_success = self.update_runner_to_runstart()
        results["rebranding_results"]["런스타트"] = "✅ 성공" if runner_success else "❌ 실패"

        # 3. 시리즈 요약
        series_summary = self.create_final_series_summary()
        results["series_summary"] = series_summary

        # 4. 결과 저장
        with open("final_rebranding_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # 5. 최종 요약 출력
        self.print_final_results(results)

        return results

    def print_final_results(self, results):
        """최종 결과 출력"""
        print("\n" + "="*60)
        print("✅ 한국 시장 맞춤 리브랜딩 완료!")
        print("="*60)

        print("\n📱 최종 앱 시리즈:")
        series = results["series_summary"]["apps"]
        for app_name, info in series.items():
            print(f"  • {app_name}: {info['status']}")
            print(f"    - {info['marketing']}")
            print(f"    - {info['package']}")

        print("\n🎯 마케팅 전략:")
        strategy = results["series_summary"]["marketing_strategy"]
        print(f"  • 타겟: {strategy['타겟']}")
        print(f"  • 차별화: {strategy['차별화']}")

        print("\n📁 생성된 파일:")
        print("  • 각 앱 폴더에 STORE_DESCRIPTION.md")
        print("  • final_rebranding_results.json")

        print("\n🚀 다음 단계:")
        print("  1. 각 앱 APK 빌드 (flutter build apk --release)")
        print("  2. Google Play Console에서 앱 등록")
        print("  3. 한국어 스토어 설명 및 스크린샷 업로드")
        print("  4. Mission100 성과 기반 교차 마케팅")

        print("\n💡 예상 효과:")
        print("  • PT비 절감 메시지로 2030 직장인 어필")
        print("  • 초보자 친화적 이름으로 진입장벽 제거")
        print("  • Mission100 성공 → 시리즈 전체 성장")

if __name__ == "__main__":
    rebranding = FinalKoreanRebranding()
    rebranding.run_final_rebranding()