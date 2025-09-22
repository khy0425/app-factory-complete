#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Budget Guardian - 절대 예산 초과 방지 시스템
월 $30 예산을 절대로 넘지 않도록 보장
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

@dataclass
class BudgetConfig:
    """예산 설정"""
    monthly_total: float = 30.0
    midjourney_allocation: float = 20.0
    dalle_allocation: float = 10.0
    emergency_reserve: float = 2.0  # 긴급 상황용

@dataclass
class SpendingRecord:
    """지출 기록"""
    date: datetime
    service: str  # "midjourney" or "dalle"
    amount: float
    description: str
    transaction_id: str

class BudgetGuardian:
    """절대 예산 초과 방지 시스템"""

    def __init__(self, config_path: str = "budget_config.json"):
        self.config = BudgetConfig()
        self.config_path = Path(config_path)
        self.spending_log_path = Path("spending_log.json")
        self.lock_file_path = Path("budget.lock")

        # 가격 정보 (실시간 업데이트)
        self.pricing = {
            "dalle": {
                "1024x1024": 0.040,
                "1792x1024": 0.080
            },
            "midjourney": {
                "fast_generation": 0.15,  # 추정치
                "relax_generation": 0.05   # 추정치
            }
        }

        self.logger = self._setup_logging()
        self._load_config()

    def _setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [BUDGET-GUARDIAN] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('budget_guardian.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def _load_config(self):
        """설정 로드"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
                self.config = BudgetConfig(**config_data)
        else:
            self._save_config()

    def _save_config(self):
        """설정 저장"""
        with open(self.config_path, 'w') as f:
            json.dump(asdict(self.config), f, indent=2)

    def _get_current_month_spending(self) -> Dict[str, float]:
        """현재 월 지출 계산"""
        if not self.spending_log_path.exists():
            return {"midjourney": 0.0, "dalle": 0.0, "total": 0.0}

        with open(self.spending_log_path, 'r') as f:
            records = json.load(f)

        current_month = datetime.now().strftime("%Y-%m")
        monthly_spending = {"midjourney": 0.0, "dalle": 0.0}

        for record in records:
            record_date = datetime.fromisoformat(record["date"])
            if record_date.strftime("%Y-%m") == current_month:
                service = record["service"]
                monthly_spending[service] += record["amount"]

        monthly_spending["total"] = sum(monthly_spending.values())
        return monthly_spending

    def _log_spending(self, service: str, amount: float, description: str) -> str:
        """지출 기록"""
        import uuid
        transaction_id = str(uuid.uuid4())[:8]

        record = SpendingRecord(
            date=datetime.now(),
            service=service,
            amount=amount,
            description=description,
            transaction_id=transaction_id
        )

        # 기존 기록 로드
        records = []
        if self.spending_log_path.exists():
            with open(self.spending_log_path, 'r') as f:
                records = json.load(f)

        # 새 기록 추가
        record_dict = asdict(record)
        record_dict["date"] = record.date.isoformat()
        records.append(record_dict)

        # 저장
        with open(self.spending_log_path, 'w') as f:
            json.dump(records, f, indent=2)

        self.logger.info(f"💰 Spending logged: {service} ${amount:.3f} - {description}")
        return transaction_id

    async def check_budget_availability(self, service: str, estimated_cost: float) -> Tuple[bool, str]:
        """예산 사용 가능성 체크"""

        # 1. 예산 잠금 파일 체크 (동시 요청 방지)
        if self.lock_file_path.exists():
            return False, "Budget system locked by another process"

        # 2. 현재 월 지출 확인
        current_spending = self._get_current_month_spending()

        # 3. 서비스별 예산 한도 체크
        service_budget = getattr(self.config, f"{service}_allocation")
        service_spent = current_spending[service]
        service_remaining = service_budget - service_spent

        # 4. 전체 예산 한도 체크
        total_spent = current_spending["total"]
        total_remaining = self.config.monthly_total - total_spent

        # 5. 긴급 예비비 보호
        protected_budget = self.config.monthly_total - self.config.emergency_reserve
        if total_spent + estimated_cost > protected_budget:
            return False, f"Would exceed protected budget (${protected_budget:.2f})"

        # 6. 서비스별 예산 체크
        if service_spent + estimated_cost > service_budget:
            return False, f"{service} budget exhausted (${service_remaining:.2f} remaining)"

        # 7. 전체 예산 체크
        if total_spent + estimated_cost > self.config.monthly_total:
            return False, f"Total budget exhausted (${total_remaining:.2f} remaining)"

        # 8. 모든 체크 통과
        return True, f"Budget OK - {service}: ${service_remaining:.2f}, Total: ${total_remaining:.2f}"

    async def reserve_budget(self, service: str, estimated_cost: float, description: str) -> Optional[str]:
        """예산 예약 (실제 사용 전 선점)"""

        # 예산 잠금
        with open(self.lock_file_path, 'w') as f:
            f.write(f"{datetime.now().isoformat()}\n{service}\n{estimated_cost}")

        try:
            # 예산 체크
            can_spend, message = await self.check_budget_availability(service, estimated_cost)

            if not can_spend:
                self.logger.error(f"❌ Budget reservation failed: {message}")
                return None

            # 예산 예약 성공
            transaction_id = self._log_spending(service, estimated_cost, f"RESERVED: {description}")
            self.logger.info(f"✅ Budget reserved: {service} ${estimated_cost:.3f}")

            return transaction_id

        finally:
            # 예산 잠금 해제
            if self.lock_file_path.exists():
                self.lock_file_path.unlink()

    async def confirm_spending(self, transaction_id: str, actual_cost: float):
        """실제 지출 확정 (예약과 차이 조정)"""

        # 기존 기록에서 예약 찾기
        with open(self.spending_log_path, 'r') as f:
            records = json.load(f)

        for record in records:
            if record["transaction_id"] == transaction_id:
                # 예약 금액과 실제 금액 차이 조정
                difference = actual_cost - record["amount"]
                record["amount"] = actual_cost
                record["description"] = record["description"].replace("RESERVED:", "CONFIRMED:")

                if difference != 0:
                    self.logger.info(f"💱 Cost adjusted: ${difference:+.3f} for {transaction_id}")

                break

        # 업데이트된 기록 저장
        with open(self.spending_log_path, 'w') as f:
            json.dump(records, f, indent=2)

    async def cancel_reservation(self, transaction_id: str):
        """예산 예약 취소"""

        # 기존 기록에서 예약 제거
        with open(self.spending_log_path, 'r') as f:
            records = json.load(f)

        records = [r for r in records if r["transaction_id"] != transaction_id]

        with open(self.spending_log_path, 'w') as f:
            json.dump(records, f, indent=2)

        self.logger.info(f"🔄 Budget reservation cancelled: {transaction_id}")

    def get_budget_status(self) -> Dict:
        """현재 예산 상태 조회"""
        current_spending = self._get_current_month_spending()

        status = {
            "monthly_budget": self.config.monthly_total,
            "emergency_reserve": self.config.emergency_reserve,
            "spending": current_spending,
            "remaining": {
                "midjourney": self.config.midjourney_allocation - current_spending["midjourney"],
                "dalle": self.config.dalle_allocation - current_spending["dalle"],
                "total": self.config.monthly_total - current_spending["total"]
            },
            "utilization": {
                "midjourney": (current_spending["midjourney"] / self.config.midjourney_allocation) * 100,
                "dalle": (current_spending["dalle"] / self.config.dalle_allocation) * 100,
                "total": (current_spending["total"] / self.config.monthly_total) * 100
            }
        }

        return status

    def estimate_generation_cost(self, service: str, generation_type: str, quantity: int = 1) -> float:
        """생성 비용 추정"""
        if service == "dalle":
            cost_per_unit = self.pricing["dalle"].get(generation_type, 0.040)
        elif service == "midjourney":
            cost_per_unit = self.pricing["midjourney"].get(generation_type, 0.15)
        else:
            raise ValueError(f"Unknown service: {service}")

        return cost_per_unit * quantity

    async def safe_generate_asset(self, service: str, generation_type: str, prompt: str, **kwargs):
        """안전한 에셋 생성 (예산 보호)"""

        # 1. 비용 추정
        estimated_cost = self.estimate_generation_cost(service, generation_type)

        # 2. 예산 예약
        transaction_id = await self.reserve_budget(
            service,
            estimated_cost,
            f"{generation_type} generation: {prompt[:50]}..."
        )

        if not transaction_id:
            raise Exception("Budget exhausted - cannot generate asset")

        try:
            # 3. 실제 생성 (여기서 외부 API 호출)
            if service == "dalle":
                result = await self._call_dalle_api(generation_type, prompt, **kwargs)
            elif service == "midjourney":
                result = await self._call_midjourney_api(generation_type, prompt, **kwargs)
            else:
                raise ValueError(f"Unknown service: {service}")

            # 4. 실제 비용 확정
            actual_cost = result.get("cost", estimated_cost)
            await self.confirm_spending(transaction_id, actual_cost)

            return result

        except Exception as e:
            # 5. 실패시 예약 취소
            await self.cancel_reservation(transaction_id)
            raise e

    async def _call_dalle_api(self, generation_type: str, prompt: str, **kwargs):
        """DALL-E API 호출 (구현 필요)"""
        # 실제 DALL-E API 연동 코드
        await asyncio.sleep(1)  # 시뮬레이션
        return {
            "image_url": "https://example.com/generated_image.jpg",
            "cost": self.pricing["dalle"][generation_type]
        }

    async def _call_midjourney_api(self, generation_type: str, prompt: str, **kwargs):
        """미드저니 API 호출 (구현 필요)"""
        # 실제 미드저니 API 연동 코드
        await asyncio.sleep(2)  # 시뮬레이션
        return {
            "image_url": "https://example.com/midjourney_image.jpg",
            "cost": self.pricing["midjourney"][generation_type]
        }

    def reset_monthly_budget(self):
        """월 예산 리셋 (새 달 시작시)"""
        current_month = datetime.now().strftime("%Y-%m")

        # 백업 파일 생성
        backup_path = f"spending_log_backup_{current_month}.json"
        if self.spending_log_path.exists():
            import shutil
            shutil.copy2(self.spending_log_path, backup_path)

        # 새로운 로그 파일 생성
        with open(self.spending_log_path, 'w') as f:
            json.dump([], f)

        self.logger.info(f"🔄 Monthly budget reset for {current_month}")

# 사용 예시 및 테스트
async def main():
    """테스트 및 사용 예시"""
    guardian = BudgetGuardian()

    # 현재 예산 상태 확인
    status = guardian.get_budget_status()
    print(f"💰 Budget Status:")
    print(f"  Total: ${status['spending']['total']:.2f} / ${status['monthly_budget']:.2f}")
    print(f"  Midjourney: ${status['spending']['midjourney']:.2f} / ${status['remaining']['midjourney']:.2f}")
    print(f"  DALL-E: ${status['spending']['dalle']:.2f} / ${status['remaining']['dalle']:.2f}")

    # 안전한 에셋 생성 테스트
    try:
        result = await guardian.safe_generate_asset(
            service="midjourney",
            generation_type="fast_generation",
            prompt="Modern fitness app icon, minimalist design"
        )
        print(f"✅ Asset generated: {result['image_url']}")

    except Exception as e:
        print(f"❌ Generation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())