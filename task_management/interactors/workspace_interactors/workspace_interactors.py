from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO, \
    UpdateWorkspaceDTO, AddMemberToWorkspaceDTO

from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.interactors.workspace_interactors.workspace_member_interactors import \
    WorkspaceMemberInteractor


class WorkspaceInteractor(ValidationMixin):
    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 account_storage: AccountStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 space_storage: SpaceStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 folder_storage: FolderStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 list_storage: ListStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface, ):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.account_storage = account_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_storage = space_storage
        self.space_permission_storage = space_permission_storage
        self.folder_storage = folder_storage
        self.folder_permission_storage = folder_permission_storage
        self.list_storage = list_storage
        self.list_permission_storage = list_permission_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(self, create_workspace_data: CreateWorkspaceDTO) \
            -> WorkspaceDTO:
        self.validate_user_is_active(create_workspace_data.user_id,
                                     user_storage=self.user_storage)
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
        self.validate_user_access_for_workspace(
            user_id=user_id, workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)
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

        workspace_member_interactor = WorkspaceMemberInteractor(
            workspace_member_storage=self.workspace_member_storage,
            user_storage=self.user_storage,
            workspace_storage=self.workspace_storage,
            list_storage=self.list_storage,
            list_permission_storage=self.list_permission_storage,
            folder_storage=self.folder_storage,
            folder_permission_storage=self.folder_permission_storage,
            space_storage=self.space_storage,
            space_permission_storage=self.space_permission_storage,
        )
        workspace_member_data = self.workspace_member_storage.get_workspace_member(
            workspace_id=workspace_id, user_id=user_id)
        workspace_member_interactor.remove_member_from_workspace(
            workspace_member_id=workspace_member_data.id, removed_by=user_id)

        workspace_member_input_data = AddMemberToWorkspaceDTO(
            workspace_id=workspace_id,
            user_id=new_user_id,
            role=Role.OWNER,
            added_by=new_user_id,
        )
        workspace_member_interactor.add_member_to_workspace(
            workspace_member_data=workspace_member_input_data)
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
