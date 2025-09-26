#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
완전 자동화 CI/CD 시스템
앱 생성 → Flutter 프로젝트 생성 → GitHub 업로드 → APK 빌드 → 릴리즈
"""

import os
import sys
import json
import time
import subprocess
import requests
import shutil
from datetime import datetime
from pathlib import Path

class CompleteCICDAutomation:
    def __init__(self):
        self.github_token = "your_github_token_here"
        self.github_username = "reaf-dev"  # 실제 GitHub 사용자명
        self.base_dir = Path("E:/Projects/app-factory-complete")
        self.generated_dir = self.base_dir / "generated_projects"
        self.flutter_apps_dir = self.base_dir / "flutter_apps"
        self.mission100_assets = Path("E:/Projects/Flutter/misson100_version_2/assets")

        # Flutter 기본 템플릿 설정
        self.flutter_template = {
            "sdk": ">=3.0.0 <4.0.0",
            "dependencies": {
                "flutter": {"sdk": "flutter"},
                "provider": "^6.0.5",
                "shared_preferences": "^2.0.15",
                "google_mobile_ads": "^3.0.0",
                "geolocator": "^9.0.2",
                "permission_handler": "^10.4.3"
            },
            "dev_dependencies": {
                "flutter_test": {"sdk": "flutter"},
                "flutter_lints": "^2.0.0"
            }
        }

    def run_complete_automation(self, app_count=3):
        """완전 자동화 실행"""
        print("🚀 완전 자동화 CI/CD 시작!")
        print(f"📱 {app_count}개 앱을 생성하고 자동 배포합니다")
        print("=" * 60)

        successful_apps = []
        failed_apps = []

        # 앱 아이디어 목록
        app_ideas = [
            "스쿼트 챌린지 앱",
            "푸시업 마스터 앱",
            "플랭크 타이머 앱",
            "점핑잭 카운터 앱",
            "런지 트레이너 앱",
            "버피 챌린지 앱",
            "크런치 카운터 앱",
            "마운틴 클라이머 앱"
        ]

        for i in range(min(app_count, len(app_ideas))):
            idea = app_ideas[i]
            print(f"\n🎯 [{i+1}/{app_count}] {idea} 자동화 시작")
            print("-" * 40)

            try:
                # 1. 앱 생성
                project_name = self.generate_project_name(idea)
                print(f"📋 프로젝트명: {project_name}")

                # 2. Flutter 프로젝트 생성
                flutter_project_path = self.create_flutter_project(project_name, idea)
                print(f"💻 Flutter 프로젝트 생성: {flutter_project_path}")

                # 3. GitHub 저장소 생성 및 업로드
                repo_url = self.create_and_upload_to_github(project_name, flutter_project_path)
                print(f"📤 GitHub 업로드: {repo_url}")

                # 4. GitHub Actions 설정
                self.setup_github_actions(flutter_project_path)
                print("⚙️ GitHub Actions 설정 완료")

                # 5. 최종 커밋 및 푸시 (자동 빌드 트리거)
                self.final_commit_and_push(flutter_project_path)
                print("🚀 자동 빌드 트리거됨")

                successful_apps.append({
                    "name": project_name,
                    "idea": idea,
                    "repo_url": repo_url,
                    "status": "success"
                })

                print(f"✅ {project_name} 완전 자동화 성공!")
                time.sleep(2)  # API 제한 방지

            except Exception as e:
                print(f"❌ {idea} 실패: {str(e)}")
                failed_apps.append({
                    "idea": idea,
                    "error": str(e),
                    "status": "failed"
                })

        # 결과 요약
        self.print_automation_summary(successful_apps, failed_apps)
        return successful_apps, failed_apps

    def generate_project_name(self, idea):
        """아이디어를 기반으로 프로젝트명 생성"""
        name_mapping = {
            "스쿼트 챌린지 앱": "squat_master",
            "푸시업 마스터 앱": "pushup_hero",
            "플랭크 타이머 앱": "plank_timer",
            "점핑잭 카운터 앱": "jumping_jack",
            "런지 트레이너 앱": "lunge_trainer",
            "버피 챌린지 앱": "burpee_challenge",
            "크런치 카운터 앱": "crunch_counter",
            "마운틴 클라이머 앱": "mountain_climber"
        }
        return name_mapping.get(idea, "workout_app")

    def create_flutter_project(self, project_name, app_idea):
        """Flutter 프로젝트 생성"""
        project_path = self.flutter_apps_dir / project_name

        # 기존 디렉터리 삭제
        if project_path.exists():
            shutil.rmtree(project_path)

        # Flutter 프로젝트 생성
        cmd = f'flutter create --org com.reaf {project_name}'
        result = subprocess.run(cmd, shell=True, cwd=self.flutter_apps_dir,
                              capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            raise Exception(f"Flutter create 실패: {result.stderr}")

        # Mission100 에셋 복사
        self.copy_mission100_assets(project_path)

        # 앱별 커스터마이징
        self.customize_flutter_app(project_path, project_name, app_idea)

        return project_path

    def copy_mission100_assets(self, project_path):
        """Mission100 에셋 복사"""
        assets_source = self.mission100_assets / "images"
        assets_dest = project_path / "assets" / "images"

        # assets 디렉터리 생성
        assets_dest.mkdir(parents=True, exist_ok=True)

        if assets_source.exists():
            # 모든 이미지 파일 복사
            for file in assets_source.glob("*"):
                if file.is_file():
                    shutil.copy2(file, assets_dest)

    def customize_flutter_app(self, project_path, project_name, app_idea):
        """Flutter 앱 커스터마이징"""

        # pubspec.yaml 업데이트
        self.update_pubspec_yaml(project_path, project_name)

        # main.dart 생성
        self.create_main_dart(project_path, project_name, app_idea)

        # AdMob 설정
        self.setup_admob_config(project_path)

        # AndroidManifest.xml 업데이트
        self.update_android_manifest(project_path)

    def update_pubspec_yaml(self, project_path, project_name):
        """pubspec.yaml 업데이트"""
        pubspec_content = f"""name: {project_name}
description: Chad-themed workout app generated by automation
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  provider: ^6.0.5
  shared_preferences: ^2.0.15
  google_mobile_ads: ^3.0.0
  geolocator: ^9.0.2
  permission_handler: ^10.4.3
  google_fonts: ^5.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
"""

        with open(project_path / "pubspec.yaml", "w", encoding="utf-8") as f:
            f.write(pubspec_content)

    def create_main_dart(self, project_path, project_name, app_idea):
        """main.dart 생성"""
        main_dart_content = f'''import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();
  await MobileAds.instance.initialize();
  runApp(const {self.pascal_case(project_name)}App());
}}

class {self.pascal_case(project_name)}App extends StatelessWidget {{
  const {self.pascal_case(project_name)}App({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{app_idea}',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF1A1A1A),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF2A2A2A),
          foregroundColor: Color(0xFFFFD700),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFFFFD700),
            foregroundColor: Colors.black,
          ),
        ),
      ),
      home: const HomeScreen(),
    );
  }}
}}

class HomeScreen extends StatefulWidget {{
  const HomeScreen({{super.key}});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}}

class _HomeScreenState extends State<HomeScreen> {{
  BannerAd? _bannerAd;
  int _counter = 0;

  @override
  void initState() {{
    super.initState();
    _loadBannerAd();
  }}

  void _loadBannerAd() {{
    _bannerAd = BannerAd(
      adUnitId: 'ca-app-pub-3940256099942544/6300978111', // Test ID
      size: AdSize.banner,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) => setState(() {{}}),
        onAdFailedToLoad: (ad, error) => ad.dispose(),
      ),
    )..load();
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text(
          '{app_idea}',
          style: GoogleFonts.bebasNeue(fontSize: 24),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Chad Level: $_counter',
                    style: GoogleFonts.bebasNeue(
                      fontSize: 32,
                      color: const Color(0xFFFFD700),
                    ),
                  ),
                  const SizedBox(height: 20),
                  Image.asset(
                    'assets/images/chad_level_1.png',
                    width: 200,
                    height: 200,
                    errorBuilder: (context, error, stackTrace) =>
                        const Icon(Icons.fitness_center, size: 200, color: Color(0xFFFFD700)),
                  ),
                  const SizedBox(height: 40),
                  ElevatedButton(
                    onPressed: () => setState(() => _counter++),
                    child: Text(
                      'Chad Up!',
                      style: GoogleFonts.robotoCondensed(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          if (_bannerAd != null)
            Container(
              alignment: Alignment.center,
              width: _bannerAd!.size.width.toDouble(),
              height: _bannerAd!.size.height.toDouble(),
              child: AdWidget(ad: _bannerAd!),
            ),
        ],
      ),
    );
  }}

  @override
  void dispose() {{
    _bannerAd?.dispose();
    super.dispose();
  }}
}}
'''

        lib_dir = project_path / "lib"
        lib_dir.mkdir(exist_ok=True)

        with open(lib_dir / "main.dart", "w", encoding="utf-8") as f:
            f.write(main_dart_content)

    def pascal_case(self, snake_str):
        """snake_case를 PascalCase로 변환"""
        return ''.join(word.capitalize() for word in snake_str.split('_'))

    def setup_admob_config(self, project_path):
        """AdMob 설정"""
        android_manifest = project_path / "android" / "app" / "src" / "main" / "AndroidManifest.xml"

        manifest_content = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:label="Chad Workout"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">

        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-3940256099942544~3347511713"/>

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:taskAffinity=""
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            <meta-data
              android:name="io.flutter.embedding.android.NormalTheme"
              android:resource="@style/NormalTheme" />
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
'''

        with open(android_manifest, "w", encoding="utf-8") as f:
            f.write(manifest_content)

    def update_android_manifest(self, project_path):
        """Android Manifest 업데이트"""
        # 이미 setup_admob_config에서 처리됨
        pass

    def create_and_upload_to_github(self, project_name, project_path):
        """GitHub 저장소 생성 및 업로드"""

        # 1. GitHub 저장소 생성
        repo_url = self.create_github_repository(project_name)

        # 2. Git 초기화 및 설정
        self.initialize_git_repository(project_path, repo_url)

        # 3. 파일 커밋 및 푸시
        self.commit_and_push_initial_files(project_path)

        return repo_url

    def create_github_repository(self, project_name):
        """GitHub 저장소 생성"""
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "name": project_name,
            "description": f"Chad-themed workout app: {project_name}",
            "private": False,
            "auto_init": False
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            repo_data = response.json()
            return repo_data["clone_url"]
        else:
            raise Exception(f"GitHub 저장소 생성 실패: {response.status_code} - {response.text}")

    def initialize_git_repository(self, project_path, repo_url):
        """Git 저장소 초기화"""
        os.chdir(project_path)

        commands = [
            "git init",
            'git config user.name "App Factory Bot"',
            'git config user.email "bot@appfactory.com"',
            f"git remote add origin {repo_url}"
        ]

        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Git 명령 실패: {cmd} - {result.stderr}")

    def commit_and_push_initial_files(self, project_path):
        """초기 파일 커밋 및 푸시"""
        os.chdir(project_path)

        commands = [
            "git add .",
            'git commit -m "Initial commit: Chad workout app with automation"',
            "git branch -M main",
            "git push -u origin main"
        ]

        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Git 명령 실패: {cmd} - {result.stderr}")

    def setup_github_actions(self, project_path):
        """GitHub Actions 워크플로우 설정"""
        workflows_dir = project_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        workflow_content = '''name: Flutter CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - uses: actions/setup-java@v3
      with:
        distribution: 'zulu'
        java-version: '17'

    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.32.0'

    - name: Install dependencies
      run: flutter pub get

    - name: Run tests
      run: flutter test

    - name: Build APK
      run: flutter build apk --release

    - name: Upload APK to Release
      uses: actions/upload-artifact@v3
      with:
        name: release-apk
        path: build/app/outputs/flutter-apk/app-release.apk

    - name: Create Release
      if: github.ref == 'refs/heads/main'
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: v${{ github.run_number }}
        release_name: Release v${{ github.run_number }}
        draft: false
        prerelease: false

    - name: Upload Release Asset
      if: github.ref == 'refs/heads/main'
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: build/app/outputs/flutter-apk/app-release.apk
        asset_name: app-release.apk
        asset_content_type: application/vnd.android.package-archive
'''

        with open(workflows_dir / "flutter-cicd.yml", "w", encoding="utf-8") as f:
            f.write(workflow_content)

    def final_commit_and_push(self, project_path):
        """최종 커밋 및 푸시 (GitHub Actions 트리거)"""
        os.chdir(project_path)

        commands = [
            "git add .",
            'git commit -m "Add GitHub Actions CI/CD workflow"',
            "git push origin main"
        ]

        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"경고: {cmd} 실행 중 오류 (계속 진행): {result.stderr}")

    def print_automation_summary(self, successful_apps, failed_apps):
        """자동화 결과 요약 출력"""
        print("\n" + "="*60)
        print("🎉 완전 자동화 CI/CD 결과 요약")
        print("="*60)
        print(f"✅ 성공: {len(successful_apps)}개")
        print(f"❌ 실패: {len(failed_apps)}개")

        if successful_apps:
            print("\n📱 성공한 앱들:")
            for app in successful_apps:
                print(f"  • {app['name']} - {app['repo_url']}")

        if failed_apps:
            print("\n❌ 실패한 앱들:")
            for app in failed_apps:
                print(f"  • {app['idea']} - {app['error']}")

        print(f"\n📅 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚀 GitHub Actions가 자동으로 APK를 빌드하고 릴리즈합니다!")

if __name__ == "__main__":
    automation = CompleteCICDAutomation()

    print("🤖 완전 자동화 CI/CD 시스템")
    print("앱 생성부터 GitHub 업로드, APK 빌드까지 완전 자동화!")
    print("="*60)

    try:
        app_count = 3  # 테스트용으로 3개
        automation.run_complete_automation(app_count)
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 치명적 오류: {e}")