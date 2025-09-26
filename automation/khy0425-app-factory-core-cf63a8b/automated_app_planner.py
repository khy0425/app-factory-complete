#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 자동 앱 기획 시스템
사용자는 간단한 아이디어만 제공하면 완전한 앱 기획서를 자동 생성
"""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class AutomatedAppPlanner:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def create_full_app_plan(self, simple_idea: str):
        """간단한 아이디어를 완전한 앱 기획서로 확장"""

        planning_prompt = f"""
당신은 전문 앱 기획자입니다. 다음 간단한 아이디어를 완전한 앱 기획서로 확장해주세요:

아이디어: "{simple_idea}"

다음 형식으로 상세한 기획서를 작성해주세요:

## 앱 기본 정보
- 앱 이름: (창의적이고 기억하기 쉬운 이름)
- 한줄 설명: (앱의 핵심 가치를 한 문장으로)
- 타겟 사용자: (구체적인 사용자 페르소나)
- 카테고리: (앱스토어 카테고리)

## 핵심 기능 (MVP)
1. [기능 1]: (구체적인 설명)
2. [기능 2]: (구체적인 설명)
3. [기능 3]: (구체적인 설명)

## UI/UX 디자인 방향
- 컬러 테마: (hex 코드 포함)
- 디자인 스타일: (모던, 미니멀, 게임틱 등)
- 핵심 화면들: (홈, 메인 기능, 설정 등)

## 기술적 구현 방안
- 필요한 권한: (GPS, 카메라, 알림 등)
- 외부 API: (필요한 경우)
- 데이터 저장 방식: (로컬 DB, 클라우드 등)
- 특별한 기술: (진동, 센서 등)

## 수익화 방안
- 비즈니스 모델: (무료, 프리미엄, 광고 등)
- 프리미엄 기능: (유료 기능들)

## 마케팅 포인트
- 차별화 요소: (경쟁앱과의 차이점)
- 바이럴 요소: (공유하고 싶어지는 기능)
- ASO 키워드: (앱스토어 최적화용)

## 개발 우선순위
1단계: (필수 기능들)
2단계: (추가 기능들)
3단계: (고급 기능들)

## 예상 개발 기간
- MVP: X주
- 정식 출시: X주
- 업데이트 주기: X주

모든 기능은 실제 구현 가능하고 안전해야 합니다.
창의적이면서도 현실적인 제안을 해주세요.
한국 시장에 적합한 내용으로 작성해주세요.
"""

        try:
            response = await self.model.generate_content_async(planning_prompt)
            return response.text
        except Exception as e:
            return f"기획서 생성 실패: {e}"

    async def create_technical_specs(self, app_plan: str):
        """앱 기획서를 기술 명세서로 변환"""

        tech_prompt = f"""
다음 앱 기획서를 바탕으로 Flutter 개발을 위한 상세한 기술 명세서를 작성해주세요:

{app_plan}

다음 형식으로 기술 명세서를 작성해주세요:

## Flutter 프로젝트 구조
- 패키지명: com.reaf.[앱이름]
- 필요한 dependencies: (pubspec.yaml용)
- 폴더 구조: (lib 폴더 내부)

## 화면별 구현 상세
각 화면마다:
- 위젯 구조
- 상태 관리 방식
- 필요한 패키지들

## 데이터 모델
- 필요한 클래스들
- 데이터베이스 스키마 (sqflite용)
- API 연동 방식

## 권한 및 설정
- android/app/src/main/AndroidManifest.xml 설정
- iOS 권한 설정 (필요시)

## 핵심 기능 구현 방법
각 주요 기능별로:
- 사용할 Flutter 패키지
- 구현 난이도 (1-5점)
- 예상 개발 시간

## 테스트 계획
- 단위 테스트 대상
- 통합 테스트 시나리오
- 사용자 테스트 계획

실제 구현 가능한 기술 스택만 사용해주세요.
성능과 배터리 최적화를 고려해주세요.
"""

        try:
            response = await self.model.generate_content_async(tech_prompt)
            return response.text
        except Exception as e:
            return f"기술 명세서 생성 실패: {e}"

    async def create_flutter_code_structure(self, tech_specs: str):
        """기술 명세서를 바탕으로 Flutter 코드 구조 생성"""

        code_prompt = f"""
다음 기술 명세서를 바탕으로 Flutter 앱의 main.dart 파일을 생성해주세요:

{tech_specs}

요구사항:
1. 완전히 작동하는 Flutter 코드
2. Material Design 3 사용
3. Provider 패턴으로 상태 관리
4. 모든 화면과 기본 기능 포함
5. 한국어 UI
6. 다크 테마 적용
7. 주석 포함

pubspec.yaml에 필요한 dependencies도 함께 제공해주세요.

코드는 다음 형식으로:
```yaml
# pubspec.yaml
[dependencies 내용]
```

```dart
// main.dart
[Flutter 코드]
```
"""

        try:
            response = await self.model.generate_content_async(code_prompt)
            return response.text
        except Exception as e:
            return f"코드 생성 실패: {e}"

    async def generate_marketing_assets(self, app_plan: str):
        """앱 기획서를 바탕으로 마케팅 에셋 기획"""

        marketing_prompt = f"""
다음 앱 기획서를 바탕으로 Play Store용 마케팅 에셋을 기획해주세요:

{app_plan}

다음 내용을 포함해주세요:

## Feature Graphic (1024x500)
- 이미지 컨셉 설명
- 포함할 텍스트
- 색상 팔레트
- 디자인 스타일

## 앱 아이콘 (512x512)
- 아이콘 컨셉
- 심볼/로고 아이디어
- 색상 조합

## 스크린샷 (1080x1920) - 5개
각 스크린샷별로:
- 화면명
- 강조할 기능
- 오버레이 텍스트

## 앱 설명문
- 짧은 설명 (80자 이내)
- 긴 설명 (4000자 이내)
- 주요 키워드
- 특징 요약

## ASO 최적화
- 제목 키워드
- 태그 키워드
- 경쟁 앱 분석

모든 내용은 한국어로 작성해주세요.
Play Store 정책을 준수해주세요.
"""

        try:
            response = await self.model.generate_content_async(marketing_prompt)
            return response.text
        except Exception as e:
            return f"마케팅 에셋 기획 실패: {e}"

    async def save_complete_project(self, idea: str, app_plan: str, tech_specs: str,
                                   flutter_code: str, marketing_assets: str):
        """완성된 프로젝트를 파일로 저장"""

        # 앱 이름 추출 (기획서에서)
        app_name = "new_app"  # 기본값
        if "앱 이름:" in app_plan:
            try:
                app_name = app_plan.split("앱 이름:")[1].split("\n")[0].strip()
                # 한글과 특수문자 제거, 영문과 숫자만 남기기
                import re
                app_name = re.sub(r'[^a-zA-Z0-9]', '_', app_name).lower()
                app_name = re.sub(r'_+', '_', app_name)  # 연속된 underscore 하나로
                app_name = app_name.strip('_')  # 앞뒤 underscore 제거
                if not app_name or len(app_name) < 3:
                    app_name = "meditation_app"  # 기본값
            except:
                app_name = "meditation_app"

        project_dir = Path(f"generated_projects/{app_name}")
        project_dir.mkdir(parents=True, exist_ok=True)

        # 기획서 저장
        with open(project_dir / "01_app_plan.md", "w", encoding="utf-8") as f:
            f.write(f"# {app_name} 앱 기획서\n\n")
            f.write(f"**원본 아이디어:** {idea}\n\n")
            f.write(app_plan)

        # 기술 명세서 저장
        with open(project_dir / "02_technical_specs.md", "w", encoding="utf-8") as f:
            f.write(f"# {app_name} 기술 명세서\n\n")
            f.write(tech_specs)

        # Flutter 코드 저장
        with open(project_dir / "03_flutter_code.md", "w", encoding="utf-8") as f:
            f.write(f"# {app_name} Flutter 코드\n\n")
            f.write(flutter_code)

        # 마케팅 에셋 저장
        with open(project_dir / "04_marketing_assets.md", "w", encoding="utf-8") as f:
            f.write(f"# {app_name} 마케팅 에셋\n\n")
            f.write(marketing_assets)

        # 프로젝트 요약 저장
        summary = {
            "app_name": app_name,
            "original_idea": idea,
            "generated_date": "2025-09-21",
            "status": "planning_complete",
            "next_steps": [
                "Flutter 프로젝트 생성",
                "코드 구현",
                "Play Store 에셋 생성",
                "테스트 및 배포"
            ]
        }

        with open(project_dir / "project_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        return project_dir

async def main():
    """메인 실행 함수"""
    print("🤖 AI 자동 앱 기획 시스템")
    print("=" * 60)

    # 자동화된 아이디어들 (배치 생성용)
    auto_ideas = [
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

    # 첫 번째 아이디어로 테스트
    idea = auto_ideas[0]

    planner = AutomatedAppPlanner()

    print(f"\n🎯 아이디어: {idea}")
    print("\n📋 1단계: 앱 기획서 생성 중...")
    app_plan = await planner.create_full_app_plan(idea)

    print("🔧 2단계: 기술 명세서 생성 중...")
    tech_specs = await planner.create_technical_specs(app_plan)

    print("💻 3단계: Flutter 코드 구조 생성 중...")
    flutter_code = await planner.create_flutter_code_structure(tech_specs)

    print("🎨 4단계: 마케팅 에셋 기획 중...")
    marketing_assets = await planner.generate_marketing_assets(app_plan)

    print("💾 5단계: 프로젝트 파일 저장 중...")
    project_dir = await planner.save_complete_project(
        idea, app_plan, tech_specs, flutter_code, marketing_assets
    )

    print(f"\n✅ 완료! 프로젝트가 저장되었습니다:")
    print(f"📁 위치: {project_dir}")
    print("\n📄 생성된 파일들:")
    print("  - 01_app_plan.md (앱 기획서)")
    print("  - 02_technical_specs.md (기술 명세서)")
    print("  - 03_flutter_code.md (Flutter 코드)")
    print("  - 04_marketing_assets.md (마케팅 에셋)")
    print("  - project_summary.json (프로젝트 요약)")

    print(f"\n🚀 다음 단계:")
    print("1. generated_projects 폴더 확인")
    print("2. Flutter 프로젝트 생성 및 코드 적용")
    print("3. Play Store 에셋 이미지 생성")
    print("4. 테스트 및 배포")

if __name__ == "__main__":
    asyncio.run(main())