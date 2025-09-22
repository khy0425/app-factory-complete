#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
앱 공장 통합 대시보드 실행 스크립트
성과 모니터링, 수익 시뮬레이션, 마케팅 현황을 한 번에
"""

import streamlit as st
import sys
import os
from pathlib import Path

# 현재 디렉토리를 Python path에 추가
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from dashboard.streamlit_dashboard import AppFactoryDashboard
from dashboard.revenue_simulator import RevenueSimulator, create_sample_app_portfolio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="🏭 앱 공장 통합 대시보드",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """메인 대시보드"""
    st.title("🏭 Mission100 앱 공장 통합 대시보드")
    st.markdown("**실시간 성과 모니터링 + 수익 시뮬레이션 + 마케팅 자동화 현황**")
    
    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["📊 실시간 성과", "💰 수익 시뮬레이션", "🤖 마케팅 자동화", "📋 워크플로우"])
    
    # Tab 1: 실시간 성과
    with tab1:
        st.header("📊 실시간 성과 모니터링")
        dashboard = AppFactoryDashboard()
        
        # 기본 메트릭
        dashboard.render_header()
        
        col1, col2 = st.columns(2)
        with col1:
            dashboard.render_revenue_chart()
        with col2:
            dashboard.render_downloads_chart()
        
        dashboard.render_review_analysis()
        dashboard.render_marketing_performance()
        dashboard.render_app_details()
    
    # Tab 2: 수익 시뮬레이션
    with tab2:
        st.header("💰 수익 시뮬레이션 & 예측")
        
        simulator = RevenueSimulator()
        sample_apps = create_sample_app_portfolio()
        
        # 시나리오 분석
        st.subheader("📈 시나리오별 수익 예측")
        scenarios = simulator.create_revenue_scenarios(sample_apps)
        
        scenario_names = ['보수적', '기본', '낙관적']
        scenario_keys = ['conservative', 'base', 'optimistic']
        
        # 시나리오 비교 차트
        fig = go.Figure()
        
        for i, (name, key) in enumerate(zip(scenario_names, scenario_keys)):
            data = scenarios[key]
            fig.add_trace(go.Scatter(
                x=data['month'],
                y=data['total_revenue'],
                mode='lines+markers',
                name=f'{name} 시나리오',
                line=dict(width=3)
            ))
        
        fig.update_layout(
            title="📊 18개월 수익 예측 시나리오",
            xaxis_title="개월",
            yaxis_title="월 수익 (원)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 손익분기점 분석
        st.subheader("💡 손익분기점 분석")
        break_even = simulator.calculate_break_even_point(sample_apps, 3000000)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("손익분기점", f"{break_even['break_even_month']}개월")
        with col2:
            st.metric("초기 투자", f"₩{break_even['initial_investment']:,}")
        with col3:
            target_month = break_even['target_achievement_month']
            st.metric("목표 달성", f"{target_month}개월" if target_month else "미달성")
        
        # 수익화 방식별 기여도
        st.subheader("💰 수익화 방식별 기여도")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 앱별 수익화 분석
            app_monetization = []
            for app in sample_apps:
                analysis = simulator.analyze_monetization_mix(app)
                app_monetization.append({
                    'app_name': app.name,
                    'ads': analysis['percentages']['ads'],
                    'subscriptions': analysis['percentages']['subscriptions'],
                    'iap': analysis['percentages']['iap']
                })
            
            df_monetization = pd.DataFrame(app_monetization)
            
            fig = px.bar(
                df_monetization,
                x='app_name',
                y=['ads', 'subscriptions', 'iap'],
                title="앱별 수익화 방식 비중 (%)",
                labels={'value': '비중 (%)', 'variable': '수익화 방식'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 민감도 분석
            sensitivity = simulator.create_sensitivity_analysis(sample_apps[0])
            
            fig = px.line(
                sensitivity,
                x='factor',
                y='change_percent',
                color='variable',
                title="주요 변수 민감도 분석",
                labels={'factor': '변화 배수', 'change_percent': '수익 변화 (%)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: 마케팅 자동화
    with tab3:
        st.header("🤖 마케팅 자동화 현황")
        
        # 자동화 상태
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎯 ASO 자동화")
            st.success("✅ 활성화")
            st.markdown("- 2주마다 키워드 업데이트")
            st.markdown("- 경쟁 앱 분석 자동화")
            st.markdown("- 앱 설명 AI 최적화")
            
        with col2:
            st.subheader("📝 콘텐츠 생성")
            st.success("✅ 활성화") 
            st.markdown("- 블로그 포스트 자동 생성")
            st.markdown("- 유튜브 스크립트 생성")
            st.markdown("- 썸네일 이미지 생성")
            
        with col3:
            st.subheader("⭐ 리뷰 관리")
            st.success("✅ 활성화")
            st.markdown("- 실시간 리뷰 모니터링")
            st.markdown("- AI 기반 자동 응답")
            st.markdown("- 감정 분석 및 분류")
        
        # 최근 자동화 작업 로그
        st.subheader("📋 최근 자동화 작업")
        
        automation_log = pd.DataFrame([
            {'시간': '2024-01-15 14:30', '작업': 'ASO 최적화', '앱': 'Focus Timer Pro', '상태': '완료'},
            {'시간': '2024-01-15 14:25', '작업': '블로그 포스트 생성', '앱': 'Daily Habits', '상태': '완료'},
            {'시간': '2024-01-15 14:20', '작업': '리뷰 응답', '앱': 'Mission 100', '상태': '완료'},
            {'시간': '2024-01-15 14:15', '작업': '키워드 분석', '앱': 'Simple Todo', '상태': '진행중'},
        ])
        
        st.dataframe(automation_log, use_container_width=True)
        
        # 마케팅 성과 요약
        st.subheader("📈 마케팅 성과 요약")
        
        marketing_metrics = pd.DataFrame([
            {'지표': 'ASO 키워드 순위 개선', '이번 주': '+12위', '지난 주': '+8위'},
            {'지표': '리뷰 응답률', '이번 주': '94%', '지난 주': '87%'},
            {'지표': '콘텐츠 생성 수', '이번 주': '15개', '지난 주': '12개'},
            {'지표': '평균 앱 평점', '이번 주': '4.3', '지난 주': '4.1'},
        ])
        
        st.dataframe(marketing_metrics, use_container_width=True)
    
    # Tab 4: 워크플로우
    with tab4:
        st.header("📋 앱 공장 워크플로우")
        
        # 워크플로우 단계
        st.subheader("🔄 전체 프로세스")
        
        workflow_steps = [
            {"단계": "1. 아이디어 선정", "소요시간": "30분", "자동화율": "30%", "도구": "Google Trends, 경쟁 분석"},
            {"단계": "2. 앱 생성", "소요시간": "5분", "자동화율": "95%", "도구": "create_new_app.ps1"},
            {"단계": "3. UI 커스터마이징", "소요시간": "1-2시간", "자동화율": "60%", "도구": "Template + Manual"},
            {"단계": "4. 테스트 & 빌드", "소요시간": "1시간", "자동화율": "80%", "도구": "GitHub Actions"},
            {"단계": "5. 스토어 배포", "소요시간": "10분", "자동화율": "90%", "도구": "Fastlane + CI/CD"},
            {"단계": "6. 마케팅 실행", "소요시간": "5분", "자동화율": "95%", "도구": "Marketing Automation"},
            {"단계": "7. 성과 모니터링", "소요시간": "지속적", "자동화율": "85%", "도구": "Dashboard + Alerts"},
        ]
        
        df_workflow = pd.DataFrame(workflow_steps)
        st.dataframe(df_workflow, use_container_width=True)
        
        # 자동화율 차트
        fig = px.bar(
            df_workflow,
            x='단계',
            y='자동화율',
            title="단계별 자동화율",
            labels={'자동화율': '자동화율 (%)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # 다음 액션 추천
        st.subheader("🎯 다음 액션 추천")
        
        next_actions = [
            "🚀 **첫 번째 타이머 앱 출시** - Focus Timer Pro 개발 완료 및 배포",
            "📱 **두 번째 습관 앱 기획** - Daily Habits 아이디어 구체화",
            "🎯 **ASO 키워드 최적화** - '집중력', '타이머' 키워드 순위 개선",
            "📝 **콘텐츠 마케팅 강화** - 블로그 포스트 3개 추가 생성",
            "⭐ **리뷰 관리 개선** - 부정 리뷰 대응 템플릿 고도화"
        ]
        
        for action in next_actions:
            st.markdown(action)

if __name__ == "__main__":
    main()
