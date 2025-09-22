#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고급 KPI 추적 모듈
LTV, 바이럴 계수, 시장 포화도, 트렌드 점수 등 예측 지표
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import requests
import json

@dataclass
class AdvancedKPI:
    app_name: str
    ltv: float  # 생애가치 (원)
    viral_coefficient: float  # 바이럴 계수
    market_saturation: float  # 시장 포화도 (0-1)
    trend_score: float  # 트렌드 점수 (0-100)
    predicted_monthly_revenue: float  # 예측 월 수익
    confidence_level: float  # 예측 신뢰도 (0-1)

class AdvancedKPITracker:
    def __init__(self):
        """고급 KPI 추적기 초기화"""
        self.google_trends_keywords = [
            "타이머", "집중력", "포모도로", "생산성", "시간관리",
            "습관", "루틴", "건강", "운동", "다이어트",
            "할일", "메모", "목표", "계획", "관리"
        ]
        
    def calculate_ltv(self, app_data: Dict) -> float:
        """사용자 생애가치(LTV) 계산"""
        # 기본 지표
        daily_downloads = app_data.get('daily_downloads', 50)
        retention_7day = app_data.get('retention_7day', 0.35)
        retention_30day = app_data.get('retention_30day', 0.15)
        avg_session_revenue = app_data.get('avg_session_revenue', 0.05)  # 세션당 평균 수익
        avg_sessions_per_user = app_data.get('avg_sessions_per_user', 3.5)
        
        # LTV 계산 공식
        # LTV = (평균 세션 수익 × 일일 세션 수 × 평균 생존 기간)
        avg_lifetime_days = self._calculate_user_lifetime(retention_7day, retention_30day)
        total_sessions = avg_sessions_per_user * avg_lifetime_days
        ltv = avg_session_revenue * total_sessions
        
        return round(ltv, 2)
    
    def _calculate_user_lifetime(self, retention_7day: float, retention_30day: float) -> float:
        """사용자 평균 생존 기간 계산"""
        # 지수 감소 모델 사용
        if retention_30day <= 0:
            return 7.0
        
        # 일일 이탈률 계산
        daily_churn_rate = 1 - (retention_30day / retention_7day) ** (1/23)  # 7일~30일 기간
        
        # 평균 생존 기간 = 1 / 이탈률
        avg_lifetime = 1 / max(daily_churn_rate, 0.01)  # 최소 1% 이탈률
        
        return min(avg_lifetime, 365)  # 최대 1년
    
    def calculate_viral_coefficient(self, app_data: Dict) -> float:
        """바이럴 계수 계산"""
        # 바이럴 계수 = 기존 사용자가 초대하는 새 사용자 수
        
        share_rate = app_data.get('share_rate', 0.05)  # 사용자 중 공유하는 비율
        conversion_rate = app_data.get('share_conversion_rate', 0.15)  # 공유 링크 클릭 시 설치율
        
        # 소셜 기능이 있는지 확인
        has_social_features = app_data.get('social_features_enabled', True)
        
        base_viral_coefficient = share_rate * conversion_rate
        
        # 앱 품질에 따른 조정
        app_rating = app_data.get('rating', 4.0)
        quality_multiplier = max(0.5, (app_rating - 2.5) / 2.5)  # 2.5점 이상부터 바이럴 효과
        
        viral_coefficient = base_viral_coefficient * quality_multiplier
        
        if not has_social_features:
            viral_coefficient *= 0.3  # 소셜 기능 없으면 30%로 감소
        
        return round(viral_coefficient, 3)
    
    def calculate_market_saturation(self, category: str, app_data: Dict) -> float:
        """시장 포화도 분석"""
        # 카테고리별 경쟁 앱 수 (추정)
        category_competition = {
            "productivity": {"total_apps": 15000, "top_apps": 50},
            "health": {"total_apps": 25000, "top_apps": 100},
            "entertainment": {"total_apps": 50000, "top_apps": 200},
            "lifestyle": {"total_apps": 20000, "top_apps": 80}
        }
        
        competition_data = category_competition.get(category, {"total_apps": 10000, "top_apps": 50})
        
        # 앱의 현재 순위 추정 (다운로드 기반)
        daily_downloads = app_data.get('daily_downloads', 50)
        
        if daily_downloads >= 1000:
            estimated_rank = 10  # 상위 10위
        elif daily_downloads >= 500:
            estimated_rank = 25
        elif daily_downloads >= 200:
            estimated_rank = 50
        elif daily_downloads >= 100:
            estimated_rank = 100
        else:
            estimated_rank = 500
        
        # 포화도 계산 (0: 경쟁 없음, 1: 완전 포화)
        saturation = min(estimated_rank / competition_data["total_apps"], 1.0)
        
        return round(saturation, 3)
    
    def calculate_trend_score(self, keywords: List[str], category: str) -> float:
        """트렌드 점수 계산 (Google Trends 기반)"""
        # 실제로는 Google Trends API 사용
        # 여기서는 키워드 기반 추정
        
        trending_keywords = {
            "AI": 95, "인공지능": 90, "자동화": 85,
            "집중력": 80, "생산성": 75, "시간관리": 70,
            "습관": 78, "루틴": 65, "건강": 72,
            "명상": 68, "운동": 75, "다이어트": 70,
            "포모도로": 60, "타이머": 55, "알람": 50
        }
        
        # 앱 키워드의 트렌드 점수 평균
        keyword_scores = []
        for keyword in keywords:
            score = trending_keywords.get(keyword, 30)  # 기본 점수 30
            keyword_scores.append(score)
        
        if not keyword_scores:
            return 50.0  # 기본값
        
        base_score = sum(keyword_scores) / len(keyword_scores)
        
        # 카테고리별 트렌드 보정
        category_trends = {
            "productivity": 1.2,  # 생산성 앱 트렌드 상승
            "health": 1.1,       # 건강 앱 꾸준한 인기
            "entertainment": 0.9, # 엔터테인먼트 포화
            "lifestyle": 1.0     # 라이프스타일 평균
        }
        
        trend_multiplier = category_trends.get(category, 1.0)
        final_score = base_score * trend_multiplier
        
        return round(min(final_score, 100), 1)
    
    def predict_monthly_revenue(self, app_data: Dict, months_ahead: int = 3) -> Tuple[float, float]:
        """월 수익 예측 (기계학습 스타일 예측)"""
        # 현재 성과 지표
        current_daily_downloads = app_data.get('daily_downloads', 50)
        current_retention = app_data.get('retention_7day', 0.35)
        current_rating = app_data.get('rating', 4.0)
        viral_coefficient = self.calculate_viral_coefficient(app_data)
        
        # 성장률 예측
        base_growth_rate = 0.05  # 월 5% 기본 성장
        
        # 바이럴 효과에 따른 성장률 조정
        viral_boost = viral_coefficient * 2  # 바이럴 계수 × 2
        adjusted_growth_rate = base_growth_rate + viral_boost
        
        # 평점에 따른 성장률 조정
        rating_multiplier = max(0.5, (current_rating - 2.0) / 3.0)
        final_growth_rate = adjusted_growth_rate * rating_multiplier
        
        # 월별 예측
        predicted_downloads = current_daily_downloads
        predicted_revenues = []
        
        for month in range(1, months_ahead + 1):
            # 성장률 적용 (점진적 감소)
            growth_decay = 0.9 ** (month - 1)  # 성장률 점진적 감소
            monthly_growth = final_growth_rate * growth_decay
            
            predicted_downloads *= (1 + monthly_growth)
            
            # 수익 계산
            monthly_active_users = predicted_downloads * 30 * current_retention
            revenue_per_user_per_month = app_data.get('revenue_per_user', 1.5)
            monthly_revenue = monthly_active_users * revenue_per_user_per_month
            
            predicted_revenues.append(monthly_revenue)
        
        final_prediction = predicted_revenues[-1] if predicted_revenues else 0
        
        # 신뢰도 계산 (데이터 품질 기반)
        data_completeness = len([v for v in app_data.values() if v is not None]) / len(app_data)
        confidence = min(data_completeness * 0.8, 0.9)  # 최대 90% 신뢰도
        
        return round(final_prediction, 2), round(confidence, 2)
    
    def generate_comprehensive_kpi_report(self, app_config: Dict, performance_data: Dict) -> AdvancedKPI:
        """종합 KPI 리포트 생성"""
        app_name = app_config['app']['name']
        category = self._determine_category(app_config)
        keywords = app_config.get('marketing', {}).get('aso_keywords', [])
        
        # 각 KPI 계산
        ltv = self.calculate_ltv(performance_data)
        viral_coeff = self.calculate_viral_coefficient(performance_data)
        market_sat = self.calculate_market_saturation(category, performance_data)
        trend_score = self.calculate_trend_score(keywords, category)
        predicted_revenue, confidence = self.predict_monthly_revenue(performance_data, 3)
        
        return AdvancedKPI(
            app_name=app_name,
            ltv=ltv,
            viral_coefficient=viral_coeff,
            market_saturation=market_sat,
            trend_score=trend_score,
            predicted_monthly_revenue=predicted_revenue,
            confidence_level=confidence
        )
    
    def _determine_category(self, app_config: Dict) -> str:
        """앱 카테고리 결정"""
        app_name = app_config.get('app', {}).get('name', '').lower()
        description = app_config.get('app', {}).get('description', '').lower()
        
        text = app_name + ' ' + description
        
        if any(keyword in text for keyword in ['timer', '타이머', 'focus', '집중', 'productivity', '생산성']):
            return "productivity"
        elif any(keyword in text for keyword in ['habit', '습관', 'health', '건강', 'fitness', '운동']):
            return "health"
        elif any(keyword in text for keyword in ['game', '게임', 'fun', '재미']):
            return "entertainment"
        else:
            return "lifestyle"
    
    def create_success_probability_matrix(self, apps_data: List[Dict]) -> pd.DataFrame:
        """앱별 성공 확률 매트릭스 생성"""
        matrix_data = []
        
        for app_data in apps_data:
            app_config = app_data['config']
            performance = app_data['performance']
            
            kpi = self.generate_comprehensive_kpi_report(app_config, performance)
            
            # 성공 확률 계산 (여러 지표 종합)
            success_factors = {
                'ltv_score': min(kpi.ltv / 5000, 1.0),  # LTV 5000원 기준
                'viral_score': min(kpi.viral_coefficient / 0.5, 1.0),  # 바이럴 계수 0.5 기준
                'market_score': 1 - kpi.market_saturation,  # 포화도 낮을수록 좋음
                'trend_score': kpi.trend_score / 100,  # 트렌드 점수
                'rating_score': min((performance.get('rating', 4.0) - 3.0) / 2.0, 1.0)  # 평점 3점 이상
            }
            
            # 가중 평균으로 종합 성공 확률 계산
            weights = {'ltv_score': 0.25, 'viral_score': 0.2, 'market_score': 0.2, 'trend_score': 0.2, 'rating_score': 0.15}
            success_probability = sum(score * weights[factor] for factor, score in success_factors.items())
            
            matrix_data.append({
                'app_name': kpi.app_name,
                'ltv': kpi.ltv,
                'viral_coefficient': kpi.viral_coefficient,
                'market_saturation': kpi.market_saturation,
                'trend_score': kpi.trend_score,
                'predicted_revenue': kpi.predicted_monthly_revenue,
                'confidence': kpi.confidence_level,
                'success_probability': round(success_probability, 3),
                'recommendation': self._generate_recommendation(success_probability, kpi)
            })
        
        return pd.DataFrame(matrix_data)
    
    def _generate_recommendation(self, success_prob: float, kpi: AdvancedKPI) -> str:
        """성공 확률 기반 추천사항 생성"""
        if success_prob >= 0.8:
            return "🚀 고투자 추천 - 마케팅 예산 집중"
        elif success_prob >= 0.6:
            return "✅ 안정적 - 점진적 확장"
        elif success_prob >= 0.4:
            return "⚠️ 개선 필요 - ASO/UX 최적화"
        elif success_prob >= 0.2:
            return "🔄 피벗 고려 - 타겟 변경"
        else:
            return "❌ 중단 권장 - 리소스 재배치"
    
    def analyze_portfolio_risk(self, apps_kpi: List[AdvancedKPI]) -> Dict:
        """포트폴리오 리스크 분석"""
        if not apps_kpi:
            return {"error": "분석할 앱 데이터 없음"}
        
        # 리스크 지표 계산
        ltv_variance = np.var([kpi.ltv for kpi in apps_kpi])
        avg_market_saturation = np.mean([kpi.market_saturation for kpi in apps_kpi])
        trend_diversity = len(set(kpi.trend_score // 20 for kpi in apps_kpi))  # 트렌드 다양성
        
        # 수익 집중도 (지니 계수)
        revenues = [kpi.predicted_monthly_revenue for kpi in apps_kpi]
        gini_coefficient = self._calculate_gini_coefficient(revenues)
        
        # 리스크 레벨 결정
        risk_factors = {
            'revenue_concentration': gini_coefficient,  # 수익 집중도 (높을수록 위험)
            'market_saturation': avg_market_saturation,  # 시장 포화도
            'ltv_instability': min(ltv_variance / 10000, 1.0),  # LTV 변동성
            'trend_diversity': max(0, (5 - trend_diversity) / 5)  # 트렌드 다양성 부족
        }
        
        overall_risk = sum(risk_factors.values()) / len(risk_factors)
        
        risk_level = "낮음" if overall_risk < 0.3 else "보통" if overall_risk < 0.6 else "높음"
        
        return {
            'overall_risk_score': round(overall_risk, 3),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'recommendations': self._generate_risk_recommendations(risk_factors),
            'diversification_needed': overall_risk > 0.5
        }
    
    def _calculate_gini_coefficient(self, values: List[float]) -> float:
        """지니 계수 계산 (불평등 지수)"""
        if not values or len(values) < 2:
            return 0.0
        
        values = sorted(values)
        n = len(values)
        cumsum = np.cumsum(values)
        
        return (n + 1 - 2 * sum(cumsum) / cumsum[-1]) / n if cumsum[-1] > 0 else 0.0
    
    def _generate_risk_recommendations(self, risk_factors: Dict) -> List[str]:
        """리스크 기반 추천사항 생성"""
        recommendations = []
        
        if risk_factors['revenue_concentration'] > 0.6:
            recommendations.append("수익 다변화: 더 많은 앱 카테고리 진출 필요")
        
        if risk_factors['market_saturation'] > 0.7:
            recommendations.append("블루오션 탐색: 경쟁이 적은 틈새 시장 공략")
        
        if risk_factors['ltv_instability'] > 0.5:
            recommendations.append("사용자 유지율 개선: 리텐션 전략 강화")
        
        if risk_factors['trend_diversity'] > 0.6:
            recommendations.append("트렌드 다양화: 다양한 키워드 영역 확장")
        
        return recommendations
    
    def create_kpi_alerts(self, current_kpi: AdvancedKPI, previous_kpi: Optional[AdvancedKPI] = None) -> List[Dict]:
        """KPI 기반 알림 생성"""
        alerts = []
        
        # 절대적 임계값 알림
        if current_kpi.ltv < 1000:
            alerts.append({
                "level": "warning",
                "message": f"{current_kpi.app_name}: LTV 너무 낮음 (₩{current_kpi.ltv:,.0f})",
                "action": "사용자 유지율 개선 또는 수익화 모델 변경 필요"
            })
        
        if current_kpi.market_saturation > 0.8:
            alerts.append({
                "level": "critical",
                "message": f"{current_kpi.app_name}: 시장 포화도 위험 ({current_kpi.market_saturation:.1%})",
                "action": "차별화 전략 또는 새로운 시장 진출 고려"
            })
        
        if current_kpi.trend_score < 40:
            alerts.append({
                "level": "info",
                "message": f"{current_kpi.app_name}: 트렌드 점수 낮음 ({current_kpi.trend_score}점)",
                "action": "키워드 최적화 또는 기능 업데이트 고려"
            })
        
        # 변화율 기반 알림 (이전 데이터가 있는 경우)
        if previous_kpi:
            ltv_change = (current_kpi.ltv - previous_kpi.ltv) / previous_kpi.ltv if previous_kpi.ltv > 0 else 0
            
            if ltv_change < -0.2:  # 20% 이상 감소
                alerts.append({
                    "level": "critical",
                    "message": f"{current_kpi.app_name}: LTV 급감 ({ltv_change:.1%})",
                    "action": "긴급 사용자 분석 및 개선 조치 필요"
                })
            elif ltv_change > 0.3:  # 30% 이상 증가
                alerts.append({
                    "level": "success",
                    "message": f"{current_kpi.app_name}: LTV 급상승 ({ltv_change:.1%})",
                    "action": "성공 요인 분석 및 다른 앱에 적용"
                })
        
        return alerts
    
    def calculate_portfolio_optimization_score(self, apps_kpi: List[AdvancedKPI]) -> Dict:
        """포트폴리오 최적화 점수"""
        if len(apps_kpi) < 2:
            return {"error": "최소 2개 앱 필요"}
        
        # 다양성 점수
        categories = [self._determine_category_from_kpi(kpi) for kpi in apps_kpi]
        category_diversity = len(set(categories)) / 4  # 최대 4개 카테고리
        
        # 수익 안정성 점수
        revenues = [kpi.predicted_monthly_revenue for kpi in apps_kpi]
        revenue_stability = 1 - (np.std(revenues) / np.mean(revenues)) if np.mean(revenues) > 0 else 0
        
        # 성장 잠재력 점수
        avg_trend_score = np.mean([kpi.trend_score for kpi in apps_kpi])
        growth_potential = avg_trend_score / 100
        
        # 종합 최적화 점수
        optimization_score = (category_diversity * 0.3 + 
                            revenue_stability * 0.4 + 
                            growth_potential * 0.3)
        
        return {
            'optimization_score': round(optimization_score, 3),
            'category_diversity': round(category_diversity, 3),
            'revenue_stability': round(revenue_stability, 3),
            'growth_potential': round(growth_potential, 3),
            'grade': self._get_optimization_grade(optimization_score)
        }
    
    def _get_optimization_grade(self, score: float) -> str:
        """최적화 점수 등급"""
        if score >= 0.8:
            return "A+ (최적화)"
        elif score >= 0.7:
            return "A (우수)"
        elif score >= 0.6:
            return "B+ (양호)"
        elif score >= 0.5:
            return "B (보통)"
        elif score >= 0.4:
            return "C+ (개선 필요)"
        else:
            return "C (재구성 필요)"
    
    def _determine_category_from_kpi(self, kpi: AdvancedKPI) -> str:
        """KPI에서 카테고리 추정"""
        # 간단한 휴리스틱 (실제로는 더 정교한 분류 필요)
        if kpi.trend_score > 70:
            return "productivity"
        elif kpi.viral_coefficient > 0.3:
            return "entertainment"
        elif kpi.ltv > 3000:
            return "health"
        else:
            return "lifestyle"

def main():
    """고급 KPI 추적 테스트"""
    print("📊 고급 KPI 추적 테스트")
    print("=" * 50)
    
    tracker = AdvancedKPITracker()
    
    # 테스트 데이터
    test_apps = [
        {
            'config': {
                'app': {'name': 'Focus Timer Pro', 'description': '집중력 향상 타이머'},
                'marketing': {'aso_keywords': ['타이머', '집중력', '포모도로']}
            },
            'performance': {
                'daily_downloads': 80,
                'retention_7day': 0.4,
                'retention_30day': 0.18,
                'rating': 4.3,
                'avg_session_revenue': 0.08,
                'avg_sessions_per_user': 4.2,
                'share_rate': 0.06,
                'revenue_per_user': 2.1
            }
        },
        {
            'config': {
                'app': {'name': 'Daily Habits', 'description': '습관 추적 앱'},
                'marketing': {'aso_keywords': ['습관', '루틴', '건강']}
            },
            'performance': {
                'daily_downloads': 60,
                'retention_7day': 0.45,
                'retention_30day': 0.22,
                'rating': 4.1,
                'avg_session_revenue': 0.06,
                'avg_sessions_per_user': 3.8,
                'share_rate': 0.04,
                'revenue_per_user': 1.8
            }
        }
    ]
    
    # 각 앱별 고급 KPI 분석
    apps_kpi = []
    for app_data in test_apps:
        kpi = tracker.generate_comprehensive_kpi_report(
            app_data['config'], 
            app_data['performance']
        )
        apps_kpi.append(kpi)
        
        print(f"\n📱 {kpi.app_name}")
        print(f"  LTV: ₩{kpi.ltv:,.0f}")
        print(f"  바이럴 계수: {kpi.viral_coefficient}")
        print(f"  시장 포화도: {kpi.market_saturation:.1%}")
        print(f"  트렌드 점수: {kpi.trend_score}점")
        print(f"  예측 월 수익: ₩{kpi.predicted_monthly_revenue:,.0f}")
        print(f"  신뢰도: {kpi.confidence_level:.1%}")
    
    # 포트폴리오 분석
    portfolio_risk = tracker.analyze_portfolio_risk(apps_kpi)
    print(f"\n🎯 포트폴리오 리스크 분석:")
    print(f"  전체 리스크: {portfolio_risk['risk_level']} ({portfolio_risk['overall_risk_score']:.3f})")
    print(f"  다변화 필요: {'예' if portfolio_risk['diversification_needed'] else '아니오'}")
    
    # 최적화 점수
    optimization = tracker.calculate_portfolio_optimization_score(apps_kpi)
    print(f"\n📈 포트폴리오 최적화:")
    print(f"  최적화 등급: {optimization['grade']}")
    print(f"  카테고리 다양성: {optimization['category_diversity']:.1%}")
    print(f"  수익 안정성: {optimization['revenue_stability']:.1%}")
    
    # 알림 생성
    all_alerts = []
    for kpi in apps_kpi:
        alerts = tracker.create_kpi_alerts(kpi)
        all_alerts.extend(alerts)
    
    if all_alerts:
        print(f"\n🚨 중요 알림 ({len(all_alerts)}개):")
        for alert in all_alerts:
            emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵", "success": "🟢"}
            print(f"  {emoji.get(alert['level'], '📍')} {alert['message']}")

if __name__ == "__main__":
    main()
