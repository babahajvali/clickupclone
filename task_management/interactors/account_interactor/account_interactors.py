from task_management.exceptions.custom_exceptions import \
    AccountNameAlreadyExistsException, InvalidAccountIdsException, \
    InactiveAccountIdsException
from task_management.interactors.dtos import CreateAccountDTO, AccountDTO, \
    CreateWorkspaceDTO, CreateSpaceDTO, CreateListDTO
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface

from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
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
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.interactors.workspace_interactors.workspace_interactors import \
    WorkspaceInteractor


class AccountInteractor(ValidationMixin):
    def __init__(self, account_storage: AccountStorageInterface,
                 user_storage: UserStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 space_storage: SpaceStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 list_storage: ListStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 template_storage: TemplateStorageInterface,
                 field_storage: FieldStorageInterface,
                 folder_storage: FolderStorageInterface,
                 task_storage: TaskStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface, ):
        self.account_storage = account_storage
        self.user_storage = user_storage
        self.workspace_storage = workspace_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_storage = space_storage
        self.space_permission_storage = space_permission_storage
        self.list_storage = list_storage
        self.list_permission_storage = list_permission_storage
        self.template_storage = template_storage
        self.field_storage = field_storage
        self.folder_storage = folder_storage
        self.task_storage = task_storage
        self.folder_permission_storage = folder_permission_storage

    def create_account(self,
                       create_account_data: CreateAccountDTO) -> AccountDTO:
        self._validate_account_name_exists(
            account_name=create_account_data.name)

        result = self.account_storage.create_account(create_account_data)
        self._create_workspace(account_id=result.account_id,
                               owner_id=result.owner_id, name=result.name)

        return result

    def transfer_account(self, account_id: str, old_owner_id: str,
                         new_owner_id: str) -> AccountDTO:
        self.validate_account_is_active(account_id=account_id,
                                        account_storage=self.account_storage)
        self.validate_user_is_account_owner(
            account_id=account_id, user_id=old_owner_id,
            account_storage=self.account_storage)
        self.validate_user_is_active(user_id=new_owner_id,
                                     user_storage=self.user_storage)

        return self.account_storage.transfer_account(account_id=account_id,
                                                     new_owner_id=new_owner_id)

    def delete_account(self, account_id: str, deleted_by: str):
        self.validate_account_is_active(account_id=account_id,
                                        account_storage=self.account_storage)

        self.validate_user_is_account_owner(
            account_id=account_id, user_id=deleted_by,
            account_storage=self.account_storage)

        return self.account_storage.delete_account(account_id=account_id)

    def get_accounts(self, account_ids: list[str]) -> list[AccountDTO]:
        accounts_data = self._check_accounts_active(account_ids=account_ids)

        return accounts_data

    # Helping functions

    def _validate_account_name_exists(self, account_name: str):
        is_name_exist = self.account_storage.validate_account_name_exists(
            name=account_name)

        if is_name_exist:
            raise AccountNameAlreadyExistsException(name=account_name)

    def _create_workspace(self, owner_id: str, account_id: str, name: str):
        workspace_interactor = WorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            account_storage=self.account_storage,
            workspace_member_storage=self.workspace_member_storage,
            space_storage=self.space_storage,
            space_permission_storage=self.space_permission_storage,
            folder_storage=self.folder_storage,
            folder_permission_storage=self.folder_permission_storage,
            list_storage=self.list_storage,
            list_permission_storage=self.list_permission_storage,
            template_storage=self.template_storage,
            task_storage=self.task_storage,
            field_storage=self.field_storage
        )

        workspace_input_data = CreateWorkspaceDTO(
            name=name + "'s Workspace",
            description="Default workspace",
            user_id=owner_id,
            account_id=account_id
        )
        return workspace_interactor.create_workspace(workspace_input_data)

    def _check_accounts_active(self, account_ids: list[str]):
        accounts_data = self.account_storage.get_accounts(
            account_ids=account_ids)

        existed_active_account_ids = [str(obj.account_id) for obj in
                                      accounts_data if obj.is_active]
        existed_inactive_account_ids = [str(obj.account_id) for obj in
                                        accounts_data if not obj.is_active]
        invalid_accounts_ids = []
        inactive_accounts_ids = []

        for account_id in account_ids:
            if account_id not in existed_active_account_ids and account_id not in existed_inactive_account_ids:
                invalid_accounts_ids.append(account_id)
            elif account_id in existed_inactive_account_ids:
                inactive_accounts_ids.append(account_id)

        if invalid_accounts_ids:
            raise InvalidAccountIdsException(
                account_ids=invalid_accounts_ids)

        if inactive_accounts_ids:
            raise InactiveAccountIdsException(
                account_ids=inactive_accounts_ids)

        return accounts_data
