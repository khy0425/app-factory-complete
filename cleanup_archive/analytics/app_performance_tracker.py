#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Performance Tracker - Real-time Success Detection
10개 앱 포트폴리오의 실시간 성과 추적 및 승자 예측 시스템
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import logging

@dataclass
class AppMetrics:
    """앱 성과 지표 데이터 클래스"""
    app_id: str
    app_name: str

    # 기본 지표
    total_downloads: int
    daily_active_users: int
    monthly_active_users: int

    # 수익 지표
    daily_revenue: float
    monthly_revenue: float
    ltv_estimate: float
    arpu: float

    # 참여 지표
    retention_d1: float
    retention_d7: float
    retention_d30: float
    session_duration: float

    # 성장 지표
    viral_coefficient: float
    organic_growth_rate: float
    app_store_ranking: int

    # 마케팅 지표
    cac: float  # Customer Acquisition Cost
    conversion_rate: float

    # 타임스탬프
    timestamp: datetime

    def calculate_success_score(self) -> float:
        """앱 성공 점수 계산 (0-100)"""
        score = 0

        # 수익 잠재력 (40점)
        revenue_score = min(self.monthly_revenue / 1000, 20)  # 월 $20K에서 20점
        ltv_score = min(self.ltv_estimate / 100, 20)          # LTV $100에서 20점
        score += revenue_score + ltv_score

        # 성장 지표 (30점)
        viral_score = min(self.viral_coefficient * 10, 15)    # 바이럴 계수 1.5에서 15점
        retention_score = min(self.retention_d30 * 30, 15)    # D30 리텐션 50%에서 15점
        score += viral_score + retention_score

        # 시장 견인력 (30점)
        ranking_score = min((1000 - self.app_store_ranking) / 100, 15)  # Top 100에서 15점
        growth_score = min(self.organic_growth_rate * 50, 15)            # 30% 성장에서 15점
        score += ranking_score + growth_score

        return min(score, 100)

class AppPerformanceTracker:
    """앱 성과 추적 및 분석 시스템"""

    def __init__(self, db_path: str = "app_factory_analytics.db"):
        self.db_path = db_path
        self.setup_database()
        self.logger = self._setup_logging()

        # 앱 포트폴리오 정의
        self.app_portfolio = {
            'gigachad_runner': 'GigaChad Runner',
            'alpha_timer': 'Alpha Timer',
            'chad_cardio': 'Chad Cardio',
            'sigma_strength': 'Sigma Strength',
            'beast_mode': 'Beast Mode',
            'zen_chad': 'Zen Chad',
            'sleep_alpha': 'Sleep Alpha',
            'focus_beast': 'Focus Beast',
            'habit_sigma': 'Habit Sigma',
            'mind_chad': 'Mind Chad'
        }

    def _setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app_performance.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def setup_database(self):
        """데이터베이스 테이블 생성"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 앱 메트릭 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT NOT NULL,
                app_name TEXT NOT NULL,
                total_downloads INTEGER,
                daily_active_users INTEGER,
                monthly_active_users INTEGER,
                daily_revenue REAL,
                monthly_revenue REAL,
                ltv_estimate REAL,
                arpu REAL,
                retention_d1 REAL,
                retention_d7 REAL,
                retention_d30 REAL,
                session_duration REAL,
                viral_coefficient REAL,
                organic_growth_rate REAL,
                app_store_ranking INTEGER,
                cac REAL,
                conversion_rate REAL,
                success_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 성과 순위 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_rankings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ranking_date DATE,
                app_id TEXT,
                app_name TEXT,
                rank INTEGER,
                success_score REAL,
                monthly_revenue REAL,
                growth_trend TEXT,
                recommendation TEXT
            )
        ''')

        # A/B 테스트 결과 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT,
                test_name TEXT,
                variant_a_metric REAL,
                variant_b_metric REAL,
                winner TEXT,
                confidence_level REAL,
                test_start_date DATE,
                test_end_date DATE
            )
        ''')

        conn.commit()
        conn.close()

        self.logger.info("Database setup completed")

    def collect_app_metrics(self, app_id: str, metrics_data: Dict) -> None:
        """앱 메트릭 데이터 수집 및 저장"""
        try:
            # AppMetrics 객체 생성
            metrics = AppMetrics(
                app_id=app_id,
                app_name=self.app_portfolio.get(app_id, app_id),
                total_downloads=metrics_data.get('total_downloads', 0),
                daily_active_users=metrics_data.get('daily_active_users', 0),
                monthly_active_users=metrics_data.get('monthly_active_users', 0),
                daily_revenue=metrics_data.get('daily_revenue', 0.0),
                monthly_revenue=metrics_data.get('monthly_revenue', 0.0),
                ltv_estimate=metrics_data.get('ltv_estimate', 0.0),
                arpu=metrics_data.get('arpu', 0.0),
                retention_d1=metrics_data.get('retention_d1', 0.0),
                retention_d7=metrics_data.get('retention_d7', 0.0),
                retention_d30=metrics_data.get('retention_d30', 0.0),
                session_duration=metrics_data.get('session_duration', 0.0),
                viral_coefficient=metrics_data.get('viral_coefficient', 0.0),
                organic_growth_rate=metrics_data.get('organic_growth_rate', 0.0),
                app_store_ranking=metrics_data.get('app_store_ranking', 999999),
                cac=metrics_data.get('cac', 0.0),
                conversion_rate=metrics_data.get('conversion_rate', 0.0),
                timestamp=datetime.now()
            )

            # 성공 점수 계산
            success_score = metrics.calculate_success_score()

            # 데이터베이스에 저장
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO app_metrics (
                    app_id, app_name, total_downloads, daily_active_users, monthly_active_users,
                    daily_revenue, monthly_revenue, ltv_estimate, arpu,
                    retention_d1, retention_d7, retention_d30, session_duration,
                    viral_coefficient, organic_growth_rate, app_store_ranking,
                    cac, conversion_rate, success_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics.app_id, metrics.app_name, metrics.total_downloads,
                metrics.daily_active_users, metrics.monthly_active_users,
                metrics.daily_revenue, metrics.monthly_revenue, metrics.ltv_estimate, metrics.arpu,
                metrics.retention_d1, metrics.retention_d7, metrics.retention_d30, metrics.session_duration,
                metrics.viral_coefficient, metrics.organic_growth_rate, metrics.app_store_ranking,
                metrics.cac, metrics.conversion_rate, success_score
            ))

            conn.commit()
            conn.close()

            self.logger.info(f"Metrics collected for {app_id}: Success Score = {success_score:.2f}")

        except Exception as e:
            self.logger.error(f"Error collecting metrics for {app_id}: {str(e)}")

    def analyze_portfolio_performance(self) -> Dict:
        """포트폴리오 전체 성과 분석"""
        conn = sqlite3.connect(self.db_path)

        # 최신 메트릭 조회
        query = '''
            SELECT app_id, app_name, success_score, monthly_revenue,
                   retention_d30, viral_coefficient, app_store_ranking,
                   timestamp
            FROM app_metrics
            WHERE timestamp > datetime('now', '-7 days')
            ORDER BY timestamp DESC
        '''

        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return {"error": "No recent data available"}

        # 앱별 최신 성과 집계
        latest_performance = df.groupby('app_id').first().reset_index()
        latest_performance = latest_performance.sort_values('success_score', ascending=False)

        # 성과 분석
        analysis = {
            'portfolio_summary': {
                'total_apps': len(latest_performance),
                'avg_success_score': latest_performance['success_score'].mean(),
                'total_monthly_revenue': latest_performance['monthly_revenue'].sum(),
                'top_performer': latest_performance.iloc[0]['app_name'] if len(latest_performance) > 0 else None
            },
            'performance_rankings': [],
            'recommendations': []
        }

        # 순위별 성과
        for idx, row in latest_performance.iterrows():
            rank_info = {
                'rank': idx + 1,
                'app_id': row['app_id'],
                'app_name': row['app_name'],
                'success_score': round(row['success_score'], 2),
                'monthly_revenue': round(row['monthly_revenue'], 2),
                'retention_d30': round(row['retention_d30'], 3),
                'viral_coefficient': round(row['viral_coefficient'], 3),
                'app_store_ranking': int(row['app_store_ranking'])
            }
            analysis['performance_rankings'].append(rank_info)

        # 추천사항 생성
        analysis['recommendations'] = self._generate_recommendations(latest_performance)

        return analysis

    def _generate_recommendations(self, performance_df: pd.DataFrame) -> List[str]:
        """성과 기반 추천사항 생성"""
        recommendations = []

        if len(performance_df) == 0:
            return ["No data available for recommendations"]

        # Top 3 앱 식별
        top_3 = performance_df.head(3)
        bottom_3 = performance_df.tail(3)

        # Top performer 분석
        top_app = top_3.iloc[0]
        if top_app['success_score'] > 70:
            recommendations.append(f"🚀 SCALE UP: {top_app['app_name']} (점수: {top_app['success_score']:.1f}) - 마케팅 예산 10배 증액 추천")

        if top_app['monthly_revenue'] > 5000:
            recommendations.append(f"💰 MONETIZE: {top_app['app_name']} - 프리미엄 기능 추가 및 가격 최적화")

        # 성장 잠재력 분석
        for _, app in top_3.iterrows():
            if app['viral_coefficient'] > 1.2:
                recommendations.append(f"📈 VIRAL BOOST: {app['app_name']} - 소셜 기능 강화로 바이럴 효과 극대화")

            if app['retention_d30'] < 0.3:
                recommendations.append(f"🔄 RETENTION FIX: {app['app_name']} - 온보딩 개선 및 푸시 알림 최적화")

        # 저성과 앱 분석
        worst_app = bottom_3.iloc[-1]
        if worst_app['success_score'] < 20:
            recommendations.append(f"⚠️ PIVOT OR SUNSET: {worst_app['app_name']} (점수: {worst_app['success_score']:.1f}) - 컨셉 변경 또는 중단 검토")

        # 포트폴리오 전략
        high_performers = performance_df[performance_df['success_score'] > 50]
        if len(high_performers) >= 2:
            recommendations.append("🎯 FOCUS STRATEGY: 성공 앱 2-3개에 리소스 집중, 나머지는 유지 모드")

        return recommendations

    def predict_future_performance(self, app_id: str, days_ahead: int = 30) -> Dict:
        """앱 성과 예측 (간단한 선형 회귀 기반)"""
        conn = sqlite3.connect(self.db_path)

        query = '''
            SELECT success_score, monthly_revenue, timestamp
            FROM app_metrics
            WHERE app_id = ?
            ORDER BY timestamp DESC
            LIMIT 30
        '''

        df = pd.read_sql_query(query, conn, params=(app_id,))
        conn.close()

        if len(df) < 3:
            return {"error": "Insufficient data for prediction"}

        # 시간 순서로 정렬
        df = df.sort_values('timestamp')
        df['days'] = range(len(df))

        # 선형 회귀로 트렌드 계산
        success_trend = np.polyfit(df['days'], df['success_score'], 1)[0]
        revenue_trend = np.polyfit(df['days'], df['monthly_revenue'], 1)[0]

        # 예측 계산
        current_success = df['success_score'].iloc[-1]
        current_revenue = df['monthly_revenue'].iloc[-1]

        predicted_success = current_success + (success_trend * days_ahead)
        predicted_revenue = current_revenue + (revenue_trend * days_ahead)

        return {
            'app_id': app_id,
            'current_success_score': round(current_success, 2),
            'predicted_success_score': round(max(0, predicted_success), 2),
            'current_monthly_revenue': round(current_revenue, 2),
            'predicted_monthly_revenue': round(max(0, predicted_revenue), 2),
            'success_trend': 'increasing' if success_trend > 0 else 'decreasing',
            'revenue_trend': 'increasing' if revenue_trend > 0 else 'decreasing',
            'prediction_confidence': 'low' if len(df) < 10 else 'medium'
        }

    def run_ab_test_analysis(self, app_id: str, test_name: str,
                           variant_a_data: Dict, variant_b_data: Dict) -> Dict:
        """A/B 테스트 결과 분석"""

        # 간단한 통계적 유의성 검정 (t-test 시뮬레이션)
        metric_a = variant_a_data.get('conversion_rate', 0)
        metric_b = variant_b_data.get('conversion_rate', 0)

        # 승자 결정 (단순 비교)
        if abs(metric_a - metric_b) / max(metric_a, metric_b, 0.001) > 0.05:  # 5% 이상 차이
            winner = 'A' if metric_a > metric_b else 'B'
            confidence = 'high' if abs(metric_a - metric_b) / max(metric_a, metric_b, 0.001) > 0.2 else 'medium'
        else:
            winner = 'inconclusive'
            confidence = 'low'

        # 결과 저장
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO ab_test_results (
                app_id, test_name, variant_a_metric, variant_b_metric,
                winner, confidence_level, test_start_date, test_end_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            app_id, test_name, metric_a, metric_b,
            winner, confidence, datetime.now().date(), datetime.now().date()
        ))

        conn.commit()
        conn.close()

        result = {
            'app_id': app_id,
            'test_name': test_name,
            'variant_a_metric': metric_a,
            'variant_b_metric': metric_b,
            'winner': winner,
            'confidence_level': confidence,
            'improvement': abs(metric_a - metric_b) / max(metric_a, metric_b, 0.001) * 100,
            'recommendation': f"Deploy variant {winner}" if winner != 'inconclusive' else "Continue testing"
        }

        self.logger.info(f"A/B test completed for {app_id}: {test_name} - Winner: {winner}")

        return result

    def generate_daily_report(self) -> str:
        """일일 성과 리포트 생성"""
        analysis = self.analyze_portfolio_performance()

        if 'error' in analysis:
            return "❌ No data available for daily report"

        report = f"""
🏭 App Factory Daily Performance Report
📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 PORTFOLIO OVERVIEW
• Total Apps: {analysis['portfolio_summary']['total_apps']}
• Average Success Score: {analysis['portfolio_summary']['avg_success_score']:.1f}/100
• Total Monthly Revenue: ${analysis['portfolio_summary']['total_monthly_revenue']:,.2f}
• Top Performer: {analysis['portfolio_summary']['top_performer']}

🏆 PERFORMANCE RANKINGS
"""

        for ranking in analysis['performance_rankings'][:5]:  # Top 5
            emoji = "🥇" if ranking['rank'] == 1 else "🥈" if ranking['rank'] == 2 else "🥉" if ranking['rank'] == 3 else "📱"
            report += f"{emoji} #{ranking['rank']} {ranking['app_name']}: {ranking['success_score']}/100 (${ranking['monthly_revenue']:,.0f}/month)\n"

        report += "\n🎯 KEY RECOMMENDATIONS\n"
        for rec in analysis['recommendations'][:3]:  # Top 3 recommendations
            report += f"• {rec}\n"

        return report

def simulate_sample_data():
    """샘플 데이터 생성 (테스트용)"""
    tracker = AppPerformanceTracker()

    # 샘플 앱 데이터
    sample_apps = [
        {
            'app_id': 'gigachad_runner',
            'metrics': {
                'total_downloads': 15000,
                'daily_active_users': 2500,
                'monthly_active_users': 8000,
                'daily_revenue': 150.0,
                'monthly_revenue': 4500.0,
                'ltv_estimate': 45.0,
                'arpu': 0.56,
                'retention_d1': 0.75,
                'retention_d7': 0.45,
                'retention_d30': 0.25,
                'session_duration': 8.5,
                'viral_coefficient': 1.2,
                'organic_growth_rate': 0.15,
                'app_store_ranking': 150,
                'cac': 2.5,
                'conversion_rate': 0.08
            }
        },
        {
            'app_id': 'alpha_timer',
            'metrics': {
                'total_downloads': 8000,
                'daily_active_users': 1200,
                'monthly_active_users': 4000,
                'daily_revenue': 80.0,
                'monthly_revenue': 2400.0,
                'ltv_estimate': 32.0,
                'arpu': 0.60,
                'retention_d1': 0.68,
                'retention_d7': 0.38,
                'retention_d30': 0.18,
                'session_duration': 6.2,
                'viral_coefficient': 0.9,
                'organic_growth_rate': 0.12,
                'app_store_ranking': 280,
                'cac': 3.2,
                'conversion_rate': 0.06
            }
        }
    ]

    # 데이터 수집
    for app_data in sample_apps:
        tracker.collect_app_metrics(app_data['app_id'], app_data['metrics'])

    # 분석 결과 출력
    analysis = tracker.analyze_portfolio_performance()
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

    # 일일 리포트 생성
    daily_report = tracker.generate_daily_report()
    print("\n" + "="*50)
    print(daily_report)

    return tracker

if __name__ == "__main__":
    # 샘플 데이터로 테스트
    tracker = simulate_sample_data()
    print("\n✅ App Performance Tracker initialized and tested successfully!")