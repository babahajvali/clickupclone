from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    NothingToUpdateWorkspaceException, EmptyNameException
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceDTO, CreateWorkspaceDTO, \
    AddMemberToWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, AccountStorageInterface, \
     UserStorageInterface
from task_management.mixins import AccountValidationMixin, \
    WorkspaceValidationMixin, UserValidationMixin



class Workspace(AccountValidationMixin, WorkspaceValidationMixin,
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
                 user_storage: UserStorageInterface, ):
        super().__init__(
            account_storage=account_storage,
            workspace_storage=workspace_storage, user_storage=user_storage)
        self.workspace_storage = workspace_storage
        self.account_storage = account_storage
        self.user_storage = user_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(self, workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:

        self.validate_account_is_active(workspace_data.account_id)
        self.validate_user_is_account_owner(
            workspace_data.user_id,
            account_id=workspace_data.account_id)
        self._validate_workspace_name_not_empty(
            workspace_name=workspace_data.name)

        result = self.workspace_storage.create_workspace(
            workspace_data=workspace_data)

        create_workspace_member = AddMemberToWorkspaceDTO(
            workspace_id=result.workspace_id, user_id=workspace_data.user_id,
            role=Role.OWNER, added_by=workspace_data.user_id,
        )
        self.workspace_storage.add_member_to_workspace(
            create_workspace_member)

        return result

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(self, workspace_id: str, name: Optional[str],
                         description: Optional[str],
                         user_id: str) -> WorkspaceDTO:
        self.validate_workspace_is_active(workspace_id=workspace_id)
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)
        has_name_provided = name is not None
        has_description_provided = description is not None

        fields_to_update = {}
        if has_name_provided:
            fields_to_update['name'] = name
        if has_description_provided:
            fields_to_update['description'] = description

        if not fields_to_update:
            raise NothingToUpdateWorkspaceException(workspace_id=workspace_id)

        return self.workspace_storage.update_workspace(
            workspace_id=workspace_id, update_fields=fields_to_update)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def delete_workspace(self, workspace_id: str,
                         user_id: str) -> WorkspaceDTO:
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)
        self.validate_workspace_is_active(workspace_id=workspace_id)
        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def transfer_workspace(self, workspace_id: str, user_id: str,
                           new_user_id: str) -> WorkspaceDTO:
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id)
        self.validate_user_is_active(user_id=new_user_id)
        result = self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)

        return result

    def get_workspace(self, workspace_id: str) -> WorkspaceDTO:
        self.validate_workspace_is_active(workspace_id=workspace_id)

        return self.workspace_storage.get_workspace(workspace_id=workspace_id)

    def account_workspaces(self, account_id: str) -> list[WorkspaceDTO]:
        self.validate_account_is_active(account_id=account_id)

        return self.workspace_storage.get_workspaces_by_account(
            account_id=account_id)

    @staticmethod
    def _validate_workspace_name_not_empty(workspace_name: str):
        if not workspace_name or not workspace_name.strip():
            raise EmptyNameException(name=workspace_name)
