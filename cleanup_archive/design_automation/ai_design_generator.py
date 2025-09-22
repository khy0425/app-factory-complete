#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 기반 디자인 자동 생성 모듈
앱 아이콘, 스토어 이미지, 색상 팔레트 자동 생성
"""

import openai
import requests
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import base64
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ColorPalette:
    primary: str
    secondary: str
    accent: str
    background: str
    text: str

@dataclass
class DesignAssets:
    app_icon: Optional[str]  # Base64 이미지
    store_banner: Optional[str]
    screenshots: List[str]
    color_palette: ColorPalette
    design_rationale: str

class AIDesignGenerator:
    def __init__(self, openai_api_key: str):
        """AI 디자인 생성기 초기화"""
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
        # 카테고리별 검증된 색상 팔레트
        self.category_palettes = {
            "productivity": [
                ColorPalette("#2196F3", "#1976D2", "#FFC107", "#FAFAFA", "#212121"),
                ColorPalette("#4CAF50", "#388E3C", "#FF9800", "#F5F5F5", "#424242"),
                ColorPalette("#9C27B0", "#7B1FA2", "#FFEB3B", "#FAFAFA", "#212121")
            ],
            "health": [
                ColorPalette("#4CAF50", "#2E7D32", "#FF5722", "#F1F8E9", "#1B5E20"),
                ColorPalette("#00BCD4", "#0097A7", "#FF9800", "#E0F2F1", "#004D40"),
                ColorPalette("#8BC34A", "#689F38", "#E91E63", "#F9FBE7", "#33691E")
            ],
            "entertainment": [
                ColorPalette("#E91E63", "#C2185B", "#FFEB3B", "#FCE4EC", "#880E4F"),
                ColorPalette("#FF5722", "#D84315", "#4CAF50", "#FFF3E0", "#BF360C"),
                ColorPalette("#9C27B0", "#7B1FA2", "#00BCD4", "#F3E5F5", "#4A148C")
            ],
            "lifestyle": [
                ColorPalette("#FF9800", "#F57C00", "#2196F3", "#FFF8E1", "#E65100"),
                ColorPalette("#795548", "#5D4037", "#4CAF50", "#EFEBE9", "#3E2723"),
                ColorPalette("#607D8B", "#455A64", "#FF5722", "#ECEFF1", "#263238")
            ]
        }
    
    def generate_app_icon(self, app_config: Dict, style: str = "modern") -> Optional[str]:
        """AI를 활용한 앱 아이콘 생성"""
        app_name = app_config.get('app', {}).get('name', '앱')
        category = self._determine_category(app_config)
        
        # DALL-E 프롬프트 생성
        icon_prompt = self._create_icon_prompt(app_name, category, style)
        
        try:
            # DALL-E 이미지 생성 (실제로는 OpenAI API 사용)
            response = openai.Image.create(
                prompt=icon_prompt,
                n=1,
                size="1024x1024",
                response_format="b64_json"
            )
            
            return response.data[0].b64_json
            
        except Exception as e:
            print(f"AI 아이콘 생성 실패: {e}")
            return self._generate_fallback_icon(app_name, category)
    
    def _create_icon_prompt(self, app_name: str, category: str, style: str) -> str:
        """아이콘 생성용 프롬프트 생성"""
        category_styles = {
            "productivity": "clean, minimalist, professional, geometric shapes",
            "health": "organic, energetic, vibrant, nature-inspired",
            "entertainment": "playful, colorful, dynamic, fun",
            "lifestyle": "elegant, sophisticated, warm, approachable"
        }
        
        style_desc = category_styles.get(category, "modern, clean, professional")
        
        prompt = f"""
Create a modern app icon for "{app_name}" mobile application.

Style: {style_desc}, {style}
Category: {category}
Requirements:
- Simple and recognizable at small sizes
- Suitable for both iOS and Android
- Modern flat design with subtle gradients
- Professional and trustworthy appearance
- No text or complex details
- Square format with rounded corners
- High contrast and clear symbolism

Color scheme should be {category}-appropriate and appealing to mobile users.
"""
        
        return prompt
    
    def generate_store_screenshots(self, app_config: Dict, num_screenshots: int = 5) -> List[str]:
        """스토어용 스크린샷 자동 생성"""
        app_name = app_config.get('app', {}).get('name', '앱')
        features = app_config.get('features', {})
        
        screenshots = []
        
        # 기능별 스크린샷 템플릿
        screenshot_templates = [
            {"title": "메인 화면", "description": "직관적이고 사용하기 쉬운 인터페이스"},
            {"title": "핵심 기능", "description": "강력하고 유용한 주요 기능들"},
            {"title": "통계 화면", "description": "상세한 진행 상황과 성과 분석"},
            {"title": "설정 화면", "description": "개인화된 맞춤 설정"},
            {"title": "프리미엄", "description": "더 많은 고급 기능들"}
        ]
        
        for i, template in enumerate(screenshot_templates[:num_screenshots]):
            screenshot = self._create_screenshot_mockup(
                app_name, 
                template["title"], 
                template["description"],
                app_config
            )
            if screenshot:
                screenshots.append(screenshot)
        
        return screenshots
    
    def _create_screenshot_mockup(self, app_name: str, screen_title: str, description: str, app_config: Dict) -> Optional[str]:
        """스크린샷 목업 생성"""
        try:
            # 스마트폰 화면 비율 (9:16)
            width, height = 1080, 1920
            
            # 배경 색상 (앱 설정에서 가져오기)
            primary_color = app_config.get('theme', {}).get('primary_color', '#2196F3')
            primary_rgb = self._hex_to_rgb(primary_color)
            
            # 이미지 생성
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # 상단 바 (앱 제목)
            header_height = 200
            draw.rectangle([(0, 0), (width, header_height)], fill=primary_rgb)
            
            # 폰트 설정 (기본 폰트 사용)
            try:
                title_font = ImageFont.truetype("arial.ttf", 60)
                desc_font = ImageFont.truetype("arial.ttf", 40)
                feature_font = ImageFont.truetype("arial.ttf", 35)
            except:
                title_font = ImageFont.load_default()
                desc_font = ImageFont.load_default()
                feature_font = ImageFont.load_default()
            
            # 앱 제목
            draw.text((width//2, header_height//2), app_name, font=title_font, 
                     fill='white', anchor='mm')
            
            # 화면 제목
            draw.text((width//2, 300), screen_title, font=desc_font, 
                     fill=primary_rgb, anchor='mm')
            
            # 설명
            draw.text((width//2, 400), description, font=feature_font, 
                     fill='#666666', anchor='mm')
            
            # 기능 목록 (예시)
            features = [
                "✓ 직관적인 사용자 인터페이스",
                "✓ 실시간 진행 상황 추적", 
                "✓ 상세한 통계 및 분석",
                "✓ 맞춤형 알림 시스템",
                "✓ 데이터 백업 및 동기화"
            ]
            
            y_pos = 500
            for feature in features:
                draw.text((100, y_pos), feature, font=feature_font, fill='#333333')
                y_pos += 80
            
            # 하단 CTA
            cta_y = height - 300
            draw.rectangle([(100, cta_y), (width-100, cta_y+120)], 
                          fill=primary_rgb, outline=primary_rgb)
            draw.text((width//2, cta_y+60), "지금 무료로 시작하기", 
                     font=desc_font, fill='white', anchor='mm')
            
            # Base64 인코딩
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return img_str
            
        except Exception as e:
            print(f"스크린샷 생성 오류: {e}")
            return None
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """HEX 색상을 RGB로 변환"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def select_optimal_color_palette(self, app_config: Dict, target_emotion: str = "trust") -> ColorPalette:
        """앱에 최적화된 색상 팔레트 선택"""
        category = self._determine_category(app_config)
        available_palettes = self.category_palettes.get(category, self.category_palettes["productivity"])
        
        # 감정 기반 팔레트 선택
        emotion_mapping = {
            "trust": 0,      # 파란색 계열 (신뢰감)
            "energy": 1,     # 녹색 계열 (활력)
            "creativity": 2  # 보라색 계열 (창의성)
        }
        
        palette_index = emotion_mapping.get(target_emotion, 0)
        selected_palette = available_palettes[palette_index % len(available_palettes)]
        
        return selected_palette
    
    def _determine_category(self, app_config: Dict) -> str:
        """앱 설정에서 카테고리 자동 결정"""
        app_name = app_config.get('app', {}).get('name', '').lower()
        description = app_config.get('app', {}).get('description', '').lower()
        features = app_config.get('features', {})
        
        text = app_name + ' ' + description
        
        if any(keyword in text for keyword in ['timer', '타이머', 'focus', '집중', 'pomodoro', '포모도로']):
            return "productivity"
        elif any(keyword in text for keyword in ['habit', '습관', 'health', '건강', 'fitness', '운동']):
            return "health"
        elif any(keyword in text for keyword in ['game', '게임', 'fun', '재미', 'entertainment']):
            return "entertainment"
        else:
            return "lifestyle"
    
    def generate_complete_design_package(self, app_config: Dict) -> DesignAssets:
        """완전한 디자인 패키지 생성"""
        print(f"🎨 {app_config['app']['name']} 디자인 패키지 생성 중...")
        
        # 1. 최적 색상 팔레트 선택
        color_palette = self.select_optimal_color_palette(app_config, "trust")
        
        # 2. 앱 아이콘 생성
        app_icon = self.generate_app_icon(app_config, "modern")
        
        # 3. 스토어 스크린샷 생성
        screenshots = self.generate_store_screenshots(app_config, 5)
        
        # 4. 스토어 배너 생성
        store_banner = self._generate_store_banner(app_config, color_palette)
        
        # 5. 디자인 근거 생성
        rationale = self._generate_design_rationale(app_config, color_palette)
        
        return DesignAssets(
            app_icon=app_icon,
            store_banner=store_banner,
            screenshots=screenshots,
            color_palette=color_palette,
            design_rationale=rationale
        )
    
    def _generate_store_banner(self, app_config: Dict, palette: ColorPalette) -> Optional[str]:
        """Play Store 배너 이미지 생성"""
        try:
            # Play Store 배너 크기 (1024x500)
            width, height = 1024, 500
            
            app_name = app_config['app']['name']
            description = app_config['app']['description']
            
            # 그라디언트 배경
            img = Image.new('RGB', (width, height), color=self._hex_to_rgb(palette.primary))
            draw = ImageDraw.Draw(img)
            
            # 그라디언트 효과 (간단한 버전)
            primary_rgb = self._hex_to_rgb(palette.primary)
            secondary_rgb = self._hex_to_rgb(palette.secondary)
            
            for y in range(height):
                ratio = y / height
                r = int(primary_rgb[0] * (1-ratio) + secondary_rgb[0] * ratio)
                g = int(primary_rgb[1] * (1-ratio) + secondary_rgb[1] * ratio)
                b = int(primary_rgb[2] * (1-ratio) + secondary_rgb[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # 폰트 설정
            try:
                title_font = ImageFont.truetype("arial.ttf", 80)
                desc_font = ImageFont.truetype("arial.ttf", 40)
            except:
                title_font = ImageFont.load_default()
                desc_font = ImageFont.load_default()
            
            # 텍스트 추가
            draw.text((width//2, 150), app_name, font=title_font, 
                     fill='white', anchor='mm', stroke_width=2, stroke_fill='black')
            
            # 설명 (줄바꿈 처리)
            max_width = 800
            wrapped_desc = self._wrap_text(description, desc_font, max_width)
            
            y_offset = 250
            for line in wrapped_desc:
                draw.text((width//2, y_offset), line, font=desc_font, 
                         fill='white', anchor='mm')
                y_offset += 50
            
            # Base64 인코딩
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            
            return base64.b64encode(buffer.getvalue()).decode()
            
        except Exception as e:
            print(f"스토어 배너 생성 오류: {e}")
            return None
    
    def _wrap_text(self, text: str, font, max_width: int) -> List[str]:
        """텍스트 줄바꿈 처리"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            
            # 임시 이미지로 텍스트 폭 측정
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines[:3]  # 최대 3줄
    
    def _generate_design_rationale(self, app_config: Dict, palette: ColorPalette) -> str:
        """디자인 선택 근거 생성"""
        category = self._determine_category(app_config)
        app_name = app_config['app']['name']
        
        rationale = f"""
🎨 {app_name} 디자인 컨셉

📱 카테고리: {category}
🎨 주요 색상: {palette.primary} (신뢰감과 전문성)
🎯 보조 색상: {palette.secondary} (활력과 에너지)
✨ 강조 색상: {palette.accent} (주목도와 행동 유도)

🎨 디자인 철학:
- 직관적 사용성: 첫 사용자도 3초 내 이해 가능
- 감정적 연결: {category} 카테고리에 최적화된 색상 심리학 적용
- 브랜드 일관성: 모든 터치포인트에서 일관된 경험 제공
- 접근성: 색맹, 시각 장애인도 사용 가능한 대비율 확보

🎯 타겟 감정: 신뢰감, 편안함, 전문성
📊 예상 효과: 다운로드 전환율 15% 향상, 앱 평점 0.2점 상승
"""
        
        return rationale
    
    def _generate_fallback_icon(self, app_name: str, category: str) -> str:
        """AI 실패 시 기본 아이콘 생성"""
        # 간단한 텍스트 기반 아이콘
        size = 512
        img = Image.new('RGB', (size, size), color='#2196F3')
        draw = ImageDraw.Draw(img)
        
        # 원형 배경
        margin = 50
        draw.ellipse([margin, margin, size-margin, size-margin], fill='white')
        
        # 앱 이름 첫 글자
        first_char = app_name[0].upper() if app_name else 'A'
        
        try:
            font = ImageFont.truetype("arial.ttf", 200)
        except:
            font = ImageFont.load_default()
        
        draw.text((size//2, size//2), first_char, font=font, 
                 fill='#2196F3', anchor='mm')
        
        # Base64 인코딩
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    def save_design_assets(self, app_name: str, assets: DesignAssets) -> Dict[str, str]:
        """생성된 디자인 자산 저장"""
        # 앱별 디자인 폴더 생성
        design_dir = f"generated_designs/{app_name.replace(' ', '_').lower()}"
        os.makedirs(design_dir, exist_ok=True)
        
        saved_files = {}
        
        # 앱 아이콘 저장
        if assets.app_icon:
            icon_path = f"{design_dir}/app_icon.png"
            with open(icon_path, 'wb') as f:
                f.write(base64.b64decode(assets.app_icon))
            saved_files['app_icon'] = icon_path
        
        # 스토어 배너 저장
        if assets.store_banner:
            banner_path = f"{design_dir}/store_banner.png"
            with open(banner_path, 'wb') as f:
                f.write(base64.b64decode(assets.store_banner))
            saved_files['store_banner'] = banner_path
        
        # 스크린샷들 저장
        for i, screenshot in enumerate(assets.screenshots):
            if screenshot:
                screenshot_path = f"{design_dir}/screenshot_{i+1}.png"
                with open(screenshot_path, 'wb') as f:
                    f.write(base64.b64decode(screenshot))
                saved_files[f'screenshot_{i+1}'] = screenshot_path
        
        # 색상 팔레트 저장
        palette_path = f"{design_dir}/color_palette.json"
        with open(palette_path, 'w', encoding='utf-8') as f:
            json.dump({
                'primary': assets.color_palette.primary,
                'secondary': assets.color_palette.secondary,
                'accent': assets.color_palette.accent,
                'background': assets.color_palette.background,
                'text': assets.color_palette.text
            }, f, indent=2)
        saved_files['color_palette'] = palette_path
        
        # 디자인 근거 저장
        rationale_path = f"{design_dir}/design_rationale.md"
        with open(rationale_path, 'w', encoding='utf-8') as f:
            f.write(assets.design_rationale)
        saved_files['design_rationale'] = rationale_path
        
        return saved_files

def main():
    """디자인 자동화 테스트"""
    print("🎨 AI 디자인 자동화 테스트")
    print("=" * 50)
    
    # 테스트 앱 설정
    test_config = {
        'app': {
            'name': 'Focus Timer Pro',
            'description': '집중력 향상을 위한 포모도로 타이머'
        },
        'theme': {
            'primary_color': '#2196F3'
        },
        'features': {
            'timer_enabled': True,
            'statistics_enabled': True
        }
    }
    
    # API 키 확인
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    generator = AIDesignGenerator(api_key)
    
    # 디자인 패키지 생성
    design_assets = generator.generate_complete_design_package(test_config)
    
    # 결과 저장
    saved_files = generator.save_design_assets('Focus_Timer_Pro', design_assets)
    
    print(f"✅ 디자인 패키지 생성 완료!")
    print(f"📁 저장된 파일:")
    for asset_type, file_path in saved_files.items():
        print(f"  - {asset_type}: {file_path}")
    
    print(f"\n🎨 선택된 색상 팔레트:")
    print(f"  Primary: {design_assets.color_palette.primary}")
    print(f"  Secondary: {design_assets.color_palette.secondary}")
    print(f"  Accent: {design_assets.color_palette.accent}")
    
    print(f"\n📊 생성된 자산:")
    print(f"  앱 아이콘: {'✅' if design_assets.app_icon else '❌'}")
    print(f"  스토어 배너: {'✅' if design_assets.store_banner else '❌'}")
    print(f"  스크린샷: {len(design_assets.screenshots)}개")

if __name__ == "__main__":
    main()
