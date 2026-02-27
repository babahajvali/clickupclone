from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    UserValidationMixin


class TransferWorkspaceInteractor:

    def __init__(self, workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def transfer_workspace(
            self, workspace_id: str, user_id: str, new_user_id: str) \
            -> WorkspaceDTO:
        self.workspace_mixin.check_workspace_not_deleted(
            workspace_id=workspace_id
        )
        self.workspace_mixin.check_user_is_workspace_owner(
            user_id=user_id, workspace_id=workspace_id
        )
        self.user_mixin.check_user_is_active(user_id=new_user_id)

        return self.workspace_storage.transfer_workspace(
            workspace_id=workspace_id, new_user_id=new_user_id)
