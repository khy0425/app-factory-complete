#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마케팅 자동화 시스템
생성된 앱들의 Play Store 최적화 및 홍보 콘텐츠 자동 생성
"""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class MarketingAutomation:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_store_listing(self, project_dir: Path):
        """Play Store 등록 최적화 콘텐츠 생성"""

        # 기획서 읽기
        plan_file = project_dir / "01_app_plan.md"
        marketing_file = project_dir / "04_marketing_assets.md"

        if not plan_file.exists():
            return None

        with open(plan_file, "r", encoding="utf-8") as f:
            app_plan = f.read()

        marketing_content = ""
        if marketing_file.exists():
            with open(marketing_file, "r", encoding="utf-8") as f:
                marketing_content = f.read()

        store_prompt = f"""
다음 앱 기획서와 마케팅 에셋을 바탕으로 Play Store 등록에 최적화된 콘텐츠를 생성해주세요:

앱 기획서:
{app_plan}

마케팅 에셋:
{marketing_content}

다음 형식으로 작성해주세요:

## Play Store 앱 제목
(30자 이내, ASO 최적화된 제목)

## 짧은 설명
(80자 이내, 핵심 기능과 이점 강조)

## 긴 설명
(4000자 이내, 다음 구조로 작성)
- 앱 소개 (2-3줄)
- 주요 기능 (3-5개 불릿 포인트)
- 사용자 혜택 (2-3줄)
- 차별화 포인트 (2-3줄)
- 사용 방법 (간단한 스텝)

## 키워드
(Play Store ASO용 키워드 10-15개)

## 카테고리
(적절한 Play Store 카테고리 추천)

## 타겟 연령
(적절한 연령 등급)

모든 내용은 한국어로 작성하되, 자연스럽고 매력적인 톤으로 작성해주세요.
Play Store 정책을 준수하고 과도한 홍보성 표현은 피해주세요.
"""

        try:
            response = await self.model.generate_content_async(store_prompt)
            return response.text
        except Exception as e:
            return f"Store listing 생성 실패: {e}"

    async def generate_social_media_content(self, project_dir: Path):
        """소셜 미디어 홍보 콘텐츠 생성"""

        # 기획서 읽기
        plan_file = project_dir / "01_app_plan.md"

        if not plan_file.exists():
            return None

        with open(plan_file, "r", encoding="utf-8") as f:
            app_plan = f.read()

        social_prompt = f"""
다음 앱 기획서를 바탕으로 소셜 미디어 홍보 콘텐츠를 생성해주세요:

{app_plan}

다음 형식으로 작성해주세요:

## 페이스북 포스트 (3개)
### 포스트 1 - 앱 소개
(300자 이내, 앱의 핵심 가치 소개)

### 포스트 2 - 기능 소개
(300자 이내, 주요 기능 하이라이트)

### 포스트 3 - 사용자 혜택
(300자 이내, 사용자가 얻을 수 있는 이점)

## 인스타그램 캡션 (3개)
### 캡션 1 - 라이프스타일
(150자 이내, 해시태그 5-10개 포함)

### 캡션 2 - 팁 & 트릭
(150자 이내, 해시태그 5-10개 포함)

### 캡션 3 - 결과 & 성과
(150자 이내, 해시태그 5-10개 포함)

## 유튜브 영상 아이디어 (3개)
### 영상 1
- 제목: (70자 이내)
- 내용 요약: (200자)
- 대상: (타겟 시청자)

### 영상 2
- 제목: (70자 이내)
- 내용 요약: (200자)
- 대상: (타겟 시청자)

### 영상 3
- 제목: (70자 이내)
- 내용 요약: (200자)
- 대상: (타겟 시청자)

## 블로그 포스트 아이디어 (2개)
### 포스트 1
- 제목: (50자 이내)
- 개요: (300자)
- 키워드: (SEO용 키워드 5개)

### 포스트 2
- 제목: (50자 이내)
- 개요: (300자)
- 키워드: (SEO용 키워드 5개)

모든 콘텐츠는 자연스럽고 친근한 톤으로 작성해주세요.
과도한 홍보성 표현은 피하고 사용자에게 도움이 되는 내용을 중심으로 해주세요.
"""

        try:
            response = await self.model.generate_content_async(social_prompt)
            return response.text
        except Exception as e:
            return f"소셜 미디어 콘텐츠 생성 실패: {e}"

    async def create_marketing_plan(self, project_dir: Path):
        """전체 마케팅 계획 생성"""

        # 기획서 읽기
        plan_file = project_dir / "01_app_plan.md"

        if not plan_file.exists():
            return None

        with open(plan_file, "r", encoding="utf-8") as f:
            app_plan = f.read()

        marketing_plan_prompt = f"""
다음 앱 기획서를 바탕으로 80% MVP 전략에 맞는 마케팅 계획을 수립해주세요:

{app_plan}

다음 형식으로 작성해주세요:

## 마케팅 전략 개요
- 목표: (출시 후 1개월, 3개월 목표)
- 타겟: (구체적인 타겟 사용자)
- 핵심 메시지: (한 줄 메시지)

## 출시 전 준비 (1주차)
- [ ] Play Store 등록 최적화
- [ ] 스크린샷 5개 제작
- [ ] 앱 아이콘 최적화
- [ ] 첫 홍보 콘텐츠 준비

## 출시 초기 (2-4주차)
- [ ] 소셜 미디어 계정 개설
- [ ] 주 3회 콘텐츠 발행
- [ ] 관련 커뮤니티 참여
- [ ] 피드백 수집 및 개선

## 성장 단계 (2-3개월)
- [ ] 사용자 리뷰 관리
- [ ] 기능 업데이트 홍보
- [ ] 인플루언서 협업
- [ ] 유료 광고 테스트

## 예산 계획 (월 10만원 기준)
- 유료 광고: 6만원 (60%)
- 콘텐츠 제작: 2만원 (20%)
- 도구 및 서비스: 2만원 (20%)

## KPI 지표
- 다운로드 수: (월 목표)
- 활성 사용자: (DAU 목표)
- 수익: (AdMob 수익 목표)
- 평점: (Play Store 평점 목표)

## 자동화 가능한 작업
- [ ] 소셜 미디어 예약 발행
- [ ] 리뷰 모니터링 알림
- [ ] 성과 리포트 자동 생성
- [ ] 경쟁 앱 분석 자동화

실행 가능하고 구체적인 계획으로 작성해주세요.
80% MVP 전략에 맞게 최소한의 노력으로 최대 효과를 낼 수 있는 방법을 중심으로 해주세요.
"""

        try:
            response = await self.model.generate_content_async(marketing_plan_prompt)
            return response.text
        except Exception as e:
            return f"마케팅 계획 생성 실패: {e}"

    async def process_project_marketing(self, project_dir: Path):
        """단일 프로젝트의 마케팅 자료 생성"""

        print(f"\n📢 마케팅 자료 생성 중: {project_dir.name}")

        try:
            # 1. Play Store 등록 최적화
            print("🏪 Play Store 등록 최적화...")
            store_listing = await self.generate_store_listing(project_dir)

            # 2. 소셜 미디어 콘텐츠
            print("📱 소셜 미디어 콘텐츠...")
            social_content = await self.generate_social_media_content(project_dir)

            # 3. 마케팅 계획
            print("📈 마케팅 계획...")
            marketing_plan = await self.create_marketing_plan(project_dir)

            # 파일 저장
            marketing_dir = project_dir / "marketing"
            marketing_dir.mkdir(exist_ok=True)

            if store_listing:
                with open(marketing_dir / "play_store_listing.md", "w", encoding="utf-8") as f:
                    f.write(f"# {project_dir.name} Play Store 등록\n\n{store_listing}")

            if social_content:
                with open(marketing_dir / "social_media_content.md", "w", encoding="utf-8") as f:
                    f.write(f"# {project_dir.name} 소셜 미디어 콘텐츠\n\n{social_content}")

            if marketing_plan:
                with open(marketing_dir / "marketing_plan.md", "w", encoding="utf-8") as f:
                    f.write(f"# {project_dir.name} 마케팅 계획\n\n{marketing_plan}")

            print(f"✅ 마케팅 자료 생성 완료: {project_dir.name}")

            return {
                "project_name": project_dir.name,
                "status": "success",
                "files_created": ["play_store_listing.md", "social_media_content.md", "marketing_plan.md"]
            }

        except Exception as e:
            print(f"❌ 마케팅 자료 생성 실패: {project_dir.name} - {e}")
            return {
                "project_name": project_dir.name,
                "status": "failed",
                "error": str(e)
            }

    async def process_all_projects(self):
        """모든 프로젝트의 마케팅 자료 생성"""

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

        print(f"📢 총 {len(project_dirs)}개 프로젝트의 마케팅 자료를 생성합니다.")

        results = []

        for project_dir in project_dirs:
            result = await self.process_project_marketing(project_dir)
            if result:
                results.append(result)

            # API 제한을 위한 대기
            await asyncio.sleep(2)

        # 결과 요약 저장
        await self.save_marketing_summary(results)

        return results

    async def save_marketing_summary(self, results):
        """마케팅 자료 생성 결과 요약"""

        summary = {
            "marketing_automation_date": "2025-09-21",
            "total_projects": len(results),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "results": results
        }

        with open("marketing_automation_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"\n📊 마케팅 자동화 요약:")
        print(f"✅ 성공: {summary['successful']}개")
        print(f"❌ 실패: {summary['failed']}개")
        print(f"📁 요약 파일: marketing_automation_summary.json")

async def main():
    """메인 실행 함수"""
    print("📢 마케팅 자동화 시스템")
    print("생성된 앱들의 마케팅 자료를 자동 생성합니다")
    print("=" * 60)

    marketing = MarketingAutomation()
    await marketing.process_all_projects()

    print("\n🎉 마케팅 자료 생성이 완료되었습니다!")

if __name__ == "__main__":
    asyncio.run(main())