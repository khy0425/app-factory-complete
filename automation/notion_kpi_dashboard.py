#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion KPI Dashboard
서버리스 앱 팩토리 KPI 대시보드 자동 업데이트 시스템
"""

import json
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from .config_manager import SecureConfigManager

class NotionKPIDashboard:
    """Notion KPI 대시보드 관리자"""

    def __init__(self):
        self.config_manager = SecureConfigManager()
        self.notion_token = self.config_manager.get_api_key("NOTION_API_TOKEN")

        if not self.notion_token:
            raise Exception("NOTION_API_TOKEN이 설정되지 않았습니다. config_manager --setup을 실행하세요.")

        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        self.logger = logging.getLogger(__name__)

        # 데이터베이스 ID들 (실제 FAF Console DB)
        self.databases = {
            "apps": "2740ba1b-861e-813e-be14-cedfd41e3ff5",  # FAF Console 앱 마스터 DB
            "kpis": None,           # KPI 추적 DB
            "budget": None,         # 예산 추적 DB
            "decisions": None       # AI 의사결정 로그 DB
        }

    def create_dashboard_structure(self) -> Dict:
        """Notion 대시보드 구조 생성"""

        results = {
            "success": True,
            "created_databases": {},
            "errors": []
        }

        try:
            # 1. 앱 마스터 데이터베이스 생성
            apps_db = self._create_apps_database()
            if apps_db:
                results["created_databases"]["apps"] = apps_db["id"]
                self.databases["apps"] = apps_db["id"]

            # 2. KPI 추적 데이터베이스 생성
            kpis_db = self._create_kpis_database()
            if kpis_db:
                results["created_databases"]["kpis"] = kpis_db["id"]
                self.databases["kpis"] = kpis_db["id"]

            # 3. 예산 추적 데이터베이스 생성
            budget_db = self._create_budget_database()
            if budget_db:
                results["created_databases"]["budget"] = budget_db["id"]
                self.databases["budget"] = budget_db["id"]

            # 4. AI 의사결정 로그 데이터베이스 생성
            decisions_db = self._create_decisions_database()
            if decisions_db:
                results["created_databases"]["decisions"] = decisions_db["id"]
                self.databases["decisions"] = decisions_db["id"]

            # 5. 대시보드 페이지 생성
            dashboard_page = self._create_dashboard_page()
            if dashboard_page:
                results["dashboard_page"] = dashboard_page["id"]

            self.logger.info("Notion 대시보드 구조 생성 완료")

        except Exception as e:
            results["success"] = False
            results["errors"].append(str(e))
            self.logger.error(f"대시보드 생성 실패: {e}")

        return results

    def _create_apps_database(self) -> Optional[Dict]:
        """앱 마스터 데이터베이스 생성"""

        schema = {
            "title": [{"type": "title"}],
            "Status": {
                "select": {
                    "options": [
                        {"name": "Draft", "color": "gray"},
                        {"name": "Generating", "color": "yellow"},
                        {"name": "QA Testing", "color": "orange"},
                        {"name": "Store Review", "color": "blue"},
                        {"name": "Published", "color": "green"},
                        {"name": "Rejected", "color": "red"},
                        {"name": "Archived", "color": "default"}
                    ]
                }
            },
            "Category": {
                "select": {
                    "options": [
                        {"name": "Fitness", "color": "green"},
                        {"name": "Productivity", "color": "blue"},
                        {"name": "Utilities", "color": "orange"},
                        {"name": "Health", "color": "pink"},
                        {"name": "Education", "color": "purple"},
                        {"name": "Finance", "color": "yellow"}
                    ]
                }
            },
            "Generation Cost": {"number": {"format": "dollar"}},
            "Quality Score": {"number": {}},
            "Store Ready": {"checkbox": {}},
            "Monthly Revenue": {"number": {"format": "dollar"}},
            "Downloads": {"number": {}},
            "Rating": {"number": {}},
            "Crash Rate": {"number": {"format": "percent"}},
            "Created Date": {"date": {}},
            "Launch Date": {"date": {}},
            "Duplicate Risk": {
                "select": {
                    "options": [
                        {"name": "Low", "color": "green"},
                        {"name": "Warning", "color": "yellow"},
                        {"name": "Critical", "color": "red"}
                    ]
                }
            },
            "Budget Month": {"select": {"options": []}},  # 동적으로 추가
            "Notes": {"rich_text": {}}
        }

        return self._create_database("🏭 서버리스 앱 팩토리 - 앱 마스터", schema)

    def _create_kpis_database(self) -> Optional[Dict]:
        """KPI 추적 데이터베이스 생성"""

        schema = {
            "title": [{"type": "title"}],
            "App Name": {
                "relation": {
                    "database_id": self.databases.get("apps", ""),
                    "type": "dual_property"
                }
            },
            "Date": {"date": {}},
            "Metric Type": {
                "select": {
                    "options": [
                        {"name": "Downloads", "color": "blue"},
                        {"name": "Revenue", "color": "green"},
                        {"name": "Active Users", "color": "orange"},
                        {"name": "Retention D1", "color": "purple"},
                        {"name": "Retention D7", "color": "pink"},
                        {"name": "ARPU", "color": "yellow"},
                        {"name": "Crash Rate", "color": "red"},
                        {"name": "Rating", "color": "gray"}
                    ]
                }
            },
            "Value": {"number": {}},
            "Previous Value": {"number": {}},
            "Change": {"formula": {"expression": "prop(\"Value\") - prop(\"Previous Value\")"}},
            "Change %": {"formula": {"expression": "if(prop(\"Previous Value\") > 0, (prop(\"Value\") - prop(\"Previous Value\")) / prop(\"Previous Value\") * 100, 0)"}},
            "Target": {"number": {}},
            "Target Achievement": {"formula": {"expression": "if(prop(\"Target\") > 0, prop(\"Value\") / prop(\"Target\") * 100, 0)"}},
            "Alert": {"checkbox": {}},
            "Notes": {"rich_text": {}}
        }

        return self._create_database("📊 KPI 추적", schema)

    def _create_budget_database(self) -> Optional[Dict]:
        """예산 추적 데이터베이스 생성"""

        schema = {
            "title": [{"type": "title"}],
            "Month": {"date": {}},
            "Budget Type": {
                "select": {
                    "options": [
                        {"name": "Claude Pro", "color": "blue"},
                        {"name": "Gemini API", "color": "green"},
                        {"name": "App Generation", "color": "orange"},
                        {"name": "Store Fees", "color": "yellow"},
                        {"name": "Marketing", "color": "purple"},
                        {"name": "Other", "color": "gray"}
                    ]
                }
            },
            "Budgeted Amount": {"number": {"format": "dollar"}},
            "Actual Spent": {"number": {"format": "dollar"}},
            "Remaining": {"formula": {"expression": "prop(\"Budgeted Amount\") - prop(\"Actual Spent\")"}},
            "Usage %": {"formula": {"expression": "if(prop(\"Budgeted Amount\") > 0, prop(\"Actual Spent\") / prop(\"Budgeted Amount\") * 100, 0)"}},
            "Apps Generated": {"number": {}},
            "Cost Per App": {"formula": {"expression": "if(prop(\"Apps Generated\") > 0, prop(\"Actual Spent\") / prop(\"Apps Generated\"), 0)"}},
            "Revenue Generated": {"number": {"format": "dollar"}},
            "ROI": {"formula": {"expression": "if(prop(\"Actual Spent\") > 0, (prop(\"Revenue Generated\") - prop(\"Actual Spent\")) / prop(\"Actual Spent\") * 100, 0)"}},
            "Alert Level": {
                "select": {
                    "options": [
                        {"name": "Green", "color": "green"},
                        {"name": "Yellow", "color": "yellow"},
                        {"name": "Red", "color": "red"}
                    ]
                }
            }
        }

        return self._create_database("💰 예산 추적", schema)

    def _create_decisions_database(self) -> Optional[Dict]:
        """AI 의사결정 로그 데이터베이스 생성"""

        schema = {
            "title": [{"type": "title"}],
            "Timestamp": {"date": {}},
            "Decision Type": {
                "select": {
                    "options": [
                        {"name": "App Generation", "color": "blue"},
                        {"name": "Budget Control", "color": "green"},
                        {"name": "Quality Gate", "color": "orange"},
                        {"name": "Store Compliance", "color": "purple"},
                        {"name": "Revenue Optimization", "color": "yellow"},
                        {"name": "Risk Management", "color": "red"}
                    ]
                }
            },
            "App Name": {"rich_text": {}},
            "Input Data": {"rich_text": {}},
            "AI Recommendation": {"rich_text": {}},
            "Confidence Score": {"number": {}},
            "Action Taken": {"rich_text": {}},
            "Result": {
                "select": {
                    "options": [
                        {"name": "Success", "color": "green"},
                        {"name": "Partial", "color": "yellow"},
                        {"name": "Failed", "color": "red"},
                        {"name": "Pending", "color": "gray"}
                    ]
                }
            },
            "Impact": {"rich_text": {}},
            "Learning": {"rich_text": {}}
        }

        return self._create_database("🤖 AI 의사결정 로그", schema)

    def _create_database(self, title: str, properties: Dict) -> Optional[Dict]:
        """Notion 데이터베이스 생성"""

        payload = {
            "parent": {"type": "page_id", "page_id": ""},  # 부모 페이지 ID 필요
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties
        }

        try:
            # 실제 구현에서는 부모 페이지를 먼저 생성하거나 기존 페이지 ID 사용
            # 현재는 스키마만 정의
            self.logger.info(f"데이터베이스 스키마 정의 완료: {title}")
            return {"id": f"mock_db_{title.replace(' ', '_').lower()}", "title": title}

        except Exception as e:
            self.logger.error(f"데이터베이스 생성 실패: {title} - {e}")
            return None

    def _create_dashboard_page(self) -> Optional[Dict]:
        """대시보드 메인 페이지 생성"""

        dashboard_content = {
            "title": "🏭 서버리스 앱 팩토리 대시보드",
            "sections": [
                {
                    "type": "summary",
                    "title": "📊 실시간 현황",
                    "content": [
                        "월간 생성 앱 수",
                        "총 누적 수익",
                        "평균 앱당 수익",
                        "예산 사용률",
                        "성공률"
                    ]
                },
                {
                    "type": "kpi_charts",
                    "title": "📈 핵심 지표",
                    "content": [
                        "월별 수익 추이",
                        "앱별 성과 비교",
                        "비용 대비 수익률",
                        "스토어 승인율"
                    ]
                },
                {
                    "type": "alerts",
                    "title": "🚨 알림 및 액션",
                    "content": [
                        "예산 초과 경고",
                        "품질 이슈 앱",
                        "중복 위험 앱",
                        "수익 목표 미달"
                    ]
                }
            ]
        }

        # 실제 구현에서는 Notion API로 페이지 생성
        return {"id": "mock_dashboard_page", "content": dashboard_content}

    def update_app_record(self, app_data: Dict) -> bool:
        """앱 레코드 업데이트 (실제 Notion API 사용)"""

        try:
            if not self.databases["apps"]:
                self.logger.warning("FAF Console 데이터베이스 ID가 설정되지 않음")
                return False

            # Notion 레코드 페이로드 구성
            record_payload = {
                "parent": {
                    "database_id": self.databases["apps"]
                },
                "properties": {
                    "App Name": {
                        "title": [
                            {
                                "text": {
                                    "content": app_data.get("app_name", "Unknown App")
                                }
                            }
                        ]
                    },
                    "Status": {
                        "select": {
                            "name": self._map_status(app_data.get("status", "draft"))
                        }
                    },
                    "Category": {
                        "select": {
                            "name": app_data.get("category", "Utilities").title()
                        }
                    },
                    "Cost": {
                        "number": app_data.get("total_cost", 0)
                    },
                    "Quality Score": {
                        "number": app_data.get("quality_score", 0)
                    },
                    "Store Ready": {
                        "checkbox": app_data.get("store_ready", False)
                    }
                }
            }

            # Notion API 호출
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.headers,
                json=record_payload
            )

            if response.status_code == 200:
                created_record = response.json()
                self.logger.info(f"✅ FAF Console 레코드 생성: {app_data.get('app_name')}")
                self.logger.info(f"📊 Record URL: {created_record.get('url', 'N/A')}")
                return True
            else:
                self.logger.error(f"❌ FAF Console 레코드 생성 실패: {response.status_code}")
                self.logger.error(f"Error: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"❌ 앱 레코드 업데이트 실패: {e}")
            return False

    def log_kpi_update(self, app_name: str, metric_type: str, value: float, target: float = None) -> bool:
        """KPI 업데이트 로그"""

        try:
            kpi_record = {
                "App Name": app_name,
                "Date": datetime.now().isoformat(),
                "Metric Type": metric_type,
                "Value": value,
                "Target": target or 0,
                "Alert": value < (target * 0.8) if target else False
            }

            # 실제 구현에서는 Notion API 호출
            self.logger.info(f"KPI 업데이트: {app_name} - {metric_type}: {value}")
            return True

        except Exception as e:
            self.logger.error(f"KPI 로그 실패: {e}")
            return False

    def log_budget_update(self, budget_type: str, amount: float, apps_count: int = 0) -> bool:
        """예산 업데이트 로그"""

        try:
            current_month = datetime.now().strftime("%Y-%m")

            budget_record = {
                "Month": current_month,
                "Budget Type": budget_type,
                "Actual Spent": amount,
                "Apps Generated": apps_count,
                "Alert Level": self._calculate_budget_alert(amount)
            }

            # 실제 구현에서는 Notion API 호출
            self.logger.info(f"예산 업데이트: {budget_type} - ${amount}")
            return True

        except Exception as e:
            self.logger.error(f"예산 로그 실패: {e}")
            return False

    def log_ai_decision(self, decision_type: str, app_name: str, input_data: str,
                       recommendation: str, confidence: float, action: str, result: str) -> bool:
        """AI 의사결정 로그"""

        try:
            decision_record = {
                "Timestamp": datetime.now().isoformat(),
                "Decision Type": decision_type,
                "App Name": app_name,
                "Input Data": input_data[:500],  # 길이 제한
                "AI Recommendation": recommendation[:500],
                "Confidence Score": confidence,
                "Action Taken": action,
                "Result": result
            }

            # 실제 구현에서는 Notion API 호출
            self.logger.info(f"AI 의사결정 로그: {decision_type} - {app_name}")
            return True

        except Exception as e:
            self.logger.error(f"AI 의사결정 로그 실패: {e}")
            return False

    def get_dashboard_summary(self) -> Dict:
        """대시보드 요약 정보 생성"""

        # 실제 구현에서는 Notion API에서 데이터 집계
        summary = {
            "current_month": datetime.now().strftime("%Y-%m"),
            "apps_generated": 0,
            "total_revenue": 0,
            "budget_used": 0,
            "budget_remaining": 30.0,
            "success_rate": 0,
            "avg_quality_score": 0,
            "top_performing_apps": [],
            "alerts": []
        }

        return summary

    def _map_status(self, status: str) -> str:
        """상태 매핑"""
        status_map = {
            "draft": "Draft",
            "generating": "Generating",
            "testing": "QA Testing",
            "review": "Store Review",
            "published": "Published",
            "rejected": "Rejected",
            "archived": "Archived"
        }
        return status_map.get(status.lower(), "Draft")

    def _calculate_budget_alert(self, spent_amount: float) -> str:
        """예산 알림 레벨 계산"""
        config = self.config_manager.get_config()
        budget_limit = config.get("monthly_budget", 30.0)

        usage_rate = spent_amount / budget_limit

        if usage_rate >= 0.9:
            return "Red"
        elif usage_rate >= 0.7:
            return "Yellow"
        else:
            return "Green"

def main():
    """테스트 실행"""
    try:
        dashboard = NotionKPIDashboard()

        print("=== Notion 대시보드 구조 생성 ===")
        result = dashboard.create_dashboard_structure()

        if result["success"]:
            print("✅ 대시보드 생성 성공")
            for db_type, db_id in result["created_databases"].items():
                print(f"  {db_type}: {db_id}")
        else:
            print("❌ 대시보드 생성 실패")
            for error in result["errors"]:
                print(f"  {error}")

        print("\n=== 테스트 데이터 업데이트 ===")

        # 테스트 앱 데이터
        test_app = {
            "app_name": "Premium Fitness Tracker Pro",
            "status": "published",
            "category": "fitness",
            "total_cost": 0.665,
            "quality_score": 87,
            "store_ready": True,
            "monthly_revenue": 1250,
            "downloads": 2500,
            "rating": 4.2,
            "crash_rate": 0.008,
            "duplicate_risk": "low"
        }

        dashboard.update_app_record(test_app)
        dashboard.log_kpi_update("Premium Fitness Tracker Pro", "Revenue", 1250, 1000)
        dashboard.log_budget_update("App Generation", 0.665, 1)
        dashboard.log_ai_decision(
            "Quality Gate",
            "Premium Fitness Tracker Pro",
            "Quality score: 87%, Store ready: True",
            "Approve for store submission",
            0.92,
            "Approved for store upload",
            "Success"
        )

        print("✅ 테스트 데이터 업데이트 완료")

    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

if __name__ == "__main__":
    main()