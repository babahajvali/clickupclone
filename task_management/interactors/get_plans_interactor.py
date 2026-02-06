# task_management/interactors/get_plans_interactor.py

from typing import List
from task_management.interactors.dtos import PlanDTO
from task_management.interactors.storage_interface.plan_storage_interface import PlanStorageInterface


class GetPlansInteractor:

    def __init__(self, plan_storage: PlanStorageInterface):
        self.plan_storage = plan_storage

    def get_all_plans(self) -> List[PlanDTO]:
        """Get all available subscription plans"""
        return self.plan_storage.get_all_plans()