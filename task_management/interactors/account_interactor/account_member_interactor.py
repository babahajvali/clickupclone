from task_management.exceptions.custom_exceptions import \
    AccountMemberNotFoundException
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateAccountMemberDTO, \
    AccountMemberDTO, AddMemberToWorkspaceDTO
from task_management.interactors.storage_interface.account_member_storage_interface import \
    AccountMemberStorageInterface
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


class AccountMemberInteractor(ValidationMixin):

    def __init__(self, account_member_storage: AccountMemberStorageInterface,
                 account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 space_storage: SpaceStorageInterface,
                 folder_storage: FolderStorageInterface,
                 list_storage: ListStorageInterface):
        self.account_member_storage = account_member_storage
        self.account_storage = account_storage
        self.user_storage = user_storage
        self.workspace_storage = workspace_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_permission_storage = space_permission_storage
        self.folder_permission_storage = folder_permission_storage
        self.list_permission_storage = list_permission_storage
        self.space_storage = space_storage
        self.folder_storage = folder_storage
        self.list_storage = list_storage

        self._workspace_member_interactor = None

    def get_workspace_interactor(self):
        if self._workspace_member_interactor is None:
            self._workspace_member_interactor = WorkspaceMemberInteractor(
                workspace_storage=self.workspace_storage,
                workspace_member_storage=self.workspace_member_storage,
                user_storage=self.user_storage,
                space_permission_storage=self.space_permission_storage,
                space_storage=self.space_storage,
                folder_storage=self.folder_storage,
                folder_permission_storage=self.folder_permission_storage,
                list_permission_storage=self.list_permission_storage,
                list_storage=self.list_storage
            )
        return self._workspace_member_interactor

    def add_member_to_account(
        self, create_account_member_data: CreateAccountMemberDTO) -> \
            AccountMemberDTO:
        self.validate_account_is_active(
            account_id=create_account_member_data.account_id,
            account_storage=self.account_storage)
        self.validate_user_is_active(user_storage=self.user_storage,
                                     user_id=create_account_member_data.user_id)
        self.validate_role(role=create_account_member_data.role.value)

        self.validate_user_access_for_account(
            user_id=create_account_member_data.added_by,
            account_id=create_account_member_data.account_id,
            account_member_storage=self.account_member_storage)

        result = self.account_member_storage.add_member_to_account(
            user_data=create_account_member_data)

        self._add_member_to_account_workspaces(
            account_id=result.account_id, user_id=result.user_id,
            account_role=create_account_member_data.role, added_by=result.added_by)

        return result

    def update_member_role(self, account_member_id: int, role: Role,
                           changed_by: str) -> AccountMemberDTO:
        account_member_data = self._validate_and_get_account_member_data(
            account_member_id=account_member_id)
        self.validate_role(role=role.value)
        self.validate_user_access_for_account(
            user_id=changed_by, account_id=account_member_data.account_id,
            account_member_storage=self.account_member_storage)

        result = self.account_member_storage.update_member_role(
            account_member_id=account_member_id, role=role)
        self._update_member_role_in_workspaces(
            account_id=result.account_id, user_id=result.user_id,
            changed_by=changed_by, new_role=Role(result.role))

        return result

    def remove_member_from_account(self, account_member_id: int,
                                   removed_by: str):

        account_member_data = self._validate_and_get_account_member_data(
            account_member_id=account_member_id
        )
        self.validate_user_access_for_account(
            user_id=removed_by, account_id=account_member_data.account_id,
            account_member_storage=self.account_member_storage)

        result = self.account_member_storage.delete_account_member_permission(
            account_member_id=account_member_id)
        self._remove_member_from_account_workspaces(
            account_id=result.account_id, user_id=result.user_id,
            removed_by=removed_by)

        return result

    def get_user_accounts(self,user_id: str) -> list[AccountMemberDTO]:
        self.validate_user_is_active(user_id=user_id,user_storage=self.user_storage)

        return self.account_member_storage.get_user_accounts(user_id=user_id)


    def _add_member_to_account_workspaces(self, account_id: str, user_id: str,
                                          account_role: Role,
                                          added_by: str):

        workspaces = self.workspace_storage.get_workspaces_by_account(
            account_id=account_id
        )
        interactor = self.get_workspace_interactor()
        for workspace in workspaces:
            workspace_member_data = AddMemberToWorkspaceDTO(
                user_id=user_id,
                workspace_id=workspace.workspace_id,
                role=account_role,
                added_by=added_by

            )
            interactor.add_member_to_workspace(
                workspace_member_data=workspace_member_data
            )

    def _update_member_role_in_workspaces(self, account_id: str, user_id: str,
                                          new_role: Role, changed_by: str):
        workspaces = self.workspace_storage.get_workspaces_by_account(
            account_id=account_id
        )
        interactor = self.get_workspace_interactor()
        for workspace in workspaces:
            interactor.change_member_role(
                user_id=user_id,
                workspace_id=workspace.workspace_id,
                role=new_role.value,
                changed_by=changed_by
            )

    def _remove_member_from_account_workspaces(self, account_id: str,
                                               user_id: str,
                                               removed_by: str):
        workspaces = self.workspace_storage.get_workspaces_by_account(
            account_id=account_id
        )
        interactor = self.get_workspace_interactor()
        for workspace in workspaces:
            workspace_member_data = self.workspace_member_storage.get_workspace_member(
                workspace_id=workspace.workspace_id, user_id=user_id)
            interactor.remove_member_from_workspace(
                removed_by=removed_by,
                workspace_member_id=workspace_member_data.id
            )

    def _validate_and_get_account_member_data(self, account_member_id: int):
        account_member_data = self.account_member_storage.get_account_member_permission(
            account_member_id=account_member_id)
        if not account_member_data:
            raise AccountMemberNotFoundException(
                account_member_id=account_member_id)

        return account_member_data
