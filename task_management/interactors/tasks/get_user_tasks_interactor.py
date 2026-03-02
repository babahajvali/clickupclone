from task_management.interactors.dtos import UserTasksDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, UserStorageInterface

from task_management.mixins import UserValidationMixin


class GetUserTasksInteractor:
    """Task Assignee Management Business Logic Interactor.
    
    Handles all tasks assignment operations including assigning users to tasks,
    removing assignments, and retrieving assignment information. This interactor
    enforces business rules and validates user permissions before performing
    any tasks assignment operations.
    
    Key Responsibilities:
        - Assign users to tasks with validation
        - Remove tasks assignments with permission checks
        - Retrieve tasks assignee information
        - Get all assignees for specific tasks
        - Get all assignees for lists
        - Get all tasks assigned to specific users
        - Handle tasks reassignment scenarios
    
    Dependencies:
        - TaskStorageInterface: Task validation and access control
        - TaskAssigneeStorageInterface: Assignment data persistence
        - UserStorageInterface: User validation and information
        - WorkspaceMemberStorageInterface: Workspace permission validation
        - ListStorageInterface: List access validation
        - SpaceStorageInterface: Space access validation
    
    Attributes:
        task_storage (TaskStorageInterface): Storage for tasks operations
        task_storage (TaskAssigneeStorageInterface): Storage for assignment operations
        user_storage (UserStorageInterface): Storage for user operations
    """

    def __init__(self, task_storage: TaskStorageInterface,
                 user_storage: UserStorageInterface):
        self.task_storage = task_storage
        self.user_storage = user_storage

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        self.user_mixin.check_user_is_active(user_id=user_id)

        return self.task_storage.get_user_assigned_tasks(user_id=user_id)
