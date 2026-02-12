from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    TaskAssigneeNotFoundException, InActiveTaskAssigneeFoundException
from task_management.interactors.dtos import TaskAssigneeDTO, UserTasksDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, TaskAssigneeStorageInterface, UserStorageInterface, \
    WorkspaceStorageInterface, ListStorageInterface, \
    SpaceStorageInterface

from task_management.mixins import TaskValidationMixin, UserValidationMixin, \
    WorkspaceValidationMixin, ListValidationMixin


class TaskAssigneeInteractor(TaskValidationMixin, UserValidationMixin,
                             WorkspaceValidationMixin,ListValidationMixin):
    """Task Assignee Management Business Logic Interactor.
    
    Handles all task assignment operations including assigning users to tasks,
    removing assignments, and retrieving assignment information. This interactor
    enforces business rules and validates user permissions before performing
    any task assignment operations.
    
    Key Responsibilities:
        - Assign users to tasks with validation
        - Remove task assignments with permission checks
        - Retrieve task assignee information
        - Get all assignees for specific tasks
        - Get all assignees for lists
        - Get all tasks assigned to specific users
        - Handle task reassignment scenarios
    
    Dependencies:
        - TaskStorageInterface: Task validation and access control
        - TaskAssigneeStorageInterface: Assignment data persistence
        - UserStorageInterface: User validation and information
        - WorkspaceMemberStorageInterface: Workspace permission validation
        - ListStorageInterface: List access validation
        - SpaceStorageInterface: Space access validation
    
    Attributes:
        task_storage (TaskStorageInterface): Storage for task operations
        task_assignee_storage (TaskAssigneeStorageInterface): Storage for assignment operations
        user_storage (UserStorageInterface): Storage for user operations
        workspace_member_storage (WorkspaceMemberStorageInterface): Storage for member validation
        list_storage (ListStorageInterface): Storage for list operations
        space_storage (SpaceStorageInterface): Storage for space operations
    """
    def __init__(self, task_storage: TaskStorageInterface,
                 task_assignee_storage: TaskAssigneeStorageInterface,
                 user_storage: UserStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 list_storage: ListStorageInterface,
                 space_storage: SpaceStorageInterface):
        super().__init__(task_storage=task_storage, user_storage=user_storage,
                         workspace_storage=workspace_storage,
                         list_storage=list_storage)
        self.task_storage = task_storage
        self.task_assignee_storage = task_assignee_storage
        self.user_storage = user_storage
        self.workspace_storage = workspace_storage
        self.list_storage = list_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def assign_task_assignee(self, task_id: str, user_id: str,
                             assigned_by: str) -> TaskAssigneeDTO:
        existing_assignee = self.task_assignee_storage.get_user_task_assignee(
            user_id=user_id, task_id=task_id, assigned_by=assigned_by)
        if existing_assignee:
            return self.task_assignee_storage.reassign_task_assignee(
                assign_id=existing_assignee.assign_id)

        self.validate_task_is_active(task_id=task_id)
        self.validate_user_is_active(user_id=user_id)

        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        self._validate_user_access_for_list(list_id=list_id, user_id=user_id)

        return self.task_assignee_storage.assign_task_assignee(
            task_id=task_id, assigned_by=assigned_by, user_id=user_id)

    @invalidate_interactor_cache(cache_name="list_task_assignees")
    def remove_task_assignee(self, assign_id: str,
                             user_id: str) -> TaskAssigneeDTO:
        assignee_data = self._validate_task_assignee_exists(
            assign_id=assign_id)
        list_id = self.task_storage.get_task_list_id(
            task_id=assignee_data.task_id)
        self._validate_user_access_for_list(list_id=list_id, user_id=user_id)

        return self.task_assignee_storage.remove_task_assignee(
            assign_id=assign_id)

    def get_task_assignees(self, task_id: str) -> list[TaskAssigneeDTO]:
        self.validate_task_is_active(task_id=task_id)

        return self.task_assignee_storage.get_task_assignees(task_id=task_id)

    @interactor_cache(timeout=30 * 60, cache_name="list_task_assignees")
    def get_list_task_assignees(self, list_id: str) -> list[TaskAssigneeDTO]:
        self.validate_list_is_active(list_id=list_id)

        return self.task_assignee_storage.get_list_task_assignees(
            list_id=list_id)

    def get_user_assigned_tasks(self, user_id: str) -> UserTasksDTO:
        self.validate_user_is_active(user_id=user_id)

        return self.task_assignee_storage.get_user_assigned_tasks(
            user_id=user_id)

    def _validate_task_assignee_exists(self, assign_id: str):
        assignee_data = self.task_assignee_storage.get_task_assignee(
            assign_id=assign_id)

        if not assignee_data:
            raise TaskAssigneeNotFoundException(assign_id=assign_id)

        if not assignee_data.is_active:
            raise InActiveTaskAssigneeFoundException(assign_id=assign_id)

        return assignee_data

    def _validate_user_access_for_list(self, list_id: str, user_id: str):

        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
