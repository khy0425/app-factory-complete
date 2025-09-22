#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
키워드 필터링 및 정제 모듈
Play Store에서 추출한 키워드를 ASO에 유용한 형태로 정제
"""

import re
from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass
class KeywordScore:
    keyword: str
    relevance: float
    search_potential: float
    competition: str
    final_score: float

class KeywordFilter:
    def __init__(self):
        """키워드 필터 초기화"""
        # 불용어 (ASO에 도움이 안 되는 단어들)
        self.stopwords = {
            # 일반 불용어
            '있습니다', '합니다', '됩니다', '입니다', '해보세요', '가능합니다',
            '제공합니다', '지원합니다', '만들어', '사용하여', '통해서',
            
            # 앱 관련 일반어
            '사용자', '기능', '서비스', '시스템', '프로그램', '어플', '애플리케이션',
            '안드로이드', '아이폰', '모바일', '스마트폰', '다운로드', '설치',
            '업데이트', '버전', '개선', '수정', '추가', '삭제', '변경',
            
            # 형용사/부사
            '최고', '최적', '완벽', '훌륭', '멋진', '좋은', '나쁜', '빠른', '느린',
            '쉬운', '어려운', '간단한', '복잡한', '무료', '유료', '프리미엄',
            
            # 조사/접속사
            '그리고', '하지만', '그러나', '또한', '또는', '만약', '때문에',
            '따라서', '그래서', '하지만', '그런데', '그러면', '그럼에도'
        }
        
        # ASO 가치가 높은 키워드 패턴
        self.valuable_patterns = {
            'action': ['관리', '추적', '기록', '측정', '분석', '계획', '달성', '향상', '개선'],
            'benefit': ['효율', '생산성', '집중력', '건강', '성장', '발전', '성취', '성공'],
            'category': ['타이머', '알람', '스케줄', '캘린더', '노트', '메모', '일기', '운동'],
            'target': ['직장인', '학생', '주부', '운동선수', '개발자', '디자이너'],
            'time': ['일일', '주간', '월간', '매일', '정기', '꾸준히', '지속적'],
            'method': ['포모도로', '습관형성', '루틴', '체크리스트', '목표설정']
        }
    
    def filter_keywords(self, raw_keywords: List[Dict]) -> List[KeywordScore]:
        """원시 키워드를 필터링하고 점수화"""
        filtered_keywords = []
        
        for kw_data in raw_keywords:
            keyword = kw_data['keyword']
            
            # 기본 필터링
            if self._is_valid_keyword(keyword):
                score = self._calculate_keyword_score(keyword, kw_data)
                
                if score.final_score > 2.0:  # 임계값 이상만 선택
                    filtered_keywords.append(score)
        
        # 최종 점수순 정렬
        filtered_keywords.sort(key=lambda x: x.final_score, reverse=True)
        return filtered_keywords
    
    def _is_valid_keyword(self, keyword: str) -> bool:
        """키워드 유효성 검사"""
        # 불용어 체크
        if keyword in self.stopwords:
            return False
        
        # 길이 체크 (2-8글자)
        if len(keyword) < 2 or len(keyword) > 8:
            return False
        
        # 숫자만 있는 것 제외
        if keyword.isdigit():
            return False
        
        # 자음/모음만 있는 것 제외
        if re.match(r'^[ㄱ-ㅎㅏ-ㅣ]+$', keyword):
            return False
        
        # 특수문자가 포함된 것 제외
        if re.search(r'[^\w가-힣]', keyword):
            return False
        
        return True
    
    def _calculate_keyword_score(self, keyword: str, kw_data: Dict) -> KeywordScore:
        """키워드 점수 계산"""
        base_score = kw_data.get('score', 0)
        frequency = kw_data.get('frequency', 1)
        avg_rating = kw_data.get('avg_rating', 4.0)
        
        # 1. 관련성 점수 (패턴 매칭)
        relevance = self._calculate_relevance(keyword)
        
        # 2. 검색 잠재력 (빈도 + 평점 기반)
        search_potential = (frequency * 0.6) + (avg_rating * 0.4)
        
        # 3. 경쟁도 추정
        competition = self._estimate_competition(keyword, frequency)
        
        # 4. 최종 점수 (가중 평균)
        final_score = (relevance * 0.4) + (search_potential * 0.4) + (base_score * 0.2)
        
        return KeywordScore(
            keyword=keyword,
            relevance=relevance,
            search_potential=search_potential,
            competition=competition,
            final_score=final_score
        )
    
    def _calculate_relevance(self, keyword: str) -> float:
        """키워드 관련성 점수 계산"""
        relevance_score = 1.0  # 기본 점수
        
        # 가치 있는 패턴 매칭
        for category, patterns in self.valuable_patterns.items():
            for pattern in patterns:
                if pattern in keyword:
                    if category == 'benefit':
                        relevance_score += 2.0  # 혜택 키워드 높은 점수
                    elif category == 'action':
                        relevance_score += 1.5
                    elif category == 'category':
                        relevance_score += 1.0
                    else:
                        relevance_score += 0.5
                    break
        
        return min(relevance_score, 5.0)  # 최대 5점
    
    def _estimate_competition(self, keyword: str, frequency: int) -> str:
        """키워드 경쟁도 추정"""
        # 빈도가 높을수록 경쟁이 치열
        if frequency >= 8:
            return "high"
        elif frequency >= 4:
            return "medium" 
        else:
            return "low"
    
    def get_top_keywords_by_category(self, keywords: List[KeywordScore]) -> Dict[str, List[str]]:
        """카테고리별 상위 키워드 분류"""
        categorized = {
            'primary': [],      # 주요 키워드 (점수 4.0+)
            'secondary': [],    # 보조 키워드 (점수 3.0+)
            'long_tail': [],    # 롱테일 키워드 (점수 2.0+)
            'action_words': [], # 액션 키워드
            'benefit_words': [] # 혜택 키워드
        }
        
        for kw in keywords:
            keyword = kw.keyword
            score = kw.final_score
            
            # 점수별 분류
            if score >= 4.0:
                categorized['primary'].append(keyword)
            elif score >= 3.0:
                categorized['secondary'].append(keyword)
            elif score >= 2.0:
                categorized['long_tail'].append(keyword)
            
            # 패턴별 분류
            for pattern in self.valuable_patterns['action']:
                if pattern in keyword:
                    categorized['action_words'].append(keyword)
                    break
            
            for pattern in self.valuable_patterns['benefit']:
                if pattern in keyword:
                    categorized['benefit_words'].append(keyword)
                    break
        
        # 중복 제거 및 상위 5개씩만
        for category in categorized:
            categorized[category] = list(dict.fromkeys(categorized[category]))[:5]
        
        return categorized
    
    def generate_aso_recommendations(self, keywords: List[KeywordScore]) -> List[str]:
        """ASO 개선 추천사항 생성"""
        recommendations = []
        
        categorized = self.get_top_keywords_by_category(keywords)
        
        if categorized['primary']:
            recommendations.append(
                f"핵심 키워드 활용: {', '.join(categorized['primary'][:3])}"
            )
        
        if categorized['action_words']:
            recommendations.append(
                f"액션 키워드 강화: {', '.join(categorized['action_words'][:2])}"
            )
        
        if categorized['benefit_words']:
            recommendations.append(
                f"혜택 키워드 부각: {', '.join(categorized['benefit_words'][:2])}"
            )
        
        # 경쟁도 기반 추천
        low_competition = [kw.keyword for kw in keywords if kw.competition == 'low'][:3]
        if low_competition:
            recommendations.append(
                f"저경쟁 키워드 공략: {', '.join(low_competition)}"
            )
        
        return recommendations

def main():
    """키워드 필터링 테스트"""
    print("🔍 키워드 필터링 테스트")
    print("=" * 40)
    
    # 이전 분석 결과 로드
    try:
        with open('aso_analysis_20250920_045305.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
    except:
        print("❌ 이전 분석 결과 파일을 찾을 수 없습니다.")
        return
    
    filter_engine = KeywordFilter()
    
    # 키워드 필터링 적용
    filtered_keywords = filter_engine.filter_keywords(analysis_data['top_keywords'])
    
    print(f"📊 필터링 결과:")
    print(f"  원본 키워드: {len(analysis_data['top_keywords'])}개")
    print(f"  필터링 후: {len(filtered_keywords)}개")
    
    print(f"\n🏆 정제된 상위 키워드:")
    for i, kw in enumerate(filtered_keywords[:10], 1):
        print(f"  {i:2d}. {kw.keyword} (점수: {kw.final_score:.1f}, 경쟁도: {kw.competition})")
    
    # 카테고리별 분류
    categorized = filter_engine.get_top_keywords_by_category(filtered_keywords)
    
    print(f"\n📂 카테고리별 키워드:")
    for category, keywords in categorized.items():
        if keywords:
            print(f"  {category}: {', '.join(keywords)}")
    
    # ASO 추천사항
    recommendations = filter_engine.generate_aso_recommendations(filtered_keywords)
    
    print(f"\n🎯 ASO 추천사항:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    # 최종 결과를 새 파일로 저장
    filtered_result = {
        'filtered_keywords': [
            {
                'keyword': kw.keyword,
                'final_score': kw.final_score,
                'relevance': kw.relevance,
                'search_potential': kw.search_potential,
                'competition': kw.competition
            }
            for kw in filtered_keywords
        ],
        'categorized_keywords': categorized,
        'aso_recommendations': recommendations,
        'filter_applied_at': datetime.now().isoformat()
    }
    
    with open('filtered_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 필터링 결과 저장: filtered_keywords.json")

if __name__ == "__main__":
    import json
    from datetime import datetime
    main()
