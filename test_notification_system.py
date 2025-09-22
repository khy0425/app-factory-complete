#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
통합 알림 시스템 테스트 및 검증 도구
알림 시스템이 모든 Flutter 앱에 올바르게 적용되었는지 확인
"""

import os
import re
from pathlib import Path

class NotificationSystemTester:
    def __init__(self):
        self.base_dir = Path(".")
        self.flutter_apps_dir = self.base_dir / "flutter_apps"
        self.template_dir = self.base_dir / "templates"

        self.app_configs = {
            "mission100_v3": {"app_name": "Mission100", "app_title": "MISSION 100"},
            "squat_master": {"app_name": "SquatMaster", "app_title": "SQUAT MASTER"},
            "burpeebeast": {"app_name": "BurpeeBeast", "app_title": "BURPEE BEAST"},
            "gigachad_runner": {"app_name": "GigaChadRunner", "app_title": "GIGACHAD RUNNER"},
            "jumpingjackjedi": {"app_name": "JumpingJackJedi", "app_title": "JUMPING JACK JEDI"},
            "lungelegend": {"app_name": "LungeLegend", "app_title": "LUNGE LEGEND"},
            "plankchampion": {"app_name": "PlankChampion", "app_title": "PLANK CHAMPION"},
            "pulluppro": {"app_name": "PullUpPro", "app_title": "PULL UP PRO"}
        }

    def test_all(self):
        """모든 테스트 실행"""
        print("🔧 통합 알림 시스템 테스트 시작")
        print("=" * 60)

        results = {
            "template_integrity": self.test_template_integrity(),
            "file_presence": self.test_file_presence(),
            "content_verification": self.test_content_verification(),
            "dependencies": self.test_dependencies(),
            "branding": self.test_branding_consistency()
        }

        self.print_summary(results)
        return results

    def test_template_integrity(self):
        """템플릿 파일 무결성 검사"""
        print("\n📋 1. 템플릿 무결성 검사")

        template_file = self.template_dir / "notification_service_template.dart"

        if not template_file.exists():
            print("❌ 템플릿 파일이 존재하지 않습니다")
            return False

        content = template_file.read_text(encoding='utf-8')

        # 필수 플레이스홀더 확인
        required_placeholders = ["{{APP_NAME}}", "{{APP_TITLE}}", "{{CHANNEL_NAME}}"]
        missing_placeholders = []

        for placeholder in required_placeholders:
            if placeholder not in content:
                missing_placeholders.append(placeholder)

        if missing_placeholders:
            print(f"❌ 누락된 플레이스홀더: {missing_placeholders}")
            return False

        print("✅ 템플릿 무결성 확인 완료")
        return True

    def test_file_presence(self):
        """모든 앱에 알림 서비스 파일 존재 확인"""
        print("\n📁 2. 파일 존재 확인")

        missing_files = []

        for app_name in self.app_configs.keys():
            notification_file = self.flutter_apps_dir / app_name / "lib" / "services" / "notification_service.dart"

            if not notification_file.exists():
                missing_files.append(app_name)
                print(f"❌ {app_name}: notification_service.dart 누락")
            else:
                print(f"✅ {app_name}: notification_service.dart 존재")

        if missing_files:
            print(f"❌ 누락된 파일이 있는 앱: {missing_files}")
            return False

        return True

    def test_content_verification(self):
        """알림 서비스 내용 검증"""
        print("\n🔍 3. 알림 서비스 내용 검증")

        failed_apps = []

        for app_name in self.app_configs.keys():
            notification_file = self.flutter_apps_dir / app_name / "lib" / "services" / "notification_service.dart"

            if not notification_file.exists():
                continue

            content = notification_file.read_text(encoding='utf-8')

            # 핵심 기능 존재 확인
            required_methods = [
                "canScheduleExactAlarms",
                "requestExactAlarmPermission",
                "_safeScheduleNotification",
                "scheduleInexactNotification",
                "showPermissionRequestDialog",
                "scheduleDailyWorkoutReminder"
            ]

            missing_methods = []
            for method in required_methods:
                if method not in content:
                    missing_methods.append(method)

            if missing_methods:
                print(f"❌ {app_name}: 누락된 메소드 - {missing_methods}")
                failed_apps.append(app_name)
            else:
                print(f"✅ {app_name}: 모든 핵심 메소드 존재")

        return len(failed_apps) == 0

    def test_dependencies(self):
        """의존성 확인"""
        print("\n📦 4. 의존성 확인")

        apps_with_deps = []
        apps_without_deps = []

        required_deps = [
            "flutter_local_notifications",
            "permission_handler",
            "timezone"
        ]

        for app_name in self.app_configs.keys():
            pubspec_file = self.flutter_apps_dir / app_name / "pubspec.yaml"

            if not pubspec_file.exists():
                print(f"❌ {app_name}: pubspec.yaml 파일 없음")
                apps_without_deps.append(app_name)
                continue

            content = pubspec_file.read_text(encoding='utf-8')

            has_all_deps = all(dep in content for dep in required_deps)

            if has_all_deps:
                print(f"✅ {app_name}: 모든 의존성 존재")
                apps_with_deps.append(app_name)
            else:
                missing_deps = [dep for dep in required_deps if dep not in content]
                print(f"⚠️  {app_name}: 누락된 의존성 - {missing_deps}")
                apps_without_deps.append(app_name)

        print(f"\n📊 의존성 현황:")
        print(f"   ✅ 완전한 의존성: {len(apps_with_deps)}개 앱")
        print(f"   ⚠️  누락된 의존성: {len(apps_without_deps)}개 앱")

        return len(apps_without_deps) == 0

    def test_branding_consistency(self):
        """브랜딩 일관성 확인"""
        print("\n🎨 5. 브랜딩 일관성 확인")

        failed_apps = []

        for app_name, config in self.app_configs.items():
            notification_file = self.flutter_apps_dir / app_name / "lib" / "services" / "notification_service.dart"

            if not notification_file.exists():
                continue

            content = notification_file.read_text(encoding='utf-8')

            # 앱별 브랜딩 확인
            app_title = config["app_title"]

            branding_checks = [
                f"/// {config['app_name']} 통합 알림 서비스",
                f"Text('🔥 {app_title} 알림 활성화! 🔥')",
                f"💪 {app_title} 운동 시간! LEGENDARY CHAD MODE 활성화! 💪"
            ]

            missing_branding = []
            for check in branding_checks:
                if check not in content:
                    missing_branding.append(check)

            if missing_branding:
                print(f"❌ {app_name}: 브랜딩 불일치")
                failed_apps.append(app_name)
            else:
                print(f"✅ {app_name}: 브랜딩 일관성 확인")

        return len(failed_apps) == 0

    def print_summary(self, results):
        """테스트 결과 요약 출력"""
        print("\n" + "=" * 60)
        print("📊 테스트 결과 요약")
        print("=" * 60)

        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result)

        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:20} : {status}")

        print(f"\n🏆 종합 결과: {passed_tests}/{total_tests} 테스트 통과")

        if passed_tests == total_tests:
            print("🎉 모든 테스트 통과! 알림 시스템이 성공적으로 시스템화되었습니다!")
        else:
            print("⚠️  일부 테스트 실패. 수동 설정이 필요할 수 있습니다.")

        return passed_tests / total_tests

def main():
    """메인 실행 함수"""
    print("🚀 Flutter 앱 통합 알림 시스템 테스트")
    print("개선된 권한 요청 시스템 검증 중...")

    tester = NotificationSystemTester()
    results = tester.test_all()

    # 추가 정보 출력
    print("\n💡 추가 설정 필요사항:")
    print("1. 의존성이 누락된 앱들은 pubspec.yaml에 의존성 추가 필요")
    print("2. Android MainActivity에 MethodChannel 설정 필요")
    print("3. flutter pub get 실행하여 의존성 설치")

    return results

if __name__ == "__main__":
    main()