#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
완전 자동화 오류 모니터링 시스템
- 오류 자동 감지 및 분석
- Notion 데이터베이스 자동 정리
- Slack 알림 시스템
- 자동 수정 시도 및 수동 수정 필요시 알림
"""

import asyncio
import json
import os
import re
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import requests
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class ErrorMonitoringSystem:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Notion 설정
        self.notion_token = os.getenv('NOTION_API_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')

        # Slack 설정
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

        # 오류 로그 폴더
        self.error_logs_dir = Path("error_logs")
        self.error_logs_dir.mkdir(exist_ok=True)

        # 자동 수정 시도 히스토리
        self.auto_fix_history = []

    async def monitor_all_processes(self):
        """모든 백그라운드 프로세스 모니터링"""

        print("🔍 오류 모니터링 시스템 시작")
        print("- 백그라운드 프로세스 감시")
        print("- Flutter 빌드 오류 감지")
        print("- Python 스크립트 오류 감지")
        print("- 자동 수정 시도")
        print("- Notion 정리 및 Slack 알림")
        print("=" * 60)

        monitoring_tasks = [
            self.monitor_flutter_builds(),
            self.monitor_python_scripts(),
            self.monitor_api_errors(),
            self.check_dependency_issues()
        ]

        await asyncio.gather(*monitoring_tasks)

    async def monitor_flutter_builds(self):
        """Flutter 빌드 오류 모니터링"""

        flutter_apps_dir = Path("flutter_apps")
        if not flutter_apps_dir.exists():
            return

        for app_dir in flutter_apps_dir.iterdir():
            if app_dir.is_dir():
                await self.check_flutter_app_health(app_dir)

    async def check_flutter_app_health(self, app_dir: Path):
        """개별 Flutter 앱 상태 체크"""

        print(f"🔍 Flutter 앱 상태 체크: {app_dir.name}")

        try:
            # pubspec.yaml 체크
            pubspec_file = app_dir / "pubspec.yaml"
            if not pubspec_file.exists():
                await self.report_error(
                    error_type="Missing File",
                    app_name=app_dir.name,
                    description="pubspec.yaml 파일이 없습니다",
                    severity="High",
                    auto_fixable=True
                )
                return

            # 의존성 체크
            result = subprocess.run(
                ["flutter", "pub", "get"],
                cwd=app_dir,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                await self.handle_flutter_dependency_error(app_dir, result.stderr)

            # 분석 체크
            result = subprocess.run(
                ["flutter", "analyze"],
                cwd=app_dir,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                await self.handle_flutter_analysis_error(app_dir, result.stdout)

        except subprocess.TimeoutExpired:
            await self.report_error(
                error_type="Timeout",
                app_name=app_dir.name,
                description="Flutter 명령어 실행 시간 초과",
                severity="Medium",
                auto_fixable=False
            )

        except Exception as e:
            await self.report_error(
                error_type="System Error",
                app_name=app_dir.name,
                description=f"시스템 오류: {str(e)}",
                severity="High",
                auto_fixable=False
            )

    async def handle_flutter_dependency_error(self, app_dir: Path, error_output: str):
        """Flutter 의존성 오류 처리"""

        print(f"⚠️ 의존성 오류 감지: {app_dir.name}")

        # AI를 사용해 오류 분석
        analysis = await self.analyze_error_with_ai(error_output, "Flutter Dependency")

        if analysis.get("auto_fixable", False):
            fix_success = await self.attempt_dependency_fix(app_dir, analysis)

            if fix_success:
                await self.report_success(
                    app_name=app_dir.name,
                    issue="의존성 오류",
                    fix_applied=analysis.get("fix_description", "의존성 수정")
                )
            else:
                await self.report_error(
                    error_type="Dependency Error",
                    app_name=app_dir.name,
                    description=error_output,
                    severity="High",
                    auto_fixable=False,
                    ai_analysis=analysis
                )
        else:
            await self.report_error(
                error_type="Dependency Error",
                app_name=app_dir.name,
                description=error_output,
                severity="High",
                auto_fixable=False,
                ai_analysis=analysis
            )

    async def attempt_dependency_fix(self, app_dir: Path, analysis: Dict) -> bool:
        """의존성 오류 자동 수정 시도"""

        try:
            # 일반적인 수정 방법들
            fixes = [
                ["flutter", "clean"],
                ["flutter", "pub", "get"],
                ["flutter", "pub", "upgrade"]
            ]

            for fix_command in fixes:
                print(f"🔧 수정 시도: {' '.join(fix_command)}")

                result = subprocess.run(
                    fix_command,
                    cwd=app_dir,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                if result.returncode == 0:
                    # 수정 후 다시 테스트
                    test_result = subprocess.run(
                        ["flutter", "pub", "get"],
                        cwd=app_dir,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )

                    if test_result.returncode == 0:
                        self.auto_fix_history.append({
                            "app": app_dir.name,
                            "issue": "dependency_error",
                            "fix": ' '.join(fix_command),
                            "timestamp": datetime.now().isoformat(),
                            "success": True
                        })
                        return True

            return False

        except Exception as e:
            print(f"❌ 자동 수정 실패: {e}")
            return False

    async def monitor_python_scripts(self):
        """Python 스크립트 오류 모니터링"""

        # 실행 중인 Python 스크립트들의 로그 확인
        log_files = list(Path(".").glob("*.log"))

        for log_file in log_files:
            if log_file.stat().st_size > 0:
                await self.check_python_log_errors(log_file)

    async def check_python_log_errors(self, log_file: Path):
        """Python 로그 파일에서 오류 확인"""

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 오류 패턴 감지
            error_patterns = [
                r"ERROR:.*",
                r"Traceback.*",
                r"Exception:.*",
                r"Failed.*",
                r"TimeoutError.*"
            ]

            for pattern in error_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)

                if matches:
                    await self.report_error(
                        error_type="Python Script Error",
                        app_name=log_file.stem,
                        description="\n".join(matches[-3:]),  # 최근 3개 오류
                        severity="Medium",
                        auto_fixable=True
                    )

        except Exception as e:
            print(f"❌ 로그 파일 읽기 실패: {e}")

    async def monitor_api_errors(self):
        """API 호출 오류 모니터링"""

        # Gemini API 상태 체크
        try:
            test_response = await self.model.generate_content_async("Test")
            if not test_response.text:
                raise Exception("Empty response from Gemini API")

        except Exception as e:
            await self.report_error(
                error_type="API Error",
                app_name="Gemini API",
                description=f"Gemini API 오류: {str(e)}",
                severity="Critical",
                auto_fixable=False
            )

        # Notion API 상태 체크 (설정되어 있다면)
        if self.notion_token:
            try:
                headers = {
                    "Authorization": f"Bearer {self.notion_token}",
                    "Notion-Version": "2022-06-28"
                }
                response = requests.get("https://api.notion.com/v1/users/me", headers=headers)
                if response.status_code != 200:
                    raise Exception(f"Notion API error: {response.status_code}")

            except Exception as e:
                await self.report_error(
                    error_type="API Error",
                    app_name="Notion API",
                    description=f"Notion API 오류: {str(e)}",
                    severity="Medium",
                    auto_fixable=False
                )

    async def check_dependency_issues(self):
        """의존성 및 환경 문제 체크"""

        # Flutter 설치 체크
        try:
            result = subprocess.run(["flutter", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                await self.report_error(
                    error_type="Environment Error",
                    app_name="Flutter",
                    description="Flutter가 설치되지 않았거나 PATH에 없습니다",
                    severity="Critical",
                    auto_fixable=False
                )
        except FileNotFoundError:
            await self.report_error(
                error_type="Environment Error",
                app_name="Flutter",
                description="Flutter 명령어를 찾을 수 없습니다",
                severity="Critical",
                auto_fixable=False
            )

        # Python 패키지 체크
        required_packages = ["google-generativeai", "python-dotenv", "requests"]
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                await self.report_error(
                    error_type="Dependency Error",
                    app_name="Python",
                    description=f"필수 패키지 누락: {package}",
                    severity="High",
                    auto_fixable=True
                )

    async def analyze_error_with_ai(self, error_message: str, error_type: str) -> Dict:
        """AI를 사용한 오류 분석"""

        analysis_prompt = f"""
다음 {error_type} 오류를 분석하고 해결 방법을 제시해주세요:

오류 메시지:
{error_message}

다음 JSON 형식으로 분석 결과를 제공해주세요:
{{
    "error_category": "오류 카테고리",
    "severity": "Low/Medium/High/Critical",
    "auto_fixable": true/false,
    "fix_description": "수정 방법 설명",
    "manual_steps": ["수동으로 해야할 단계들"],
    "prevention": "예방 방법",
    "estimated_fix_time": "예상 수정 시간"
}}
"""

        try:
            response = await self.model.generate_content_async(analysis_prompt)

            # JSON 추출
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "error_category": "Unknown",
                    "severity": "Medium",
                    "auto_fixable": False,
                    "fix_description": response.text,
                    "manual_steps": ["AI 분석 결과를 참조하여 수동 수정"],
                    "prevention": "정기적인 모니터링",
                    "estimated_fix_time": "30분"
                }

        except Exception as e:
            return {
                "error_category": "AI Analysis Failed",
                "severity": "Medium",
                "auto_fixable": False,
                "fix_description": f"AI 분석 실패: {str(e)}",
                "manual_steps": ["수동으로 오류 분석 및 수정"],
                "prevention": "AI API 상태 확인",
                "estimated_fix_time": "1시간"
            }

    async def report_error(self, error_type: str, app_name: str, description: str,
                          severity: str, auto_fixable: bool, ai_analysis: Optional[Dict] = None):
        """오류 보고 (Notion + Slack)"""

        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "app_name": app_name,
            "description": description,
            "severity": severity,
            "auto_fixable": auto_fixable,
            "ai_analysis": ai_analysis or {},
            "status": "New"
        }

        # 로컬 로그 저장
        await self.save_error_log(error_data)

        # Notion에 오류 기록
        await self.create_notion_error_entry(error_data)

        # Slack 알림
        await self.send_slack_notification(error_data)

        print(f"🚨 오류 보고 완료: {error_type} - {app_name}")

    async def report_success(self, app_name: str, issue: str, fix_applied: str):
        """자동 수정 성공 보고"""

        success_data = {
            "timestamp": datetime.now().isoformat(),
            "app_name": app_name,
            "issue": issue,
            "fix_applied": fix_applied,
            "status": "Auto-Fixed"
        }

        # Notion에 성공 기록
        await self.create_notion_success_entry(success_data)

        # Slack 성공 알림
        await self.send_slack_success_notification(success_data)

        print(f"✅ 자동 수정 성공: {app_name} - {issue}")

    async def save_error_log(self, error_data: Dict):
        """로컬 오류 로그 저장"""

        log_file = self.error_logs_dir / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(error_data, f, ensure_ascii=False, indent=2)

    async def create_notion_error_entry(self, error_data: Dict):
        """Notion 데이터베이스에 오류 기록"""

        if not self.notion_token or not self.notion_database_id:
            print("⚠️ Notion 설정이 없어 로컬 로그만 저장")
            return

        try:
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }

            # Notion 페이지 생성
            data = {
                "parent": {"database_id": self.notion_database_id},
                "properties": {
                    "제목": {
                        "title": [{"text": {"content": f"[{error_data['severity']}] {error_data['error_type']} - {error_data['app_name']}"}}]
                    },
                    "타입": {
                        "select": {"name": error_data['error_type']}
                    },
                    "앱": {
                        "rich_text": [{"text": {"content": error_data['app_name']}}]
                    },
                    "심각도": {
                        "select": {"name": error_data['severity']}
                    },
                    "자동수정가능": {
                        "checkbox": error_data['auto_fixable']
                    },
                    "상태": {
                        "select": {"name": error_data['status']}
                    },
                    "발생시간": {
                        "date": {"start": error_data['timestamp']}
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": error_data['description']}}]
                        }
                    }
                ]
            }

            if error_data.get('ai_analysis'):
                ai_analysis = error_data['ai_analysis']
                data["children"].extend([
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "AI 분석 결과"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"수정 방법: {ai_analysis.get('fix_description', 'N/A')}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"예상 수정 시간: {ai_analysis.get('estimated_fix_time', 'N/A')}"}}]
                        }
                    }
                ])

            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                print("✅ Notion에 오류 기록 완료")
            else:
                print(f"⚠️ Notion 기록 실패: {response.status_code}")

        except Exception as e:
            print(f"❌ Notion 오류 기록 실패: {e}")

    async def create_notion_success_entry(self, success_data: Dict):
        """Notion에 자동 수정 성공 기록"""

        if not self.notion_token or not self.notion_database_id:
            return

        try:
            headers = {
                "Authorization": f"Bearer {self.notion_token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }

            data = {
                "parent": {"database_id": self.notion_database_id},
                "properties": {
                    "제목": {
                        "title": [{"text": {"content": f"[SUCCESS] {success_data['issue']} - {success_data['app_name']}"}}]
                    },
                    "타입": {
                        "select": {"name": "Auto-Fix Success"}
                    },
                    "앱": {
                        "rich_text": [{"text": {"content": success_data['app_name']}}]
                    },
                    "심각도": {
                        "select": {"name": "Low"}
                    },
                    "상태": {
                        "select": {"name": "Resolved"}
                    },
                    "발생시간": {
                        "date": {"start": success_data['timestamp']}
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"자동 수정 적용: {success_data['fix_applied']}"}}]
                        }
                    }
                ]
            }

            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                print("✅ Notion에 성공 기록 완료")

        except Exception as e:
            print(f"❌ Notion 성공 기록 실패: {e}")

    async def send_slack_notification(self, error_data: Dict):
        """Slack 오류 알림"""

        if not self.slack_webhook_url:
            print("⚠️ Slack Webhook URL이 설정되지 않음")
            return

        try:
            severity_emoji = {
                "Low": "🟡",
                "Medium": "🟠",
                "High": "🔴",
                "Critical": "🆘"
            }

            emoji = severity_emoji.get(error_data['severity'], "⚠️")

            if error_data['auto_fixable']:
                action_text = "🔧 자동 수정 시도 중..."
            else:
                action_text = "👨‍💻 수동 수정 필요"

            message = {
                "text": f"{emoji} 앱 팩토리 오류 발생",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{emoji} 앱 팩토리 오류 발생"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*앱:* {error_data['app_name']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*유형:* {error_data['error_type']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*심각도:* {error_data['severity']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*상태:* {action_text}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*오류 내용:*\n```{error_data['description'][:500]}```"
                        }
                    }
                ]
            }

            if error_data.get('ai_analysis'):
                ai_analysis = error_data['ai_analysis']
                message["blocks"].append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*AI 분석:*\n• {ai_analysis.get('fix_description', 'N/A')}\n• 예상 수정 시간: {ai_analysis.get('estimated_fix_time', 'N/A')}"
                    }
                })

            response = requests.post(self.slack_webhook_url, json=message)

            if response.status_code == 200:
                print("✅ Slack 알림 전송 완료")
            else:
                print(f"⚠️ Slack 알림 실패: {response.status_code}")

        except Exception as e:
            print(f"❌ Slack 알림 전송 실패: {e}")

    async def send_slack_success_notification(self, success_data: Dict):
        """Slack 자동 수정 성공 알림"""

        if not self.slack_webhook_url:
            return

        try:
            message = {
                "text": "✅ 자동 수정 성공",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "✅ 자동 수정 성공"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*앱:* {success_data['app_name']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*문제:* {success_data['issue']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*수정 내용:* {success_data['fix_applied']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*시간:* {success_data['timestamp']}"
                            }
                        ]
                    }
                ]
            }

            response = requests.post(self.slack_webhook_url, json=message)

            if response.status_code == 200:
                print("✅ Slack 성공 알림 전송 완료")

        except Exception as e:
            print(f"❌ Slack 성공 알림 실패: {e}")

    async def generate_daily_report(self):
        """일일 오류 리포트 생성"""

        today = datetime.now().strftime('%Y-%m-%d')

        # 오늘 발생한 오류들 수집
        error_files = list(self.error_logs_dir.glob(f"error_{today.replace('-', '')}*.json"))

        if not error_files:
            print("📊 오늘 발생한 오류가 없습니다.")
            return

        errors = []
        for error_file in error_files:
            with open(error_file, "r", encoding="utf-8") as f:
                errors.append(json.load(f))

        # 통계 생성
        stats = {
            "total_errors": len(errors),
            "by_severity": {},
            "by_type": {},
            "auto_fixed": len([e for e in errors if e.get('status') == 'Auto-Fixed']),
            "manual_required": len([e for e in errors if not e.get('auto_fixable', False)])
        }

        for error in errors:
            severity = error.get('severity', 'Unknown')
            error_type = error.get('error_type', 'Unknown')

            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
            stats['by_type'][error_type] = stats['by_type'].get(error_type, 0) + 1

        # Slack 일일 리포트 전송
        await self.send_daily_report_to_slack(stats, today)

    async def send_daily_report_to_slack(self, stats: Dict, date: str):
        """Slack 일일 리포트 전송"""

        if not self.slack_webhook_url:
            return

        try:
            severity_emojis = {"Low": "🟡", "Medium": "🟠", "High": "🔴", "Critical": "🆘"}

            severity_text = "\n".join([
                f"{severity_emojis.get(sev, '⚪')} {sev}: {count}개"
                for sev, count in stats['by_severity'].items()
            ])

            type_text = "\n".join([
                f"• {error_type}: {count}개"
                for error_type, count in stats['by_type'].items()
            ])

            message = {
                "text": f"📊 앱 팩토리 일일 리포트 ({date})",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"📊 앱 팩토리 일일 리포트 ({date})"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*총 오류:* {stats['total_errors']}개"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*자동 수정:* {stats['auto_fixed']}개"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*수동 필요:* {stats['manual_required']}개"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*심각도별 분포:*\n{severity_text}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*오류 유형별:*\n{type_text}"
                        }
                    }
                ]
            }

            response = requests.post(self.slack_webhook_url, json=message)

            if response.status_code == 200:
                print("✅ 일일 리포트 전송 완료")

        except Exception as e:
            print(f"❌ 일일 리포트 전송 실패: {e}")

async def main():
    """메인 실행 함수"""
    print("🤖 완전 자동화 오류 모니터링 시스템")
    print("- 실시간 오류 감지 및 분석")
    print("- AI 기반 자동 수정 시도")
    print("- Notion 데이터베이스 자동 정리")
    print("- Slack 실시간 알림")
    print("=" * 60)

    monitor = ErrorMonitoringSystem()

    # 모니터링 시작
    await monitor.monitor_all_processes()

    # 일일 리포트 생성
    await monitor.generate_daily_report()

if __name__ == "__main__":
    asyncio.run(main())