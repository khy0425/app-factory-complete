#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asset Cache Manager
로컬 에셋 캐싱으로 Nano Banana 비용 50% 절감 시스템
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

class AssetCacheManager:
    """로컬 에셋 캐시 관리자"""

    def __init__(self, cache_dir: str = None):
        self.logger = logging.getLogger(__name__)

        # 캐시 디렉토리 설정
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / ".cache" / "app-factory" / "assets"

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # 메타데이터 파일
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        self.stats_file = self.cache_dir / "cache_stats.json"

        # 캐시 설정
        self.cache_config = {
            "max_cache_size_mb": 500,  # 최대 500MB
            "max_age_days": 90,        # 90일 후 만료
            "cleanup_threshold": 0.8,   # 80% 찼을 때 정리
            "similarity_threshold": 0.85  # 85% 유사도면 재사용
        }

        # 메타데이터 로드
        self.metadata = self._load_metadata()
        self.stats = self._load_stats()

        self.logger.info(f"🗂️ 에셋 캐시 초기화: {self.cache_dir}")
        self.logger.info(f"📊 캐시된 에셋: {len(self.metadata)}개")

    def _load_metadata(self) -> Dict:
        """캐시 메타데이터 로드"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"메타데이터 로드 실패: {e}")

        return {
            "assets": {},
            "created": datetime.now().isoformat(),
            "last_cleanup": datetime.now().isoformat()
        }

    def _load_stats(self) -> Dict:
        """캐시 통계 로드"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"통계 로드 실패: {e}")

        return {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_saved_cost": 0.0,
            "last_updated": datetime.now().isoformat()
        }

    def _save_metadata(self):
        """메타데이터 저장"""
        try:
            self.metadata["last_updated"] = datetime.now().isoformat()
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"메타데이터 저장 실패: {e}")

    def _save_stats(self):
        """통계 저장"""
        try:
            self.stats["last_updated"] = datetime.now().isoformat()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"통계 저장 실패: {e}")

    def generate_cache_key(self, prompt: str, category: str, style_params: Dict = None) -> str:
        """캐시 키 생성"""

        # 프롬프트 정규화
        normalized_prompt = self._normalize_prompt(prompt)

        # 스타일 파라미터 정규화
        style_str = ""
        if style_params:
            sorted_params = sorted(style_params.items())
            style_str = json.dumps(sorted_params, sort_keys=True)

        # 키 생성용 문자열 구성
        key_string = f"{category}|{normalized_prompt}|{style_str}"

        # SHA256 해시 생성
        hash_key = hashlib.sha256(key_string.encode()).hexdigest()[:16]

        return f"{category}_{hash_key}"

    def _normalize_prompt(self, prompt: str) -> str:
        """프롬프트 정규화 (유사한 프롬프트 캐시 재사용을 위해)"""

        # 소문자 변환
        normalized = prompt.lower().strip()

        # 공통 단어 제거/통일
        replacements = {
            "premium": "pro",
            "professional": "pro",
            "advanced": "pro",
            "modern": "clean",
            "contemporary": "clean",
            "sleek": "clean",
            "beautiful": "elegant",
            "stunning": "elegant",
            "amazing": "elegant"
        }

        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        # 연속 공백 제거
        normalized = " ".join(normalized.split())

        return normalized

    def find_similar_asset(self, cache_key: str, prompt: str, category: str) -> Optional[str]:
        """유사한 에셋 찾기"""

        if cache_key in self.metadata["assets"]:
            # 정확한 키 매치
            asset_info = self.metadata["assets"][cache_key]
            cached_file = self.cache_dir / asset_info["filename"]

            if cached_file.exists() and not self._is_expired(asset_info):
                self.logger.info(f"🎯 캐시 정확 매치: {cache_key}")
                return str(cached_file)

        # 유사도 기반 검색
        normalized_prompt = self._normalize_prompt(prompt)

        best_match = None
        best_similarity = 0.0

        for key, asset_info in self.metadata["assets"].items():
            if asset_info["category"] != category:
                continue

            cached_file = self.cache_dir / asset_info["filename"]
            if not cached_file.exists() or self._is_expired(asset_info):
                continue

            # 프롬프트 유사도 계산
            similarity = self._calculate_similarity(
                normalized_prompt,
                self._normalize_prompt(asset_info["original_prompt"])
            )

            if similarity > best_similarity and similarity >= self.cache_config["similarity_threshold"]:
                best_similarity = similarity
                best_match = str(cached_file)

        if best_match:
            self.logger.info(f"🔍 캐시 유사 매치: {best_similarity:.2%} 유사도")

        return best_match

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """텍스트 유사도 계산 (Jaccard 유사도)"""

        words1 = set(text1.split())
        words2 = set(text2.split())

        if not words1 and not words2:
            return 1.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

    def _is_expired(self, asset_info: Dict) -> bool:
        """에셋 만료 여부 확인"""

        created_time = datetime.fromisoformat(asset_info["created_at"])
        expiry_time = created_time + timedelta(days=self.cache_config["max_age_days"])

        return datetime.now() > expiry_time

    def cache_asset(self, asset_data: Dict, cache_key: str, prompt: str, category: str) -> str:
        """에셋을 캐시에 저장"""

        try:
            # 파일명 생성
            filename = f"{cache_key}.png"  # 기본적으로 PNG로 저장
            cached_file = self.cache_dir / filename

            # 에셋 데이터에서 파일 저장 (실제 구현에서는 URL에서 다운로드)
            if "image_url" in asset_data:
                # 실제로는 URL에서 다운로드
                self._download_and_save(asset_data["image_url"], cached_file)
            elif "local_path" in asset_data:
                # 로컬 파일 복사
                shutil.copy2(asset_data["local_path"], cached_file)
            else:
                # 시뮬레이션: 더미 파일 생성
                cached_file.write_text(f"Cached asset: {cache_key}")

            # 메타데이터 저장
            self.metadata["assets"][cache_key] = {
                "filename": filename,
                "category": category,
                "original_prompt": prompt,
                "normalized_prompt": self._normalize_prompt(prompt),
                "created_at": datetime.now().isoformat(),
                "access_count": 1,
                "last_accessed": datetime.now().isoformat(),
                "file_size": cached_file.stat().st_size if cached_file.exists() else 0,
                "cost_saved": 0.0
            }

            self._save_metadata()

            self.logger.info(f"💾 에셋 캐시됨: {cache_key} -> {filename}")
            return str(cached_file)

        except Exception as e:
            self.logger.error(f"에셋 캐시 실패: {e}")
            return None

    def _download_and_save(self, url: str, file_path: Path):
        """URL에서 에셋 다운로드 및 저장"""
        # 실제 구현에서는 requests로 다운로드
        # 지금은 시뮬레이션
        file_path.write_text(f"Downloaded from: {url}")

    def get_cached_asset(self, cache_key: str, prompt: str, category: str) -> Tuple[Optional[str], bool]:
        """캐시된 에셋 가져오기"""

        self.stats["total_requests"] += 1

        # 캐시 검색
        cached_file = self.find_similar_asset(cache_key, prompt, category)

        if cached_file:
            # 캐시 히트
            self.stats["cache_hits"] += 1
            self.stats["total_saved_cost"] += 0.039  # Nano Banana 비용 절약

            # 접근 기록 업데이트
            if cache_key in self.metadata["assets"]:
                self.metadata["assets"][cache_key]["access_count"] += 1
                self.metadata["assets"][cache_key]["last_accessed"] = datetime.now().isoformat()
                self.metadata["assets"][cache_key]["cost_saved"] += 0.039

            self._save_metadata()
            self._save_stats()

            self.logger.info(f"🎯 캐시 히트! ${0.039:.3f} 절약")
            return cached_file, True
        else:
            # 캐시 미스
            self.stats["cache_misses"] += 1
            self._save_stats()

            self.logger.info(f"❌ 캐시 미스 - 새 에셋 생성 필요")
            return None, False

    def cleanup_cache(self, force: bool = False):
        """캐시 정리"""

        current_size = self._get_cache_size_mb()
        max_size = self.cache_config["max_cache_size_mb"]

        if not force and current_size < max_size * self.cache_config["cleanup_threshold"]:
            return  # 정리 불필요

        self.logger.info(f"🧹 캐시 정리 시작: {current_size:.1f}MB / {max_size}MB")

        # 정리 대상 선정 (오래되고 적게 사용된 것부터)
        assets_to_remove = []

        for cache_key, asset_info in self.metadata["assets"].items():
            cached_file = self.cache_dir / asset_info["filename"]

            # 만료된 파일
            if self._is_expired(asset_info):
                assets_to_remove.append((cache_key, cached_file, "expired"))
                continue

            # 파일이 실제로 존재하지 않음
            if not cached_file.exists():
                assets_to_remove.append((cache_key, cached_file, "missing"))
                continue

        # 오래된/적게 사용된 파일 (용량이 여전히 클 때)
        if current_size > max_size * 0.5:  # 50% 이상일 때 추가 정리
            sorted_assets = sorted(
                self.metadata["assets"].items(),
                key=lambda x: (x[1]["access_count"], x[1]["last_accessed"])
            )

            # 하위 30% 제거
            remove_count = max(1, len(sorted_assets) // 3)
            for i in range(remove_count):
                cache_key, asset_info = sorted_assets[i]
                cached_file = self.cache_dir / asset_info["filename"]
                assets_to_remove.append((cache_key, cached_file, "low_usage"))

        # 실제 파일 삭제
        removed_count = 0
        freed_space = 0

        for cache_key, cached_file, reason in assets_to_remove:
            try:
                if cached_file.exists():
                    file_size = cached_file.stat().st_size
                    cached_file.unlink()
                    freed_space += file_size

                del self.metadata["assets"][cache_key]
                removed_count += 1

            except Exception as e:
                self.logger.warning(f"파일 삭제 실패 {cached_file}: {e}")

        # 메타데이터 업데이트
        self.metadata["last_cleanup"] = datetime.now().isoformat()
        self._save_metadata()

        new_size = self._get_cache_size_mb()
        self.logger.info(f"✅ 캐시 정리 완료: {removed_count}개 파일, {freed_space/1024/1024:.1f}MB 확보")
        self.logger.info(f"📊 정리 후 크기: {new_size:.1f}MB / {max_size}MB")

    def _get_cache_size_mb(self) -> float:
        """캐시 디렉토리 크기 계산 (MB)"""
        total_size = 0

        for file_path in self.cache_dir.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size

        return total_size / 1024 / 1024

    def get_cache_stats(self) -> Dict:
        """캐시 통계 조회"""

        total_requests = self.stats["total_requests"]
        hit_rate = (self.stats["cache_hits"] / total_requests * 100) if total_requests > 0 else 0

        cache_size = self._get_cache_size_mb()
        asset_count = len(self.metadata["assets"])

        return {
            "cache_performance": {
                "total_requests": total_requests,
                "cache_hits": self.stats["cache_hits"],
                "cache_misses": self.stats["cache_misses"],
                "hit_rate": f"{hit_rate:.1f}%",
                "total_cost_saved": f"${self.stats['total_saved_cost']:.2f}"
            },
            "cache_storage": {
                "total_assets": asset_count,
                "cache_size_mb": f"{cache_size:.1f}MB",
                "max_size_mb": f"{self.cache_config['max_cache_size_mb']}MB",
                "usage_percentage": f"{(cache_size / self.cache_config['max_cache_size_mb'] * 100):.1f}%"
            },
            "cache_health": {
                "last_cleanup": self.metadata.get("last_cleanup", "Never"),
                "expired_assets": self._count_expired_assets(),
                "missing_files": self._count_missing_files()
            }
        }

    def _count_expired_assets(self) -> int:
        """만료된 에셋 수 계산"""
        count = 0
        for asset_info in self.metadata["assets"].values():
            if self._is_expired(asset_info):
                count += 1
        return count

    def _count_missing_files(self) -> int:
        """실제 파일이 없는 에셋 수 계산"""
        count = 0
        for asset_info in self.metadata["assets"].values():
            cached_file = self.cache_dir / asset_info["filename"]
            if not cached_file.exists():
                count += 1
        return count

    def generate_cache_report(self) -> str:
        """캐시 리포트 생성"""

        stats = self.get_cache_stats()

        report = f"""
💾 에셋 캐시 리포트
{'='*50}

📊 성능 통계:
  총 요청 수: {stats['cache_performance']['total_requests']}
  캐시 히트: {stats['cache_performance']['cache_hits']}
  캐시 미스: {stats['cache_performance']['cache_misses']}
  히트율: {stats['cache_performance']['hit_rate']}
  절약된 비용: {stats['cache_performance']['total_cost_saved']}

💽 저장소 현황:
  캐시된 에셋: {stats['cache_storage']['total_assets']}개
  사용 용량: {stats['cache_storage']['cache_size_mb']} / {stats['cache_storage']['max_size_mb']}
  사용률: {stats['cache_storage']['usage_percentage']}

🔧 캐시 상태:
  마지막 정리: {stats['cache_health']['last_cleanup']}
  만료된 에셋: {stats['cache_health']['expired_assets']}개
  누락된 파일: {stats['cache_health']['missing_files']}개

💡 예상 효과:
  월간 절약 (50% 히트율): $4.38
  연간 절약 (50% 히트율): $52.56
"""

        return report

def main():
    """테스트 실행"""

    # 캐시 매니저 초기화
    cache_manager = AssetCacheManager()

    print("💾 에셋 캐시 매니저 테스트")
    print("=" * 50)

    # 테스트 에셋들
    test_assets = [
        {
            "prompt": "Modern fitness app icon with blue gradient",
            "category": "app_icons",
            "style": {"color": "blue", "style": "modern"}
        },
        {
            "prompt": "Premium fitness application icon with clean blue design",
            "category": "app_icons",
            "style": {"color": "blue", "style": "clean"}
        },
        {
            "prompt": "Workout tracking app screenshot with dashboard",
            "category": "screenshots",
            "style": {"type": "dashboard", "theme": "light"}
        }
    ]

    # 캐시 테스트
    for i, asset in enumerate(test_assets):
        print(f"\n🧪 테스트 {i+1}: {asset['prompt'][:50]}...")

        # 캐시 키 생성
        cache_key = cache_manager.generate_cache_key(
            asset["prompt"],
            asset["category"],
            asset.get("style")
        )

        # 캐시에서 찾기
        cached_file, is_hit = cache_manager.get_cached_asset(
            cache_key,
            asset["prompt"],
            asset["category"]
        )

        if not is_hit:
            # 새 에셋 생성 시뮬레이션
            print(f"  🎨 새 에셋 생성 중...")

            fake_asset_data = {
                "image_url": f"https://fake-nano-banana.com/{cache_key}.png",
                "cost": 0.039
            }

            # 캐시에 저장
            cache_manager.cache_asset(
                fake_asset_data,
                cache_key,
                asset["prompt"],
                asset["category"]
            )

    # 최종 리포트
    print(cache_manager.generate_cache_report())

    # 캐시 정리 테스트
    print("\n🧹 캐시 정리 테스트...")
    cache_manager.cleanup_cache(force=True)

if __name__ == "__main__":
    main()