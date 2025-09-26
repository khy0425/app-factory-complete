#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Duplicate Detection System
스토어 리젝 방지를 위한 고급 중복 탐지 시스템
"""

import re
import json
import hashlib
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
import logging

class AdvancedDuplicateDetector:
    """고급 중복 탐지 시스템"""

    def __init__(self, db_path: str = "automation/app_fingerprints.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)

        self.fingerprint_db = self._load_fingerprint_db()
        self.logger = logging.getLogger(__name__)

        # 중복 임계값 설정
        self.thresholds = {
            "name_similarity": 0.80,      # 이름 유사도
            "description_similarity": 0.75, # 설명 유사도
            "keyword_overlap": 0.70,       # 키워드 겹침률
            "feature_similarity": 0.65,    # 기능 유사도
            "critical_risk": 0.85,         # 위험 수준
            "warning_risk": 0.70          # 경고 수준
        }

    def _load_fingerprint_db(self) -> Dict:
        """핑거프린트 DB 로드"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"DB 로드 실패: {e}")

        return {"apps": {}, "metadata": {"created": datetime.now().isoformat()}}

    def _save_fingerprint_db(self):
        """핑거프린트 DB 저장"""
        try:
            self.fingerprint_db["metadata"]["last_updated"] = datetime.now().isoformat()
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.fingerprint_db, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"DB 저장 실패: {e}")

    def create_app_fingerprint(self, app_data: Dict) -> Dict:
        """앱 핑거프린트 생성"""

        name = app_data.get("app_name", "").lower().strip()
        description = app_data.get("description", "").lower().strip()
        features = app_data.get("core_features", [])
        category = app_data.get("category", "").lower()

        # 텍스트 정규화
        normalized_name = self._normalize_text(name)
        normalized_desc = self._normalize_text(description)

        # 키워드 추출
        name_keywords = self._extract_keywords(normalized_name)
        desc_keywords = self._extract_keywords(normalized_desc)

        # 기능 해시
        feature_signatures = [self._normalize_text(f) for f in features]

        fingerprint = {
            "app_id": app_data.get("app_name", "unknown"),
            "created_at": datetime.now().isoformat(),

            # 원본 데이터
            "raw_name": name,
            "raw_description": description,

            # 정규화된 데이터
            "normalized_name": normalized_name,
            "normalized_description": normalized_desc,

            # 키워드 세트
            "name_keywords": sorted(name_keywords),
            "desc_keywords": sorted(desc_keywords),
            "all_keywords": sorted(name_keywords | desc_keywords),

            # 기능 시그니처
            "feature_signatures": sorted(feature_signatures),
            "category": category,

            # 해시값들
            "name_hash": hashlib.md5(normalized_name.encode()).hexdigest(),
            "desc_hash": hashlib.md5(normalized_desc.strip().encode()).hexdigest(),
            "combined_hash": hashlib.md5(f"{normalized_name}|{normalized_desc}".encode()).hexdigest(),

            # 메타데이터
            "generation_cost": app_data.get("total_cost", 0),
            "quality_score": app_data.get("quality_score", 0)
        }

        return fingerprint

    def detect_duplicates(self, new_app_data: Dict) -> Dict:
        """중복 탐지 및 위험 평가"""

        new_fingerprint = self.create_app_fingerprint(new_app_data)
        existing_apps = self.fingerprint_db.get("apps", {})

        if not existing_apps:
            return {
                "is_duplicate": False,
                "risk_level": "low",
                "risk_score": 0.0,
                "matches": [],
                "recommendations": ["첫 번째 앱이므로 중복 위험 없음"]
            }

        matches = []
        max_risk_score = 0.0

        for app_id, existing_fp in existing_apps.items():
            match_result = self._compare_fingerprints(new_fingerprint, existing_fp)

            if match_result["total_similarity"] > self.thresholds["warning_risk"]:
                matches.append({
                    "app_id": app_id,
                    "similarity_score": match_result["total_similarity"],
                    "similar_aspects": match_result["similar_aspects"],
                    "details": match_result
                })

                max_risk_score = max(max_risk_score, match_result["total_similarity"])

        # 위험 수준 결정
        if max_risk_score >= self.thresholds["critical_risk"]:
            risk_level = "critical"
            is_duplicate = True
        elif max_risk_score >= self.thresholds["warning_risk"]:
            risk_level = "warning"
            is_duplicate = False
        else:
            risk_level = "low"
            is_duplicate = False

        # 권장사항 생성
        recommendations = self._generate_recommendations(matches, new_fingerprint)

        return {
            "is_duplicate": is_duplicate,
            "risk_level": risk_level,
            "risk_score": max_risk_score,
            "matches": sorted(matches, key=lambda x: x["similarity_score"], reverse=True),
            "recommendations": recommendations,
            "fingerprint": new_fingerprint
        }

    def _compare_fingerprints(self, fp1: Dict, fp2: Dict) -> Dict:
        """두 핑거프린트 비교"""

        # 1. 이름 유사도
        name_sim = self._text_similarity(fp1["normalized_name"], fp2["normalized_name"])

        # 2. 설명 유사도
        desc_sim = self._text_similarity(fp1["normalized_description"], fp2["normalized_description"])

        # 3. 키워드 겹침률
        keyword_overlap = self._set_overlap(
            set(fp1["all_keywords"]),
            set(fp2["all_keywords"])
        )

        # 4. 기능 유사도
        feature_sim = self._feature_similarity(
            fp1["feature_signatures"],
            fp2["feature_signatures"]
        )

        # 5. 카테고리 일치
        category_match = 1.0 if fp1["category"] == fp2["category"] else 0.0

        # 가중 평균으로 총 유사도 계산
        weights = {
            "name": 0.30,
            "description": 0.25,
            "keywords": 0.20,
            "features": 0.15,
            "category": 0.10
        }

        total_similarity = (
            name_sim * weights["name"] +
            desc_sim * weights["description"] +
            keyword_overlap * weights["keywords"] +
            feature_sim * weights["features"] +
            category_match * weights["category"]
        )

        # 유사한 측면들 식별
        similar_aspects = []
        if name_sim > 0.8:
            similar_aspects.append("name")
        if desc_sim > 0.7:
            similar_aspects.append("description")
        if keyword_overlap > 0.7:
            similar_aspects.append("keywords")
        if feature_sim > 0.6:
            similar_aspects.append("features")
        if category_match > 0:
            similar_aspects.append("category")

        return {
            "total_similarity": total_similarity,
            "name_similarity": name_sim,
            "description_similarity": desc_sim,
            "keyword_overlap": keyword_overlap,
            "feature_similarity": feature_sim,
            "category_match": category_match,
            "similar_aspects": similar_aspects
        }

    def _normalize_text(self, text: str) -> str:
        """텍스트 정규화"""
        if not text:
            return ""

        # 소문자 변환
        text = text.lower()

        # 특수문자 제거 (공백은 유지)
        text = re.sub(r'[^\w\s가-힣]', ' ', text)

        # 연속 공백 제거
        text = re.sub(r'\s+', ' ', text)

        # 공통 단어 제거 (너무 일반적인 단어들)
        common_words = {
            'app', 'pro', 'premium', 'best', 'top', 'smart', 'super',
            'advanced', 'ultimate', 'perfect', 'amazing', 'incredible',
            '앱', '프로', '프리미엄', '최고', '스마트', '고급', '완벽'
        }

        words = text.split()
        filtered_words = [w for w in words if w not in common_words and len(w) > 2]

        return ' '.join(filtered_words).strip()

    def _extract_keywords(self, text: str) -> set:
        """키워드 추출"""
        if not text:
            return set()

        # 단어 분할
        words = re.findall(r'\b\w{3,}\b', text)

        # 의미있는 키워드만 추출 (길이 3자 이상)
        keywords = {word.lower() for word in words if len(word) >= 3}

        return keywords

    def _text_similarity(self, text1: str, text2: str) -> float:
        """텍스트 유사도 계산"""
        if not text1 or not text2:
            return 0.0

        return SequenceMatcher(None, text1, text2).ratio()

    def _set_overlap(self, set1: set, set2: set) -> float:
        """집합 겹침률 계산"""
        if not set1 or not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _feature_similarity(self, features1: List[str], features2: List[str]) -> float:
        """기능 유사도 계산"""
        if not features1 or not features2:
            return 0.0

        # 각 기능을 키워드 세트로 변환
        f1_keywords = set()
        f2_keywords = set()

        for f in features1:
            f1_keywords.update(self._extract_keywords(f))

        for f in features2:
            f2_keywords.update(self._extract_keywords(f))

        return self._set_overlap(f1_keywords, f2_keywords)

    def _generate_recommendations(self, matches: List[Dict], new_fp: Dict) -> List[str]:
        """권장사항 생성"""
        recommendations = []

        if not matches:
            recommendations.append("✅ 중복 위험이 낮습니다. 안전하게 진행 가능")
            return recommendations

        highest_match = matches[0]
        similarity = highest_match["similarity_score"]
        similar_aspects = highest_match["similar_aspects"]

        if similarity >= self.thresholds["critical_risk"]:
            recommendations.append("🚨 높은 중복 위험! 다음을 수정하세요:")

            if "name" in similar_aspects:
                recommendations.append("  • 앱 이름을 완전히 다르게 변경")

            if "description" in similar_aspects:
                recommendations.append("  • 앱 설명을 새로 작성 (50% 이상 변경)")

            if "keywords" in similar_aspects:
                recommendations.append("  • 키워드 3개 이상 교체")

            if "features" in similar_aspects:
                recommendations.append("  • 핵심 기능 2개 이상 차별화")

        elif similarity >= self.thresholds["warning_risk"]:
            recommendations.append("⚠️ 중간 위험도. 다음 개선 권장:")

            if "name" in similar_aspects:
                recommendations.append("  • 앱 이름에 고유 수식어 추가")

            if "description" in similar_aspects:
                recommendations.append("  • 설명 첫 문장을 다르게 작성")

            recommendations.append("  • 차별화 포인트 3개 이상 강조")

        # 일반적인 개선 제안
        if len(new_fp["all_keywords"]) < 5:
            recommendations.append("💡 키워드가 부족합니다. 5개 이상 권장")

        return recommendations

    def add_app_to_db(self, app_data: Dict) -> bool:
        """앱을 DB에 추가"""
        try:
            fingerprint = self.create_app_fingerprint(app_data)
            app_id = fingerprint["app_id"]

            self.fingerprint_db["apps"][app_id] = fingerprint
            self._save_fingerprint_db()

            self.logger.info(f"앱 '{app_id}' 핑거프린트가 DB에 추가됨")
            return True

        except Exception as e:
            self.logger.error(f"DB 추가 실패: {e}")
            return False

    def generate_duplicate_report(self, app_data: Dict) -> str:
        """중복 탐지 리포트 생성"""

        result = self.detect_duplicates(app_data)

        report = f"""
🔍 중복 탐지 리포트
{'='*50}

앱 이름: {app_data.get('app_name', 'N/A')}
검사 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 종합 평가:
  위험 수준: {result['risk_level'].upper()}
  유사도 점수: {result['risk_score']:.2%}
  중복 판정: {'예' if result['is_duplicate'] else '아니오'}

"""

        if result["matches"]:
            report += "⚠️ 유사한 앱들:\n"
            for match in result["matches"][:3]:  # 상위 3개만
                report += f"  • {match['app_id']}: {match['similarity_score']:.1%} 유사\n"
                report += f"    유사 측면: {', '.join(match['similar_aspects'])}\n"

        report += "\n💡 권장사항:\n"
        for rec in result["recommendations"]:
            report += f"  {rec}\n"

        return report

    def get_db_stats(self) -> Dict:
        """DB 통계 정보"""
        apps = self.fingerprint_db.get("apps", {})

        if not apps:
            return {"total_apps": 0, "categories": {}, "avg_quality": 0}

        categories = {}
        total_quality = 0

        for app_data in apps.values():
            cat = app_data.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
            total_quality += app_data.get("quality_score", 0)

        return {
            "total_apps": len(apps),
            "categories": categories,
            "avg_quality": total_quality / len(apps) if apps else 0,
            "last_updated": self.fingerprint_db.get("metadata", {}).get("last_updated", "N/A")
        }

def main():
    """테스트 실행"""
    detector = AdvancedDuplicateDetector()

    # 테스트 앱 1
    test_app1 = {
        "app_name": "Premium Fitness Tracker Pro",
        "description": "Advanced fitness tracking app with workout monitoring, nutrition logging, and health analytics for professional athletes and fitness enthusiasts.",
        "core_features": ["Workout tracking", "Nutrition logging", "Health analytics", "Social sharing"],
        "category": "fitness",
        "total_cost": 0.665,
        "quality_score": 87
    }

    # 테스트 앱 2 (유사함)
    test_app2 = {
        "app_name": "Elite Fitness Monitor",
        "description": "Professional fitness monitoring application with advanced workout tracking, meal planning, and comprehensive health analytics.",
        "core_features": ["Exercise monitoring", "Meal planning", "Health statistics", "Progress sharing"],
        "category": "fitness",
        "total_cost": 0.665,
        "quality_score": 85
    }

    print("=== 첫 번째 앱 등록 ===")
    detector.add_app_to_db(test_app1)

    print("\n=== 두 번째 앱 중복 검사 ===")
    report = detector.generate_duplicate_report(test_app2)
    print(report)

    print("\n=== DB 통계 ===")
    stats = detector.get_db_stats()
    print(f"총 앱 수: {stats['total_apps']}")
    print(f"카테고리: {stats['categories']}")
    print(f"평균 품질: {stats['avg_quality']:.1f}")

if __name__ == "__main__":
    main()