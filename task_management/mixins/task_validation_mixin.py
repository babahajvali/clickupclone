from task_management.exceptions.custom_exceptions import TaskNotFoundException, \
    DeletedTaskException
from task_management.interactors.storage_interfaces import TaskStorageInterface


class TaskValidationMixin:

    def __init__(self, task_storage: TaskStorageInterface, **kwargs):
        self.task_storage = task_storage
        super().__init__(**kwargs)

    def validate_task_is_active(self, task_id: str):
        task_data = self.task_storage.get_task_by_id(task_id=task_id)

        is_task_not_found = not task_data
        if is_task_not_found:
            raise TaskNotFoundException(task_id=task_id)

        is_task_deleted = task_data.is_deleted
        if is_task_deleted:
            raise DeletedTaskException(task_id=task_id)
