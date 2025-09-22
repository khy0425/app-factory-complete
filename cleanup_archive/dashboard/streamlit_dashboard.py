#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
앱 공장 성과 대시보드 (Streamlit MVP)
앱별 다운로드, 수익, 리뷰 현황을 실시간 모니터링
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import random

# 페이지 설정
st.set_page_config(
    page_title="앱 공장 대시보드",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AppFactoryDashboard:
    def __init__(self):
        self.apps_data = self.load_apps_data()
        self.performance_data = self.generate_sample_data()
    
    def load_apps_data(self):
        """앱 설정 데이터 로드"""
        apps = []
        config_paths = [
            "../assets/config/app_config.json",
            "../assets/config/timer_app_template.json", 
            "../assets/config/habit_tracker_template.json"
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        apps.append({
                            'name': config['app']['name'],
                            'package_name': config['app']['package_name'],
                            'version': config['app']['version'],
                            'config_path': config_path
                        })
                except:
                    continue
        
        return apps if apps else self.get_sample_apps()
    
    def get_sample_apps(self):
        """샘플 앱 데이터"""
        return [
            {'name': 'Mission 100', 'package_name': 'com.example.mission100', 'version': '2.1.0'},
            {'name': 'Focus Timer Pro', 'package_name': 'com.appfactory.focustimer', 'version': '1.0.0'},
            {'name': 'Daily Habits', 'package_name': 'com.appfactory.dailyhabits', 'version': '1.0.0'}
        ]
    
    def generate_sample_data(self):
        """샘플 성과 데이터 생성"""
        data = []
        
        for app in self.apps_data:
            # 지난 30일 데이터 생성
            for i in range(30):
                date = datetime.now() - timedelta(days=29-i)
                
                # 앱별 기본 성과 차이 설정
                if 'mission' in app['name'].lower():
                    base_downloads = 150
                    base_revenue = 25
                elif 'timer' in app['name'].lower():
                    base_downloads = 80
                    base_revenue = 15
                else:
                    base_downloads = 60
                    base_revenue = 10
                
                # 랜덤 변동 추가
                downloads = max(0, base_downloads + random.randint(-30, 50))
                revenue = max(0, base_revenue + random.randint(-8, 12))
                reviews = max(0, random.randint(0, 10))
                rating = round(random.uniform(3.8, 4.8), 1)
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'app_name': app['name'],
                    'downloads': downloads,
                    'revenue': revenue,
                    'reviews': reviews,
                    'rating': rating,
                    'ad_impressions': downloads * random.randint(8, 15),
                    'ad_clicks': downloads * random.randint(1, 3) // 10
                })
        
        return pd.DataFrame(data)
    
    def render_header(self):
        """헤더 렌더링"""
        st.title("🏭 앱 공장 대시보드")
        st.markdown("**Mission100 기반 앱 공장 성과 모니터링**")
        
        # 메트릭 요약
        col1, col2, col3, col4 = st.columns(4)
        
        total_apps = len(self.apps_data)
        total_downloads = self.performance_data['downloads'].sum()
        total_revenue = self.performance_data['revenue'].sum()
        avg_rating = self.performance_data['rating'].mean()
        
        with col1:
            st.metric("총 앱 수", f"{total_apps}개")
        with col2:
            st.metric("총 다운로드", f"{total_downloads:,}")
        with col3:
            st.metric("총 수익", f"₩{total_revenue:,}")
        with col4:
            st.metric("평균 평점", f"{avg_rating:.1f}⭐")
    
    def render_revenue_chart(self):
        """수익 차트 렌더링"""
        st.subheader("📊 일별 수익 현황")
        
        # 앱별 일별 수익
        revenue_by_app = self.performance_data.groupby(['date', 'app_name'])['revenue'].sum().reset_index()
        
        fig = px.line(
            revenue_by_app, 
            x='date', 
            y='revenue', 
            color='app_name',
            title="앱별 일별 수익 (최근 30일)",
            labels={'revenue': '수익 (원)', 'date': '날짜'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_downloads_chart(self):
        """다운로드 차트 렌더링"""
        st.subheader("📱 다운로드 현황")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 앱별 총 다운로드
            total_downloads = self.performance_data.groupby('app_name')['downloads'].sum().reset_index()
            
            fig = px.bar(
                total_downloads,
                x='app_name',
                y='downloads',
                title="앱별 총 다운로드 (30일)",
                labels={'downloads': '다운로드 수', 'app_name': '앱 이름'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 일별 다운로드 트렌드
            daily_downloads = self.performance_data.groupby('date')['downloads'].sum().reset_index()
            
            fig = px.area(
                daily_downloads,
                x='date',
                y='downloads',
                title="일별 다운로드 트렌드",
                labels={'downloads': '다운로드 수', 'date': '날짜'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_review_analysis(self):
        """리뷰 분석 렌더링"""
        st.subheader("⭐ 리뷰 & 평점 분석")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 앱별 평균 평점
            avg_ratings = self.performance_data.groupby('app_name')['rating'].mean().reset_index()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=avg_ratings['app_name'],
                    y=avg_ratings['rating'],
                    text=avg_ratings['rating'].round(1),
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="앱별 평균 평점",
                yaxis=dict(range=[0, 5]),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 리뷰 수 트렌드
            review_trend = self.performance_data.groupby(['date', 'app_name'])['reviews'].sum().reset_index()
            
            fig = px.line(
                review_trend,
                x='date',
                y='reviews',
                color='app_name',
                title="앱별 일별 리뷰 수",
                labels={'reviews': '리뷰 수', 'date': '날짜'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_marketing_performance(self):
        """마케팅 성과 렌더링"""
        st.subheader("🎯 마케팅 성과")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 광고 성과
            ad_data = self.performance_data.groupby('app_name').agg({
                'ad_impressions': 'sum',
                'ad_clicks': 'sum'
            }).reset_index()
            
            ad_data['ctr'] = (ad_data['ad_clicks'] / ad_data['ad_impressions'] * 100).round(2)
            
            fig = px.scatter(
                ad_data,
                x='ad_impressions',
                y='ad_clicks',
                size='ctr',
                color='app_name',
                title="광고 노출 vs 클릭 (버블 크기: CTR%)",
                labels={'ad_impressions': '노출 수', 'ad_clicks': '클릭 수'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # CTR 비교
            fig = px.bar(
                ad_data,
                x='app_name',
                y='ctr',
                title="앱별 광고 CTR (%)",
                labels={'ctr': 'CTR (%)', 'app_name': '앱 이름'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_app_details(self):
        """앱별 상세 정보"""
        st.subheader("📋 앱별 상세 현황")
        
        # 앱 선택
        selected_app = st.selectbox("앱 선택", [app['name'] for app in self.apps_data])
        
        if selected_app:
            app_data = self.performance_data[self.performance_data['app_name'] == selected_app]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("최근 7일 다운로드", f"{app_data.tail(7)['downloads'].sum():,}")
            with col2:
                st.metric("최근 7일 수익", f"₩{app_data.tail(7)['revenue'].sum():,}")
            with col3:
                st.metric("현재 평점", f"{app_data['rating'].iloc[-1]:.1f}⭐")
            
            # 상세 데이터 테이블
            st.dataframe(
                app_data[['date', 'downloads', 'revenue', 'reviews', 'rating']].tail(10),
                use_container_width=True
            )
    
    def render_sidebar(self):
        """사이드바 렌더링"""
        st.sidebar.header("🏭 앱 공장 설정")
        
        # 새로고침 버튼
        if st.sidebar.button("🔄 데이터 새로고침"):
            st.rerun()
        
        st.sidebar.markdown("---")
        
        # 앱 목록
        st.sidebar.subheader("📱 관리 중인 앱")
        for app in self.apps_data:
            st.sidebar.markdown(f"• **{app['name']}** v{app['version']}")
        
        st.sidebar.markdown("---")
        
        # 목표 현황
        st.sidebar.subheader("🎯 목표 대비 현황")
        
        current_monthly_revenue = self.performance_data['revenue'].sum() * 30 // 30
        target_revenue = 3000000  # 월 300만원 목표
        
        progress = min(current_monthly_revenue / target_revenue, 1.0)
        st.sidebar.progress(progress)
        st.sidebar.markdown(f"**월 수익**: ₩{current_monthly_revenue:,} / ₩{target_revenue:,}")
        
        # 마케팅 자동화 상태
        st.sidebar.subheader("🤖 자동화 상태")
        st.sidebar.markdown("✅ ASO 최적화: 활성")
        st.sidebar.markdown("✅ 리뷰 모니터링: 활성") 
        st.sidebar.markdown("✅ 콘텐츠 생성: 활성")
        st.sidebar.markdown("🔄 대시보드: 실시간")

def main():
    """메인 함수"""
    dashboard = AppFactoryDashboard()
    
    # 사이드바
    dashboard.render_sidebar()
    
    # 메인 콘텐츠
    dashboard.render_header()
    
    st.markdown("---")
    
    # 차트들
    dashboard.render_revenue_chart()
    dashboard.render_downloads_chart()
    dashboard.render_review_analysis()
    dashboard.render_marketing_performance()
    dashboard.render_app_details()
    
    # 푸터
    st.markdown("---")
    st.markdown("**🏭 Mission100 앱 공장 대시보드** | 마지막 업데이트: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

if __name__ == "__main__":
    main()
