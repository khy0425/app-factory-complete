#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
블로그/유튜브 콘텐츠 자동 생성 모듈
앱 출시 시 자동으로 리뷰 콘텐츠 생성 및 배포
"""

import json
import openai
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import os
import base64
from PIL import Image, ImageDraw, ImageFont
import io

@dataclass
class ContentTemplate:
    title: str
    content: str
    tags: List[str]
    thumbnail_prompt: str

class ContentGenerator:
    def __init__(self, openai_api_key: str):
        """콘텐츠 생성기 초기화"""
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
    def generate_blog_post(self, app_config: Dict, content_type: str = "review") -> ContentTemplate:
        """블로그 포스트 자동 생성"""
        app_name = app_config.get('app', {}).get('name', '앱')
        app_desc = app_config.get('app', {}).get('description', '')
        keywords = app_config.get('marketing', {}).get('keywords', [])
        
        if content_type == "review":
            return self._generate_review_post(app_name, app_desc, keywords)
        elif content_type == "tutorial":
            return self._generate_tutorial_post(app_name, app_desc, keywords)
        elif content_type == "comparison":
            return self._generate_comparison_post(app_name, app_desc, keywords)
        
    def _generate_review_post(self, app_name: str, app_desc: str, keywords: List[str]) -> ContentTemplate:
        """앱 리뷰 포스트 생성"""
        prompt = f"""
다음 앱에 대한 상세한 리뷰 블로그 포스트를 한국어로 작성해주세요:

앱 이름: {app_name}
앱 설명: {app_desc}
주요 키워드: {', '.join(keywords[:5])}

포스트 구조:
1. 흥미로운 도입부 (문제 제기)
2. 앱 소개 및 주요 기능
3. 실제 사용 후기 (긍정적이지만 진실성 있게)
4. 장단점 분석
5. 추천 대상 및 사용 팁
6. 다운로드 링크 및 마무리

요구사항:
- 2000-2500자 분량
- SEO 친화적 키워드 자연스럽게 포함
- 개인적 경험담 스타일로 작성
- 읽기 쉬운 문체 사용
- 제목은 클릭률 높은 스타일로
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # 제목 추출 (첫 번째 줄)
            lines = content.split('\n')
            title = lines[0].replace('#', '').strip()
            
            # 태그 생성
            tags = keywords[:5] + [app_name, "앱리뷰", "추천앱"]
            
            # 썸네일 프롬프트
            thumbnail_prompt = f"{app_name} 앱 스크린샷과 별점, 깔끔한 리뷰 썸네일"
            
            return ContentTemplate(
                title=title,
                content=content,
                tags=tags,
                thumbnail_prompt=thumbnail_prompt
            )
            
        except Exception as e:
            print(f"블로그 포스트 생성 오류: {e}")
            return self._generate_fallback_review(app_name, app_desc, keywords)
    
    def _generate_tutorial_post(self, app_name: str, app_desc: str, keywords: List[str]) -> ContentTemplate:
        """사용법 튜토리얼 포스트 생성"""
        prompt = f"""
{app_name} 앱의 상세한 사용법 가이드를 작성해주세요:

앱 정보: {app_desc}
핵심 기능: {', '.join(keywords[:3])}

구조:
1. 앱 설치 및 첫 설정
2. 주요 기능별 사용법 (단계별 설명)
3. 고급 활용 팁
4. 자주 묻는 질문 FAQ
5. 마무리 및 추천 이유

스타일: 초보자도 쉽게 따라할 수 있는 친절한 설명
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.6
            )
            
            content = response.choices[0].message.content.strip()
            title = f"{app_name} 완벽 사용법 가이드 - 초보자도 5분만에 마스터!"
            tags = keywords[:3] + [app_name, "사용법", "가이드", "튜토리얼"]
            
            return ContentTemplate(
                title=title,
                content=content,
                tags=tags,
                thumbnail_prompt=f"{app_name} 튜토리얼 스크린샷 단계별 가이드"
            )
            
        except Exception as e:
            print(f"튜토리얼 생성 오류: {e}")
            return self._generate_fallback_tutorial(app_name, keywords)
    
    def generate_youtube_script(self, app_config: Dict) -> str:
        """유튜브 리뷰 스크립트 생성"""
        app_name = app_config.get('app', {}).get('name', '앱')
        app_desc = app_config.get('app', {}).get('description', '')
        
        prompt = f"""
{app_name} 앱 리뷰 유튜브 영상 스크립트를 작성해주세요:

앱 정보: {app_desc}

스크립트 구성:
[인트로] (0-30초) - 시청자 주목끌기
[앱 소개] (30초-1분) - 기본 정보
[기능 시연] (1-3분) - 실제 사용 모습
[장단점] (3-4분) - 솔직한 평가
[마무리] (4-5분) - 추천 및 구독 유도

요구사항:
- 친근하고 자연스러운 말투
- 각 섹션별 시간 표시
- 화면 전환 포인트 명시
- 시청자 참여 유도 문구 포함
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"유튜브 스크립트 생성 오류: {e}")
            return f"""
[인트로] (0-30초)
안녕하세요! 오늘은 정말 유용한 앱 하나를 소개해드리려고 해요. {app_name}라는 앱인데요, 사용해보니 정말 만족스러워서 여러분께도 공유하고 싶어졌어요!

[앱 소개] (30초-1분)
{app_name}은 {app_desc} 이런 기능을 가진 앱이에요. 설치하자마자 바로 사용할 수 있을 정도로 직관적이더라구요.

[기능 시연] (1-3분)
자, 이제 실제로 어떻게 사용하는지 보여드릴게요. 화면을 보시면...

[마무리] (4-5분)
전반적으로 정말 추천하고 싶은 앱이에요. 링크는 설명란에 남겨놓을게요!
"""
    
    def generate_thumbnail_image(self, app_name: str, thumbnail_prompt: str) -> Optional[str]:
        """썸네일 이미지 생성 (AI 이미지 생성 API 활용)"""
        # DALL-E나 Stable Diffusion API 사용
        # 여기서는 간단한 텍스트 썸네일 생성
        try:
            # 기본 썸네일 생성
            img = Image.new('RGB', (1280, 720), color='#2196F3')
            draw = ImageDraw.Draw(img)
            
            # 폰트 설정 (기본 폰트 사용)
            try:
                font = ImageFont.truetype("arial.ttf", 60)
                small_font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # 텍스트 추가
            draw.text((640, 300), app_name, font=font, fill='white', anchor='mm')
            draw.text((640, 400), "앱 리뷰", font=small_font, fill='#FFD700', anchor='mm')
            
            # 이미지 저장
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Base64 인코딩
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return img_str
            
        except Exception as e:
            print(f"썸네일 생성 오류: {e}")
            return None
    
    def _generate_fallback_review(self, app_name: str, app_desc: str, keywords: List[str]) -> ContentTemplate:
        """기본 리뷰 템플릿"""
        title = f"{app_name} 솔직 후기 - 정말 쓸만할까?"
        content = f"""
# {title}

안녕하세요! 오늘은 최근에 사용해본 {app_name}에 대해 솔직한 후기를 남겨보려고 해요.

## 앱 소개
{app_name}은 {app_desc} 기능을 제공하는 앱입니다. {', '.join(keywords[:3])}에 관심이 있으시다면 한번 살펴볼만한 앱이에요.

## 주요 기능
- 직관적인 사용자 인터페이스
- 핵심 기능에 충실한 설계
- 안정적인 성능

## 사용 후기
실제로 며칠간 사용해본 결과, 전반적으로 만족스러운 앱이었습니다. 특히 {keywords[0] if keywords else '주요 기능'}이 잘 구현되어 있어서 실용적이더라구요.

## 추천 대상
{', '.join(keywords[:2])}에 관심이 있는 분들께 추천드려요!

다운로드 링크: [Google Play Store]
"""
        
        return ContentTemplate(
            title=title,
            content=content,
            tags=keywords[:3] + [app_name, "리뷰"],
            thumbnail_prompt=f"{app_name} 리뷰 썸네일"
        )
    
    def _generate_fallback_tutorial(self, app_name: str, keywords: List[str]) -> ContentTemplate:
        """기본 튜토리얼 템플릿"""
        return ContentTemplate(
            title=f"{app_name} 기본 사용법",
            content=f"# {app_name} 사용 가이드\n\n기본적인 사용법을 안내드립니다...",
            tags=keywords[:3] + ["가이드"],
            thumbnail_prompt=f"{app_name} 가이드"
        )

def main():
    """테스트 실행"""
    api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
    generator = ContentGenerator(api_key)
    
    # 테스트 앱 설정
    test_config = {
        'app': {
            'name': 'Focus Timer Pro',
            'description': '집중력 향상을 위한 포모도로 타이머'
        },
        'marketing': {
            'keywords': ['집중력', '타이머', '포모도로', '생산성', '시간관리']
        }
    }
    
    # 블로그 포스트 생성
    blog_post = generator.generate_blog_post(test_config, "review")
    print(f"제목: {blog_post.title}")
    print(f"태그: {blog_post.tags}")
    print(f"내용 길이: {len(blog_post.content)}자")
    
    # 유튜브 스크립트 생성
    youtube_script = generator.generate_youtube_script(test_config)
    print(f"\n유튜브 스크립트 길이: {len(youtube_script)}자")

if __name__ == "__main__":
    main()
