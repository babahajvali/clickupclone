from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.mixins import UserValidationMixin


class GetUserWorkspacesInteractor:

    def __init__(self,
                 workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    @interactor_cache(cache_name="user_workspaces", timeout=5 * 60)
    def get_user_workspaces(self, user_id: str) -> list[WorkspaceMemberDTO]:
        self.user_mixin.check_user_is_active(user_id=user_id)

        return self.workspace_storage.get_active_user_workspaces(
            user_id=user_id
        )
