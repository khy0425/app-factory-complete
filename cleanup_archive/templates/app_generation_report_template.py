#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Generation Report Template System
앱 생성 과정 자동 문서화 및 보고서 템플릿
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from jinja2 import Template, Environment, FileSystemLoader
import markdown

@dataclass
class GenerationMetrics:
    """앱 생성 메트릭"""
    generation_time: float  # 초
    lines_of_code: int
    files_created: int
    dependencies_added: int
    tests_generated: int
    success_rate: float

@dataclass
class AppSpecification:
    """앱 사양"""
    app_name: str
    package_id: str
    category: str
    concept: str
    target_audience: str
    key_features: List[str]
    monetization_strategy: str
    target_rating: float
    target_downloads: int

@dataclass
class GenerationReport:
    """앱 생성 보고서"""
    app_id: str
    app_spec: AppSpecification
    generation_started: str
    generation_completed: str
    metrics: GenerationMetrics
    generated_files: List[str]
    ai_decisions: List[Dict]
    quality_score: float
    next_steps: List[str]
    estimated_launch_date: str
    risk_factors: List[str]

class AppGenerationReporter:
    """앱 생성 보고서 생성기"""

    def __init__(self, template_dir: str = None):
        self.template_dir = template_dir or os.path.join(os.path.dirname(__file__), 'notion_templates')
        self.ensure_template_directory()

    def ensure_template_directory(self):
        """템플릿 디렉토리 확인 및 생성"""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)

    def create_generation_report(self, app_data: Dict) -> GenerationReport:
        """앱 생성 보고서 생성"""

        # 앱 사양 파싱
        app_spec = AppSpecification(
            app_name=app_data.get('app_name', 'Unknown App'),
            package_id=app_data.get('package_id', 'com.unknown.app'),
            category=app_data.get('category', 'Productivity'),
            concept=app_data.get('concept', 'General'),
            target_audience=app_data.get('target_audience', 'General Users'),
            key_features=app_data.get('key_features', []),
            monetization_strategy=app_data.get('monetization', 'Freemium'),
            target_rating=app_data.get('target_rating', 4.0),
            target_downloads=app_data.get('target_downloads', 10000)
        )

        # 생성 메트릭 계산
        metrics = self._calculate_generation_metrics(app_data)

        # 품질 점수 계산
        quality_score = self._calculate_quality_score(app_spec, metrics)

        # AI 의사결정 로그
        ai_decisions = self._generate_ai_decisions(app_spec, metrics)

        # 다음 단계 생성
        next_steps = self._generate_next_steps(app_spec, quality_score)

        # 예상 출시일 계산
        estimated_launch = self._calculate_launch_date(quality_score, metrics)

        # 위험 요소 식별
        risk_factors = self._identify_risk_factors(app_spec, metrics, quality_score)

        report = GenerationReport(
            app_id=app_data.get('app_id', 'unknown'),
            app_spec=app_spec,
            generation_started=app_data.get('start_time', datetime.now().isoformat()),
            generation_completed=datetime.now().isoformat(),
            metrics=metrics,
            generated_files=app_data.get('generated_files', []),
            ai_decisions=ai_decisions,
            quality_score=quality_score,
            next_steps=next_steps,
            estimated_launch_date=estimated_launch,
            risk_factors=risk_factors
        )

        return report

    def _calculate_generation_metrics(self, app_data: Dict) -> GenerationMetrics:
        """생성 메트릭 계산"""

        # 실제 데이터가 없으면 예상값 생성
        generated_files = app_data.get('generated_files', [])

        return GenerationMetrics(
            generation_time=app_data.get('generation_time', 120.0),  # 2분 기본
            lines_of_code=len(generated_files) * 150,  # 파일당 평균 150줄
            files_created=len(generated_files),
            dependencies_added=app_data.get('dependencies_count', 8),
            tests_generated=app_data.get('tests_count', len(generated_files) // 2),
            success_rate=app_data.get('success_rate', 0.95)
        )

    def _calculate_quality_score(self, app_spec: AppSpecification, metrics: GenerationMetrics) -> float:
        """품질 점수 계산"""

        # 기본 점수 (60점)
        base_score = 60.0

        # 성공률 보너스 (20점)
        success_bonus = metrics.success_rate * 20

        # 기능 복잡도 보너스 (10점)
        feature_bonus = min(len(app_spec.key_features) * 2, 10)

        # 코드 품질 보너스 (10점)
        code_quality_bonus = min(metrics.lines_of_code / 1000 * 5, 10)

        total_score = base_score + success_bonus + feature_bonus + code_quality_bonus
        return min(total_score, 100.0)

    def _generate_ai_decisions(self, app_spec: AppSpecification, metrics: GenerationMetrics) -> List[Dict]:
        """AI 의사결정 로그 생성"""

        decisions = []

        # 아키텍처 선택
        decisions.append({
            'decision': 'MVVM Architecture Selected',
            'reasoning': f'{app_spec.category} 앱에 적합한 확장 가능한 아키텍처',
            'confidence': 0.9,
            'impact': 'High maintainability and testability'
        })

        # UI 프레임워크 선택
        decisions.append({
            'decision': 'Flutter Framework with Material Design',
            'reasoning': 'Cross-platform compatibility and rapid development',
            'confidence': 0.85,
            'impact': 'Faster time to market, consistent UI'
        })

        # 성과 기반 의사결정
        if metrics.success_rate > 0.9:
            decisions.append({
                'decision': 'High-Priority Development Track',
                'reasoning': f'Generation success rate {metrics.success_rate*100:.1f}%',
                'confidence': 0.95,
                'impact': 'Accelerated development timeline'
            })

        # 카테고리별 특화 결정
        if app_spec.category == 'Fitness':
            decisions.append({
                'decision': 'GigaChad Theme Integration',
                'reasoning': 'Target audience alignment with motivational fitness content',
                'confidence': 0.8,
                'impact': 'Enhanced user engagement and retention'
            })

        return decisions

    def _generate_next_steps(self, app_spec: AppSpecification, quality_score: float) -> List[str]:
        """다음 단계 생성"""

        steps = []

        # 품질 점수에 따른 단계
        if quality_score >= 85:
            steps.extend([
                "✅ Code review and quality assurance",
                "🧪 Comprehensive testing suite execution",
                "🎨 UI/UX polish and optimization",
                "📱 Device compatibility testing",
                "🚀 Store preparation and submission"
            ])
        elif quality_score >= 70:
            steps.extend([
                "🔧 Code optimization and refactoring",
                "🧪 Unit and integration testing",
                "🎯 Feature completion and validation",
                "📱 Performance optimization",
                "🔍 Security audit and compliance check"
            ])
        else:
            steps.extend([
                "⚠️ Critical issues resolution",
                "🔄 Architecture review and improvement",
                "🧪 Basic functionality testing",
                "📋 Requirements validation",
                "🛠️ Development environment setup"
            ])

        # 카테고리별 특화 단계
        if app_spec.category == 'Fitness':
            steps.append("💪 GigaChad branding and motivational content integration")
        elif app_spec.category == 'Productivity':
            steps.append("⏰ Time tracking and analytics implementation")

        # 마케팅 관련 단계
        steps.extend([
            "📊 ASO keyword research and optimization",
            "🎬 App store screenshots and videos creation",
            "📈 Marketing campaign planning",
            "🔄 User feedback collection system setup"
        ])

        return steps

    def _calculate_launch_date(self, quality_score: float, metrics: GenerationMetrics) -> str:
        """예상 출시일 계산"""

        base_days = 14  # 기본 2주

        # 품질 점수에 따른 조정
        if quality_score >= 85:
            adjustment_days = -3  # 3일 단축
        elif quality_score >= 70:
            adjustment_days = 0   # 변경 없음
        else:
            adjustment_days = 7   # 7일 연장

        # 복잡도에 따른 조정
        complexity_days = max(0, (metrics.files_created - 10) // 5)

        total_days = base_days + adjustment_days + complexity_days
        launch_date = datetime.now() + timedelta(days=total_days)

        return launch_date.strftime('%Y-%m-%d')

    def _identify_risk_factors(self, app_spec: AppSpecification, metrics: GenerationMetrics, quality_score: float) -> List[str]:
        """위험 요소 식별"""

        risks = []

        # 품질 기반 위험
        if quality_score < 70:
            risks.append("🔴 Low quality score - additional development time required")

        if metrics.success_rate < 0.8:
            risks.append("⚠️ Low generation success rate - potential technical issues")

        # 시장 위험
        if app_spec.target_downloads > 50000:
            risks.append("📈 High download target - requires strong marketing strategy")

        if app_spec.target_rating > 4.5:
            risks.append("⭐ High rating target - exceptional UX required")

        # 경쟁 위험
        competitive_categories = ['Fitness', 'Productivity', 'Social']
        if app_spec.category in competitive_categories:
            risks.append(f"🏆 Highly competitive {app_spec.category} market")

        # 기술 위험
        if metrics.dependencies_added > 15:
            risks.append("📦 High dependency count - maintenance complexity")

        if len(app_spec.key_features) > 8:
            risks.append("🔧 Feature complexity - scope creep risk")

        return risks

    def generate_notion_page_content(self, report: GenerationReport) -> str:
        """노션 페이지 콘텐츠 생성"""

        template = """
# 🏭 App Generation Report: {{ report.app_spec.app_name }}

**Generated on:** {{ report.generation_completed[:10] }}
**App ID:** `{{ report.app_id }}`
**Package:** `{{ report.app_spec.package_id }}`

---

## 📱 App Specification

| Property | Value |
|----------|-------|
| **Category** | {{ report.app_spec.category }} |
| **Concept** | {{ report.app_spec.concept }} |
| **Target Audience** | {{ report.app_spec.target_audience }} |
| **Monetization** | {{ report.app_spec.monetization_strategy }} |
| **Target Rating** | ⭐ {{ report.app_spec.target_rating }}/5.0 |
| **Target Downloads** | 📱 {{ "{:,}".format(report.app_spec.target_downloads) }} |

### 🎯 Key Features
{% for feature in report.app_spec.key_features %}
- {{ feature }}
{% endfor %}

---

## 📊 Generation Metrics

| Metric | Value |
|--------|-------|
| **Generation Time** | {{ "%.1f"|format(report.metrics.generation_time) }} seconds |
| **Files Created** | {{ report.metrics.files_created }} |
| **Lines of Code** | {{ "{:,}".format(report.metrics.lines_of_code) }} |
| **Dependencies** | {{ report.metrics.dependencies_added }} |
| **Tests Generated** | {{ report.metrics.tests_generated }} |
| **Success Rate** | {{ "%.1f"|format(report.metrics.success_rate * 100) }}% |

---

## 🏆 Quality Assessment

### Overall Score: {{ "%.1f"|format(report.quality_score) }}/100

{% if report.quality_score >= 85 %}
🟢 **Excellent** - Ready for advanced development
{% elif report.quality_score >= 70 %}
🟡 **Good** - Minor improvements needed
{% else %}
🔴 **Needs Work** - Significant improvements required
{% endif %}

---

## 🤖 AI Decisions Made

{% for decision in report.ai_decisions %}
### {{ decision.decision }}
- **Reasoning:** {{ decision.reasoning }}
- **Confidence:** {{ "%.0f"|format(decision.confidence * 100) }}%
- **Impact:** {{ decision.impact }}

{% endfor %}

---

## 📋 Next Steps

{% for step in report.next_steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

---

## ⚠️ Risk Factors

{% if report.risk_factors %}
{% for risk in report.risk_factors %}
- {{ risk }}
{% endfor %}
{% else %}
✅ No significant risks identified
{% endif %}

---

## 📅 Timeline

| Milestone | Date |
|-----------|------|
| **Generation Completed** | {{ report.generation_completed[:10] }} |
| **Estimated Launch** | {{ report.estimated_launch_date }} |
| **Time to Market** | {{ ((report.estimated_launch_date | strptime('%Y-%m-%d')) - (report.generation_completed[:10] | strptime('%Y-%m-%d'))).days }} days |

---

## 📁 Generated Files

```
{% for file in report.generated_files %}
{{ file }}
{% endfor %}
```

---

**Report generated by Ultra-Automated App Factory** 🤖
*Last updated: {{ report.generation_completed }}*
"""

        env = Environment()
        template_obj = env.from_string(template)

        return template_obj.render(report=report)

    def generate_markdown_report(self, report: GenerationReport) -> str:
        """마크다운 보고서 생성"""
        return self.generate_notion_page_content(report)

    def save_report(self, report: GenerationReport, format: str = 'json') -> str:
        """보고서 저장"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"app_generation_report_{report.app_id}_{timestamp}"

        if format == 'json':
            filepath = f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(report), f, indent=2, ensure_ascii=False)

        elif format == 'markdown':
            filepath = f"{filename}.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate_markdown_report(report))

        elif format == 'html':
            filepath = f"{filename}.html"
            md_content = self.generate_markdown_report(report)
            html_content = markdown.markdown(md_content, extensions=['tables'])
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

        return os.path.abspath(filepath)

def create_sample_report():
    """샘플 보고서 생성"""

    sample_app_data = {
        'app_id': 'gigachad_runner_pro',
        'app_name': 'GigaChad Runner Pro',
        'package_id': 'com.gigachad.runner.pro',
        'category': 'Fitness',
        'concept': 'Motivational Running App',
        'target_audience': 'Fitness Enthusiasts, Male 18-35',
        'key_features': [
            'Level System (Virgin → Ultra Chad)',
            '100-Day Challenge System',
            'Voice Coaching ("Pain is temporary, Chad is forever!")',
            'Social Leaderboard',
            'Progress Photo Tracking',
            'Aggressive Motivational Notifications'
        ],
        'monetization': 'Freemium with Premium Chad Mode',
        'target_rating': 4.5,
        'target_downloads': 25000,
        'start_time': (datetime.now() - timedelta(minutes=2)).isoformat(),
        'generation_time': 125.5,
        'generated_files': [
            'lib/main_mvvm.dart',
            'lib/models/user_profile.dart',
            'lib/models/mission.dart',
            'lib/viewmodels/home_viewmodel.dart',
            'lib/viewmodels/leaderboard_viewmodel.dart',
            'lib/views/home_view.dart',
            'lib/views/leaderboard_view.dart',
            'lib/services/mission_repository.dart',
            'lib/services/user_repository.dart',
            'lib/themes/app_theme.dart',
            'test/unit_tests.dart',
            'test/widget_tests.dart'
        ],
        'dependencies_count': 12,
        'tests_count': 8,
        'success_rate': 0.94
    }

    reporter = AppGenerationReporter()
    report = reporter.create_generation_report(sample_app_data)

    return report, reporter

def main():
    """메인 실행 함수"""

    print("📋 App Generation Report Template System")
    print("=" * 50)

    # 샘플 보고서 생성
    report, reporter = create_sample_report()

    print(f"✅ Generated report for: {report.app_spec.app_name}")
    print(f"📊 Quality Score: {report.quality_score:.1f}/100")
    print(f"🎯 Estimated Launch: {report.estimated_launch_date}")
    print(f"⚠️ Risk Factors: {len(report.risk_factors)}")

    # 다양한 형식으로 저장
    json_file = reporter.save_report(report, 'json')
    md_file = reporter.save_report(report, 'markdown')
    html_file = reporter.save_report(report, 'html')

    print(f"\n📁 Reports saved:")
    print(f"  JSON: {json_file}")
    print(f"  Markdown: {md_file}")
    print(f"  HTML: {html_file}")

    # 노션 콘텐츠 미리보기
    print(f"\n📄 Notion Content Preview:")
    print("-" * 30)
    notion_content = reporter.generate_notion_page_content(report)
    print(notion_content[:500] + "..." if len(notion_content) > 500 else notion_content)

if __name__ == "__main__":
    main()