from typing import List, Optional

from task_management.exceptions.custom_exceptions import PlanNotFoundException
from task_management.interactors.dtos import PlanDTO
from task_management.interactors.storage_interfaces.plan_storage_interface import (
    PlanStorageInterface,
)
from task_management.models import Plan


class PlanStorage(PlanStorageInterface):
    def get_all_plans(self) -> List[PlanDTO]:
        plans = Plan.objects.filter(is_active=True).order_by("price",
                                                             "billing_period")
        return [self._convert_to_dto(plan) for plan in plans]

    def get_plan_by_id(self, plan_id: str) -> PlanDTO:
        try:
            plan = Plan.objects.get(plan_id=plan_id, is_active=True)
        except Plan.DoesNotExist as exc:
            raise PlanNotFoundException(plan_id=plan_id) from exc
        return self._convert_to_dto(plan)

    def get_plan_by_stripe_price_id(self, stripe_price_id: str) -> Optional[
        PlanDTO]:
        try:
            plan = Plan.objects.get(stripe_price_id=stripe_price_id,
                                    is_active=True)
        except Plan.DoesNotExist:
            return None
        return self._convert_to_dto(plan)

    @staticmethod
    def _convert_to_dto(plan: Plan) -> PlanDTO:
        return PlanDTO(
            plan_id=str(plan.plan_id),
            plan_name=plan.plan_name,
            stripe_price_id=plan.stripe_price_id,
            price=float(plan.price),
            currency=plan.currency,
            billing_period=plan.billing_period,
            features=plan.features,
            is_active=plan.is_active,
        )
