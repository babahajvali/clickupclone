from typing import List

from task_management.interactors.dtos import PlanDTO
from task_management.interactors.storage_interfaces.plan_storage_interface import (
    PlanStorageInterface,
)


class GetPlansInteractor:
    def __init__(self, plan_storage: PlanStorageInterface):
        self.plan_storage = plan_storage

    def get_all_plans(self) -> List[PlanDTO]:
        return self.plan_storage.get_all_plans()
