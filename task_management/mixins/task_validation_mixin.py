from task_management.exceptions.custom_exceptions import TaskNotFound, \
    DeletedTaskFound, EmptyTaskTitle
from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import TaskStorageInterface


class TaskValidationMixin:

    def __init__(self, task_storage: TaskStorageInterface):
        self.task_storage = task_storage

    def check_task_not_deleted(self, task_id: str):
        task_data = self.check_task_exists(task_id=task_id)

        is_task_deleted = task_data.is_deleted
        if is_task_deleted:
            raise DeletedTaskFound(task_id=task_id)

    def check_task_exists(self, task_id: str) -> TaskDTO:
        task_data = self.task_storage.get_task(task_id=task_id)

        is_task_not_found = not task_data
        if is_task_not_found:
            raise TaskNotFound(task_id=task_id)

        return task_data

    @staticmethod
    def check_task_title_not_empty(title: str):
        is_title_empty = not title or not title.strip()
        if is_title_empty:
            raise EmptyTaskTitle(title=title)
