#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Play Store 리뷰 모니터링 및 자동 응답 시스템
부정 리뷰 자동 대응, 긍정 리뷰 감사 메시지
"""

import requests
import json
import openai
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import time

class ReviewSentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass
class Review:
    review_id: str
    user_name: str
    rating: int
    content: str
    date: datetime
    sentiment: ReviewSentiment
    response: Optional[str] = None
    
@dataclass
class ReviewResponse:
    response_text: str
    tone: str
    should_respond: bool

class ReviewMonitor:
    def __init__(self, openai_api_key: str, play_console_credentials: Optional[Dict] = None):
        """리뷰 모니터 초기화"""
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.play_console_credentials = play_console_credentials
        
    def analyze_sentiment(self, review_text: str, rating: int) -> ReviewSentiment:
        """리뷰 감정 분석"""
        # 평점 기반 1차 분류
        if rating >= 4:
            base_sentiment = ReviewSentiment.POSITIVE
        elif rating <= 2:
            base_sentiment = ReviewSentiment.NEGATIVE
        else:
            base_sentiment = ReviewSentiment.NEUTRAL
        
        # 텍스트 기반 감정 분석 (간단한 키워드 방식)
        positive_keywords = ['좋', '훌륭', '완벽', '최고', '추천', '만족', '편리', '유용']
        negative_keywords = ['나쁨', '최악', '실망', '버그', '느림', '불편', '짜증', '환불']
        
        review_lower = review_text.lower()
        positive_count = sum(1 for kw in positive_keywords if kw in review_lower)
        negative_count = sum(1 for kw in negative_keywords if kw in review_lower)
        
        # 키워드 기반 조정
        if negative_count > positive_count and negative_count > 0:
            return ReviewSentiment.NEGATIVE
        elif positive_count > negative_count and positive_count > 0:
            return ReviewSentiment.POSITIVE
        
        return base_sentiment
    
    def generate_review_response(self, review: Review, app_name: str) -> ReviewResponse:
        """리뷰에 대한 자동 응답 생성"""
        if review.sentiment == ReviewSentiment.POSITIVE:
            return self._generate_positive_response(review, app_name)
        elif review.sentiment == ReviewSentiment.NEGATIVE:
            return self._generate_negative_response(review, app_name)
        else:
            return self._generate_neutral_response(review, app_name)
    
    def _generate_positive_response(self, review: Review, app_name: str) -> ReviewResponse:
        """긍정 리뷰 응답 생성"""
        templates = [
            f"{review.user_name}님, {app_name}을 사랑해주셔서 감사합니다! 🙏 앞으로도 더 좋은 서비스로 보답하겠습니다.",
            f"소중한 리뷰 감사드려요! {review.user_name}님 같은 사용자분들 덕분에 {app_name}이 더욱 발전할 수 있습니다. ❤️",
            f"⭐⭐⭐⭐⭐ 리뷰 정말 감사합니다! {review.user_name}님의 피드백이 저희에게 큰 힘이 됩니다. 계속 좋은 앱으로 찾아뵙겠어요!",
        ]
        
        # 평점이 5점인 경우 더 감사 표현
        if review.rating == 5:
            response_text = templates[2]  # 가장 감사한 응답
        else:
            response_text = templates[0]
        
        return ReviewResponse(
            response_text=response_text,
            tone="grateful",
            should_respond=True
        )
    
    def _generate_negative_response(self, review: Review, app_name: str) -> ReviewResponse:
        """부정 리뷰 응답 생성 (AI 활용)"""
        prompt = f"""
다음 부정적인 앱 리뷰에 대한 정중하고 해결책 중심의 응답을 한국어로 작성해주세요:

앱 이름: {app_name}
사용자: {review.user_name}
평점: {review.rating}/5
리뷰 내용: "{review.content}"

응답 가이드라인:
1. 정중하고 공감하는 톤
2. 구체적인 해결책 제시
3. 개선 의지 표현
4. 연락처나 피드백 채널 안내
5. 150자 이내로 간결하게
6. 사과 표현 포함

응답 형식: 일반적인 고객 서비스 응답 스타일
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.6
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            return ReviewResponse(
                response_text=ai_response,
                tone="apologetic_helpful",
                should_respond=True
            )
            
        except Exception as e:
            print(f"AI 응답 생성 오류: {e}")
            return self._generate_fallback_negative_response(review, app_name)
    
    def _generate_fallback_negative_response(self, review: Review, app_name: str) -> ReviewResponse:
        """AI 실패시 기본 부정 리뷰 응답"""
        response_text = f"""
{review.user_name}님, 불편을 끼쳐드려 죄송합니다. 말씀해주신 문제를 개발팀에 전달하여 빠른 시일 내에 개선하도록 하겠습니다. 
추가 문의사항이 있으시면 언제든 연락 주세요. {app_name}을 더 나은 앱으로 만들어가겠습니다.
"""
        
        return ReviewResponse(
            response_text=response_text,
            tone="apologetic",
            should_respond=True
        )
    
    def _generate_neutral_response(self, review: Review, app_name: str) -> ReviewResponse:
        """중립 리뷰 응답 (선택적 응답)"""
        # 중립 리뷰는 내용에 따라 응답 여부 결정
        if len(review.content) < 10:  # 너무 짧은 리뷰는 응답하지 않음
            return ReviewResponse(
                response_text="",
                tone="neutral",
                should_respond=False
            )
        
        response_text = f"{review.user_name}님, 소중한 피드백 감사드립니다. 더 나은 {app_name}을 위해 지속적으로 개선해나가겠습니다!"
        
        return ReviewResponse(
            response_text=response_text,
            tone="neutral",
            should_respond=True
        )
    
    def fetch_recent_reviews(self, package_name: str, days: int = 7) -> List[Review]:
        """최근 리뷰 가져오기 (실제로는 Play Console API 사용)"""
        # 여기서는 예시 데이터 제공
        sample_reviews = [
            Review(
                review_id="review_1",
                user_name="김철수",
                rating=5,
                content="정말 유용한 앱이네요! 집중력이 많이 향상됐어요.",
                date=datetime.now() - timedelta(days=1),
                sentiment=ReviewSentiment.POSITIVE
            ),
            Review(
                review_id="review_2",
                user_name="박영희",
                rating=2,
                content="자꾸 앱이 꺼져요. 버그 수정 부탁드립니다.",
                date=datetime.now() - timedelta(days=2),
                sentiment=ReviewSentiment.NEGATIVE
            ),
            Review(
                review_id="review_3",
                user_name="이민수",
                rating=4,
                content="전반적으로 괜찮은데 UI가 조금 아쉬워요",
                date=datetime.now() - timedelta(days=3),
                sentiment=ReviewSentiment.POSITIVE
            )
        ]
        
        return sample_reviews
    
    def process_reviews_batch(self, package_name: str, app_name: str) -> Dict[str, int]:
        """리뷰 일괄 처리"""
        reviews = self.fetch_recent_reviews(package_name)
        
        processed_count = {
            'total': len(reviews),
            'positive_responses': 0,
            'negative_responses': 0,
            'no_response': 0
        }
        
        for review in reviews:
            # 감정 분석
            review.sentiment = self.analyze_sentiment(review.content, review.rating)
            
            # 응답 생성
            response = self.generate_review_response(review, app_name)
            
            if response.should_respond:
                # 실제로는 Play Console API로 응답 전송
                print(f"[{review.sentiment.value}] {review.user_name}: {response.response_text}")
                
                if review.sentiment == ReviewSentiment.POSITIVE:
                    processed_count['positive_responses'] += 1
                else:
                    processed_count['negative_responses'] += 1
            else:
                processed_count['no_response'] += 1
        
        return processed_count
    
    def generate_review_summary_report(self, package_name: str, days: int = 30) -> Dict:
        """리뷰 요약 리포트 생성"""
        reviews = self.fetch_recent_reviews(package_name, days)
        
        sentiment_count = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_reviews = len(reviews)
        
        for review in reviews:
            sentiment = self.analyze_sentiment(review.content, review.rating)
            sentiment_count[sentiment.value] += 1
            rating_distribution[review.rating] += 1
        
        average_rating = sum(rating * count for rating, count in rating_distribution.items()) / total_reviews if total_reviews > 0 else 0
        
        return {
            'period_days': days,
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 2),
            'sentiment_distribution': sentiment_count,
            'rating_distribution': rating_distribution,
            'response_rate': 85,  # 예시 응답률
            'generated_at': datetime.now().isoformat()
        }
    
    def schedule_review_monitoring(self, apps_config: List[Dict], check_interval_hours: int = 6):
        """정기적 리뷰 모니터링 스케줄링"""
        print(f"리뷰 모니터링 스케줄 설정: {check_interval_hours}시간마다 확인")
        
        for app_config in apps_config:
            package_name = app_config.get('app', {}).get('package_name', '')
            app_name = app_config.get('app', {}).get('name', '')
            
            print(f"모니터링 대상: {app_name} ({package_name})")
            
        # TODO: 실제 스케줄러 구현 (cron, APScheduler 등)

def main():
    """테스트 실행"""
    api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
    monitor = ReviewMonitor(api_key)
    
    # 리뷰 처리 테스트
    result = monitor.process_reviews_batch('com.example.focustimer', 'Focus Timer Pro')
    print(f"처리 결과: {result}")
    
    # 리포트 생성 테스트
    report = monitor.generate_review_summary_report('com.example.focustimer')
    print(f"리뷰 요약: {json.dumps(report, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()
