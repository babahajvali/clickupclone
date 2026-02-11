from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceDTO, CreateWorkspaceDTO, \
    AddMemberToWorkspaceDTO, UpdateWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, AccountStorageInterface, \
    WorkspaceMemberStorageInterface, UserStorageInterface
from task_management.mixins import AccountValidationMixin, \
    WorkspaceValidationMixin, UserValidationMixin
from task_management.mixins.workspace_member_validation_mixin import \
    WorkspaceMemberValidationMixin


class Workspace(AccountValidationMixin, WorkspaceValidationMixin,
                UserValidationMixin, WorkspaceMemberValidationMixin):
    """ Workspace Management
        Create , update, transfer , delete , get workspace
        storage's:
            1. workspace_storage
            2. account_storage
            3.workspace_member_storage
    """

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 account_storage: AccountStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 user_storage: UserStorageInterface, ):
        super().__init__(
            account_storage=account_storage,
            workspace_member_storage=workspace_member_storage,
            workspace_storage=workspace_storage, user_storage=user_storage)
        self.workspace_storage = workspace_storage
        self.account_storage = account_storage
        self.workspace_member_storage = workspace_member_storage
        self.user_storage = user_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(self, workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:

        self.validate_account_is_active(workspace_data.account_id)
        self.validate_user_is_account_owner(
            workspace_data.user_id,
            account_id=workspace_data.account_id)

        result = self.workspace_storage.create_workspace(
            workspace_data=workspace_data)

        create_workspace_member = AddMemberToWorkspaceDTO(
            workspace_id=result.workspace_id,
            user_id=workspace_data.user_id,
            role=Role.OWNER,
            added_by=workspace_data.user_id,
        )
        self.workspace_member_storage.add_member_to_workspace(
            create_workspace_member)

        return result

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(self, workspace_data: UpdateWorkspaceDTO,
                         user_id: str) -> WorkspaceDTO:
        self.validate_workspace_is_active(
            workspace_data.workspace_id)
        self.validate_user_access_for_workspace(
            user_id=user_id, workspace_id=workspace_data.workspace_id)

        return self.workspace_storage.update_workspace(
            workspace_data=workspace_data)

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
            user_id=user_id,workspace_id=workspace_id)
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
