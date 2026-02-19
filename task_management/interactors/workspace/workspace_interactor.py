from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    NothingToUpdateWorkspaceException, EmptyNameException, \
    InvalidWorkspaceIdsFoundException
from task_management.interactors.dtos import WorkspaceDTO, CreateWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, AccountStorageInterface, \
    UserStorageInterface
from task_management.mixins import AccountValidationMixin, \
    WorkspaceValidationMixin, UserValidationMixin


class WorkspaceInteractor(AccountValidationMixin, WorkspaceValidationMixin,
                          UserValidationMixin):
    """Workspace Management Business Logic Interactor.
    
    Handles all workspace-related operations including creation, updating, transferring,
    deletion, and retrieval of workspaces. This interactor enforces business
    rules and validates user permissions before performing any workspace operations.
    
    Key Responsibilities:
        - Create new workspaces with validation
        - Update existing workspace properties
        - Transfer workspace ownership between users
        - Delete workspaces with permission checks
        - Retrieve workspace information
        - Manage workspace member relationships
        - Validate workspace names and descriptions
    
    Dependencies:
        - WorkspaceStorageInterface: Workspace data persistence
        - AccountStorageInterface: Account validation and access
        - WorkspaceMemberStorageInterface: Member management operations
        - UserStorageInterface: User validation and information
    
    Attributes:
        workspace_storage (WorkspaceStorageInterface): Storage for workspace operations
        account_storage (AccountStorageInterface): Storage for account operations
        user_storage (UserStorageInterface): Storage for user operations
    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface):
        super().__init__(
            account_storage=account_storage,
            workspace_storage=workspace_storage, user_storage=user_storage)
        self.workspace_storage = workspace_storage
        self.account_storage = account_storage
        self.user_storage = user_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(self, workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:

        self.check_account_is_active(workspace_data.account_id)
        self.check_user_is_account_owner(
            workspace_data.user_id,
            account_id=workspace_data.account_id)
        self._validate_workspace_name_not_empty(
            workspace_name=workspace_data.name)

        return self.workspace_storage.create_workspace(
            workspace_data=workspace_data)

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(
            self, workspace_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> WorkspaceDTO:

        self.validate_workspace_is_active(workspace_id=workspace_id)
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)
        has_name_provided = name is not None
        has_description_provided = description is not None

        field_properties_to_update = {}
        if has_name_provided:
            self._validate_workspace_name_not_empty(workspace_name=name)
            field_properties_to_update['name'] = name
        if has_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateWorkspaceException(workspace_id=workspace_id)

        return self.workspace_storage.update_workspace(
            workspace_id=workspace_id, field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def delete_workspace(self, workspace_id: str,
                         user_id: str) -> WorkspaceDTO:

        self.validate_workspace_is_active(workspace_id=workspace_id)
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)

        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def transfer_workspace(self, workspace_id: str, user_id: str,
                           new_user_id: str) -> WorkspaceDTO:

        self.validate_workspace_is_active(workspace_id=workspace_id)
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)
        self.check_user_is_active(user_id=new_user_id)

        return self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)

    def get_workspaces(self, workspace_ids: list[str]) -> list[WorkspaceDTO]:

        self.check_workspace_ids(workspace_ids=workspace_ids)

        return self.workspace_storage.get_active_workspaces(
            workspace_ids=workspace_ids)

    def get_active_account_workspaces(self, account_id: str) -> list[
        WorkspaceDTO]:
        self.check_account_is_active(account_id=account_id)

        return self.workspace_storage.get_active_account_workspaces(
            account_id=account_id)

    @staticmethod
    def _validate_workspace_name_not_empty(workspace_name: str):
        is_name_empty = not workspace_name or not workspace_name.strip()

        if is_name_empty:
            raise EmptyNameException(name=workspace_name)

    def check_workspace_ids(self, workspace_ids: list[str]):

        workspaces_data = self.workspace_storage.get_workspaces(
            workspace_ids=workspace_ids)

        existed_workspace_ids = [obj.workspace_id for obj in workspaces_data]
        invalid_workspace_ids = [workspace_id for workspace_id in workspace_ids
                                 if workspace_id not in existed_workspace_ids]

        if invalid_workspace_ids:
            raise InvalidWorkspaceIdsFoundException(
                workspace_ids=invalid_workspace_ids)
