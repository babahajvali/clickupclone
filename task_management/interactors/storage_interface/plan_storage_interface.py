# task_management/interactors/storage_interface/plan_storage_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from task_management.interactors.dtos import PlanDTO


class PlanStorageInterface(ABC):

    @abstractmethod
    def get_all_plans(self) -> List[PlanDTO]:
        pass

    @abstractmethod
    def get_plan_by_id(self, plan_id: str) -> PlanDTO:
        pass

    @abstractmethod
    def get_plan_by_stripe_price_id(self, stripe_price_id: str) -> Optional[PlanDTO]:
        pass