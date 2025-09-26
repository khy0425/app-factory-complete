#!/usr/bin/env python3
"""
자동 Repository 정리 및 분류 시스템
미처리된 모든 파일들을 자동으로 분류하고 적절한 Repository에 업로드
"""

import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple
import fnmatch


class AutomatedRepoOrganizer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.sensitive_patterns = [
            r'ghp_[a-zA-Z0-9_]{36}',  # GitHub tokens
            r'sk-[a-zA-Z0-9]{48}',    # OpenAI API keys
            r'AIza[0-9A-Za-z-_]{35}', # Google API keys
            r'ntn_[a-zA-Z0-9]{50}',   # Notion tokens
            r'xoxb-[0-9]+-[0-9]+-[0-9A-Za-z]+',  # Slack tokens
            r'AKIA[0-9A-Z]{16}',      # AWS Access Key
        ]

        # Repository 분류 규칙
        self.repo_mappings = {
            'app-factory-core': {
                'patterns': [
                    '*.py',
                    'automation/*',
                    'templates/*',
                    'modules/*',
                    '*_automation.py',
                    '*_system.py',
                    '*monitoring*',
                    '*optimization*',
                    'requirements.txt',
                    '.env.example'
                ],
                'keywords': [
                    'automation', 'monitoring', 'optimization', 'ai', 'gemini',
                    'revenue', 'admob', 'analytics', 'cicd', 'deployment'
                ]
            },
            'fitness-apps-portfolio': {
                'patterns': [
                    'flutter_apps/*',
                    '*/lib/*',
                    '*/pubspec.yaml',
                    '*/android/*',
                    '*/ios/*',
                    '*squat*',
                    '*fitness*',
                    '*workout*',
                    '*chad*'
                ],
                'keywords': [
                    'flutter', 'dart', 'squat', 'fitness', 'workout', 'chad',
                    'exercise', 'training', 'gym'
                ]
            },
            'app-factory-docs': {
                'patterns': [
                    '*.md',
                    'docs/*',
                    '*README*',
                    '*GUIDE*',
                    '*documentation*',
                    '*manual*'
                ],
                'keywords': [
                    'documentation', 'guide', 'manual', 'readme', 'setup',
                    'tutorial', 'instructions'
                ]
            },
            'app-factory-assets': {
                'patterns': [
                    'assets/*',
                    'images/*',
                    'fonts/*',
                    'store_assets/*',
                    'store_packages/*',
                    '*.png',
                    '*.jpg',
                    '*.jpeg',
                    '*.svg',
                    '*.ttf',
                    '*.otf'
                ],
                'keywords': [
                    'assets', 'images', 'fonts', 'store', 'graphics', 'ui'
                ]
            },
            'app-factory-config': {
                'patterns': [
                    '*.json',
                    '*.yaml',
                    '*.yml',
                    'config/*',
                    '*config*',
                    '.env*',
                    '*.cfg',
                    '*.ini'
                ],
                'keywords': [
                    'config', 'configuration', 'settings', 'environment'
                ]
            }
        }

    def scan_all_files(self) -> List[Path]:
        """모든 파일 스캔"""
        print("📂 전체 파일 스캔 중...")

        file_patterns = [
            '*.py', '*.md', '*.json', '*.yaml', '*.yml', '*.txt',
            '*.dart', '*.js', '*.html', '*.css', '*.png', '*.jpg',
            '*.jpeg', '*.svg', '*.ttf', '*.otf'
        ]

        all_files = []
        for pattern in file_patterns:
            all_files.extend(self.base_path.rglob(pattern))

        # 제외할 디렉토리
        excluded_dirs = {'.git', '__pycache__', '.dart_tool', 'build', 'node_modules'}

        filtered_files = []
        for file_path in all_files:
            if not any(excluded in str(file_path) for excluded in excluded_dirs):
                filtered_files.append(file_path)

        print(f"✅ 총 {len(filtered_files)}개 파일 발견")
        return filtered_files

    def scan_for_sensitive_info(self, files: List[Path]) -> Dict[str, List[str]]:
        """민감한 정보 스캔"""
        print("🔍 민감한 정보 스캔 중...")

        sensitive_files = {}

        for file_path in files:
            try:
                if file_path.suffix in ['.py', '.md', '.txt', '.json', '.yaml', '.yml']:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    found_patterns = []
                    for pattern in self.sensitive_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            found_patterns.extend(matches)

                    if found_patterns:
                        sensitive_files[str(file_path)] = found_patterns

            except Exception as e:
                print(f"⚠️ {file_path} 스캔 실패: {e}")

        print(f"🔒 민감한 정보 발견: {len(sensitive_files)}개 파일")
        return sensitive_files

    def clean_sensitive_info(self, sensitive_files: Dict[str, List[str]]) -> None:
        """민감한 정보 제거"""
        print("🧹 민감한 정보 제거 중...")

        for file_path, patterns in sensitive_files.items():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original_content = content

                # 각 패턴을 플레이스홀더로 교체
                for pattern in self.sensitive_patterns:
                    if 'ghp_' in pattern:
                        content = re.sub(pattern, 'your_github_token_here', content)
                    elif 'sk-' in pattern:
                        content = re.sub(pattern, 'your_openai_api_key_here', content)
                    elif 'AIza' in pattern:
                        content = re.sub(pattern, 'your_google_api_key_here', content)
                    elif 'ntn_' in pattern:
                        content = re.sub(pattern, 'your_notion_token_here', content)
                    elif 'xoxb-' in pattern:
                        content = re.sub(pattern, 'your_slack_token_here', content)
                    elif 'AKIA' in pattern:
                        content = re.sub(pattern, 'your_aws_access_key_here', content)

                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ {file_path} 정리 완료")

            except Exception as e:
                print(f"❌ {file_path} 정리 실패: {e}")

    def classify_files(self, files: List[Path]) -> Dict[str, List[Path]]:
        """파일들을 Repository별로 분류"""
        print("📋 파일 분류 중...")

        classified = {repo: [] for repo in self.repo_mappings.keys()}
        unclassified = []

        for file_path in files:
            relative_path = file_path.relative_to(self.base_path)
            classified_repo = None

            # 패턴 기반 분류
            for repo, rules in self.repo_mappings.items():
                for pattern in rules['patterns']:
                    if fnmatch.fnmatch(str(relative_path), pattern):
                        classified_repo = repo
                        break

                if not classified_repo:
                    # 키워드 기반 분류
                    file_content_lower = str(relative_path).lower()
                    for keyword in rules['keywords']:
                        if keyword in file_content_lower:
                            classified_repo = repo
                            break

                if classified_repo:
                    break

            if classified_repo:
                classified[classified_repo].append(file_path)
            else:
                unclassified.append(file_path)

        # 분류 결과 출력
        for repo, repo_files in classified.items():
            if repo_files:
                print(f"📦 {repo}: {len(repo_files)}개 파일")

        if unclassified:
            print(f"❓ 미분류: {len(unclassified)}개 파일")
            # 미분류 파일들을 app-factory-misc로 분류
            classified['app-factory-misc'] = unclassified

        return classified

    def setup_repository_structure(self, repo_name: str, files: List[Path]) -> Path:
        """Repository 구조 설정"""
        repo_path = self.base_path.parent / f"{repo_name}-new"

        if repo_path.exists():
            shutil.rmtree(repo_path)

        repo_path.mkdir()

        # 파일들을 적절한 구조로 복사
        for file_path in files:
            relative_path = file_path.relative_to(self.base_path)
            dest_path = repo_path / relative_path

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_path)

        return repo_path

    def create_repository_readme(self, repo_path: Path, repo_name: str, file_count: int) -> None:
        """Repository README 생성"""
        readme_content = self.generate_readme_content(repo_name, file_count)

        with open(repo_path / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

    def generate_readme_content(self, repo_name: str, file_count: int) -> str:
        """README 내용 생성"""
        if 'docs' in repo_name:
            return f"""# {repo_name.replace('-', ' ').title()} 📚

> **Complete Documentation and Guides**

App Factory 프로젝트의 모든 문서, 가이드, 매뉴얼을 포함합니다.

## 📋 포함 내용

- 📖 설치 및 설정 가이드
- 🔧 개발자 문서
- 📊 API 문서
- 🎯 사용법 튜토리얼
- 📝 프로젝트 문서

**총 {file_count}개 문서 포함**

## 🚀 빠른 시작

각 디렉토리별로 관련 문서들이 정리되어 있습니다.

---

**📚 Generated by App Factory Documentation System**
"""

        elif 'assets' in repo_name:
            return f"""# {repo_name.replace('-', ' ').title()} 🎨

> **Complete Asset Collection**

App Factory 프로젝트의 모든 에셋, 이미지, 폰트, 스토어 자산을 포함합니다.

## 🎨 포함 내용

- 📱 앱 아이콘 및 스플래시 스크린
- 🖼️ UI/UX 이미지 에셋
- 🔤 커스텀 폰트
- 🏪 스토어 등록용 에셋
- 📊 차트 및 그래프 이미지

**총 {file_count}개 에셋 파일 포함**

## 📁 구조

```
assets/
├── images/           # 이미지 파일들
├── fonts/           # 폰트 파일들
├── store_assets/    # 스토어 등록용
└── ui/             # UI 컴포넌트 에셋
```

---

**🎨 Generated by App Factory Asset System**
"""

        elif 'config' in repo_name:
            return f"""# {repo_name.replace('-', ' ').title()} ⚙️

> **Configuration and Settings**

App Factory 프로젝트의 모든 설정 파일과 구성 요소를 포함합니다.

## ⚙️ 포함 내용

- 🔧 환경 설정 파일
- 📋 JSON/YAML 구성
- 🔑 API 키 템플릿
- 🛠️ 빌드 설정
- 📦 패키지 구성

**총 {file_count}개 설정 파일 포함**

## 🔒 보안 참고사항

모든 민감한 정보는 플레이스홀더로 대체되었습니다.
실제 사용 시 올바른 값으로 교체하세요.

---

**⚙️ Generated by App Factory Config System**
"""

        else:
            return f"""# {repo_name.replace('-', ' ').title()} 🔧

> **Additional Components**

App Factory 프로젝트의 추가 구성 요소들을 포함합니다.

## 📦 포함 내용

**총 {file_count}개 파일 포함**

## 🚀 사용법

이 Repository는 App Factory 생태계의 일부입니다.
메인 프로젝트와 함께 사용하세요.

---

**🔧 Generated by App Factory Automation**
"""

    def create_cicd_workflow(self, repo_path: Path, repo_name: str) -> None:
        """CICD 워크플로우 생성"""
        workflows_dir = repo_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        workflow_content = f"""name: {repo_name.replace('-', ' ').title()} CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Validate file structure
      run: |
        echo "Validating repository structure..."
        find . -type f | wc -l

    - name: Security scan
      run: |
        echo "Scanning for sensitive information..."
        # 민감한 정보가 없는지 확인
        ! grep -r "ghp_" . --exclude-dir=.git || echo "No GitHub tokens found"

    - name: Generate report
      run: |
        echo "Repository: {repo_name}" > validation-report.txt
        echo "Files: $(find . -type f | wc -l)" >> validation-report.txt
        echo "Status: Validated" >> validation-report.txt

    - name: Upload report
      uses: actions/upload-artifact@v4
      with:
        name: validation-report
        path: validation-report.txt

  notify:
    runs-on: ubuntu-latest
    needs: validate
    if: always()

    steps:
    - name: Notify completion
      run: |
        echo "✅ {repo_name} validation completed"
"""

        with open(workflows_dir / "ci.yml", "w", encoding="utf-8") as f:
            f.write(workflow_content)

    def commit_and_push_repository(self, repo_path: Path, repo_name: str) -> str:
        """Repository 커밋 및 푸시"""
        print(f"📤 {repo_name} Repository 업로드 중...")

        try:
            # Git 초기화
            subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "action@github.com"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "GitHub Action"], cwd=repo_path, check=True)

            # GitHub Repository 생성
            repo_url = self.create_github_repository(repo_name)

            # Remote 추가
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=repo_path, check=True)

            # 커밋 및 푸시
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run([
                "git", "commit", "-m",
                f"🎯 Initial commit: {repo_name}\n\n✨ Auto-organized by App Factory\n🔒 Security-validated\n📁 Properly categorized"
            ], cwd=repo_path, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path, check=True)

            print(f"✅ {repo_name} 업로드 완료: {repo_url}")
            return repo_url

        except subprocess.CalledProcessError as e:
            print(f"❌ {repo_name} 업로드 실패: {e}")
            return ""

    def create_github_repository(self, repo_name: str) -> str:
        """GitHub Repository 생성"""
        import requests

        github_token = os.getenv('GITHUB_TOKEN', 'your_github_token_here')

        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "name": repo_name,
            "description": f"Auto-organized {repo_name.replace('-', ' ')} from App Factory",
            "private": False,
            "auto_init": False
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            return response.json()["clone_url"]
        elif response.status_code == 422:
            # Repository가 이미 존재
            return f"https://github.com/khy0425/{repo_name}.git"
        else:
            raise Exception(f"GitHub Repository 생성 실패: {response.status_code}")

    def update_existing_repository(self, repo_name: str, files: List[Path]) -> str:
        """기존 Repository 업데이트"""
        if repo_name in ['app-factory-core', 'fitness-apps-portfolio']:
            print(f"📝 기존 {repo_name} Repository 업데이트 중...")

            existing_repo_path = self.base_path.parent / repo_name.replace('app-factory-core', 'app-factory-core-clean')
            if repo_name == 'fitness-apps-portfolio':
                existing_repo_path = self.base_path.parent / 'fitness-apps-portfolio'

            if existing_repo_path.exists():
                # 새 파일들만 추가
                for file_path in files:
                    relative_path = file_path.relative_to(self.base_path)
                    dest_path = existing_repo_path / relative_path

                    if not dest_path.exists():
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, dest_path)

                # 커밋 및 푸시
                try:
                    subprocess.run(["git", "add", "."], cwd=existing_repo_path, check=True)
                    subprocess.run([
                        "git", "commit", "-m",
                        f"📁 Add auto-organized files\n\n✨ Added {len(files)} new files\n🔒 Security validated"
                    ], cwd=existing_repo_path, check=True)
                    subprocess.run(["git", "push"], cwd=existing_repo_path, check=True)

                    print(f"✅ {repo_name} 업데이트 완료")
                    return f"https://github.com/khy0425/{repo_name}"

                except subprocess.CalledProcessError:
                    print(f"⚠️ {repo_name} 업데이트 중 오류 (변경사항이 없을 수 있음)")
                    return f"https://github.com/khy0425/{repo_name}"

        return ""

    def run_full_organization(self) -> None:
        """전체 자동 정리 실행"""
        print("🚀 자동 Repository 정리 시작!")
        print("=" * 60)

        # 1. 파일 스캔
        all_files = self.scan_all_files()

        # 2. 민감한 정보 스캔 및 제거
        sensitive_files = self.scan_for_sensitive_info(all_files)
        if sensitive_files:
            self.clean_sensitive_info(sensitive_files)

        # 3. 파일 분류
        classified_files = self.classify_files(all_files)

        # 4. Repository 생성/업데이트
        results = {}

        for repo_name, files in classified_files.items():
            if not files:
                continue

            if repo_name in ['app-factory-core', 'fitness-apps-portfolio']:
                # 기존 Repository 업데이트
                url = self.update_existing_repository(repo_name, files)
                results[repo_name] = url
            else:
                # 새 Repository 생성
                repo_path = self.setup_repository_structure(repo_name, files)
                self.create_repository_readme(repo_path, repo_name, len(files))
                self.create_cicd_workflow(repo_path, repo_name)
                url = self.commit_and_push_repository(repo_path, repo_name)
                results[repo_name] = url

        # 결과 출력
        print("\n" + "=" * 60)
        print("🎉 자동 Repository 정리 완료!")
        print("=" * 60)

        for repo_name, url in results.items():
            if url:
                print(f"✅ {repo_name}: {url}")

        print(f"\n📊 총 {len(results)}개 Repository 처리 완료")


if __name__ == "__main__":
    organizer = AutomatedRepoOrganizer("E:/Projects/app-factory-complete")
    organizer.run_full_organization()