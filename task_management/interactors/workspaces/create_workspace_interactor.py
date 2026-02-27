from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, AccountStorageInterface
from task_management.interactors.workspaces.validators.workspace_validator import \
    WorkspaceValidator
from task_management.mixins import AccountValidationMixin


class CreateWorkspaceInteractor:

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 account_storage: AccountStorageInterface):
        self.workspace_storage = workspace_storage
        self.account_storage = account_storage

    @property
    def account_mixin(self) -> AccountValidationMixin:
        return AccountValidationMixin(account_storage=self.account_storage)

    @property
    def workspace_validator(self) -> WorkspaceValidator:
        return WorkspaceValidator(workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(
            self, workspace_data: CreateWorkspaceDTO) -> WorkspaceDTO:
        self.workspace_validator.check_workspace_name_not_empty(
            workspace_name=workspace_data.name
        )
        self.account_mixin.check_account_is_active(workspace_data.account_id)
        self.account_mixin.check_user_is_account_owner(
            workspace_data.user_id, account_id=workspace_data.account_id
        )

        return self.workspace_storage.create_workspace(
            workspace_data=workspace_data)
