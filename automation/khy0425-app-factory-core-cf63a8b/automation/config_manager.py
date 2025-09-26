#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secure Configuration Manager
안전한 API 키 및 설정 관리 시스템
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
import logging

class SecureConfigManager:
    """안전한 설정 관리자"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_file = self.project_root / ".env"
        self.user_config_dir = Path.home() / ".config" / "app-factory"
        self.user_config_file = self.user_config_dir / "secrets.json"

        # 사용자 설정 디렉토리 생성
        self.user_config_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(__name__)

    def get_api_key(self, key_name: str) -> Optional[str]:
        """API 키 안전하게 가져오기"""

        # 1. 환경변수에서 먼저 확인
        env_value = os.getenv(key_name)
        if env_value and env_value != "your_" + key_name.lower() + "_here":
            return env_value

        # 2. .env 파일에서 확인
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            if '=' in line:
                                k, v = line.strip().split('=', 1)
                                if k.strip() == key_name and v.strip():
                                    return v.strip()
            except Exception as e:
                self.logger.warning(f"Error reading .env file: {e}")

        # 3. 사용자 설정 파일에서 확인
        if self.user_config_file.exists():
            try:
                with open(self.user_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get(key_name)
            except Exception as e:
                self.logger.warning(f"Error reading user config: {e}")

        return None

    def set_api_key(self, key_name: str, key_value: str, location: str = "user") -> bool:
        """API 키 안전하게 저장"""

        if location == "user":
            # 사용자 설정 파일에 저장 (가장 안전)
            try:
                config = {}
                if self.user_config_file.exists():
                    with open(self.user_config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                config[key_name] = key_value

                with open(self.user_config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)

                # 파일 권한 설정 (읽기 전용)
                os.chmod(self.user_config_file, 0o600)
                return True

            except Exception as e:
                self.logger.error(f"Error saving to user config: {e}")
                return False

        elif location == "env":
            # .env 파일에 저장
            try:
                lines = []
                key_found = False

                if self.config_file.exists():
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                # 기존 키 업데이트 또는 새 키 추가
                for i, line in enumerate(lines):
                    if line.strip().startswith(f"{key_name}="):
                        lines[i] = f"{key_name}={key_value}\n"
                        key_found = True
                        break

                if not key_found:
                    lines.append(f"{key_name}={key_value}\n")

                with open(self.config_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

                return True

            except Exception as e:
                self.logger.error(f"Error saving to .env file: {e}")
                return False

        return False

    def get_config(self) -> Dict:
        """전체 설정 가져오기"""
        config = {
            "gemini_api_key": self.get_api_key("GEMINI_API_KEY"),
            "firebase_project_id": self.get_api_key("FIREBASE_PROJECT_ID"),
            "notion_api_token": self.get_api_key("NOTION_API_TOKEN"),
            "slack_webhook_url": self.get_api_key("SLACK_WEBHOOK_URL"),
            "monthly_budget": float(self.get_api_key("MONTHLY_BUDGET") or "30.0"),
            "cost_per_app": float(self.get_api_key("COST_PER_APP") or "0.665"),
            "debug_mode": self.get_api_key("DEBUG_MODE") == "true"
        }
        return config

    def validate_config(self) -> Dict:
        """설정 유효성 검사"""
        config = self.get_config()
        issues = []

        # 필수 키 확인
        if not config["gemini_api_key"]:
            issues.append("❌ GEMINI_API_KEY가 설정되지 않았습니다")

        # 예산 설정 확인
        if config["monthly_budget"] <= 0:
            issues.append("❌ MONTHLY_BUDGET이 0보다 커야 합니다")

        if config["cost_per_app"] <= 0:
            issues.append("❌ COST_PER_APP이 0보다 커야 합니다")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "config": config
        }

    def setup_wizard(self):
        """대화형 설정 마법사"""
        print("🔧 서버리스 앱 팩토리 설정 마법사")
        print("=" * 50)

        # Gemini API 키 설정
        print("\n1. Google Gemini API 키 설정 (필수)")
        print("   • https://makersuite.google.com/app/apikey 에서 발급")
        print("   • Nano Banana 이미지 생성에 사용")

        gemini_key = input("   Gemini API 키를 입력하세요: ").strip()
        if gemini_key:
            self.set_api_key("GEMINI_API_KEY", gemini_key)
            print("   ✅ Gemini API 키가 저장되었습니다")

        # 예산 설정
        print("\n2. 월간 예산 설정")
        budget = input("   월간 예산을 입력하세요 (기본값: 30): ").strip()
        if budget:
            try:
                budget_float = float(budget)
                self.set_api_key("MONTHLY_BUDGET", str(budget_float))
                print(f"   ✅ 월간 예산: ${budget_float}")
            except ValueError:
                print("   ❌ 유효하지 않은 숫자입니다. 기본값(30) 사용")

        # 선택적 설정들
        print("\n3. 선택적 설정")

        firebase_id = input("   Firebase Project ID (선택사항): ").strip()
        if firebase_id:
            self.set_api_key("FIREBASE_PROJECT_ID", firebase_id)
            print("   ✅ Firebase Project ID 저장됨")

        notion_token = input("   Notion API Token (선택사항): ").strip()
        if notion_token:
            self.set_api_key("NOTION_API_TOKEN", notion_token)
            print("   ✅ Notion API Token 저장됨")

        slack_webhook = input("   Slack Webhook URL (선택사항): ").strip()
        if slack_webhook:
            self.set_api_key("SLACK_WEBHOOK_URL", slack_webhook)
            print("   ✅ Slack Webhook URL 저장됨")

        print("\n🎉 설정이 완료되었습니다!")
        print(f"📁 설정 저장 위치: {self.user_config_file}")

        # 설정 검증
        validation = self.validate_config()
        if validation["valid"]:
            print("✅ 모든 설정이 유효합니다")
        else:
            print("⚠️ 설정 문제:")
            for issue in validation["issues"]:
                print(f"   {issue}")

def main():
    """설정 관리자 실행"""
    config_manager = SecureConfigManager()

    import argparse
    parser = argparse.ArgumentParser(description="Secure Config Manager")
    parser.add_argument("--setup", action="store_true", help="Run setup wizard")
    parser.add_argument("--validate", action="store_true", help="Validate configuration")
    parser.add_argument("--show", action="store_true", help="Show current configuration")

    args = parser.parse_args()

    if args.setup:
        config_manager.setup_wizard()
    elif args.validate:
        validation = config_manager.validate_config()
        if validation["valid"]:
            print("✅ 설정이 유효합니다")
        else:
            print("❌ 설정 문제들:")
            for issue in validation["issues"]:
                print(f"  {issue}")
    elif args.show:
        config = config_manager.get_config()
        print("📋 현재 설정:")
        for key, value in config.items():
            if "key" in key.lower() or "token" in key.lower():
                print(f"  {key}: {'✅ 설정됨' if value else '❌ 미설정'}")
            else:
                print(f"  {key}: {value}")
    else:
        print("사용법:")
        print("  python automation/config_manager.py --setup     # 설정 마법사")
        print("  python automation/config_manager.py --validate  # 설정 검증")
        print("  python automation/config_manager.py --show      # 현재 설정 보기")

if __name__ == "__main__":
    main()