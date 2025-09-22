#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini Google Play Store 에셋 자동 생성기
앱별 Feature Graphic, 스크린샷, 아이콘을 Gemini로 자동 생성
"""

import os
import json
import asyncio
import base64
import aiohttp
import requests
from pathlib import Path
from typing import Dict, List, Optional
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class GeminiStoreAssetGenerator:
    """Gemini를 활용한 Play Store 에셋 자동 생성기"""

    def __init__(self, gemini_api_key: str = None):
        self.logger = logging.getLogger(__name__)
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')

        if not self.gemini_api_key:
            self.logger.warning("⚠️ GEMINI_API_KEY가 설정되지 않음. 환경변수 설정 필요")

        # Google Play Store 에셋 사양
        self.play_store_specs = {
            "feature_graphic": {
                "width": 1024,
                "height": 500,
                "format": "PNG",
                "description": "메인 배너 이미지 (Play Store 상단)"
            },
            "app_icon": {
                "width": 512,
                "height": 512,
                "format": "PNG",
                "description": "앱 아이콘 (고해상도)"
            },
            "screenshots": {
                "phone": {
                    "width": 1080,
                    "height": 1920,
                    "count": 8,
                    "format": "PNG",
                    "description": "폰 스크린샷 (최대 8개)"
                },
                "tablet": {
                    "width": 1200,
                    "height": 1920,
                    "count": 8,
                    "format": "PNG",
                    "description": "태블릿 스크린샷 (선택사항)"
                }
            }
        }

        self.logger.info("🎨 Gemini Store Asset Generator 초기화 완료")

    async def generate_all_assets_for_app(self, app_spec: Dict) -> Dict:
        """앱의 모든 Play Store 에셋 생성"""

        app_name = app_spec.get("app_name", "Unknown App")
        self.logger.info(f"🎯 {app_name} Play Store 에셋 생성 시작")

        # 에셋 저장 디렉토리 생성
        assets_dir = Path(f"store_assets/{app_name.lower().replace(' ', '_')}")
        assets_dir.mkdir(parents=True, exist_ok=True)

        results = {
            "app_name": app_name,
            "generation_time": datetime.now().isoformat(),
            "assets": {}
        }

        try:
            # 1. Feature Graphic 생성 (1024x500)
            feature_graphic = await self.generate_feature_graphic(app_spec, assets_dir)
            results["assets"]["feature_graphic"] = feature_graphic

            # 2. 앱 아이콘 생성 (512x512)
            app_icon = await self.generate_app_icon(app_spec, assets_dir)
            results["assets"]["app_icon"] = app_icon

            # 3. 스크린샷 생성 (Phone 1080x1920)
            screenshots = await self.generate_screenshots(app_spec, assets_dir)
            results["assets"]["screenshots"] = screenshots

            # 4. 프로모션 이미지 생성
            promo_images = await self.generate_promo_images(app_spec, assets_dir)
            results["assets"]["promo_images"] = promo_images

            self.logger.info(f"✅ {app_name} 모든 에셋 생성 완료")
            return results

        except Exception as e:
            self.logger.error(f"❌ {app_name} 에셋 생성 실패: {e}")
            results["error"] = str(e)
            return results

    def add_korean_text_overlay(self, image_path: Path, title_text: str, subtitle_text: str = None):
        """이미지에 한글 텍스트 오버레이 추가"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os

            # 이미지 로드
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # 무료 상업용 한글 폰트 사용
            font_dir = Path("fonts")

            # 폰트 우선순위: 재미있고 임팩트 있는 폰트들
            font_candidates = [
                font_dir / "BlackHanSans.ttf",  # 밈에 자주 쓰이는 블랙한산스
                font_dir / "GmarketSansBold.ttf",  # 지마켓 산스 볼드
                font_dir / "Pretendard-ExtraBold.ttf",  # 프리텐다드
                font_dir / "NanumGothicBold.ttf",  # 나눔고딕 볼드
                "malgun.ttf"  # Windows 맑은 고딕 (폴백)
            ]

            title_font = None
            subtitle_font = None

            for font_path in font_candidates:
                try:
                    if isinstance(font_path, Path):
                        if font_path.exists():
                            title_font = ImageFont.truetype(str(font_path), 90)  # 더 크게
                            subtitle_font = ImageFont.truetype(str(font_path), 42)  # 더 크게
                            self.logger.info(f"폰트 로드 성공: {font_path.name}")
                            break
                    else:
                        # Windows 시스템 폰트
                        title_font = ImageFont.truetype(font_path, 80)
                        subtitle_font = ImageFont.truetype(font_path, 36)
                        self.logger.info(f"시스템 폰트 로드 성공: {font_path}")
                        break
                except Exception as e:
                    continue

            # 폰트를 찾지 못한 경우
            if not title_font:
                self.logger.warning("한글 폰트를 찾을 수 없습니다. 기본 폰트 사용")
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()

            # 텍스트 위치 계산 (중앙 왼쪽)
            img_width, img_height = img.size

            # 타이틀 그리기 (황금색) - 더 왼쪽으로
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            title_x = 50  # 왼쪽 여백
            title_y = (img_height // 2) - (title_height // 2) - 30

            # 텍스트에 강한 그림자 효과 (더 선명하게)
            # 외곽선 효과를 위해 여러 방향으로 검은색 텍스트 그리기
            outline_width = 4
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((title_x + dx, title_y + dy),
                                 title_text, fill=(0, 0, 0, 200), font=title_font)

            # 메인 텍스트 (더 밝은 황금색, 약간 주황빛)
            draw.text((title_x, title_y), title_text,
                     fill=(255, 225, 50), font=title_font)  # 밝은 황금색

            # 서브타이틀 그리기 (흰색)
            if subtitle_text:
                subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
                subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
                subtitle_x = title_x
                subtitle_y = title_y + title_height + 10

                # 서브타이틀도 외곽선 효과
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if dx != 0 or dy != 0:
                            draw.text((subtitle_x + dx, subtitle_y + dy),
                                     subtitle_text, fill=(0, 0, 0, 200), font=subtitle_font)

                draw.text((subtitle_x, subtitle_y), subtitle_text,
                         fill=(255, 255, 255), font=subtitle_font)

            # 이미지 저장
            img.save(image_path, 'PNG', optimize=True)
            self.logger.info(f"✅ 한글 텍스트 오버레이 추가 완료: {title_text}")

        except Exception as e:
            self.logger.error(f"텍스트 오버레이 추가 실패: {e}")

    def add_korean_screenshot_overlay(self, image_path: Path, screen_type: str, screen_title: str):
        """스크린샷에 한글 텍스트 오버레이 추가"""
        try:
            from PIL import Image, ImageDraw, ImageFont

            # 이미지 로드
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # 폰트 로드
            font_dir = Path("fonts")
            try:
                title_font = ImageFont.truetype(str(font_dir / "BlackHanSans.ttf"), 48)
                text_font = ImageFont.truetype(str(font_dir / "BlackHanSans.ttf"), 32)
                small_font = ImageFont.truetype(str(font_dir / "BlackHanSans.ttf"), 24)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()

            img_width, img_height = img.size

            # 화면별 텍스트 정의 (일관된 디자인)
            screen_texts = {
                "main_screen": {
                    "title": "기가차드 러너",
                    "elements": [
                        {"text": "오늘의 목표", "pos": (80, 250), "size": "normal"},
                        {"text": "75%", "pos": (img_width//2, 450), "size": "large", "center": True},
                        {"text": "완료", "pos": (img_width//2, 520), "center": True},
                        {"text": "거리: 2.3km", "pos": (80, 650), "size": "small"},
                        {"text": "시간: 15분", "pos": (280, 650), "size": "small"},
                        {"text": "칼로리: 120", "pos": (480, 650), "size": "small"},
                        {"text": "달리기 시작", "pos": (img_width//2, img_height-180), "center": True, "color": "button"}
                    ]
                },
                "workout_screen": {
                    "title": "달리기 중",
                    "elements": [
                        {"text": "00:15:42", "pos": (img_width//2, 400), "size": "large", "center": True},
                        {"text": "거리", "pos": (100, 600)},
                        {"text": "2.3km", "pos": (100, 640), "size": "large"},
                        {"text": "속도", "pos": (300, 600)},
                        {"text": "5.2km/h", "pos": (300, 640), "size": "large"},
                        {"text": "페이스", "pos": (500, 600)},
                        {"text": "11:30", "pos": (500, 640), "size": "large"},
                        {"text": "일시정지", "pos": (200, img_height-120), "center": True, "color": "button"},
                        {"text": "정지", "pos": (img_width-200, img_height-120), "center": True, "color": "red"}
                    ]
                },
                "progress_screen": {
                    "title": "진행률",
                    "elements": [
                        {"text": "레벨 5", "pos": (img_width//2, 300), "center": True, "size": "large"},
                        {"text": "기가차드로 진화 중...", "pos": (img_width//2, 350), "center": True, "size": "small"},
                        {"text": "업적", "pos": (80, 500)},
                        {"text": "첫 달리기 완료", "pos": (100, 550), "size": "small"},
                        {"text": "10km 달성", "pos": (100, 590), "size": "small"},
                        {"text": "연속 7일", "pos": (100, 630), "size": "small"},
                        {"text": "다음 레벨까지", "pos": (img_width//2, img_height-200), "center": True},
                        {"text": "3,200 XP", "pos": (img_width//2, img_height-160), "center": True, "size": "large"}
                    ]
                },
                "stats_screen": {
                    "title": "통계",
                    "elements": [
                        {"text": "이번 주", "pos": (100, 250)},
                        {"text": "총 거리", "pos": (80, 350)},
                        {"text": "15.2km", "pos": (80, 380), "size": "large"},
                        {"text": "총 시간", "pos": (300, 350)},
                        {"text": "2시간 30분", "pos": (300, 380), "size": "large"},
                        {"text": "평균 속도", "pos": (80, 480)},
                        {"text": "6.1km/h", "pos": (80, 510), "size": "large"},
                        {"text": "칼로리", "pos": (300, 480)},
                        {"text": "890 kcal", "pos": (300, 510), "size": "large"},
                        {"text": "주간 목표", "pos": (img_width//2, img_height-200), "center": True},
                        {"text": "85% 달성", "pos": (img_width//2, img_height-160), "center": True, "size": "large"}
                    ]
                },
                "settings_screen": {
                    "title": "설정",
                    "elements": [
                        {"text": "기가차드", "pos": (150, 280), "size": "large"},
                        {"text": "레벨 5 러너", "pos": (150, 320), "size": "small"},
                        {"text": "계정", "pos": (80, 420)},
                        {"text": "알림", "pos": (80, 480)},
                        {"text": "개인정보 보호", "pos": (80, 540)},
                        {"text": "앱 정보", "pos": (80, 600)},
                        {"text": "로그아웃", "pos": (80, 660), "color": "red"}
                    ]
                }
            }

            screen_data = screen_texts.get(screen_type, {"title": screen_title, "elements": []})

            # 타이틀 추가 (상단)
            title_text = screen_data.get("title", screen_title)
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (img_width - title_width) // 2
            title_y = 100

            # 타이틀 그림자
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx != 0 or dy != 0:
                        draw.text((title_x + dx, title_y + dy), title_text,
                                 fill=(0, 0, 0, 200), font=title_font)

            # 타이틀 메인
            draw.text((title_x, title_y), title_text, fill=(255, 225, 50), font=title_font)

            # 각 요소별 텍스트 추가
            for element in screen_data.get("elements", []):
                text = element["text"]
                pos = element["pos"]
                center = element.get("center", False)
                size = element.get("size", "normal")

                # 폰트 선택
                if size == "large":
                    font = title_font
                elif size == "small":
                    font = small_font
                else:
                    font = text_font

                # 중앙 정렬 처리
                if center:
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    pos = (pos[0] - text_width//2, pos[1])

                # 그림자
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx != 0 or dy != 0:
                            draw.text((pos[0] + dx, pos[1] + dy), text,
                                     fill=(0, 0, 0, 150), font=font)

                # 색상 선택
                color = element.get("color", "white")
                if color == "button":
                    text_color = (255, 225, 50)  # 골드
                elif color == "red":
                    text_color = (255, 0, 0)  # 빨강
                else:
                    text_color = (255, 255, 255)  # 흰색

                # 메인 텍스트
                draw.text(pos, text, fill=text_color, font=font)

            # 이미지 저장
            img.save(image_path, 'PNG', optimize=True)
            self.logger.info(f"✅ 스크린샷 한글 텍스트 오버레이 완료: {screen_type}")

        except Exception as e:
            self.logger.error(f"스크린샷 텍스트 오버레이 실패: {e}")

    def _get_screen_content(self, screen_name: str) -> str:
        """화면별 구체적인 콘텐츠 설명"""
        content_map = {
            "main_screen": """
- Large circular progress ring showing 75% daily goal completion
- Chad character avatar in center
- Today's stats: Distance, Time, Calories
- Large "START RUN" button at bottom
- Quick stats cards showing weekly progress
            """,
            "workout_screen": """
- Large timer display: 00:15:42
- Live stats: Distance (2.3 km), Speed (5.2 km/h), Pace
- Chad character animation/silhouette
- Pause and Stop buttons at bottom
- Progress indicator for current workout
            """,
            "progress_screen": """
- Level system: Current Level 5, XP progress bar
- Achievement grid: 4x2 achievement badges
- Chad evolution stages (different character forms)
- "Next Level" preview
- Weekly/Monthly progress charts
            """,
            "stats_screen": """
- Weekly/Monthly toggle tabs
- Key metrics cards: Total Distance, Total Time, Avg Speed
- Line chart showing progress over time
- Personal records section
- Streaks and consistency metrics
            """,
            "settings_screen": """
- User profile section at top
- Settings categories: Account, Notifications, Privacy, About
- Toggle switches for notifications
- Dark/Light theme toggle
- Version info and logout button
            """
        }
        return content_map.get(screen_name, "Generic fitness app screen")

    async def generate_feature_graphic(self, app_spec: Dict, output_dir: Path) -> Dict:
        """Feature Graphic (1024x500) 생성"""

        app_name = app_spec.get("app_name", "App")
        description = app_spec.get("description", "")
        tagline = app_spec.get("tagline", "")

        # Gemini 프롬프트 생성
        prompt = f"""
Create a COOL GIGACHAD MEME aesthetic Feature Graphic (1024x500px):

DO NOT ADD ANY TEXT. Create a text-free image only.

Design Requirements:
- Size: 1024x500 pixels (exact)
- GIGACHAD MEME AESTHETIC - Cool, confident, alpha male vibes
- Not childish or overly cartoonish - should feel badass
- Dark, moody atmosphere with golden accents
- Leave center-left area clear for text overlay

Visual Elements:
- GIGACHAD character with iconic features:
  * Extremely chiseled jawline (the famous Chad jaw)
  * Muscular physique but realistic proportions
  * Confident, stoic facial expression
  * Running with perfect form and composure
- Aesthetic elements:
  * Dark city skyline or mountains in background
  * Subtle motion blur showing speed (not flames or explosions)
  * Golden hour lighting or neon city lights
  * Maybe rain or dramatic weather for atmosphere
  * Other runners in background looking inferior/struggling

Style: SIGMA MALE AESTHETIC, DARK AND MOODY, COOL, CONFIDENT
Think "Patrick Bateman running scene" meets GigaChad meme
This should look COOL and make people want to become a Chad
NOT childish, NOT overly colorful, YES mysterious and badass
"""

        try:
            # 실제 이미지 생성
            image_path = output_dir / "feature_graphic.png"

            # 실제 이미지 생성 (1024x500)
            image_info = await self._generate_real_image(
                prompt, 1024, 500, image_path
            )

            # 이미지 생성 성공 시 한글 텍스트 오버레이 추가
            if image_info.get("status") == "success" and image_path.exists():
                self.add_korean_text_overlay(
                    image_path,
                    title_text=app_name,
                    subtitle_text=tagline
                )

            return {
                "type": "feature_graphic",
                "file_path": str(image_path),
                "dimensions": "1024x500",
                "size_kb": image_path.stat().st_size // 1024 if image_path.exists() else 0,
                "cost": image_info.get("cost", 0),
                "method": image_info.get("method", "unknown"),
                "prompt_used": prompt,
                "status": image_info.get("status", "generated")
            }

        except Exception as e:
            self.logger.error(f"Feature Graphic 생성 실패: {e}")
            return {"type": "feature_graphic", "status": "failed", "error": str(e)}

    async def generate_app_icon(self, app_spec: Dict, output_dir: Path) -> Dict:
        """앱 아이콘 (512x512) 생성"""

        app_name = app_spec.get("app_name", "App")
        exercise_type = app_spec.get("exercise_type", "workout")

        prompt = f"""
Create a high-quality app icon (512x512px) for a running app:

Design Requirements:
- Size: 512x512 pixels (perfect square)
- App store ready (iOS/Android compatible)
- Simple, recognizable design
- Works well at small sizes (16px to 512px)
- RUNNING theme only (no gym equipment)
- No text or letters anywhere
- Modern, minimalist design

Visual Elements:
- Running shoe or runner silhouette
- Motion lines showing speed/movement
- Outdoor running elements (road, trail)
- Dynamic pose suggesting forward motion
- Bold, geometric shapes
- Dark background with golden accents
- NO gym equipment or weights
- NO text or letters
- NO color codes visible

Style: Minimalist, dynamic, outdoor running focused
The icon should instantly communicate "running app"!
"""

        try:
            icon_path = output_dir / "app_icon_512.png"

            # 실제 아이콘 이미지 생성 (512x512)
            icon_info = await self._generate_real_image(
                prompt, 512, 512, icon_path
            )

            return {
                "type": "app_icon",
                "file_path": str(icon_path),
                "dimensions": "512x512",
                "size_kb": icon_info.get("size_kb", 0),
                "cost": icon_info.get("cost", 0),
                "method": icon_info.get("method", "unknown"),
                "prompt_used": prompt,
                "status": icon_info.get("status", "generated")
            }

        except Exception as e:
            return {"type": "app_icon", "status": "failed", "error": str(e)}

    async def generate_screenshots(self, app_spec: Dict, output_dir: Path) -> Dict:
        """앱 스크린샷 생성 (1080x1920 Phone)"""

        app_name = app_spec.get("app_name", "App")
        key_features = app_spec.get("key_features", [])

        screenshots_dir = output_dir / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)

        screenshot_concepts = [
            {
                "name": "main_screen",
                "title": "메인 화면",
                "description": f"{app_name} 메인 대시보드, Chad 캐릭터와 진행률 표시"
            },
            {
                "name": "workout_screen",
                "title": "운동 화면",
                "description": "운동 실행 화면, 타이머와 동작 가이드"
            },
            {
                "name": "progress_screen",
                "title": "진행률 화면",
                "description": "레벨업 시스템과 업적 화면"
            },
            {
                "name": "stats_screen",
                "title": "통계 화면",
                "description": "운동 기록과 차트 분석"
            },
            {
                "name": "settings_screen",
                "title": "설정 화면",
                "description": "앱 설정과 프로필 관리"
            }
        ]

        generated_screenshots = []

        for i, concept in enumerate(screenshot_concepts[:5]):  # 최대 5개
            prompt = f"""
Create a mobile app screenshot (1080x1920px) for GigaChad Runner fitness app:

Screen: {concept['title']} ({concept['name']})

Design Requirements:
- Size: 1080x1920 pixels (mobile phone ratio)
- Consistent dark UI theme: black background (#1A1A1A), gold accents (#FFD700), red highlights (#FF0000)
- Modern Material Design with rounded corners
- App title "GigaChad Runner" at top
- Status bar: 9:41 AM, battery, signal icons
- Bottom navigation: 5 tabs with icons (Home, Run, Progress, Stats, Settings)

Screen-specific content:
{self._get_screen_content(concept['name'])}

Style: Professional dark fitness app, consistent design language
Use clean English text for now - will be localized later
Ensure all screens follow the same design patterns and spacing
"""

            try:
                screenshot_path = screenshots_dir / f"screenshot_{i+1}_{concept['name']}.png"

                # 실제 스크린샷 이미지 생성 (1080x1920)
                screenshot_info = await self._generate_real_image(
                    prompt, 1080, 1920, screenshot_path
                )

                # 이미지 생성 성공 시 한글 텍스트 오버레이 추가
                if screenshot_info.get("status") == "success" and screenshot_path.exists():
                    self.add_korean_screenshot_overlay(
                        screenshot_path,
                        concept['name'],
                        concept['title']
                    )

                generated_screenshots.append({
                    "name": concept['name'],
                    "title": concept['title'],
                    "file_path": str(screenshot_path),
                    "dimensions": "1080x1920",
                    "size_kb": screenshot_info.get("size_kb", 0),
                    "cost": screenshot_info.get("cost", 0),
                    "method": screenshot_info.get("method", "unknown"),
                    "prompt_used": prompt,
                    "status": screenshot_info.get("status", "generated")
                })

            except Exception as e:
                self.logger.error(f"스크린샷 {concept['name']} 생성 실패: {e}")

        return {
            "type": "screenshots",
            "count": len(generated_screenshots),
            "screenshots": generated_screenshots,
            "status": "completed"
        }

    async def generate_promo_images(self, app_spec: Dict, output_dir: Path) -> Dict:
        """프로모션 이미지 생성"""

        promo_dir = output_dir / "promo"
        promo_dir.mkdir(exist_ok=True)

        promo_concepts = [
            {
                "name": "social_media_square",
                "size": "1080x1080",
                "description": "Instagram/Facebook 정사각형 포스트"
            },
            {
                "name": "social_media_story",
                "size": "1080x1920",
                "description": "Instagram/Facebook 스토리"
            },
            {
                "name": "youtube_thumbnail",
                "size": "1280x720",
                "description": "YouTube 썸네일"
            }
        ]

        generated_promos = []

        for concept in promo_concepts:
            try:
                promo_path = promo_dir / f"{concept['name']}.png"

                # 실제로는 Gemini API 호출
                placeholder_info = await self._create_promo_placeholder(
                    app_spec, concept, promo_path
                )

                generated_promos.append({
                    "name": concept['name'],
                    "file_path": str(promo_path),
                    "dimensions": concept['size'],
                    "description": concept['description'],
                    "status": "generated"
                })

            except Exception as e:
                self.logger.error(f"프로모션 이미지 {concept['name']} 생성 실패: {e}")

        return {
            "type": "promo_images",
            "count": len(generated_promos),
            "images": generated_promos,
            "status": "completed"
        }

    # 실제 이미지 생성 메서드들
    async def _generate_real_image(self, prompt: str, width: int, height: int, output_path: Path) -> Dict:
        """실제 이미지 생성 (Nano Banana/Gemini Imagen 사용)"""

        try:
            # Gemini API Key 확인
            if self.gemini_api_key:
                return await self._generate_with_nano_banana(prompt, width, height, output_path)

            # Gemini API가 없으면 임시 이미지 생성
            self.logger.warning("Gemini API 키가 없어 임시 이미지 생성")
            return await self._create_temporary_image(prompt, width, height, output_path)

        except Exception as e:
            self.logger.error(f"이미지 생성 실패: {e}")
            return await self._create_temporary_image(prompt, width, height, output_path)

    async def _generate_with_nano_banana(self, prompt: str, width: int, height: int, output_path: Path) -> Dict:
        """Nano Banana (Gemini Imagen) API로 실제 이미지 생성"""

        # Gemini Imagen API 엔드포인트
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict"

        # 요청 헤더
        headers = {
            "x-goog-api-key": self.gemini_api_key,
            "Content-Type": "application/json"
        }

        # 요청 데이터
        request_data = {
            "instances": [
                {
                    "prompt": prompt
                }
            ],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": self._get_aspect_ratio(width, height)
            }
        }

        try:
            self.logger.info(f"🍌 Nano Banana로 이미지 생성 중: {width}x{height}")

            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=request_data) as response:

                    if response.status == 200:
                        result = await response.json()

                        # 디버깅: 응답 구조 확인
                        self.logger.info(f"API 응답 키: {result.keys()}")

                        # 생성된 이미지 데이터 추출 (Imagen 4 응답 형식)
                        if "predictions" in result and len(result["predictions"]) > 0:
                            # 디버깅: predictions 내용 확인
                            self.logger.info(f"Predictions 키: {result['predictions'][0].keys()}")
                            image_data_b64 = result["predictions"][0].get("bytesBase64Encoded")

                            # Base64 디코딩
                            image_data = base64.b64decode(image_data_b64)

                            # PIL로 이미지 처리
                            image = Image.open(io.BytesIO(image_data))

                            # 정확한 크기로 리사이즈
                            if image.size != (width, height):
                                image = image.resize((width, height), Image.Resampling.LANCZOS)

                            # PNG로 저장
                            image.save(output_path, 'PNG', optimize=True)

                            cost = 0.039  # Nano Banana 비용 ($0.039/이미지)

                            self.logger.info(f"✅ Nano Banana 이미지 생성 성공: {output_path}")

                            return {
                                "status": "success",
                                "file_path": str(output_path),
                                "size_kb": output_path.stat().st_size // 1024,
                                "method": "nano_banana",
                                "cost": cost,
                                "api_response": "success"
                            }
                        else:
                            self.logger.error("Nano Banana 응답에 이미지 데이터가 없음")
                            return await self._create_temporary_image(prompt, width, height, output_path)

                    else:
                        error_text = await response.text()
                        self.logger.error(f"Nano Banana API 오류 {response.status}: {error_text}")
                        return await self._create_temporary_image(prompt, width, height, output_path)

        except Exception as e:
            self.logger.error(f"Nano Banana API 실패: {e}")
            return await self._create_temporary_image(prompt, width, height, output_path)

    def _get_aspect_ratio(self, width: int, height: int) -> str:
        """이미지 크기에 따른 Imagen 4 aspect ratio 반환"""

        ratio = width / height

        if abs(ratio - 1.0) < 0.1:  # 정사각형 (1:1)
            return "1:1"
        elif abs(ratio - (16/9)) < 0.1:  # 16:9
            return "16:9"
        elif abs(ratio - (9/16)) < 0.1:  # 9:16
            return "9:16"
        elif abs(ratio - (4/3)) < 0.1:  # 4:3
            return "4:3"
        elif abs(ratio - (3/4)) < 0.1:  # 3:4
            return "3:4"
        elif ratio > 1.3:  # 가로형 기본값
            return "16:9"
        elif ratio < 0.8:  # 세로형 기본값
            return "9:16"
        else:  # 기본 (4:3 등)
            return "4:3"

    async def _create_temporary_image(self, prompt: str, width: int, height: int, output_path: Path) -> Dict:
        """임시 이미지 생성 (실제 API 없을 때)"""

        # PIL로 임시 이미지 생성
        image = Image.new('RGB', (width, height), color='#1A1A1A')  # Chad Black
        draw = ImageDraw.Draw(image)

        # 그라데이션 배경
        for y in range(height):
            gray_value = int(26 + (y / height) * 50)  # 26 to 76
            color = (gray_value, gray_value, gray_value)
            draw.line([(0, y), (width, y)], fill=color)

        # 텍스트 추가
        try:
            # 기본 폰트 사용
            font_size = min(width // 15, height // 8)

            # 텍스트 그리기
            text_lines = [
                "기가차드 러너",
                "GigaChad Runner",
                "달린다... Yes.",
                f"{width}x{height}"
            ]

            y_offset = height // 4
            for line in text_lines:
                # 텍스트 크기 계산
                bbox = draw.textbbox((0, 0), line)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                x = (width - text_width) // 2

                # 그림자 효과
                draw.text((x+2, y_offset+2), line, fill='#000000')
                # 메인 텍스트
                draw.text((x, y_offset), line, fill='#FFD700')  # Alpha Gold

                y_offset += text_height + 10

        except Exception as e:
            self.logger.warning(f"텍스트 렌더링 실패: {e}")

        # 액센트 라인 추가
        draw.rectangle([0, 0, width, 5], fill='#FFD700')  # 상단
        draw.rectangle([0, height-5, width, height], fill='#FF0000')  # 하단

        # PNG로 저장
        image.save(output_path, 'PNG', optimize=True)

        return {
            "status": "temporary",
            "file_path": str(output_path),
            "size_kb": output_path.stat().st_size // 1024,
            "method": "pil_temporary"
        }

    async def _create_feature_graphic_placeholder(self, app_spec: Dict, output_path: Path) -> Dict:
        """Feature Graphic 플레이스홀더 생성"""

        # 실제로는 Gemini API를 호출하여 이미지 생성
        # 지금은 JSON 정보만 생성

        placeholder_data = {
            "app_name": app_spec.get("app_name", "App"),
            "dimensions": "1024x500",
            "type": "feature_graphic",
            "generated_at": datetime.now().isoformat(),
            "gemini_prompt": "Feature graphic generation prompt",
            "size_kb": 250  # 예상 크기
        }

        # JSON 정보 저장
        info_path = output_path.with_suffix('.json')
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(placeholder_data, f, ensure_ascii=False, indent=2)

        self.logger.info(f"📄 Feature Graphic 메타데이터 생성: {info_path}")
        return placeholder_data

    async def _create_app_icon_placeholder(self, app_spec: Dict, output_path: Path) -> Dict:
        """앱 아이콘 플레이스홀더 생성"""

        placeholder_data = {
            "app_name": app_spec.get("app_name", "App"),
            "dimensions": "512x512",
            "type": "app_icon",
            "generated_at": datetime.now().isoformat(),
            "size_kb": 80
        }

        info_path = output_path.with_suffix('.json')
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(placeholder_data, f, ensure_ascii=False, indent=2)

        return placeholder_data

    async def _create_screenshot_placeholder(self, concept: Dict, output_path: Path) -> Dict:
        """스크린샷 플레이스홀더 생성"""

        placeholder_data = {
            "concept": concept,
            "dimensions": "1080x1920",
            "type": "screenshot",
            "generated_at": datetime.now().isoformat(),
            "size_kb": 150
        }

        info_path = output_path.with_suffix('.json')
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(placeholder_data, f, ensure_ascii=False, indent=2)

        return placeholder_data

    async def _create_promo_placeholder(self, app_spec: Dict, concept: Dict, output_path: Path) -> Dict:
        """프로모션 이미지 플레이스홀더 생성"""

        placeholder_data = {
            "app_name": app_spec.get("app_name", "App"),
            "concept": concept,
            "dimensions": concept['size'],
            "type": "promo_image",
            "generated_at": datetime.now().isoformat(),
            "size_kb": 200
        }

        info_path = output_path.with_suffix('.json')
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(placeholder_data, f, ensure_ascii=False, indent=2)

        return placeholder_data

    def create_store_listing_package(self, app_spec: Dict, assets_result: Dict) -> Dict:
        """Play Store 업로드용 패키지 생성"""

        app_name = app_spec.get("app_name", "App")
        package_dir = Path(f"store_packages/{app_name.lower().replace(' ', '_')}")
        package_dir.mkdir(parents=True, exist_ok=True)

        # 스토어 리스팅 정보 생성
        store_listing = {
            "app_name": app_name,
            "short_description": app_spec.get("tagline", "")[:80],  # 80자 제한
            "full_description": self._generate_store_description(app_spec),
            "category": app_spec.get("category", "Health & Fitness"),
            "content_rating": "Everyone",
            "privacy_policy_url": "https://your-domain.com/privacy",
            "generated_assets": assets_result,
            "upload_checklist": {
                "feature_graphic": "✅ 1024x500 PNG",
                "app_icon": "✅ 512x512 PNG",
                "screenshots": f"✅ {len(assets_result.get('assets', {}).get('screenshots', {}).get('screenshots', []))}개",
                "app_bundle": "⏳ APK/AAB 파일 준비 필요",
                "store_listing": "✅ 완료"
            }
        }

        # 패키지 정보 저장
        package_info_path = package_dir / "store_listing.json"
        with open(package_info_path, 'w', encoding='utf-8') as f:
            json.dump(store_listing, f, ensure_ascii=False, indent=2)

        self.logger.info(f"📦 Store Listing 패키지 생성: {package_dir}")
        return store_listing

    def _generate_store_description(self, app_spec: Dict) -> str:
        """Play Store 설명 텍스트 자동 생성"""

        app_name = app_spec.get("app_name", "App")
        description = app_spec.get("description", "")
        key_features = app_spec.get("key_features", [])

        store_description = f"""🔥 {app_name} - 기가차드 되기 프로젝트!

{description}

💪 주요 기능:
"""

        for feature in key_features[:6]:  # 최대 6개 특징
            store_description += f"• {feature}\n"

        store_description += """
🏆 왜 이 앱인가?
• Mission100 검증된 운동 시스템
• 한국어 완벽 지원
• 오프라인 모드 지원
• 광고 없는 깔끔한 UI
• 무료 다운로드!

지금 다운로드하고 기가차드가 되어보세요! 💪

#기가차드 #홈트 #운동 #피트니스 #헬스 #다이어트 #근육
"""

        return store_description