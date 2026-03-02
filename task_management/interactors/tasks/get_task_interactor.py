from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import TaskStorageInterface
from task_management.mixins import TaskValidationMixin


class GetTaskInteractor:

    def __init__(self, task_storage: TaskStorageInterface):
        self.task_storage = task_storage

    @property
    def task_mixin(self) -> TaskValidationMixin:
        return TaskValidationMixin(task_storage=self.task_storage)

    def get_task(self, task_id: str) -> TaskDTO:
        self.task_mixin.validate_task_exists(task_id=task_id)

        return self.task_storage.get_task(task_id=task_id)
