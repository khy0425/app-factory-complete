#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mission100 앱 초기 설정 문제 해결
- 초기 테스트 메시지 제거
- 기본 사용자 프로필 자동 생성
- 권한 요구 문제 해결
"""

import os
import re
from pathlib import Path

class Mission100SetupFixer:
    def __init__(self):
        self.app_path = Path("flutter_apps/mission100_v3")

    def fix_home_screen_profile_issue(self):
        """홈 스크린에서 프로필 없을 때 자동 생성하도록 수정"""
        print("🏠 홈 스크린 프로필 문제 해결 중...")

        home_screen_path = self.app_path / "lib" / "screens" / "home_screen.dart"

        if not home_screen_path.exists():
            print(f"❌ {home_screen_path} 파일이 없습니다.")
            return False

        try:
            with open(home_screen_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(home_screen_path, "r", encoding="cp949") as f:
                content = f.read()

        # 사용자 프로필이 없을 때 기본 프로필 생성하도록 수정
        old_pattern = r'// 사용자 프로필 로드\s*_userProfile = await _databaseService\.getUserProfile\(\);'

        new_code = '''// 사용자 프로필 로드
      _userProfile = await _databaseService.getUserProfile();

      // 프로필이 없으면 기본 프로필 생성
      if (_userProfile == null) {
        debugPrint('👤 사용자 프로필이 없음 - 기본 프로필 생성');
        await _createDefaultUserProfile();
        _userProfile = await _databaseService.getUserProfile();
      }'''

        content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

        # 기본 프로필 생성 메서드 추가
        if '_createDefaultUserProfile' not in content:
            # 클래스 끝 부분에 메서드 추가
            method_to_add = '''
  Future<void> _createDefaultUserProfile() async {
    try {
      final defaultProfile = UserProfile(
        level: PushupLevel.beginner,
        initialMaxReps: 10,
        startDate: DateTime.now(),
        chadLevel: 0,
        reminderEnabled: false,
        reminderTime: null,
        workoutDays: ['월', '수', '금'], // 기본 운동 요일
      );

      await _databaseService.insertUserProfile(defaultProfile);
      debugPrint('✅ 기본 사용자 프로필 생성 완료');
    } catch (e) {
      debugPrint('❌ 기본 프로필 생성 실패: $e');
    }
  }
'''

            # 클래스의 마지막 } 앞에 메서드 추가
            content = content.rsplit('}', 1)[0] + method_to_add + '\n}\n'

        with open(home_screen_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("  ✅ 홈 스크린 프로필 자동 생성 로직 추가")
        return True

    def fix_permission_issues(self):
        """권한 관련 문제 해결"""
        print("🔐 권한 요구 문제 해결 중...")

        # settings_screen.dart 확인
        settings_path = self.app_path / "lib" / "screens" / "settings_screen.dart"

        if not settings_path.exists():
            print(f"❌ {settings_path} 파일이 없습니다.")
            return False

        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(settings_path, "r", encoding="cp949") as f:
                    content = f.read()
            except:
                print("❌ 파일 읽기 실패")
                return False

        # 권한 요청 관련 코드를 더 관대하게 수정
        if 'permission_handler' in content:
            # 권한 체크를 옵셔널로 만들기
            permission_pattern = r'await Permission\.[^.]+\.request\(\)'
            content = re.sub(permission_pattern, 'await Permission.notification.request().then((status) => status)', content)

            # 권한 거부 시에도 계속 진행하도록 수정
            content = content.replace(
                'if (status != PermissionStatus.granted)',
                'if (false) // 권한 없어도 계속 진행'
            )

        with open(settings_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("  ✅ 권한 요구 완화 처리 완료")
        return True

    def remove_initial_test_requirement(self):
        """초기 테스트 요구사항 제거"""
        print("🧪 초기 테스트 요구사항 제거 중...")

        home_screen_path = self.app_path / "lib" / "screens" / "home_screen.dart"

        if not home_screen_path.exists():
            return False

        try:
            with open(home_screen_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(home_screen_path, "r", encoding="cp949") as f:
                content = f.read()

        # _buildNoUserWidget 메서드를 기본 위젯으로 변경
        old_no_user_widget = r'else if \(_userProfile == null\)\s*_buildNoUserWidget\(\)'
        new_no_user_widget = 'else if (_userProfile == null)\n                        _buildLoadingWidget() // 프로필 생성 중'

        content = re.sub(old_no_user_widget, new_no_user_widget, content)

        with open(home_screen_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("  ✅ 초기 테스트 메시지 제거 완료")
        return True

    def create_streamlined_onboarding(self):
        """간소화된 온보딩 생성"""
        print("🚀 간소화된 온보딩 생성 중...")

        # main.dart 수정하여 바로 홈으로 이동
        main_path = self.app_path / "lib" / "main.dart"

        if main_path.exists():
            try:
                with open(main_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(main_path, "r", encoding="cp949") as f:
                    content = f.read()

            # 온보딩 스크린 대신 바로 메인으로 이동
            content = content.replace(
                'home: const OnboardingScreen()',
                'home: const MainNavigationScreen() // 바로 메인으로'
            )

            with open(main_path, "w", encoding="utf-8") as f:
                f.write(content)

            print("  ✅ 바로 메인 화면으로 이동하도록 수정")

        return True

    def add_user_profile_import(self):
        """UserProfile 관련 import 확인 및 추가"""
        print("📦 필요한 import 확인 중...")

        home_screen_path = self.app_path / "lib" / "screens" / "home_screen.dart"

        try:
            with open(home_screen_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(home_screen_path, "r", encoding="cp949") as f:
                content = f.read()

        # PushupLevel import 확인
        if "import '../models/pushup_level.dart';" not in content:
            # import 섹션에 추가
            import_section = content.split('\n')
            for i, line in enumerate(import_section):
                if line.startswith("import '../models/user_profile.dart';"):
                    import_section.insert(i + 1, "import '../models/pushup_level.dart';")
                    break

            content = '\n'.join(import_section)

            with open(home_screen_path, "w", encoding="utf-8") as f:
                f.write(content)

            print("  ✅ PushupLevel import 추가")

        return True

    def run_mission100_fix(self):
        """Mission100 설정 문제 전체 해결"""
        print("🚀 Mission100 설정 문제 해결 시작!")
        print("="*60)

        if not self.app_path.exists():
            print(f"❌ {self.app_path} 폴더가 없습니다.")
            return False

        results = {
            "profile_fix": False,
            "permission_fix": False,
            "initial_test_removal": False,
            "onboarding_streamline": False,
            "import_fix": False
        }

        # 1. 필요한 import 추가
        results["import_fix"] = self.add_user_profile_import()

        # 2. 홈 스크린 프로필 문제 해결
        results["profile_fix"] = self.fix_home_screen_profile_issue()

        # 3. 권한 요구 문제 해결
        results["permission_fix"] = self.fix_permission_issues()

        # 4. 초기 테스트 요구사항 제거
        results["initial_test_removal"] = self.remove_initial_test_requirement()

        # 5. 간소화된 온보딩
        results["onboarding_streamline"] = self.create_streamlined_onboarding()

        # 결과 출력
        self.print_fix_results(results)

        return results

    def print_fix_results(self, results):
        """수정 결과 출력"""
        print("\n" + "="*60)
        print("✅ Mission100 설정 문제 해결 완료!")
        print("="*60)

        print(f"\n🔧 수정 사항:")
        fixes = [
            ("필요한 import 추가", results["import_fix"]),
            ("기본 프로필 자동 생성", results["profile_fix"]),
            ("권한 요구 완화", results["permission_fix"]),
            ("초기 테스트 메시지 제거", results["initial_test_removal"]),
            ("바로 메인 화면 이동", results["onboarding_streamline"])
        ]

        for desc, success in fixes:
            status = "✅" if success else "❌"
            print(f"   {status} {desc}")

        success_count = sum(results.values())
        print(f"\n📊 수정 성공률: {success_count}/5 ({int(success_count/5*100)}%)")

        print(f"\n🎯 변경 사항:")
        print(f"   • 앱 실행시 자동으로 기본 사용자 프로필 생성")
        print(f"   • '초기 테스트 완료' 메시지 제거")
        print(f"   • 권한 요구 없이도 앱 사용 가능")
        print(f"   • 온보딩 과정 간소화")

        print(f"\n🚀 다음 단계:")
        print(f"   1. flutter clean && flutter pub get")
        print(f"   2. flutter build apk --release")
        print(f"   3. APK 설치 후 테스트")

if __name__ == "__main__":
    fixer = Mission100SetupFixer()
    fixer.run_mission100_fix()