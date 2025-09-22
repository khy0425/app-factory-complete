#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVP SaaS Demo - Investor Ready
실제 동작하는 App Factory 데모 (GigaChad Runner Template)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import random

# Page config
st.set_page_config(
    page_title="App Factory MVP Demo",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1A1A1A, #FFD700);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FFD700;
    }
    .demo-button {
        background: #FF0000;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">🏭 App Factory MVP Demo</h1>
        <p style="color: #FFD700; margin: 0;">The Tesla Gigafactory of Mobile Apps</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar - Demo Controls
    with st.sidebar:
        st.title("🎮 Demo Controls")

        demo_mode = st.selectbox(
            "Select Demo Mode",
            ["🚀 Live App Generation", "📊 Growth Analytics", "💰 Revenue Dashboard", "🤖 AI Marketing"]
        )

        st.markdown("---")

        # Mock customer selector
        customer_type = st.selectbox(
            "Customer Type",
            ["Startup", "Agency", "Enterprise"]
        )

        st.markdown("### 📈 Key Metrics")
        st.metric("Apps Generated", "127", "↗️ +23 this week")
        st.metric("Success Rate", "67%", "↗️ +12% vs industry")
        st.metric("Avg. Revenue/App", "$2,340", "↗️ +15% this month")

    # Main content based on demo mode
    if demo_mode == "🚀 Live App Generation":
        show_app_generation_demo()
    elif demo_mode == "📊 Growth Analytics":
        show_growth_analytics()
    elif demo_mode == "💰 Revenue Dashboard":
        show_revenue_dashboard()
    elif demo_mode == "🤖 AI Marketing":
        show_ai_marketing_demo()

def show_app_generation_demo():
    st.header("🚀 Live App Generation Demo")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎯 App Configuration")

        # App inputs
        app_name = st.text_input("App Name", "GigaChad Runner Pro")
        app_concept = st.selectbox("App Concept", ["Runner", "Timer", "Habit", "Productivity"])
        target_audience = st.text_input("Target Audience", "20-35세 남성 피트니스 애호가")
        marketing_budget = st.slider("Marketing Budget ($)", 1000, 20000, 10000)

        # Generation button
        if st.button("🏭 Generate App", type="primary"):
            show_generation_process()

    with col2:
        st.subheader("📱 Generated App Preview")

        # Mock app preview
        with st.container():
            st.markdown("#### App Details")
            st.write("**Package**: com.chadtech.gigachad_runner_pro")
            st.write("**Platform**: iOS, Android")
            st.write("**Template**: GigaChad Runner")

            # Mock screenshots
            st.markdown("#### Screenshots Preview")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.image("https://via.placeholder.com/200x400/1A1A1A/FFD700?text=Home", caption="Home Screen")
            with col_b:
                st.image("https://via.placeholder.com/200x400/FF0000/FFFFFF?text=Run", caption="Running Screen")
            with col_c:
                st.image("https://via.placeholder.com/200x400/FFD700/1A1A1A?text=Stats", caption="Stats Screen")

def show_generation_process():
    st.subheader("🔄 Generation Process")

    # Progress simulation
    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        ("🏗️ Creating Flutter project structure...", 15),
        ("🎨 Applying GigaChad branding...", 30),
        ("📱 Generating 50+ screens...", 50),
        ("🤖 Setting up AI marketing...", 70),
        ("📊 Configuring analytics...", 85),
        ("🚀 Preparing deployment...", 100)
    ]

    for step_text, progress in steps:
        status_text.text(step_text)
        progress_bar.progress(progress)
        time.sleep(0.8)

    st.success("✅ App Generated Successfully!")

    # Generation results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Generation Time", "2.3 min", "🚀 99% faster")
    with col2:
        st.metric("Cost Savings", "$47,700", "💰 95% cheaper")
    with col3:
        st.metric("Success Probability", "73%", "📈 14x higher")

    # Next steps
    st.markdown("### 🎯 Next Steps")
    st.markdown("""
    - ✅ **App Generated**: Ready for testing
    - 🚀 **Deployment**: Auto-deploy to stores in 1 click
    - 📊 **Marketing**: AI campaign already optimized
    - 📈 **Analytics**: Real-time dashboard activated
    """)

def show_growth_analytics():
    st.header("📊 Growth Analytics Dashboard")

    # Generate mock data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')

    # Mock app performance data
    apps_data = []
    for i, app_name in enumerate(["GigaChad Runner", "Alpha Timer", "Beast Habits"]):
        for date in dates:
            apps_data.append({
                'Date': date,
                'App': app_name,
                'Downloads': random.randint(50, 500) + i*100,
                'Revenue': random.randint(100, 1000) + i*200,
                'Rating': 4.0 + random.random() * 0.8,
                'Retention_D1': 60 + random.randint(-10, 20),
                'Retention_D7': 35 + random.randint(-10, 15)
            })

    df = pd.DataFrame(apps_data)

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_downloads = df.groupby('Date')['Downloads'].sum().iloc[-1]
        st.metric("Daily Downloads", f"{total_downloads:,}", "↗️ +23%")

    with col2:
        total_revenue = df.groupby('Date')['Revenue'].sum().iloc[-1]
        st.metric("Daily Revenue", f"${total_revenue:,}", "↗️ +18%")

    with col3:
        avg_rating = df['Rating'].mean()
        st.metric("Avg Rating", f"{avg_rating:.1f}★", "↗️ +0.2")

    with col4:
        avg_retention = df['Retention_D7'].mean()
        st.metric("D7 Retention", f"{avg_retention:.0f}%", "↗️ +5%")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Downloads Trend")
        daily_downloads = df.groupby(['Date', 'App'])['Downloads'].sum().reset_index()
        fig = px.line(daily_downloads, x='Date', y='Downloads', color='App',
                     title="Daily Downloads by App")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💰 Revenue Growth")
        daily_revenue = df.groupby(['Date', 'App'])['Revenue'].sum().reset_index()
        fig = px.area(daily_revenue, x='Date', y='Revenue', color='App',
                     title="Revenue Growth by App")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Retention cohort analysis
    st.subheader("🔄 Retention Cohort Analysis")

    # Mock cohort data
    cohort_data = {
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Day 1': [100, 95, 92, 89],
        'Day 7': [65, 68, 71, 73],
        'Day 30': [25, 28, 31, 34]
    }

    cohort_df = pd.DataFrame(cohort_data)
    st.dataframe(cohort_df, use_container_width=True)

def show_revenue_dashboard():
    st.header("💰 Revenue Dashboard")

    # Revenue metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Monthly Recurring Revenue", "$127K", "↗️ +34%")

    with col2:
        st.metric("Average Revenue Per User", "$23.40", "↗️ +12%")

    with col3:
        st.metric("Customer Lifetime Value", "$2,840", "↗️ +18%")

    with col4:
        st.metric("Revenue Share (Apps)", "$45K", "↗️ +67%")

    # Revenue breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Revenue by Source")
        revenue_sources = {
            'SaaS Subscriptions': 82000,
            'Revenue Share': 45000,
            'Marketplace': 12000
        }

        fig = px.pie(values=list(revenue_sources.values()),
                    names=list(revenue_sources.keys()),
                    title="Revenue Breakdown")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Growth Projection")

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        actual = [45, 67, 89, 127, 156, 198]
        projected = [45, 67, 89, 127, 156, 198, 245, 301, 370, 450, 540, 650]
        all_months = months + ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=actual, name='Actual', line=dict(color='#FFD700')))
        fig.add_trace(go.Scatter(x=all_months[6:], y=projected[6:], name='Projected',
                               line=dict(color='#FF0000', dash='dash')))
        fig.update_layout(title="MRR Growth ($K)", height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Customer breakdown
    st.subheader("👥 Customer Segments")

    customer_data = {
        'Segment': ['Startup', 'Agency', 'Enterprise'],
        'Count': [45, 23, 8],
        'ARPU': [500, 2000, 8000],
        'Total Revenue': [22500, 46000, 64000]
    }

    customer_df = pd.DataFrame(customer_data)
    st.dataframe(customer_df, use_container_width=True)

def show_ai_marketing_demo():
    st.header("🤖 AI Marketing Automation")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎯 Campaign Configuration")

        app_select = st.selectbox("Select App", ["GigaChad Runner", "Alpha Timer", "Beast Habits"])
        campaign_type = st.selectbox("Campaign Type", ["ASO Optimization", "Social Media", "Content Generation", "Review Response"])
        target_audience = st.text_input("Target Audience", "Fitness enthusiasts, age 20-35")

        if st.button("🚀 Launch AI Campaign", type="primary"):
            show_ai_campaign_process()

    with col2:
        st.subheader("📊 AI Performance")

        # AI metrics
        st.metric("Content Generation Speed", "50 posts/min", "🤖 AI-powered")
        st.metric("ASO Score Improvement", "+34%", "↗️ +12 ranking positions")
        st.metric("Response Time", "< 2 minutes", "⚡ Real-time")

        # Recent AI activities
        st.markdown("#### 🔄 Recent AI Activities")
        activities = [
            "✍️ Generated 25 Instagram posts for GigaChad Runner",
            "📊 Optimized keywords for Alpha Timer (+15 positions)",
            "👀 Responded to 12 negative reviews (sentiment +0.3)",
            "🎯 Created A/B test for Beast Habits onboarding"
        ]

        for activity in activities:
            st.write(f"• {activity}")

def show_ai_campaign_process():
    st.subheader("🤖 AI Campaign Execution")

    progress_bar = st.progress(0)
    status_text = st.empty()

    ai_steps = [
        ("🧠 Analyzing competitor data...", 20),
        ("🎯 Generating target keywords...", 40),
        ("✍️ Creating social media content...", 60),
        ("📊 Optimizing app store listing...", 80),
        ("🚀 Launching campaign...", 100)
    ]

    for step_text, progress in ai_steps:
        status_text.text(step_text)
        progress_bar.progress(progress)
        time.sleep(0.6)

    st.success("✅ AI Campaign Launched Successfully!")

    # AI results
    with st.expander("📝 Generated Content Preview"):
        st.markdown("""
        **Instagram Post 1:**
        "🗿 Ready to become a GigaChad? Start your 100-day transformation today! 💪 #GigaChadRunner #FitnessMotivation #TransformationTuesday"

        **Twitter Post:**
        "Day 1 vs Day 100. The choice is yours. 🔥 #SigmaGrindset #RunningMotivation"

        **Keywords Added:**
        - "기가차드 러닝앱" (Primary)
        - "100일 운동챌린지" (Secondary)
        - "시그마 피트니스" (Long-tail)
        """)

    # Expected results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Expected Reach", "50K", "📈 Organic")
    with col2:
        st.metric("Engagement Rate", "8.5%", "↗️ +2.3%")
    with col3:
        st.metric("Download Increase", "+25%", "🎯 Projected")

if __name__ == "__main__":
    main()