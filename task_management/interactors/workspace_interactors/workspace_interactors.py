from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO, \
    UpdateWorkspaceDTO, AddMemberToWorkspaceDTO
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.interactors.workspace_interactors.workspace_transfer_service import \
    WorkspaceTransferService


class WorkspaceInteractor(ValidationMixin):
    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 account_storage: AccountStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.account_storage = account_storage
        self.workspace_member_storage = workspace_member_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(self, create_workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:
        self.validate_account_is_active(create_workspace_data.account_id,
                                        account_storage=self.account_storage)
        self.validate_user_is_account_owner(
            create_workspace_data.user_id,
            account_id=create_workspace_data.account_id,
            account_storage=self.account_storage)

        result = self.workspace_storage.create_workspace(
            workspace_data=create_workspace_data)

        create_workspace_member = AddMemberToWorkspaceDTO(
            workspace_id=result.workspace_id,
            user_id=create_workspace_data.user_id,
            role=Role.OWNER,
            added_by=create_workspace_data.user_id,
        )
        self.workspace_member_storage.add_member_to_workspace(
            create_workspace_member)

        return result

    @invalidate_interactor_cache(cache_name="workspace_users")
    def update_workspace(self, update_workspace_data: UpdateWorkspaceDTO,
                         user_id: str) -> WorkspaceDTO:
        self.validate_workspace_is_active(
            update_workspace_data.workspace_id,
            workspace_storage=self.workspace_storage)
        self.validate_user_access_for_workspace(
            user_id=user_id, workspace_id=update_workspace_data.workspace_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.workspace_storage.update_workspace(
            workspace_data=update_workspace_data)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def delete_workspace(self, workspace_id: str,
                         user_id: str) -> WorkspaceDTO:
        self.validate_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id,
            workspace_storage=self.workspace_storage)
        self.validate_workspace_is_active(
            workspace_id, workspace_storage=self.workspace_storage)
        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def transfer_workspace(self, workspace_id: str, user_id: str,
                           new_user_id: str) -> WorkspaceDTO:
        self.validate_user_is_workspace_owner(user_id=user_id,
                                              workspace_id=workspace_id,
                                              workspace_storage=self.workspace_storage)
        self.validate_user_is_active(user_id=new_user_id,
                                     user_storage=self.user_storage)
        result = self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)

        WorkspaceTransferService.change_permissions_for_user_in_transfer(
                workspace_id=workspace_id, user_id=user_id,
                new_user_id=new_user_id)

        return result

    def get_workspace(self, workspace_id: str) -> WorkspaceDTO:
        self.validate_workspace_is_active(workspace_id,
                                          workspace_storage=self.workspace_storage)

        return self.workspace_storage.get_workspace(workspace_id=workspace_id)

    def account_workspaces(self, account_id: str) -> list[WorkspaceDTO]:
        self.validate_account_is_active(account_id,
                                        account_storage=self.account_storage)

        return self.workspace_storage.get_workspaces_by_account(
            account_id=account_id)
