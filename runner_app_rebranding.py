#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
러닝 앱 리브랜딩 시스템
기가차드 러너 → 더 매력적인 이름으로 변경
"""

import os
import json
from pathlib import Path

class RunnerAppRebranding:
    def __init__(self):
        self.current_name = "GigaChad Runner"
        self.current_folder = "gigachad_runner"
        self.current_package = "com.reaf.gigachad_runner"

        # 새 이름 후보들
        self.name_candidates = {
            "RunMaster": {
                "full_name": "RunMaster - GPS 런닝 트래커",
                "package": "com.reaf.runmaster",
                "description": "간단하고 강력한 런닝 마스터",
                "keywords": ["런닝", "GPS", "마스터", "트래커"],
                "appeal": "Mission100과 같은 'Master' 시리즈 브랜딩"
            },
            "RunGoal": {
                "full_name": "RunGoal - 목표달성 런닝 앱",
                "package": "com.reaf.rungoal",
                "description": "목표를 달성하는 런닝 앱",
                "keywords": ["런닝", "목표", "달성", "챌린지"],
                "appeal": "Mission100과 유사한 목표 달성 컨셉"
            },
            "RunChallenge": {
                "full_name": "RunChallenge - 30일 런닝 챌린지",
                "package": "com.reaf.runchallenge",
                "description": "30일 런닝 챌린지 앱",
                "keywords": ["런닝", "챌린지", "30일", "습관"],
                "appeal": "Mission100의 챌린지 컨셉과 일치"
            },
            "Run100": {
                "full_name": "Run100 - 100일 런닝 마스터",
                "package": "com.reaf.run100",
                "description": "100일 런닝 마스터 챌린지",
                "keywords": ["런닝", "100일", "마스터", "챌린지"],
                "appeal": "Mission100과 완벽한 시리즈 매치"
            },
            "RunDaily": {
                "full_name": "RunDaily - 매일 런닝 습관",
                "package": "com.reaf.rundaily",
                "description": "매일 런닝하는 습관 만들기",
                "keywords": ["런닝", "매일", "습관", "일상"],
                "appeal": "일상적이고 친근한 이미지"
            }
        }

    def analyze_name_options(self):
        """이름 옵션 분석"""
        print("🎯 러닝 앱 새 이름 후보 분석")
        print("="*60)

        analysis = {
            "현재_이름": self.current_name,
            "문제점": [
                "기가차드 밈이 일반 사용자에게 이상함",
                "브랜딩이 Mission100과 다른 방향",
                "앱스토어에서 검색하기 어려움",
                "전문적이지 않은 이미지"
            ],
            "새_이름_후보": self.name_candidates,
            "추천_이름": "Run100"
        }

        for name, info in self.name_candidates.items():
            print(f"\n🏃 {name}")
            print(f"   전체명: {info['full_name']}")
            print(f"   패키지: {info['package']}")
            print(f"   어필포인트: {info['appeal']}")
            print(f"   키워드: {', '.join(info['keywords'])}")

        return analysis

    def recommend_best_name(self):
        """최적 이름 추천"""
        print("\n🏆 최종 추천: Run100")
        print("="*40)

        reasons = [
            "Mission100과 완벽한 시리즈 매치 (100 브랜드)",
            "직관적이고 기억하기 쉬움",
            "앱스토어 검색 최적화",
            "전문적이면서도 친근한 이미지",
            "확장성 좋음 (Workout100, Fitness100 등)"
        ]

        for i, reason in enumerate(reasons, 1):
            print(f"{i}. {reason}")

        return "Run100"

    def create_rebranding_plan(self, new_name):
        """리브랜딩 계획 생성"""
        if new_name not in self.name_candidates:
            print(f"❌ {new_name}은 후보에 없습니다.")
            return None

        new_info = self.name_candidates[new_name]

        plan = {
            "리브랜딩_정보": {
                "이전_이름": self.current_name,
                "새_이름": new_info["full_name"],
                "이전_패키지": self.current_package,
                "새_패키지": new_info["package"],
                "이전_폴더": self.current_folder,
                "새_폴더": new_name.lower()
            },
            "변경_작업": [
                "폴더명 변경",
                "pubspec.yaml 앱 이름 변경",
                "Android 패키지명 변경",
                "앱 아이콘 및 브랜딩 자료 업데이트",
                "마케팅 문구 및 설명 변경"
            ],
            "파일_변경_목록": {
                "pubspec.yaml": "name 및 description 변경",
                "android/app/build.gradle.kts": "namespace 및 applicationId 변경",
                "README.md": "앱 이름 및 설명 변경",
                "마케팅 자료": "새 브랜딩으로 업데이트"
            },
            "브랜딩_전략": {
                "시리즈_통일": "Mission100 → Run100 → Squat100 시리즈",
                "목표_설정": "100일 챌린지 컨셉 통일",
                "사용자_경험": "일관된 UI/UX 디자인",
                "마케팅": "숫자 기반 목표 달성 브랜드"
            }
        }

        return plan

    def update_app_files(self, new_name):
        """앱 파일들 업데이트"""
        if new_name not in self.name_candidates:
            return False

        new_info = self.name_candidates[new_name]
        app_path = Path(f"flutter_apps/{self.current_folder}")

        if not app_path.exists():
            print(f"❌ {app_path} 폴더가 존재하지 않습니다.")
            return False

        print(f"🔧 {new_name} 리브랜딩 작업 시작...")

        # 1. pubspec.yaml 업데이트
        self.update_pubspec(app_path, new_info)

        # 2. Android 설정 업데이트
        self.update_android_config(app_path, new_info)

        # 3. README 업데이트
        self.update_readme(app_path, new_info)

        print(f"✅ {new_name} 리브랜딩 완료!")
        return True

    def update_pubspec(self, app_path, new_info):
        """pubspec.yaml 업데이트"""
        pubspec_path = app_path / "pubspec.yaml"

        if not pubspec_path.exists():
            print("❌ pubspec.yaml 파일이 없습니다.")
            return

        try:
            with open(pubspec_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(pubspec_path, "r", encoding="cp949") as f:
                content = f.read()

        lines = content.split('\n')

        for i, line in enumerate(lines):
            if line.startswith('name:'):
                lines[i] = f'name: {new_info["package"].split(".")[-1]}'
            elif line.startswith('description:'):
                lines[i] = f'description: "{new_info["description"]}"'

        with open(pubspec_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(lines))

        print("  ✅ pubspec.yaml 업데이트 완료")

    def update_android_config(self, app_path, new_info):
        """Android 설정 업데이트"""
        build_gradle = app_path / "android" / "app" / "build.gradle.kts"

        if not build_gradle.exists():
            print("❌ build.gradle.kts 파일이 없습니다.")
            return

        try:
            with open(build_gradle, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(build_gradle, "r", encoding="cp949") as f:
                content = f.read()

        # namespace 및 applicationId 변경
        content = content.replace(
            f'namespace = "{self.current_package}"',
            f'namespace = "{new_info["package"]}"'
        )
        content = content.replace(
            f'applicationId = "{self.current_package}"',
            f'applicationId = "{new_info["package"]}"'
        )

        with open(build_gradle, "w", encoding="utf-8") as f:
            f.write(content)

        print("  ✅ Android 설정 업데이트 완료")

    def update_readme(self, app_path, new_info):
        """README 업데이트"""
        readme_path = app_path / "README.md"

        if readme_path.exists():
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(readme_path, "r", encoding="cp949") as f:
                    content = f.read()

            # 제목과 설명 변경
            content = content.replace(self.current_name, new_info["full_name"])
            content = content.replace("GigaChad", new_info["package"].split(".")[-1].capitalize())

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)

            print("  ✅ README.md 업데이트 완료")

    def run_rebranding_analysis(self):
        """리브랜딩 분석 실행"""
        print("🚀 러닝 앱 리브랜딩 분석 시작!")
        print("="*50)

        # 1. 이름 옵션 분석
        analysis = self.analyze_name_options()

        # 2. 최적 이름 추천
        recommended_name = self.recommend_best_name()

        # 3. 리브랜딩 계획 생성
        plan = self.create_rebranding_plan(recommended_name)

        # 4. 결과 저장
        result = {
            "분석_결과": analysis,
            "추천_이름": recommended_name,
            "리브랜딩_계획": plan
        }

        with open("runner_rebranding_analysis.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 5. 요약 출력
        self.print_rebranding_summary(result)

        return result

    def print_rebranding_summary(self, result):
        """리브랜딩 요약 출력"""
        print("\n📊 리브랜딩 분석 결과")
        print("="*50)

        print(f"현재 이름: {result['분석_결과']['현재_이름']}")
        print(f"추천 이름: {result['추천_이름']}")

        plan = result['리브랜딩_계획']
        print(f"\n새 앱 정보:")
        print(f"   • 전체명: {plan['리브랜딩_정보']['새_이름']}")
        print(f"   • 패키지: {plan['리브랜딩_정보']['새_패키지']}")
        print(f"   • 폴더: {plan['리브랜딩_정보']['새_폴더']}")

        print(f"\n브랜딩 전략:")
        strategy = plan['브랜딩_전략']
        for key, value in strategy.items():
            print(f"   • {key.replace('_', ' ')}: {value}")

        print(f"\n📁 분석 결과 저장: runner_rebranding_analysis.json")

        print(f"\n💡 다음 단계:")
        print(f"1. Run100으로 리브랜딩 승인 여부 결정")
        print(f"2. 승인 시 앱 파일 자동 업데이트 실행")
        print(f"3. Squat Master도 Squat100으로 변경 검토")

if __name__ == "__main__":
    rebranding = RunnerAppRebranding()
    rebranding.run_rebranding_analysis()