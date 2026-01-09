from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO, \
    UpdateWorkspaceDTO
from task_management.interactors.storage_interface.account_member_storage_interface import \
    AccountMemberStorageInterface
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class WorkspaceInteractor(ValidationMixin):
    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 account_storage: AccountStorageInterface,
                 account_member_storage: AccountMemberStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.account_storage = account_storage
        self.account_member_storage = account_member_storage
        self.workspace_member_storage = workspace_member_storage

    def create_workspace(self, create_workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:
        self.validate_user_is_active(create_workspace_data.user_id,
                                     user_storage=self.user_storage)
        self.validate_account_is_active(create_workspace_data.account_id,
                                        account_storage=self.account_storage)
        self.validate_user_access_for_account(
            create_workspace_data.user_id,
            account_id=create_workspace_data.account_id,
            account_member_storage=self.account_member_storage)

        return self.workspace_storage.create_workspace(
            workspace_data=create_workspace_data)

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

    def delete_workspace(self, workspace_id: str,
                         user_id: str) -> WorkspaceDTO:
        self.validate_user_access_for_workspace(
            user_id=user_id, workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)
        self.validate_workspace_is_active(
            workspace_id, workspace_storage=self.workspace_storage)
        return self.workspace_storage.delete_workspace(
            workspace_id=workspace_id)

    def transfer_workspace(self, workspace_id: str, user_id: str,
                           new_user_id: str) -> WorkspaceDTO:
        self.validate_user_is_workspace_owner(user_id=user_id,
                                              workspace_id=workspace_id,
                                              workspace_storage=self.workspace_storage)
        self.validate_user_is_active(user_id=new_user_id,
                                     user_storage=self.user_storage)

        return self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)
