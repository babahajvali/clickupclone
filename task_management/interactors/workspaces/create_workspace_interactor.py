from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, AccountStorageInterface
from task_management.mixins import AccountValidationMixin, \
    WorkspaceValidationMixin


class CreateWorkspaceInteractor(
    AccountValidationMixin, WorkspaceValidationMixin):

    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
            account_storage: AccountStorageInterface):
        super().__init__(
            account_storage=account_storage,
            workspace_storage=workspace_storage)
        self.workspace_storage = workspace_storage
        self.account_storage = account_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def create_workspace(
            self, create_workspace_dto: CreateWorkspaceDTO) -> WorkspaceDTO:
        self.check_workspace_name_not_empty(
            workspace_name=create_workspace_dto.name
        )
        self.check_account_is_active(
            account_id=create_workspace_dto.account_id)
        self.check_user_is_account_owner(
            user_id=create_workspace_dto.user_id,
            account_id=create_workspace_dto.account_id,
        )

        return self.workspace_storage.create_workspace(
            create_workspace_sto=create_workspace_dto
        )
