#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
앱 공장 수익 시뮬레이션 모듈
다운로드, 광고, 구독 기반 수익 예측 및 시나리오 분석
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@dataclass
class AppMetrics:
    """앱 기본 지표"""
    name: str
    category: str
    daily_downloads: int
    retention_rate: float  # 7일 잔존율
    session_per_day: float
    session_duration: float  # 분
    user_rating: float

@dataclass
class MonetizationConfig:
    """수익화 설정"""
    # 광고 관련
    banner_cpm: float  # 배너 광고 CPM (1000회 노출당 수익)
    interstitial_cpm: float  # 전면 광고 CPM
    banner_fill_rate: float  # 광고 노출률
    interstitial_frequency: int  # 전면 광고 노출 빈도 (세션당)
    
    # 구독 관련
    subscription_price: float  # 월 구독료
    subscription_conversion_rate: float  # 구독 전환율
    subscription_retention_rate: float  # 구독 유지율
    
    # 일회성 결제
    iap_price: float  # 평균 인앱결제 금액
    iap_conversion_rate: float  # 인앱결제 전환율

class RevenueSimulator:
    def __init__(self):
        """수익 시뮬레이터 초기화"""
        self.default_monetization = MonetizationConfig(
            banner_cpm=500,  # 한국 기준 배너 CPM
            interstitial_cpm=2000,  # 전면 광고 CPM
            banner_fill_rate=0.85,
            interstitial_frequency=3,  # 3세션당 1회
            subscription_price=4900,  # 월 4,900원
            subscription_conversion_rate=0.02,  # 2% 구독 전환
            subscription_retention_rate=0.7,  # 70% 월 유지
            iap_price=2900,  # 평균 2,900원
            iap_conversion_rate=0.05  # 5% 결제 전환
        )
    
    def simulate_daily_revenue(self, app: AppMetrics, monetization: MonetizationConfig) -> Dict:
        """일일 수익 시뮬레이션"""
        # 활성 사용자 수 (누적)
        active_users = app.daily_downloads * 30 * app.retention_rate  # 30일 기준
        
        # 광고 수익
        daily_sessions = active_users * app.session_per_day
        
        # 배너 광고 (세션당 평균 노출 수)
        banner_impressions = daily_sessions * (app.session_duration / 2)  # 2분당 1회 노출
        banner_revenue = (banner_impressions * monetization.banner_cpm / 1000) * monetization.banner_fill_rate
        
        # 전면 광고
        interstitial_impressions = daily_sessions / monetization.interstitial_frequency
        interstitial_revenue = (interstitial_impressions * monetization.interstitial_cpm / 1000) * monetization.banner_fill_rate
        
        # 구독 수익 (신규 + 기존)
        new_subscribers = app.daily_downloads * monetization.subscription_conversion_rate
        existing_subscribers = new_subscribers * 30 * monetization.subscription_retention_rate  # 30일 평균
        subscription_revenue = (new_subscribers + existing_subscribers) * (monetization.subscription_price / 30)
        
        # 인앱결제 수익
        iap_users = active_users * monetization.iap_conversion_rate / 30  # 월 기준을 일 기준으로
        iap_revenue = iap_users * monetization.iap_price
        
        return {
            'active_users': int(active_users),
            'banner_revenue': banner_revenue,
            'interstitial_revenue': interstitial_revenue,
            'subscription_revenue': subscription_revenue,
            'iap_revenue': iap_revenue,
            'total_revenue': banner_revenue + interstitial_revenue + subscription_revenue + iap_revenue,
            'revenue_breakdown': {
                'ads': banner_revenue + interstitial_revenue,
                'subscriptions': subscription_revenue,
                'iap': iap_revenue
            }
        }
    
    def simulate_app_portfolio(self, apps: List[AppMetrics], months: int = 12) -> pd.DataFrame:
        """앱 포트폴리오 수익 시뮬레이션"""
        results = []
        
        for month in range(1, months + 1):
            monthly_data = {'month': month}
            total_monthly_revenue = 0
            
            for app in apps:
                # 월별 성장률 적용 (다운로드 증가, 최적화 효과)
                growth_factor = 1 + (month * 0.05)  # 월 5% 성장
                adjusted_app = AppMetrics(
                    name=app.name,
                    category=app.category,
                    daily_downloads=int(app.daily_downloads * growth_factor),
                    retention_rate=min(app.retention_rate * 1.02, 0.8),  # 점진적 개선
                    session_per_day=app.session_per_day,
                    session_duration=app.session_duration,
                    user_rating=min(app.user_rating + 0.01, 5.0)
                )
                
                daily_revenue = self.simulate_daily_revenue(adjusted_app, self.default_monetization)
                monthly_revenue = daily_revenue['total_revenue'] * 30
                
                monthly_data[f'{app.name}_revenue'] = monthly_revenue
                monthly_data[f'{app.name}_users'] = daily_revenue['active_users']
                total_monthly_revenue += monthly_revenue
            
            monthly_data['total_revenue'] = total_monthly_revenue
            results.append(monthly_data)
        
        return pd.DataFrame(results)
    
    def create_revenue_scenarios(self, base_apps: List[AppMetrics]) -> Dict[str, pd.DataFrame]:
        """다양한 시나리오별 수익 예측"""
        scenarios = {}
        
        # 보수적 시나리오 (낮은 성장률)
        conservative_apps = []
        for app in base_apps:
            conservative_apps.append(AppMetrics(
                name=app.name,
                category=app.category,
                daily_downloads=int(app.daily_downloads * 0.7),
                retention_rate=app.retention_rate * 0.9,
                session_per_day=app.session_per_day,
                session_duration=app.session_duration,
                user_rating=app.user_rating
            ))
        scenarios['conservative'] = self.simulate_app_portfolio(conservative_apps, 18)
        
        # 기본 시나리오
        scenarios['base'] = self.simulate_app_portfolio(base_apps, 18)
        
        # 낙관적 시나리오 (높은 성장률)
        optimistic_apps = []
        for app in base_apps:
            optimistic_apps.append(AppMetrics(
                name=app.name,
                category=app.category,
                daily_downloads=int(app.daily_downloads * 1.3),
                retention_rate=min(app.retention_rate * 1.1, 0.8),
                session_per_day=app.session_per_day * 1.2,
                session_duration=app.session_duration * 1.1,
                user_rating=min(app.user_rating + 0.2, 5.0)
            ))
        scenarios['optimistic'] = self.simulate_app_portfolio(optimistic_apps, 18)
        
        return scenarios
    
    def analyze_monetization_mix(self, app: AppMetrics) -> Dict:
        """수익화 방식별 기여도 분석"""
        daily_revenue = self.simulate_daily_revenue(app, self.default_monetization)
        
        # 월 수익으로 환산
        monthly_breakdown = {}
        for key, value in daily_revenue['revenue_breakdown'].items():
            monthly_breakdown[key] = value * 30
        
        total_monthly = sum(monthly_breakdown.values())
        
        # 비율 계산
        percentages = {}
        for key, value in monthly_breakdown.items():
            percentages[key] = (value / total_monthly * 100) if total_monthly > 0 else 0
        
        return {
            'monthly_amounts': monthly_breakdown,
            'percentages': percentages,
            'total_monthly': total_monthly
        }
    
    def calculate_break_even_point(self, apps: List[AppMetrics], target_revenue: float) -> Dict:
        """손익분기점 분석"""
        # 앱 개발/마케팅 비용 추정
        development_cost_per_app = 500000  # 50만원 (자동화 후)
        marketing_cost_per_app = 300000   # 30만원 (자동화 후)
        monthly_operational_cost = 200000  # 20만원 (서버, API 등)
        
        total_initial_cost = len(apps) * (development_cost_per_app + marketing_cost_per_app)
        
        # 월별 누적 수익 시뮬레이션
        portfolio_data = self.simulate_app_portfolio(apps, 24)
        
        cumulative_revenue = 0
        cumulative_costs = total_initial_cost
        break_even_month = None
        
        monthly_analysis = []
        
        for _, row in portfolio_data.iterrows():
            month = int(row['month'])
            monthly_revenue = row['total_revenue']
            monthly_cost = monthly_operational_cost
            
            cumulative_revenue += monthly_revenue
            cumulative_costs += monthly_cost
            
            profit = cumulative_revenue - cumulative_costs
            
            if break_even_month is None and profit > 0:
                break_even_month = month
            
            monthly_analysis.append({
                'month': month,
                'monthly_revenue': monthly_revenue,
                'cumulative_revenue': cumulative_revenue,
                'cumulative_costs': cumulative_costs,
                'profit': profit,
                'target_achieved': monthly_revenue >= target_revenue
            })
        
        return {
            'break_even_month': break_even_month,
            'initial_investment': total_initial_cost,
            'monthly_analysis': monthly_analysis,
            'target_achievement_month': next(
                (m['month'] for m in monthly_analysis if m['target_achieved']), 
                None
            )
        }
    
    def create_sensitivity_analysis(self, base_app: AppMetrics) -> pd.DataFrame:
        """민감도 분석 (주요 변수 변화에 따른 수익 영향)"""
        base_revenue = self.simulate_daily_revenue(base_app, self.default_monetization)['total_revenue'] * 30
        
        sensitivity_data = []
        
        # 다운로드 수 변화
        for factor in [0.5, 0.7, 0.9, 1.0, 1.2, 1.5, 2.0]:
            test_app = AppMetrics(
                name=base_app.name,
                category=base_app.category,
                daily_downloads=int(base_app.daily_downloads * factor),
                retention_rate=base_app.retention_rate,
                session_per_day=base_app.session_per_day,
                session_duration=base_app.session_duration,
                user_rating=base_app.user_rating
            )
            
            revenue = self.simulate_daily_revenue(test_app, self.default_monetization)['total_revenue'] * 30
            sensitivity_data.append({
                'variable': 'Daily Downloads',
                'factor': factor,
                'revenue': revenue,
                'change_percent': (revenue - base_revenue) / base_revenue * 100
            })
        
        # 잔존율 변화
        for factor in [0.7, 0.8, 0.9, 1.0, 1.1, 1.2]:
            test_app = AppMetrics(
                name=base_app.name,
                category=base_app.category,
                daily_downloads=base_app.daily_downloads,
                retention_rate=min(base_app.retention_rate * factor, 1.0),
                session_per_day=base_app.session_per_day,
                session_duration=base_app.session_duration,
                user_rating=base_app.user_rating
            )
            
            revenue = self.simulate_daily_revenue(test_app, self.default_monetization)['total_revenue'] * 30
            sensitivity_data.append({
                'variable': 'Retention Rate',
                'factor': factor,
                'revenue': revenue,
                'change_percent': (revenue - base_revenue) / base_revenue * 100
            })
        
        return pd.DataFrame(sensitivity_data)

def create_sample_app_portfolio() -> List[AppMetrics]:
    """샘플 앱 포트폴리오 생성"""
    return [
        AppMetrics(
            name="Focus Timer Pro",
            category="productivity",
            daily_downloads=50,
            retention_rate=0.35,
            session_per_day=3.5,
            session_duration=8.0,
            user_rating=4.3
        ),
        AppMetrics(
            name="Daily Habits",
            category="health",
            daily_downloads=35,
            retention_rate=0.42,
            session_per_day=2.8,
            session_duration=5.0,
            user_rating=4.1
        ),
        AppMetrics(
            name="Simple Todo",
            category="productivity",
            daily_downloads=60,
            retention_rate=0.28,
            session_per_day=4.2,
            session_duration=6.0,
            user_rating=4.0
        )
    ]

def main():
    """테스트 실행"""
    simulator = RevenueSimulator()
    apps = create_sample_app_portfolio()
    
    print("📊 수익 시뮬레이션 테스트")
    print("=" * 50)
    
    # 개별 앱 분석
    for app in apps:
        daily_revenue = simulator.simulate_daily_revenue(app, simulator.default_monetization)
        monthly_revenue = daily_revenue['total_revenue'] * 30
        
        print(f"\n📱 {app.name}")
        print(f"  일일 수익: ₩{daily_revenue['total_revenue']:,.0f}")
        print(f"  월 예상 수익: ₩{monthly_revenue:,.0f}")
        print(f"  활성 사용자: {daily_revenue['active_users']:,}명")
    
    # 포트폴리오 분석
    portfolio_data = simulator.simulate_app_portfolio(apps, 12)
    final_month_revenue = portfolio_data.iloc[-1]['total_revenue']
    
    print(f"\n🏭 포트폴리오 전체 (12개월 후)")
    print(f"  월 총 수익: ₩{final_month_revenue:,.0f}")
    
    # 손익분기점 분석
    break_even = simulator.calculate_break_even_point(apps, 3000000)
    print(f"\n💰 손익분기점 분석")
    print(f"  손익분기점: {break_even['break_even_month']}개월")
    print(f"  초기 투자: ₩{break_even['initial_investment']:,}")
    print(f"  월 300만원 달성: {break_even['target_achievement_month']}개월")

if __name__ == "__main__":
    main()
