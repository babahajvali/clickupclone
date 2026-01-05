from task_management.exceptions.custom_exceptions import \
    TaskAssigneeNotFoundException
from task_management.interactors.dtos import TaskAssigneeDTO, \
    RemoveTaskAssigneeDTO, UserTasksDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
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
                 permission_storage: ListPermissionStorageInterface):
        self.task_storage = task_storage
        self.task_assignee_storage = task_assignee_storage
        self.user_storage = user_storage
        self.permission_storage = permission_storage

    def assign_task_assignee(self, task_id: str, user_id: str,
                             assigned_by) -> TaskAssigneeDTO:
        self.validate_user_exist_and_status(user_id=user_id,
                                            user_storage=self.user_storage)
        list_id = self.validate_task_exists(task_id=task_id,
                                            task_storage=self.task_storage)
        self.check_user_has_access_to_list_modification(user_id=user_id,
                                                        list_id=list_id,
                                                        permission_storage=self.permission_storage)

        return self.task_assignee_storage.assign_task_assignee(task_id=task_id,
                                                               assigned_by=assigned_by,
                                                               user_id=user_id)

    def remove_task_assignee(self, assign_id: str,
                             removed_by: str) -> RemoveTaskAssigneeDTO:
        self._check_task_assignee_exists(assign_id=assign_id)

        return self.task_assignee_storage.remove_task_assignee(
            assign_id=assign_id, removed_by=removed_by)

    def get_task_assignee(self, task_id: str) -> list[TaskAssigneeDTO]:
        self.validate_task_exists(task_id=task_id,
                                  task_storage=self.task_storage)

        return self.task_assignee_storage.get_task_assignee(task_id=task_id)

    def get_user_assigned_tasks(self, user_id: str) -> list[UserTasksDTO]:
        self.validate_user_exist_and_status(user_id=user_id,
                                            user_storage=self.user_storage)

        return self.task_assignee_storage.get_user_assigned_tasks(
            user_id=user_id)

    def _check_task_assignee_exists(self, assign_id: str):
        is_exist = self.task_assignee_storage.check_task_assignee_exist(
            assign_id=assign_id)

        if not is_exist:
            raise TaskAssigneeNotFoundException(assign_id=assign_id)
