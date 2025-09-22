#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Growth Engine Metrics Tracking
SaaS-스타일 성장 지표 측정 및 최적화 시스템
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import sqlite3
from pathlib import Path

@dataclass
class GrowthMetrics:
    """Growth Engine 핵심 지표"""
    # Acquisition (획득)
    downloads: int = 0
    organic_downloads: int = 0
    paid_downloads: int = 0
    cac: float = 0.0  # Customer Acquisition Cost

    # Activation (활성화)
    signups: int = 0
    onboarding_completion: float = 0.0
    first_action_rate: float = 0.0

    # Retention (유지)
    dau: int = 0
    wau: int = 0
    mau: int = 0
    retention_d1: float = 0.0
    retention_d7: float = 0.0
    retention_d30: float = 0.0

    # Revenue (매출)
    revenue: float = 0.0
    arpu: float = 0.0  # Average Revenue Per User
    ltv: float = 0.0   # Lifetime Value
    premium_conversion: float = 0.0

    # Referral (추천)
    referral_rate: float = 0.0
    viral_coefficient: float = 0.0
    social_shares: int = 0

    # Product (제품)
    session_length: float = 0.0
    sessions_per_user: float = 0.0
    feature_adoption: Dict[str, float] = None

class GrowthEngineTracker:
    """SaaS Growth Engine 스타일 지표 추적기"""

    def __init__(self, db_path: str = "growth_metrics.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_database()

    def _init_database(self):
        """데이터베이스 초기화"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS apps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT UNIQUE,
                app_name TEXT,
                template_type TEXT,
                created_at TIMESTAMP,
                status TEXT
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT,
                date DATE,
                downloads INTEGER,
                dau INTEGER,
                revenue REAL,
                retention_d1 REAL,
                retention_d7 REAL,
                retention_d30 REAL,
                created_at TIMESTAMP,
                FOREIGN KEY (app_id) REFERENCES apps (app_id)
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS growth_experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT,
                experiment_name TEXT,
                variant TEXT,
                start_date DATE,
                end_date DATE,
                hypothesis TEXT,
                result TEXT,
                significance REAL,
                FOREIGN KEY (app_id) REFERENCES apps (app_id)
            )
        """)

        self.conn.commit()

    def register_app(self, app_id: str, app_name: str, template_type: str):
        """새 앱 등록"""
        self.conn.execute("""
            INSERT OR REPLACE INTO apps (app_id, app_name, template_type, created_at, status)
            VALUES (?, ?, ?, ?, ?)
        """, (app_id, app_name, template_type, datetime.now(), 'active'))
        self.conn.commit()

    def track_daily_metrics(self, app_id: str, metrics: GrowthMetrics, date: Optional[datetime] = None):
        """일일 지표 추적"""
        if date is None:
            date = datetime.now().date()

        self.conn.execute("""
            INSERT OR REPLACE INTO daily_metrics
            (app_id, date, downloads, dau, revenue, retention_d1, retention_d7, retention_d30, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            app_id, date, metrics.downloads, metrics.dau, metrics.revenue,
            metrics.retention_d1, metrics.retention_d7, metrics.retention_d30,
            datetime.now()
        ))
        self.conn.commit()

    def calculate_pirate_metrics(self, app_id: str, days: int = 30) -> Dict:
        """AARRR (해적 지표) 계산"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        query = """
            SELECT * FROM daily_metrics
            WHERE app_id = ? AND date BETWEEN ? AND ?
            ORDER BY date
        """

        df = pd.read_sql_query(query, self.conn, params=(app_id, start_date, end_date))

        if df.empty:
            return {}

        # AARRR 지표 계산
        pirate_metrics = {
            'acquisition': {
                'total_downloads': df['downloads'].sum(),
                'avg_daily_downloads': df['downloads'].mean(),
                'download_growth_rate': self._calculate_growth_rate(df['downloads'])
            },
            'activation': {
                'avg_dau': df['dau'].mean(),
                'dau_growth_rate': self._calculate_growth_rate(df['dau'])
            },
            'retention': {
                'avg_retention_d1': df['retention_d1'].mean(),
                'avg_retention_d7': df['retention_d7'].mean(),
                'avg_retention_d30': df['retention_d30'].mean(),
                'retention_trend_d1': self._calculate_trend(df['retention_d1']),
                'retention_trend_d7': self._calculate_trend(df['retention_d7'])
            },
            'revenue': {
                'total_revenue': df['revenue'].sum(),
                'avg_daily_revenue': df['revenue'].mean(),
                'revenue_growth_rate': self._calculate_growth_rate(df['revenue']),
                'arpu': df['revenue'].sum() / df['downloads'].sum() if df['downloads'].sum() > 0 else 0
            },
            'referral': {
                'viral_coefficient': self._calculate_viral_coefficient(df),
                'organic_ratio': self._calculate_organic_ratio(app_id, days)
            }
        }

        return pirate_metrics

    def _calculate_growth_rate(self, series: pd.Series) -> float:
        """성장률 계산"""
        if len(series) < 2:
            return 0.0

        first_week = series.iloc[:7].mean()
        last_week = series.iloc[-7:].mean()

        if first_week == 0:
            return 0.0

        return ((last_week - first_week) / first_week) * 100

    def _calculate_trend(self, series: pd.Series) -> str:
        """트렌드 방향 계산"""
        if len(series) < 2:
            return 'insufficient_data'

        correlation = np.corrcoef(range(len(series)), series)[0, 1]

        if correlation > 0.5:
            return 'improving'
        elif correlation < -0.5:
            return 'declining'
        else:
            return 'stable'

    def _calculate_viral_coefficient(self, df: pd.DataFrame) -> float:
        """바이럴 계수 계산 (간단한 추정)"""
        if df.empty:
            return 0.0

        # 간단한 바이럴 계수 추정: (신규 유저 / 기존 유저) 평균
        avg_new_users = df['downloads'].diff().mean()
        avg_existing_users = df['dau'].mean()

        if avg_existing_users == 0:
            return 0.0

        return avg_new_users / avg_existing_users

    def _calculate_organic_ratio(self, app_id: str, days: int) -> float:
        """오가닉 비율 계산 (모의)"""
        # 실제로는 attribution 데이터 필요
        return 0.65  # 65% organic 가정

    def get_cohort_analysis(self, app_id: str, cohort_period: str = 'weekly') -> pd.DataFrame:
        """코호트 분석"""
        # 실제 구현에서는 사용자별 데이터 필요
        # 여기서는 간단한 모의 코호트 생성

        periods = 12 if cohort_period == 'weekly' else 6
        cohort_data = []

        for i in range(periods):
            week_data = {
                'cohort': f'Week {i+1}',
                'users': 1000 - (i * 50),  # 감소 패턴
                'week_0': 100.0,
                'week_1': 85.0 - (i * 2),
                'week_2': 70.0 - (i * 3),
                'week_4': 50.0 - (i * 4),
                'week_8': 30.0 - (i * 3),
                'week_12': 20.0 - (i * 2)
            }
            cohort_data.append(week_data)

        return pd.DataFrame(cohort_data)

    def run_growth_experiments(self, app_id: str, experiment_config: Dict) -> Dict:
        """Growth 실험 실행"""
        experiment_id = f"{app_id}_{experiment_config['name']}_{datetime.now().strftime('%Y%m%d')}"

        # 실험 등록
        self.conn.execute("""
            INSERT INTO growth_experiments
            (app_id, experiment_name, variant, start_date, hypothesis)
            VALUES (?, ?, ?, ?, ?)
        """, (
            app_id,
            experiment_config['name'],
            experiment_config['variant'],
            datetime.now().date(),
            experiment_config['hypothesis']
        ))
        self.conn.commit()

        # 실험 시뮬레이션
        experiment_result = {
            'experiment_id': experiment_id,
            'status': 'running',
            'expected_duration': experiment_config.get('duration_days', 14),
            'success_metric': experiment_config.get('success_metric', 'retention_d7'),
            'expected_lift': experiment_config.get('expected_lift', 5.0),
            'confidence_level': 95,
            'sample_size_needed': 1000
        }

        return experiment_result

    def generate_growth_report(self, app_id: str) -> Dict:
        """종합 성장 리포트 생성"""
        pirate_metrics = self.calculate_pirate_metrics(app_id)
        cohort_analysis = self.get_cohort_analysis(app_id)

        # Growth Rate 계산
        current_metrics = self.get_current_metrics(app_id)
        previous_metrics = self.get_previous_metrics(app_id, days_ago=30)

        growth_rates = {}
        for metric in ['downloads', 'dau', 'revenue']:
            if metric in current_metrics and metric in previous_metrics:
                if previous_metrics[metric] > 0:
                    growth_rate = ((current_metrics[metric] - previous_metrics[metric]) / previous_metrics[metric]) * 100
                    growth_rates[f'{metric}_growth'] = growth_rate

        # 성장 단계 판정
        growth_stage = self._determine_growth_stage(pirate_metrics)

        # 개선 제안
        improvement_suggestions = self._generate_improvement_suggestions(pirate_metrics, growth_stage)

        report = {
            'app_id': app_id,
            'generated_at': datetime.now().isoformat(),
            'growth_stage': growth_stage,
            'pirate_metrics': pirate_metrics,
            'growth_rates': growth_rates,
            'cohort_retention': cohort_analysis.to_dict('records'),
            'improvement_suggestions': improvement_suggestions,
            'next_experiments': self._suggest_experiments(pirate_metrics, growth_stage)
        }

        return report

    def _determine_growth_stage(self, pirate_metrics: Dict) -> str:
        """성장 단계 판정"""
        if not pirate_metrics or 'acquisition' not in pirate_metrics:
            return 'pre_launch'

        total_downloads = pirate_metrics['acquisition'].get('total_downloads', 0)
        avg_retention_d30 = pirate_metrics['retention'].get('avg_retention_d30', 0)

        if total_downloads < 1000:
            return 'early_stage'
        elif total_downloads < 10000:
            return 'growth_stage'
        elif total_downloads < 100000:
            return 'scale_stage'
        else:
            return 'mature_stage'

    def _generate_improvement_suggestions(self, pirate_metrics: Dict, growth_stage: str) -> List[str]:
        """개선 제안 생성"""
        suggestions = []

        if not pirate_metrics:
            return ["앱 출시 후 데이터 수집을 시작하세요."]

        # Acquisition 개선
        if pirate_metrics.get('acquisition', {}).get('download_growth_rate', 0) < 10:
            suggestions.append("📈 다운로드 증가율이 낮습니다. ASO 최적화와 마케팅 채널 다양화를 고려하세요.")

        # Retention 개선
        retention_d1 = pirate_metrics.get('retention', {}).get('avg_retention_d1', 0)
        if retention_d1 < 70:
            suggestions.append("🔄 Day 1 리텐션이 낮습니다. 온보딩 개선과 첫 사용자 경험 최적화가 필요합니다.")

        retention_d30 = pirate_metrics.get('retention', {}).get('avg_retention_d30', 0)
        if retention_d30 < 20:
            suggestions.append("📅 장기 리텐션 개선이 필요합니다. 푸시 알림 최적화와 습관 형성 기능을 강화하세요.")

        # Revenue 개선
        arpu = pirate_metrics.get('revenue', {}).get('arpu', 0)
        if arpu < 5:
            suggestions.append("💰 ARPU가 낮습니다. 프리미엄 기능 가치 제안을 강화하고 가격 실험을 진행하세요.")

        # Growth Stage별 제안
        if growth_stage == 'early_stage':
            suggestions.append("🚀 제품-시장 적합성(PMF) 찾기에 집중하세요. 사용자 피드백을 적극 수집하고 반영하세요.")
        elif growth_stage == 'growth_stage':
            suggestions.append("📊 성장 동력을 찾았습니다. 마케팅 예산을 늘리고 바이럴 기능을 추가하세요.")
        elif growth_stage == 'scale_stage':
            suggestions.append("🔧 운영 효율성에 집중하세요. 자동화를 늘리고 고객 세분화를 진행하세요.")

        return suggestions

    def _suggest_experiments(self, pirate_metrics: Dict, growth_stage: str) -> List[Dict]:
        """성장 실험 제안"""
        experiments = []

        if growth_stage == 'early_stage':
            experiments.extend([
                {
                    'name': 'onboarding_optimization',
                    'hypothesis': '온보딩 단계를 줄이면 완료율이 증가할 것',
                    'success_metric': 'onboarding_completion_rate',
                    'expected_lift': 15,
                    'duration_days': 14
                },
                {
                    'name': 'first_action_incentive',
                    'hypothesis': '첫 액션에 보상을 주면 활성화율이 증가할 것',
                    'success_metric': 'retention_d1',
                    'expected_lift': 10,
                    'duration_days': 21
                }
            ])

        elif growth_stage == 'growth_stage':
            experiments.extend([
                {
                    'name': 'referral_program',
                    'hypothesis': '추천 프로그램으로 바이럴 계수가 증가할 것',
                    'success_metric': 'viral_coefficient',
                    'expected_lift': 25,
                    'duration_days': 30
                },
                {
                    'name': 'premium_pricing_test',
                    'hypothesis': '가격을 20% 올려도 전환율 감소가 적을 것',
                    'success_metric': 'revenue_per_user',
                    'expected_lift': 15,
                    'duration_days': 21
                }
            ])

        return experiments

    def get_current_metrics(self, app_id: str) -> Dict:
        """현재 지표 조회"""
        query = """
            SELECT * FROM daily_metrics
            WHERE app_id = ?
            ORDER BY date DESC
            LIMIT 7
        """
        df = pd.read_sql_query(query, self.conn, params=(app_id,))

        if df.empty:
            return {}

        return {
            'downloads': df['downloads'].mean(),
            'dau': df['dau'].mean(),
            'revenue': df['revenue'].mean()
        }

    def get_previous_metrics(self, app_id: str, days_ago: int = 30) -> Dict:
        """이전 기간 지표 조회"""
        end_date = datetime.now().date() - timedelta(days=days_ago)
        start_date = end_date - timedelta(days=7)

        query = """
            SELECT * FROM daily_metrics
            WHERE app_id = ? AND date BETWEEN ? AND ?
        """
        df = pd.read_sql_query(query, self.conn, params=(app_id, start_date, end_date))

        if df.empty:
            return {}

        return {
            'downloads': df['downloads'].mean(),
            'dau': df['dau'].mean(),
            'revenue': df['revenue'].mean()
        }

if __name__ == "__main__":
    # 테스트 실행
    tracker = GrowthEngineTracker()

    # 테스트 앱 등록
    tracker.register_app("com.chadtech.gigachad_runner", "GigaChad Runner", "runner")

    # 테스트 메트릭 추가
    for i in range(30):
        date = datetime.now().date() - timedelta(days=29-i)
        metrics = GrowthMetrics(
            downloads=1000 + i*50,
            dau=500 + i*20,
            revenue=100 + i*10,
            retention_d1=70 + i*0.5,
            retention_d7=40 + i*0.3,
            retention_d30=20 + i*0.2
        )
        tracker.track_daily_metrics("com.chadtech.gigachad_runner", metrics, date)

    # 리포트 생성
    report = tracker.generate_growth_report("com.chadtech.gigachad_runner")
    print(json.dumps(report, indent=2, default=str))