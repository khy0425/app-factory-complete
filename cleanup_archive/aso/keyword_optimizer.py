#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASO 키워드 최적화 자동화 모듈
Play Store 경쟁 앱 분석 및 키워드 추출
"""

import requests
import json
import time
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import openai
import os

@dataclass
class KeywordData:
    keyword: str
    relevance_score: float
    competition_level: str
    search_volume: int
    
@dataclass
class AppMetadata:
    title: str
    description: str
    keywords: List[str]
    category: str

class PlayStoreASO:
    def __init__(self, openai_api_key: str):
        """ASO 최적화 클래스 초기화"""
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.session = requests.Session()
        
    def analyze_competitor_apps(self, category: str, app_type: str) -> List[Dict]:
        """경쟁 앱 분석 및 키워드 추출"""
        # 실제로는 Play Store API나 크롤링 도구 사용
        # 여기서는 예시 데이터 제공
        
        competitor_data = {
            "timer": [
                {"title": "Forest: Focus for Productivity", "keywords": ["집중", "타이머", "포모도로", "생산성"]},
                {"title": "Be Focused", "keywords": ["집중", "시간관리", "업무", "효율성"]},
                {"title": "Focus Keeper", "keywords": ["집중력", "타이머", "휴식", "작업"]}
            ],
            "habit": [
                {"title": "Habitica", "keywords": ["습관", "루틴", "목표", "동기부여"]},
                {"title": "Streaks", "keywords": ["연속기록", "습관추적", "일일목표", "성취"]},
                {"title": "Way of Life", "keywords": ["생활습관", "기록", "패턴", "개선"]}
            ]
        }
        
        return competitor_data.get(app_type, [])
    
    def extract_trending_keywords(self, category: str) -> List[KeywordData]:
        """트렌딩 키워드 추출"""
        # Google Trends API나 Play Store 검색 순위 데이터 활용
        trending_keywords = [
            KeywordData("집중력 향상", 8.5, "medium", 12000),
            KeywordData("시간 관리", 9.2, "high", 25000),
            KeywordData("생산성 앱", 7.8, "medium", 8500),
            KeywordData("포모도로", 6.5, "low", 5200),
            KeywordData("습관 형성", 8.1, "medium", 15000),
            KeywordData("목표 달성", 7.9, "medium", 11000),
        ]
        
        return trending_keywords
    
    def generate_optimized_description(self, app_config: Dict, keywords: List[str]) -> str:
        """AI를 활용한 최적화된 앱 설명 생성"""
        app_name = app_config.get('app', {}).get('name', '앱')
        app_description = app_config.get('app', {}).get('description', '')
        
        prompt = f"""
다음 정보를 바탕으로 Google Play Store용 앱 설명을 한국어로 작성해주세요:

앱 이름: {app_name}
기본 설명: {app_description}
타겟 키워드: {', '.join(keywords)}

요구사항:
1. 첫 문장에 핵심 키워드 포함
2. 사용자 혜택 중심으로 작성
3. 감정적 어필 포함
4. 150자 이내 요약 + 상세 설명
5. 자연스러운 키워드 배치

형식:
[요약] (150자 이내)
[상세설명] (500자 내외)
[주요기능] (불릿 포인트)
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"GPT API 오류: {e}")
            return self._generate_fallback_description(app_config, keywords)
    
    def _generate_fallback_description(self, app_config: Dict, keywords: List[str]) -> str:
        """API 실패 시 기본 설명 생성"""
        app_name = app_config.get('app', {}).get('name', '앱')
        keyword_text = ', '.join(keywords[:3])
        
        return f"""
[요약]
{app_name}으로 {keyword_text}을 쉽고 효과적으로 관리하세요! 간단한 인터페이스와 강력한 기능으로 당신의 목표 달성을 도와드립니다.

[상세설명]
{app_name}은 {keyword_text}에 특화된 앱입니다. 직관적인 디자인과 사용하기 쉬운 기능들로 누구나 쉽게 사용할 수 있습니다.

[주요기능]
• 간편한 {keywords[0]} 관리
• 진행상황 추적 및 통계
• 알림 및 리마인더
• 데이터 백업 및 복원
"""

    def generate_app_title_variants(self, base_title: str, keywords: List[str]) -> List[str]:
        """앱 제목 변형 버전 생성 (A/B 테스트용)"""
        variants = [base_title]  # 원본
        
        # 키워드 조합 버전들
        for keyword in keywords[:3]:
            if keyword not in base_title:
                variants.append(f"{base_title} - {keyword}")
                variants.append(f"{keyword} {base_title}")
        
        return variants[:5]  # 최대 5개 버전
    
    def update_app_config_with_aso(self, config_path: str, app_type: str) -> Dict:
        """앱 설정에 ASO 최적화 적용"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 1. 경쟁 앱 분석
        competitors = self.analyze_competitor_apps("productivity", app_type)
        
        # 2. 키워드 추출
        all_keywords = []
        for comp in competitors:
            all_keywords.extend(comp.get('keywords', []))
        
        # 중복 제거 및 빈도순 정렬
        keyword_freq = {}
        for kw in all_keywords:
            keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
        
        top_keywords = sorted(keyword_freq.keys(), key=lambda x: keyword_freq[x], reverse=True)[:10]
        
        # 3. 최적화된 설명 생성
        optimized_desc = self.generate_optimized_description(config, top_keywords)
        
        # 4. 설정 업데이트
        config['marketing'] = {
            'keywords': top_keywords,
            'optimized_description': optimized_desc,
            'title_variants': self.generate_app_title_variants(config['app']['name'], top_keywords),
            'last_updated': datetime.now().isoformat(),
            'competitor_analysis': competitors
        }
        
        return config
    
    def schedule_keyword_update(self, config_paths: List[str], interval_days: int = 14):
        """정기적 키워드 업데이트 스케줄링"""
        # 실제로는 cron job이나 스케줄러 사용
        for config_path in config_paths:
            print(f"키워드 업데이트 예약: {config_path}")
            # TODO: 스케줄러 구현

def main():
    """테스트 실행"""
    api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
    aso = PlayStoreASO(api_key)
    
    # 타이머 앱 최적화 테스트
    config_path = "../assets/config/timer_app_template.json"
    if os.path.exists(config_path):
        optimized_config = aso.update_app_config_with_aso(config_path, "timer")
        
        # 결과 저장
        output_path = config_path.replace('.json', '_optimized.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(optimized_config, f, ensure_ascii=False, indent=2)
        
        print(f"ASO 최적화 완료: {output_path}")
        print(f"추천 키워드: {optimized_config['marketing']['keywords']}")

if __name__ == "__main__":
    main()
