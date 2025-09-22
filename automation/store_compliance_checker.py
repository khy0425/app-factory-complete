#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Store Compliance Checker
앱스토어 정책 준수 자동 검증 시스템
"""

import re
import json
from typing import Dict, List, Tuple
from datetime import datetime
import hashlib

class StoreComplianceChecker:
    """스토어 정책 준수 검사기"""

    def __init__(self):
        self.compliance_rules = {
            "google_play": {
                "min_description_length": 80,
                "max_description_length": 4000,
                "min_title_length": 2,
                "max_title_length": 50,
                "required_keywords": ["app", "mobile"],
                "forbidden_words": ["best", "top", "#1", "amazing", "incredible"],
                "min_unique_features": 3
            },
            "app_store": {
                "min_description_length": 170,
                "max_description_length": 4000,
                "min_title_length": 2,
                "max_title_length": 30,
                "required_privacy_policy": True,
                "min_screenshots": 3,
                "max_screenshots": 10
            }
        }

        self.generated_apps_db = {}  # 중복 체크용

    def check_app_compliance(self, app_data: Dict) -> Dict:
        """앱 정책 준수 종합 검사"""

        results = {
            "overall_compliance": True,
            "compliance_score": 0,
            "issues": [],
            "warnings": [],
            "recommendations": [],
            "store_readiness": {
                "google_play": False,
                "app_store": False
            }
        }

        # 1. 기본 메타데이터 검사
        metadata_result = self._check_metadata_compliance(app_data)
        results = self._merge_results(results, metadata_result)

        # 2. 콘텐츠 유니크성 검사
        uniqueness_result = self._check_content_uniqueness(app_data)
        results = self._merge_results(results, uniqueness_result)

        # 3. 품질 기준 검사
        quality_result = self._check_quality_standards(app_data)
        results = self._merge_results(results, quality_result)

        # 4. 법적 요구사항 검사
        legal_result = self._check_legal_requirements(app_data)
        results = self._merge_results(results, legal_result)

        # 5. 스토어별 특화 검사
        store_result = self._check_store_specific_requirements(app_data)
        results = self._merge_results(results, store_result)

        # 최종 점수 계산
        results["compliance_score"] = self._calculate_compliance_score(results)
        results["overall_compliance"] = results["compliance_score"] >= 80

        # 스토어 준비도 평가
        results["store_readiness"] = self._evaluate_store_readiness(results)

        return results

    def _check_metadata_compliance(self, app_data: Dict) -> Dict:
        """메타데이터 규정 준수 검사"""

        issues = []
        warnings = []
        recommendations = []

        app_name = app_data.get("app_name", "")
        description = app_data.get("description", "")

        # 앱 이름 검사
        if len(app_name) < 2:
            issues.append("앱 이름이 너무 짧습니다 (최소 2자)")
        elif len(app_name) > 50:
            issues.append("앱 이름이 너무 깁니다 (최대 50자)")

        # 금지 단어 검사
        forbidden_words = self.compliance_rules["google_play"]["forbidden_words"]
        for word in forbidden_words:
            if word.lower() in app_name.lower():
                warnings.append(f"앱 이름에 과장 표현 '{word}' 포함 - 스토어 리젝 위험")

        # 설명 길이 검사
        if len(description) < 80:
            issues.append("앱 설명이 너무 짧습니다 (최소 80자)")
        elif len(description) > 4000:
            issues.append("앱 설명이 너무 깁니다 (최대 4000자)")

        # 키워드 다양성 검사
        if self._count_unique_keywords(description) < 10:
            recommendations.append("설명에 더 다양한 키워드 추가 권장")

        return {
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations
        }

    def _check_content_uniqueness(self, app_data: Dict) -> Dict:
        """콘텐츠 유니크성 검사"""

        issues = []
        warnings = []
        recommendations = []

        app_name = app_data.get("app_name", "")
        description = app_data.get("description", "")

        # 앱 이름 해시 생성
        name_hash = hashlib.md5(app_name.lower().encode()).hexdigest()

        # 설명 유사도 검사 (간단한 해시 기반)
        desc_hash = hashlib.md5(description.lower().encode()).hexdigest()

        # 이전 앱들과 비교
        for existing_app, data in self.generated_apps_db.items():
            # 이름 유사도
            if data["name_hash"] == name_hash:
                issues.append(f"동일한 앱 이름이 이미 존재합니다: {existing_app}")

            # 설명 유사도 (실제로는 더 정교한 알고리즘 필요)
            if data["desc_hash"] == desc_hash:
                warnings.append(f"유사한 앱 설명이 존재합니다: {existing_app}")

        # 현재 앱을 DB에 추가
        self.generated_apps_db[app_name] = {
            "name_hash": name_hash,
            "desc_hash": desc_hash,
            "created_at": datetime.now().isoformat()
        }

        # 차별화 요소 확인
        unique_features = app_data.get("unique_features", [])
        if len(unique_features) < 3:
            recommendations.append("앱별 차별화 요소를 3개 이상 추가하세요")

        return {
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations
        }

    def _check_quality_standards(self, app_data: Dict) -> Dict:
        """품질 기준 검사"""

        issues = []
        warnings = []
        recommendations = []

        # 완성도 검사
        completion_rate = app_data.get("completion_percentage", 0)
        if completion_rate < 80:
            issues.append(f"앱 완성도가 낮습니다: {completion_rate}% (최소 80% 필요)")
        elif completion_rate < 85:
            warnings.append(f"앱 완성도 개선 권장: {completion_rate}%")

        # 기능 완성도 검사
        core_features = app_data.get("core_features_completion", 0)
        if core_features < 100:
            issues.append("핵심 기능이 모두 구현되지 않았습니다")

        # 에셋 품질 검사
        assets = app_data.get("generated_assets", {})
        if not assets.get("app_icon"):
            issues.append("앱 아이콘이 생성되지 않았습니다")

        if len(assets.get("screenshots", [])) < 3:
            warnings.append("스크린샷이 3개 미만입니다 (권장: 5개 이상)")

        return {
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations
        }

    def _check_legal_requirements(self, app_data: Dict) -> Dict:
        """법적 요구사항 검사"""

        issues = []
        warnings = []
        recommendations = []

        # Privacy Policy 확인
        if not app_data.get("privacy_policy_url"):
            issues.append("Privacy Policy URL이 설정되지 않았습니다")

        # Terms of Service 확인
        if not app_data.get("terms_of_service_url"):
            warnings.append("Terms of Service URL 권장")

        # 광고 사용 시 필수 고지
        if app_data.get("monetization", {}).get("ads_enabled", False):
            if not app_data.get("ads_disclosure"):
                issues.append("광고 사용 시 사용자 고지가 필요합니다")

        # 데이터 수집 관련
        permissions = app_data.get("required_permissions", [])
        sensitive_permissions = ["CAMERA", "LOCATION", "MICROPHONE", "CONTACTS"]

        for perm in permissions:
            if perm in sensitive_permissions:
                if not app_data.get("permission_rationale", {}).get(perm):
                    warnings.append(f"{perm} 권한 사용 이유 명시 권장")

        return {
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations
        }

    def _check_store_specific_requirements(self, app_data: Dict) -> Dict:
        """스토어별 특화 요구사항 검사"""

        issues = []
        warnings = []
        recommendations = []

        # Google Play 특화 검사
        if app_data.get("target_stores", {}).get("google_play", True):
            # Target SDK 검사
            target_sdk = app_data.get("android_config", {}).get("target_sdk", 0)
            if target_sdk < 33:  # Android 13
                warnings.append("Google Play: Target SDK 33 이상 권장")

            # 64-bit 지원 확인
            if not app_data.get("android_config", {}).get("supports_64bit", False):
                issues.append("Google Play: 64-bit 지원 필수")

        # App Store 특화 검사
        if app_data.get("target_stores", {}).get("app_store", True):
            # iOS 버전 지원
            min_ios = app_data.get("ios_config", {}).get("min_ios_version", "")
            if min_ios and float(min_ios) < 12.0:
                warnings.append("App Store: iOS 12.0 이상 지원 권장")

        return {
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations
        }

    def _merge_results(self, main_result: Dict, sub_result: Dict) -> Dict:
        """검사 결과 병합"""
        main_result["issues"].extend(sub_result.get("issues", []))
        main_result["warnings"].extend(sub_result.get("warnings", []))
        main_result["recommendations"].extend(sub_result.get("recommendations", []))
        return main_result

    def _calculate_compliance_score(self, results: Dict) -> int:
        """규정 준수 점수 계산"""
        base_score = 100

        # 이슈마다 점수 차감
        base_score -= len(results["issues"]) * 15
        base_score -= len(results["warnings"]) * 5

        return max(0, min(100, base_score))

    def _evaluate_store_readiness(self, results: Dict) -> Dict:
        """스토어 준비도 평가"""
        critical_issues = len(results["issues"])

        return {
            "google_play": critical_issues == 0 and results["compliance_score"] >= 85,
            "app_store": critical_issues == 0 and results["compliance_score"] >= 90
        }

    def _count_unique_keywords(self, text: str) -> int:
        """텍스트의 유니크 키워드 수 계산"""
        words = re.findall(r'\b\w{3,}\b', text.lower())
        return len(set(words))

    def generate_compliance_report(self, app_data: Dict) -> str:
        """규정 준수 리포트 생성"""
        result = self.check_app_compliance(app_data)

        report = f"""
📋 스토어 규정 준수 리포트
{'='*50}

앱 이름: {app_data.get('app_name', 'N/A')}
검사 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 종합 점수: {result['compliance_score']}/100
✅ 전체 준수: {'예' if result['overall_compliance'] else '아니오'}

🏪 스토어 준비도:
  Google Play: {'✅ 준비됨' if result['store_readiness']['google_play'] else '❌ 추가 작업 필요'}
  App Store: {'✅ 준비됨' if result['store_readiness']['app_store'] else '❌ 추가 작업 필요'}

"""

        if result["issues"]:
            report += "\n❌ 필수 수정 사항:\n"
            for issue in result["issues"]:
                report += f"  • {issue}\n"

        if result["warnings"]:
            report += "\n⚠️ 주의 사항:\n"
            for warning in result["warnings"]:
                report += f"  • {warning}\n"

        if result["recommendations"]:
            report += "\n💡 개선 권장 사항:\n"
            for rec in result["recommendations"]:
                report += f"  • {rec}\n"

        return report

def main():
    """테스트 실행"""
    checker = StoreComplianceChecker()

    # 테스트 앱 데이터
    test_app = {
        "app_name": "Premium Fitness Tracker Pro",
        "description": "A comprehensive fitness tracking application with advanced features for monitoring workouts, nutrition, and health metrics. Track your progress with detailed analytics and achieve your fitness goals.",
        "completion_percentage": 87,
        "core_features_completion": 100,
        "generated_assets": {
            "app_icon": {"url": "icon.png"},
            "screenshots": ["screen1.png", "screen2.png", "screen3.png"]
        },
        "privacy_policy_url": "https://example.com/privacy",
        "unique_features": ["AI workout recommendations", "Offline data sync", "Social challenges"]
    }

    report = checker.generate_compliance_report(test_app)
    print(report)

if __name__ == "__main__":
    main()