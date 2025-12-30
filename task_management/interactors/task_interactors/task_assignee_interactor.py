from task_management.interactors.dtos import TaskAssigneeDTO, \
    RemoveTaskAssigneeDTO
from task_management.interactors.storage_interface.permission_storage_interface import \
    PermissionStorageInterface
from task_management.interactors.storage_interface.task_assignee_storage_interface import \
    TaskAssigneeStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class TaskAssigneeInteractor(ValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 task_assignee_storage: TaskAssigneeStorageInterface,
                 user_storage: UserStorageInterface,
                 permission_storage: PermissionStorageInterface):
        self.task_storage = task_storage
        self.task_assignee_storage = task_assignee_storage
        self.user_storage = user_storage
        self.permission_storage = permission_storage

    def assign_task_assignee(self, task_id: str, user_id: str,assigned_by) -> TaskAssigneeDTO:
        self.check_user_exist(user_id=user_id,user_storage=self.user_storage)
        self.validate_task_exists(task_id=task_id,task_storage=self.task_storage)
        self.check_user_has_access_to_create_task(user_id=user_id,permission_storage=self.permission_storage)

        return self.task_assignee_storage.assign_task_assignee(task_id=task_id,assigned_by=assigned_by,user_id=user_id)

    def remove_task_assignee(self, assign_id:str, removed_by: str) -> RemoveTaskAssigneeDTO:
        self.check_task_assignee_exists(assign_id=assign_id,task_assignee_storage=self.task_assignee_storage)
        self.check_user_has_access_to_create_task(user_id=removed_by,
                                                  permission_storage=self.permission_storage)

        return self.task_assignee_storage.remove_task_assignee(assign_id=assign_id, removed_by=removed_by)