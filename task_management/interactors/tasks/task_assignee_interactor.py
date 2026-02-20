from django.core.exceptions import ObjectDoesNotExist
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    TaskAssigneeNotFound, InActiveTaskAssigneeFound, \
    InactiveList, ListNotFound
from task_management.interactors.dtos import TaskAssigneeDTO, UserTasksDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, UserStorageInterface, \
    WorkspaceStorageInterface

from task_management.mixins import TaskValidationMixin, UserValidationMixin, \
    WorkspaceValidationMixin


class TaskAssigneeInteractor(TaskValidationMixin, UserValidationMixin,
                             WorkspaceValidationMixin):
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
                 user_storage: UserStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        super().__init__(task_storage=task_storage, user_storage=user_storage,
                         workspace_storage=workspace_storage)
        self.task_storage = task_storage
        self.user_storage = user_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def assign_task_assignee(self, task_id: str, user_id: str,
                             assigned_by: str) -> TaskAssigneeDTO:

        is_existed_assignee = self.task_storage.get_user_task_assignee(
            user_id=user_id, task_id=task_id, assigned_by=assigned_by)
        if is_existed_assignee:
            return self.task_storage.reassign_task_assignee(
                assign_id=is_existed_assignee.assign_id)

        self.validate_task_is_active(task_id=task_id)
        self.check_user_is_active(user_id=user_id)

        self._validate_user_access_for_list(task_id=task_id,
                                            user_id=assigned_by)

        return self.task_storage.assign_task_assignee(
            task_id=task_id, assigned_by=assigned_by, user_id=user_id)

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def remove_task_assignee(self, assign_id: str,
                             user_id: str) -> TaskAssigneeDTO:

        assignee_data = self._validate_task_assignee_exists(
            assign_id=assign_id)
        self._validate_user_access_for_list(task_id=assignee_data.task_id,
                                            user_id=user_id)

        return self.task_storage.remove_task_assignee(
            assign_id=assign_id)

    def get_task_assignees(self, task_id: str) -> list[TaskAssigneeDTO]:

        self.validate_task_is_active(task_id=task_id)

        return self.task_storage.get_task_assignees(task_id=task_id)

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:

        self.check_user_is_active(user_id=user_id)

        return self.task_storage.get_user_assigned_tasks(
            user_id=user_id)

    def _validate_task_assignee_exists(self, assign_id: str):

        try:
            assignee_data = self.task_storage.get_task_assignee(
                assign_id=assign_id)
        except ObjectDoesNotExist:
            raise TaskAssigneeNotFound(assign_id=assign_id)

        if not assignee_data.is_active:
            raise InActiveTaskAssigneeFound(assign_id=assign_id)

        return assignee_data

    def _validate_user_access_for_list(self, task_id: str, user_id: str):

        workspace_id = self.task_storage.get_workspace_id_from_task_id(
            task_id=task_id)

        self.check_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
