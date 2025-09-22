#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion API Test - FAF_Console 연동 테스트
"""

import os
import json
import requests
from datetime import datetime
from config_manager import SecureConfigManager

def test_notion_connection():
    """Notion API 연결 테스트"""

    print("=== Notion API Connection Test ===")

    # API 토큰 가져오기
    config_manager = SecureConfigManager()
    notion_token = config_manager.get_api_key("NOTION_API_TOKEN")

    if not notion_token:
        print("❌ NOTION_API_TOKEN이 설정되지 않았습니다.")
        print("💡 .env 파일에 NOTION_API_TOKEN을 추가하세요.")
        return False

    print(f"✅ Notion API Token: {notion_token[:15]}...")

    # API 헤더 설정
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    try:
        # 1. 사용자 정보 조회 (기본 연결 테스트)
        print("\n1. Testing basic connection...")
        response = requests.get("https://api.notion.com/v1/users/me", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Connected successfully!")
            print(f"   User: {user_data.get('name', 'Unknown')}")
            print(f"   ID: {user_data.get('id', 'Unknown')}")
        else:
            print(f"❌ Connection failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

        # 2. 데이터베이스 검색 (FAF_Console 찾기)
        print("\n2. Searching for existing databases...")
        search_payload = {
            "query": "FAF_Console",
            "filter": {
                "value": "database",
                "property": "object"
            }
        }

        search_response = requests.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json=search_payload
        )

        if search_response.status_code == 200:
            search_results = search_response.json()
            databases = search_results.get("results", [])

            print(f"✅ Found {len(databases)} databases")

            for db in databases:
                db_title = ""
                if "title" in db.get("properties", {}):
                    title_prop = db["properties"]["title"]
                    if title_prop.get("title"):
                        db_title = title_prop["title"][0]["plain_text"]

                print(f"   📊 Database: {db_title or 'Untitled'}")
                print(f"      ID: {db['id']}")
                print(f"      URL: {db.get('url', 'N/A')}")
        else:
            print(f"❌ Database search failed: {search_response.status_code}")
            print(f"   Error: {search_response.text}")

        # 3. FAF_Console 앱 마스터 테이블에 테스트 레코드 추가
        print("\n3. Testing record creation...")

        # 실제 환경에서는 FAF_Console의 데이터베이스 ID를 사용
        # 여기서는 테스트용으로 간단한 페이지 생성
        test_page_payload = {
            "parent": {"type": "page_id", "page_id": "your_parent_page_id"},  # 실제 페이지 ID 필요
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": f"App Factory Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                            }
                        }
                    ]
                }
            }
        }

        print("ℹ️ 실제 페이지 생성을 위해서는 FAF_Console 데이터베이스 ID가 필요합니다.")
        print("   현재 연결 테스트만 진행합니다.")

        return True

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def create_faf_console_database():
    """FAF Console용 앱 마스터 데이터베이스 생성"""

    print("\n=== Creating FAF Console Database ===")

    config_manager = SecureConfigManager()
    notion_token = config_manager.get_api_key("NOTION_API_TOKEN")

    if not notion_token:
        print("❌ NOTION_API_TOKEN이 필요합니다.")
        return None

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # FAF Console용 데이터베이스 스키마
    database_payload = {
        "parent": {
            "type": "page_id",
            "page_id": "your_workspace_page_id"  # 실제 워크스페이스 페이지 ID 필요
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "FAF Console - App Master"
                }
            }
        ],
        "properties": {
            "App Name": {
                "title": {}
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Draft", "color": "gray"},
                        {"name": "Generating", "color": "yellow"},
                        {"name": "Testing", "color": "orange"},
                        {"name": "Published", "color": "green"},
                        {"name": "Failed", "color": "red"}
                    ]
                }
            },
            "Category": {
                "select": {
                    "options": [
                        {"name": "Fitness", "color": "blue"},
                        {"name": "Productivity", "color": "purple"},
                        {"name": "Utilities", "color": "yellow"},
                        {"name": "Creative", "color": "pink"}
                    ]
                }
            },
            "Cost": {
                "number": {
                    "format": "dollar"
                }
            },
            "Quality Score": {
                "number": {}
            },
            "Store Ready": {
                "checkbox": {}
            },
            "Created": {
                "created_time": {}
            },
            "Generation Time": {
                "number": {}
            },
            "Cache Hit": {
                "checkbox": {}
            },
            "Notes": {
                "rich_text": {}
            }
        }
    }

    try:
        # 실제 생성을 위해서는 상위 페이지 ID가 필요
        print("💡 실제 데이터베이스 생성을 위해서는:")
        print("   1. Notion 워크스페이스에 FAF_Console 페이지 생성")
        print("   2. 해당 페이지의 ID를 parent.page_id에 설정")
        print("   3. Notion API 권한 설정 확인")

        print("\n📊 FAF Console Database Schema:")
        for prop_name, prop_config in database_payload["properties"].items():
            prop_type = list(prop_config.keys())[0]
            print(f"   • {prop_name}: {prop_type}")

        return database_payload

    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return None

def test_app_record_creation():
    """앱 레코드 생성 테스트"""

    print("\n=== Test App Record Creation ===")

    # 실제 앱 데이터 시뮬레이션
    test_app_data = {
        "app_name": "Test Fitness Timer Pro",
        "status": "Published",
        "category": "Fitness",
        "cost": 0.665,
        "quality_score": 87,
        "store_ready": True,
        "generation_time": 45.2,
        "cache_hit": False,
        "notes": "Successfully generated with asset caching system. Ready for store deployment."
    }

    print("📱 Test App Data:")
    for key, value in test_app_data.items():
        print(f"   {key}: {value}")

    # Notion 레코드 페이로드
    record_payload = {
        "parent": {
            "database_id": "your_faf_console_database_id"  # 실제 DB ID 필요
        },
        "properties": {
            "App Name": {
                "title": [
                    {
                        "text": {
                            "content": test_app_data["app_name"]
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "name": test_app_data["status"]
                }
            },
            "Category": {
                "select": {
                    "name": test_app_data["category"]
                }
            },
            "Cost": {
                "number": test_app_data["cost"]
            },
            "Quality Score": {
                "number": test_app_data["quality_score"]
            },
            "Store Ready": {
                "checkbox": test_app_data["store_ready"]
            },
            "Generation Time": {
                "number": test_app_data["generation_time"]
            },
            "Cache Hit": {
                "checkbox": test_app_data["cache_hit"]
            },
            "Notes": {
                "rich_text": [
                    {
                        "text": {
                            "content": test_app_data["notes"]
                        }
                    }
                ]
            }
        }
    }

    print("\n💡 Notion Record Payload prepared!")
    print("   실제 생성을 위해서는 FAF_Console 데이터베이스 ID가 필요합니다.")

    return record_payload

if __name__ == "__main__":
    # 1. 기본 연결 테스트
    connection_ok = test_notion_connection()

    if connection_ok:
        # 2. FAF Console 데이터베이스 스키마 준비
        database_schema = create_faf_console_database()

        # 3. 테스트 레코드 페이로드 준비
        test_record = test_app_record_creation()

        print("\n🎉 Notion API 연동 준비 완료!")
        print("   다음 단계: FAF_Console 워크스페이스에 데이터베이스를 생성하고")
        print("   실제 데이터베이스 ID를 설정하여 레코드 생성 테스트")
    else:
        print("\n❌ Notion API 연결 실패")
        print("   NOTION_API_TOKEN 설정을 확인하세요.")