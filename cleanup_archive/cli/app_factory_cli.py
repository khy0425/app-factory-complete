#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter App Factory CLI
명령줄 인터페이스를 통한 앱 생성 및 관리
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.app_generator import FlutterAppGenerator
from marketing.marketing_automation import MarketingAutomation
from deployment.deploy_manager import DeploymentManager

def create_app(args):
    """새 앱 생성"""
    generator = FlutterAppGenerator()

    config = {
        'name': args.name,
        'package_name': args.package,
        'description': args.description,
        'target_audience': args.target,
        'language': args.language,
        'features': args.features.split(',') if args.features else []
    }

    result = generator.create_app(config)
    print(json.dumps(result, indent=2))

def run_marketing(args):
    """마케팅 자동화 실행"""
    marketing = MarketingAutomation()
    marketing.run_campaign(args.app_id, args.platform)

def deploy_app(args):
    """앱 배포"""
    deployer = DeploymentManager()
    deployer.deploy(args.app_dir, args.platform, args.track)

def list_apps(args):
    """생성된 앱 목록 표시"""
    apps_dir = Path('../../generated_apps')
    if not apps_dir.exists():
        print("No apps generated yet")
        return

    for app_dir in apps_dir.iterdir():
        if app_dir.is_dir():
            config_file = app_dir / 'app_config.json'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    print(f"📱 {config['name']} ({config['package_name']})")
                    print(f"   Created: {config.get('created_at', 'Unknown')}")
                    print(f"   Path: {app_dir}")
            else:
                print(f"📱 {app_dir.name}")
                print(f"   Path: {app_dir}")

def main():
    parser = argparse.ArgumentParser(
        description='Flutter App Factory - 자동 앱 생성 및 관리 도구'
    )

    subparsers = parser.add_subparsers(dest='command', help='사용 가능한 명령')

    # create 명령
    create_parser = subparsers.add_parser('create', help='새 앱 생성')
    create_parser.add_argument('--name', required=True, help='앱 이름')
    create_parser.add_argument('--package', required=True, help='패키지 이름 (예: com.example.app)')
    create_parser.add_argument('--description', required=True, help='앱 설명')
    create_parser.add_argument('--target', default='general', help='타겟 고객층')
    create_parser.add_argument('--language', default='ko', help='주 언어 (ko, en, ja 등)')
    create_parser.add_argument('--features', help='활성화할 기능들 (쉼표로 구분)')
    create_parser.set_defaults(func=create_app)

    # marketing 명령
    marketing_parser = subparsers.add_parser('marketing', help='마케팅 자동화 실행')
    marketing_parser.add_argument('--app-id', required=True, help='앱 ID 또는 패키지 이름')
    marketing_parser.add_argument('--platform', default='all', choices=['google', 'apple', 'all'],
                                 help='타겟 플랫폼')
    marketing_parser.set_defaults(func=run_marketing)

    # deploy 명령
    deploy_parser = subparsers.add_parser('deploy', help='앱 배포')
    deploy_parser.add_argument('--app-dir', required=True, help='앱 디렉토리 경로')
    deploy_parser.add_argument('--platform', default='all', choices=['google', 'apple', 'all'],
                              help='배포 플랫폼')
    deploy_parser.add_argument('--track', default='internal', choices=['internal', 'alpha', 'beta', 'production'],
                              help='배포 트랙')
    deploy_parser.set_defaults(func=deploy_app)

    # list 명령
    list_parser = subparsers.add_parser('list', help='생성된 앱 목록 표시')
    list_parser.set_defaults(func=list_apps)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()