from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import WorkspaceDTO, CreateWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, AccountStorageInterface, \
    UserStorageInterface
from task_management.interactors.workspaces.validators.workspace_validator import \
    WorkspaceValidator
from task_management.mixins import AccountValidationMixin, \
    WorkspaceValidationMixin, UserValidationMixin


class WorkspaceInteractor:
    """Workspace Management Business Logic Interactor.
    
    Handles all workspaces-related operations including creation, updating, transferring,
    deletion, and retrieval of workspaces. This interactor enforces business
    rules and validates user permissions before performing any workspaces operations.
    
    Key Responsibilities:
        - Create new workspaces with validation
        - Update existing workspaces properties
        - Transfer workspaces ownership between users
        - Delete workspaces with permission checks
        - Retrieve workspaces information
        - Manage workspaces member relationships
        - Validate workspaces names and descriptions
    
    Dependencies:
        - WorkspaceStorageInterface: Workspace data persistence
        - AccountStorageInterface: Account validation and access
        - WorkspaceMemberStorageInterface: Member management operations
        - UserStorageInterface: User validation and information
    
    Attributes:
        workspace_storage (WorkspaceStorageInterface): Storage for workspaces operations
        account_storage (AccountStorageInterface): Storage for accounts operations
        user_storage (UserStorageInterface): Storage for user operations
    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface):
        self.workspace_storage = workspace_storage
        self.account_storage = account_storage
        self.user_storage = user_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def account_mixin(self) -> AccountValidationMixin:
        return AccountValidationMixin(account_storage=self.account_storage)

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    @property
    def workspace_validator(self) -> WorkspaceValidator:
        return WorkspaceValidator(workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(self, workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:

        self.account_mixin.check_account_is_active(workspace_data.account_id)
        self.account_mixin.check_user_is_account_owner(
            workspace_data.user_id,
            account_id=workspace_data.account_id)
        self.workspace_validator.check_workspace_name_not_empty(
            workspace_name=workspace_data.name)

        return self.workspace_storage.create_workspace(
            workspace_data=workspace_data)

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(
            self, workspace_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> WorkspaceDTO:

        self.workspace_mixin.check_workspace_is_active(
            workspace_id=workspace_id)
        field_properties_to_update = (
            self.workspace_validator.check_workspace_update_field_properties(
            workspace_id=workspace_id, name=name, description=description))

        self.workspace_mixin.check_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)

        return self.workspace_storage.update_workspace(
            workspace_id=workspace_id,
            field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def delete_workspace(
            self, workspace_id: str, user_id: str) -> WorkspaceDTO:

        self.workspace_mixin.check_workspace_is_active(
            workspace_id=workspace_id)
        self.workspace_mixin.check_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)

        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def transfer_workspace(
            self, workspace_id: str, user_id: str, new_user_id: str) \
            -> WorkspaceDTO:

        self.workspace_mixin.check_workspace_is_active(
            workspace_id=workspace_id)
        self.workspace_mixin.check_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)
        self.user_mixin.check_user_is_active(user_id=new_user_id)

        return self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)

    def get_active_workspaces(
            self, workspace_ids: list[str]) -> list[WorkspaceDTO]:

        self.workspace_validator.check_workspace_ids(
            workspace_ids=workspace_ids)

        return self.workspace_storage.get_active_workspaces(
            workspace_ids=workspace_ids)

    def get_active_account_workspaces(
            self, account_id: str) -> list[WorkspaceDTO]:

        self.account_mixin.check_account_is_active(account_id=account_id)

        return self.workspace_storage.get_active_account_workspaces(
            account_id=account_id)
