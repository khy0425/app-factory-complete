#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
우선순위 앱 현재 상태 요약
"""

import json
from datetime import datetime
from pathlib import Path

def check_app_status():
    """우선순위 앱들 상태 확인"""

    priority_apps = {
        "1_Mission100": {
            "name": "Mission100 - 푸쉬업 마스터",
            "folder": "mission100_v3",
            "package": "com.reaf.mission100",
            "version": "2.1.0+9",
            "status": "✅ 플레이스토어 업로드 완료",
            "next_action": "성과 모니터링 및 마케팅",
            "priority": "최우선 (완료)"
        },
        "2_GigaChad_Runner": {
            "name": "GigaChad Runner - GPS 런닝 트래커",
            "folder": "gigachad_runner",
            "package": "com.reaf.gigachad_runner",
            "version": "1.0.0+1",
            "status": "⚡ 패키지명 설정 완료, APK 빌드 시도 중",
            "next_action": "APK 빌드 완료 후 스토어 등록",
            "priority": "2순위"
        },
        "3_Squat_Master": {
            "name": "Squat Master - 스쿼트 챌린지",
            "folder": "squat_master",
            "package": "com.reaf.squat_master",
            "version": "1.0.0+1",
            "status": "⚡ 패키지명 설정 완료, 의존성 준비 완료",
            "next_action": "APK 빌드 및 스토어 등록",
            "priority": "3순위"
        }
    }

    # 폴더 존재 확인
    for app_key, app_info in priority_apps.items():
        app_path = Path(f"flutter_apps/{app_info['folder']}")
        app_info["folder_exists"] = app_path.exists()

        if app_path.exists():
            # pubspec.yaml 확인
            pubspec_path = app_path / "pubspec.yaml"
            app_info["pubspec_exists"] = pubspec_path.exists()

            # Android 설정 확인
            android_config = app_path / "android" / "app" / "build.gradle.kts"
            app_info["android_config_exists"] = android_config.exists()

            # 빌드 폴더 확인
            build_path = app_path / "build"
            app_info["has_build_folder"] = build_path.exists()

    return priority_apps

def create_status_report():
    """상태 보고서 생성"""
    apps = check_app_status()

    report = {
        "보고서_생성시간": datetime.now().isoformat(),
        "우선순위_앱_현황": apps,
        "전체_요약": {
            "총_앱수": len(apps),
            "완료된_앱": 1,  # Mission100
            "준비중인_앱": 2,  # Runner, Squat
            "예상_출시순서": [
                "Mission100 (완료)",
                "GigaChad Runner (1-2일 내)",
                "Squat Master (2-3일 내)"
            ]
        },
        "다음_단계_계획": {
            "즉시_실행": [
                "GigaChad Runner APK 빌드 완료",
                "Squat Master APK 빌드 완료"
            ],
            "단기_계획": [
                "두 앱 Google Play Console 등록",
                "스토어 리스팅 자료 준비",
                "APK 업로드 및 검토 제출"
            ],
            "중기_계획": [
                "세 앱 성과 비교 분석",
                "가장 성과 좋은 앱 타입 파악",
                "성공 패턴 기반 추가 앱 개발"
            ]
        }
    }

    return report

def create_status_dashboard():
    """상태 대시보드 HTML 생성"""
    apps = check_app_status()

    dashboard_html = f'''<!DOCTYPE html>
<html>
<head>
    <title>우선순위 앱 출시 현황</title>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Malgun Gothic', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .apps-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .app-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .app-card.completed {{
            border-left: 5px solid #00ff88;
        }}
        .app-card.in-progress {{
            border-left: 5px solid #ffd700;
        }}
        .app-card.pending {{
            border-left: 5px solid #ff6b6b;
        }}
        .app-title {{
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #ffd700;
        }}
        .app-details {{
            margin: 10px 0;
        }}
        .status {{
            font-weight: bold;
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
        }}
        .next-steps {{
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
        }}
        .step-item {{
            margin: 10px 0;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }}
        .priority {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            background: rgba(255,255,255,0.2);
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 우선순위 앱 출시 현황</h1>
        <h2>Mission100 → Runner → Squat Master</h2>
        <p>업데이트: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>

    <div class="apps-grid">'''

    for app_key, app_info in apps.items():
        card_class = "completed" if "완료" in app_info["status"] else ("in-progress" if "시도 중" in app_info["status"] else "pending")

        dashboard_html += f'''
        <div class="app-card {card_class}">
            <div class="priority">{app_info["priority"]}</div>
            <div class="app-title">{app_info["name"]}</div>
            <div class="app-details">
                <strong>패키지명:</strong> {app_info["package"]}<br>
                <strong>버전:</strong> {app_info["version"]}<br>
                <strong>폴더:</strong> {'✅' if app_info.get("folder_exists", False) else '❌'}<br>
                <strong>설정파일:</strong> {'✅' if app_info.get("android_config_exists", False) else '❌'}
            </div>
            <div class="status">{app_info["status"]}</div>
            <div><strong>다음 작업:</strong> {app_info["next_action"]}</div>
        </div>'''

    dashboard_html += f'''
    </div>

    <div class="next-steps">
        <h3>🎯 다음 단계</h3>
        <div class="step-item">
            <strong>즉시 실행:</strong> GigaChad Runner & Squat Master APK 빌드 완료
        </div>
        <div class="step-item">
            <strong>이번 주:</strong> Google Play Console에 두 앱 등록 및 업로드
        </div>
        <div class="step-item">
            <strong>다음 주:</strong> 세 앱 성과 데이터 비교 분석 시작
        </div>
        <div class="step-item">
            <strong>목표:</strong> 가장 성과 좋은 앱 타입 파악하여 확장 전략 수립
        </div>
    </div>

    <div style="text-align: center; margin-top: 30px; opacity: 0.7;">
        <p>🔄 자동 업데이트: 30분마다</p>
    </div>

    <script>
        // 30분마다 페이지 새로고침
        setInterval(() => {{
            window.location.reload();
        }}, 1800000);
    </script>
</body>
</html>'''

    return dashboard_html

def main():
    print("📊 우선순위 앱 현황 분석 중...")

    # 상태 보고서 생성
    report = create_status_report()

    # JSON 파일 저장
    with open("priority_apps_status.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 대시보드 HTML 생성
    dashboard_html = create_status_dashboard()
    with open("priority_apps_dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_html)

    # 요약 출력
    print("\n🚀 우선순위 앱 출시 현황")
    print("="*50)

    for app_key, app_info in report["우선순위_앱_현황"].items():
        print(f"\n{app_info['priority']}: {app_info['name']}")
        print(f"   📦 패키지: {app_info['package']}")
        print(f"   📊 상태: {app_info['status']}")
        print(f"   🎯 다음작업: {app_info['next_action']}")

    print(f"\n📈 전체 진행률:")
    summary = report["전체_요약"]
    print(f"   • 완료: {summary['완료된_앱']}/{summary['총_앱수']} ({int(summary['완료된_앱']/summary['총_앱수']*100)}%)")
    print(f"   • 준비중: {summary['준비중인_앱']}개")

    print(f"\n📁 생성 파일:")
    print(f"   • priority_apps_status.json - 상세 현황 보고서")
    print(f"   • priority_apps_dashboard.html - 실시간 대시보드")

    print(f"\n💡 권장 작업:")
    print(f"   1. priority_apps_dashboard.html 브라우저에서 열어 모니터링")
    print(f"   2. Flutter 빌드 문제 해결 후 APK 생성 완료")
    print(f"   3. Google Play Console에서 Runner, Squat 앱 생성")

if __name__ == "__main__":
    main()