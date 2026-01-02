from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    UpdateTaskDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class CreateTaskInteractor(ValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 permission_storage: ListPermissionStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.permission_storage = permission_storage

    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        self.check_list_exists_and_status(list_id=task_data.list_id,
                                          list_storage=self.list_storage)
        self.check_user_has_access_to_list_modification(
            user_id=task_data.created_by, list_id=task_data.list_id,
            permission_storage=self.permission_storage)

        return self.task_storage.create_task(task_data=task_data)

    def update_task(self, update_task_data: UpdateTaskDTO) -> TaskDTO:
        self.validate_task_exists(task_id=update_task_data.task_id,
                                  task_storage=self.task_storage)
        self.check_list_exists_and_status(list_id=update_task_data.list_id,
                                          list_storage=self.list_storage)
        self.check_user_has_access_to_list_modification(
            user_id=update_task_data.created_by,
            list_id=update_task_data.list_id,
            permission_storage=self.permission_storage)

        return self.task_storage.update_task(update_task_data=update_task_data)

    def get_list_tasks(self, list_id: str) -> list[TaskDTO]:
        self.check_list_exists_and_status(list_id=list_id,
                                          list_storage=self.list_storage)

        return self.task_storage.get_list_tasks(list_id=list_id)

    def get_task(self, task_id: str) -> TaskDTO:
        self.validate_task_exists(task_id=task_id,
                                  task_storage=self.task_storage)

        return self.task_storage.get_task_by_id(task_id=task_id)
