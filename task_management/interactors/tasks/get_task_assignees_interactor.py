from typing import List

from task_management.interactors.dtos import TaskAssigneeDTO
from task_management.interactors.storage_interfaces import TaskStorageInterface
from task_management.mixins import TaskValidationMixin


class GetTaskAssigneesInteractor(TaskValidationMixin):

    def __init__(self, task_storage: TaskStorageInterface):
        super().__init__(task_storage=task_storage)
        self.task_storage = task_storage

    def get_task_assignees(self, task_id: str) -> List[TaskAssigneeDTO]:
        self.check_task_not_deleted(task_id=task_id)

        return self.task_storage.get_task_assignees(task_id=task_id)
