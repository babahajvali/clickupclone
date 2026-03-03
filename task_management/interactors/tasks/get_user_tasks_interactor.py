from task_management.interactors.dtos import UserTasksDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, UserStorageInterface

from task_management.mixins import UserValidationMixin


class GetUserTasksInteractor:
    """Get Task Assignees Interactor.
    
    Handles retrieving assignment information. This interactor
    get the user tasks.
    
    Key Responsibilities:
        - Get all tasks assigned to specific users

    Dependencies:
        - TaskStorageInterface: Task validation and access control
        - UserStorageInterface: User validation and information
    
    Attributes:
        task_storage (TaskStorageInterface): Storage for tasks operations
        user_storage (UserStorageInterface): Storage for user operations
    """

    def __init__(
            self, task_storage: TaskStorageInterface,
            user_storage: UserStorageInterface):
        self.task_storage = task_storage
        self.user_storage = user_storage

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        self.user_mixin.check_user_is_active(user_id=user_id)

        return self.task_storage.get_user_assigned_tasks(user_id=user_id)
