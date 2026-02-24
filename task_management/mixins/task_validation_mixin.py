from task_management.exceptions.custom_exceptions import TaskNotFound, \
    DeletedTaskFound
from task_management.interactors.storage_interfaces import TaskStorageInterface


class TaskValidationMixin:

    def __init__(self, task_storage: TaskStorageInterface):
        self.task_storage = task_storage

    def check_task_is_active(self, task_id: str):
        task_data = self.task_storage.get_task_by_id(task_id=task_id)

        is_task_not_found = not task_data
        if is_task_not_found:
            raise TaskNotFound(task_id=task_id)

        is_task_deleted = task_data.is_deleted
        if is_task_deleted:
            raise DeletedTaskFound(task_id=task_id)

    def check_task_exists(self, task_id: str):
        is_task_exists = self.task_storage.is_task_exist(task_id=task_id)

        is_task_not_found = not is_task_exists
        if is_task_not_found:
            raise TaskNotFound(task_id=task_id)
