from task_management.interactors.dtos import UpdateTaskDTO, TaskDTO
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class UpdateTaskInteractor(ValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 permission_storage: PermissionStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.permission_storage = permission_storage

    def update_task(self, update_task_data: UpdateTaskDTO)->TaskDTO:
        self.validate_task_exists(task_id=update_task_data.task_id,task_storage=self.task_storage)
        self.check_list_exists(list_id=update_task_data.list_id,
                               list_storage=self.list_storage)
        self.check_user_has_access_to_create_task(user_id=update_task_data.created_by,
                                                  permission_storage=self.permission_storage)


        return self.task_storage.update_task(update_task_data=update_task_data)

