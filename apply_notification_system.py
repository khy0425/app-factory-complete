#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter 앱들에 개선된 알림 시스템 적용 스크립트

주요 개선사항:
1. 2단계 권한 요청 (기본 알림 → 선택적 정확한 알람)
2. 사용자 친화적 권한 다이얼로그
3. 완전한 폴백 시스템
4. Chad 스타일 메시지 통합
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional

class NotificationSystemApplier:
    def __init__(self):
        self.base_path = Path("E:/Projects/app-factory-complete")
        self.flutter_apps_path = self.base_path / "flutter_apps"
        self.template_path = self.base_path / "templates" / "notification_service_template.dart"

        # 앱별 설정
        self.app_configs = {
            "mission100_v3": {
                "app_name": "Mission100",
                "app_title": "MISSION 100",
                "channel_name": "com.misson100.notification_permissions",
                "has_notification": True  # 이미 있음
            },
            "squat_master": {
                "app_name": "SquatMaster",
                "app_title": "SQUAT MASTER",
                "channel_name": "com.squatmaster.notification_permissions",
                "has_notification": False
            },
            "burpeebeast": {
                "app_name": "BurpeeBeast",
                "app_title": "BURPEE BEAST",
                "channel_name": "com.burpeebeast.notification_permissions",
                "has_notification": False
            },
            "gigachad_runner": {
                "app_name": "GigachadRunner",
                "app_title": "GIGACHAD RUNNER",
                "channel_name": "com.gigachadrunner.notification_permissions",
                "has_notification": False
            },
            "jumpingjackjedi": {
                "app_name": "JumpingJackJedi",
                "app_title": "JUMPING JACK JEDI",
                "channel_name": "com.jumpingjackjedi.notification_permissions",
                "has_notification": False
            },
            "lungelegend": {
                "app_name": "LungeLegend",
                "app_title": "LUNGE LEGEND",
                "channel_name": "com.lungelegend.notification_permissions",
                "has_notification": False
            },
            "plankchampion": {
                "app_name": "PlankChampion",
                "app_title": "PLANK CHAMPION",
                "channel_name": "com.plankchampion.notification_permissions",
                "has_notification": False
            },
            "pulluppro": {
                "app_name": "PullupPro",
                "app_title": "PULLUP PRO",
                "channel_name": "com.pulluppro.notification_permissions",
                "has_notification": False
            }
        }

    def check_apps_exist(self) -> List[str]:
        """존재하는 Flutter 앱들 확인"""
        existing_apps = []
        for app_name in self.app_configs.keys():
            app_path = self.flutter_apps_path / app_name
            if app_path.exists():
                existing_apps.append(app_name)
                print(f"✅ {app_name} - 존재함")
            else:
                print(f"❌ {app_name} - 존재하지 않음")
        return existing_apps

    def create_services_directory(self, app_path: Path) -> bool:
        """services 디렉토리 생성"""
        services_path = app_path / "lib" / "services"
        try:
            services_path.mkdir(parents=True, exist_ok=True)
            print(f"  📁 services 디렉토리 생성: {services_path}")
            return True
        except Exception as e:
            print(f"  ❌ services 디렉토리 생성 실패: {e}")
            return False

    def apply_notification_service(self, app_name: str) -> bool:
        """개선된 notification service 적용"""
        print(f"\n🔧 {app_name}에 알림 시스템 적용 중...")

        app_path = self.flutter_apps_path / app_name
        config = self.app_configs[app_name]

        # services 디렉토리 확인/생성
        if not self.create_services_directory(app_path):
            return False

        # 템플릿 파일 읽기
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except Exception as e:
            print(f"  ❌ 템플릿 파일 읽기 실패: {e}")
            return False

        # 템플릿 변수 치환
        content = template_content.replace("{{APP_NAME}}", config["app_name"])
        content = content.replace("{{APP_TITLE}}", config["app_title"])
        content = content.replace("{{CHANNEL_NAME}}", config["channel_name"])

        # notification_service.dart 파일 생성/업데이트
        notification_path = app_path / "lib" / "services" / "notification_service.dart"

        try:
            # 기존 파일이 있다면 백업
            if notification_path.exists():
                backup_path = notification_path.with_suffix('.dart.backup')
                shutil.copy2(notification_path, backup_path)
                print(f"  📦 기존 파일 백업: {backup_path}")

            # 새로운 파일 작성
            with open(notification_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  ✅ notification_service.dart 적용 완료")
            return True

        except Exception as e:
            print(f"  ❌ 파일 작성 실패: {e}")
            return False

    def update_pubspec_dependencies(self, app_name: str) -> bool:
        """pubspec.yaml에 필요한 dependencies 추가"""
        print(f"  📦 {app_name} pubspec.yaml 의존성 확인...")

        app_path = self.flutter_apps_path / app_name
        pubspec_path = app_path / "pubspec.yaml"

        if not pubspec_path.exists():
            print(f"  ❌ pubspec.yaml 파일이 없습니다")
            return False

        required_deps = [
            "flutter_local_notifications:",
            "permission_handler:",
            "shared_preferences:",
            "timezone:"
        ]

        try:
            with open(pubspec_path, 'r', encoding='utf-8') as f:
                content = f.read()

            needs_update = False
            for dep in required_deps:
                if dep not in content:
                    needs_update = True
                    print(f"  ⚠️ 누락된 의존성: {dep}")

            if needs_update:
                print(f"  💡 {app_name}의 pubspec.yaml을 수동으로 업데이트해주세요:")
                print(f"     - flutter_local_notifications: ^17.2.4")
                print(f"     - permission_handler: ^11.4.0")
                print(f"     - shared_preferences: ^2.4.10")
                print(f"     - timezone: ^0.9.4")
            else:
                print(f"  ✅ 모든 의존성이 이미 존재합니다")

            return True

        except Exception as e:
            print(f"  ❌ pubspec.yaml 읽기 실패: {e}")
            return False

    def create_android_notification_channel(self, app_name: str) -> bool:
        """Android 알림 채널 설정 추가"""
        print(f"  📱 {app_name} Android 알림 채널 설정...")

        app_path = self.flutter_apps_path / app_name
        config = self.app_configs[app_name]

        # MainActivity.java 또는 MainActivity.kt 찾기
        android_path = app_path / "android" / "app" / "src" / "main" / "java"
        if not android_path.exists():
            android_path = app_path / "android" / "app" / "src" / "main" / "kotlin"

        if not android_path.exists():
            print(f"  ⚠️ Android 소스 폴더를 찾을 수 없습니다")
            return False

        # MainActivity 파일 찾기
        main_activity_files = list(android_path.rglob("MainActivity.*"))
        if not main_activity_files:
            print(f"  ⚠️ MainActivity 파일을 찾을 수 없습니다")
            return False

        print(f"  💡 Android 설정은 수동으로 추가해주세요:")
        print(f"     - MethodChannel 설정: {config['channel_name']}")
        print(f"     - SCHEDULE_EXACT_ALARM 권한 처리")

        return True

    def apply_to_all_apps(self) -> None:
        """모든 앱에 알림 시스템 적용"""
        print("🚀 Flutter 앱들에 개선된 알림 시스템 적용 시작!")
        print("=" * 60)

        existing_apps = self.check_apps_exist()

        if not existing_apps:
            print("❌ 적용할 수 있는 앱이 없습니다.")
            return

        success_count = 0

        for app_name in existing_apps:
            try:
                # 알림 서비스 적용
                if self.apply_notification_service(app_name):
                    # 의존성 확인
                    self.update_pubspec_dependencies(app_name)
                    # Android 설정 안내
                    self.create_android_notification_channel(app_name)
                    success_count += 1
                    print(f"  ✅ {app_name} 적용 완료")
                else:
                    print(f"  ❌ {app_name} 적용 실패")

            except Exception as e:
                print(f"  ❌ {app_name} 적용 중 오류: {e}")

        print("\n" + "=" * 60)
        print(f"✅ 알림 시스템 적용 완료: {success_count}/{len(existing_apps)}개 앱")
        print("=" * 60)

        print("\n🔧 추가 작업 필요:")
        print("1. 각 앱의 pubspec.yaml에서 dependencies 확인")
        print("2. Android MainActivity에 MethodChannel 추가")
        print("3. flutter pub get 실행")
        print("4. 앱 빌드 및 테스트")

        print("\n💡 주요 개선사항:")
        print("• 2단계 권한 요청 (기본 알림 → 선택적 정확한 알람)")
        print("• 사용자 친화적 권한 다이얼로그")
        print("• 완전한 폴백 시스템")
        print("• Chad 스타일 메시지 통합")
        print("• 시스템 설정 강제 이동 없음")

    def rollback_changes(self, app_name: str) -> bool:
        """변경사항 롤백"""
        print(f"\n🔄 {app_name} 변경사항 롤백...")

        app_path = self.flutter_apps_path / app_name
        notification_path = app_path / "lib" / "services" / "notification_service.dart"
        backup_path = notification_path.with_suffix('.dart.backup')

        try:
            if backup_path.exists():
                shutil.copy2(backup_path, notification_path)
                backup_path.unlink()  # 백업 파일 삭제
                print(f"  ✅ {app_name} 롤백 완료")
                return True
            else:
                print(f"  ⚠️ {app_name} 백업 파일이 없습니다")
                return False

        except Exception as e:
            print(f"  ❌ {app_name} 롤백 실패: {e}")
            return False

def main():
    """메인 실행 함수"""
    applier = NotificationSystemApplier()

    print("📱 Flutter 앱 알림 시스템 개선 도구")
    print("=" * 50)
    print("1. 모든 앱에 적용")
    print("2. 특정 앱에 적용")
    print("3. 변경사항 롤백")
    print("=" * 50)

    choice = input("선택하세요 (1-3): ").strip()

    if choice == "1":
        applier.apply_to_all_apps()
    elif choice == "2":
        existing_apps = applier.check_apps_exist()
        if existing_apps:
            print("\n사용 가능한 앱:")
            for i, app in enumerate(existing_apps, 1):
                print(f"{i}. {app}")

            try:
                app_choice = int(input("앱 번호 선택: ")) - 1
                if 0 <= app_choice < len(existing_apps):
                    app_name = existing_apps[app_choice]
                    if applier.apply_notification_service(app_name):
                        applier.update_pubspec_dependencies(app_name)
                        applier.create_android_notification_channel(app_name)
                else:
                    print("❌ 잘못된 선택입니다")
            except ValueError:
                print("❌ 잘못된 입력입니다")
    elif choice == "3":
        existing_apps = applier.check_apps_exist()
        if existing_apps:
            print("\n롤백 가능한 앱:")
            for i, app in enumerate(existing_apps, 1):
                print(f"{i}. {app}")

            try:
                app_choice = int(input("앱 번호 선택: ")) - 1
                if 0 <= app_choice < len(existing_apps):
                    app_name = existing_apps[app_choice]
                    applier.rollback_changes(app_name)
                else:
                    print("❌ 잘못된 선택입니다")
            except ValueError:
                print("❌ 잘못된 입력입니다")
    else:
        print("❌ 잘못된 선택입니다")

if __name__ == "__main__":
    main()