from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.mixins import UserValidationMixin


class GetUserWorkspacesInteractor(UserValidationMixin):

    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
            user_storage: UserStorageInterface):
        super().__init__(user_storage=user_storage)
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @interactor_cache(cache_name="user_workspaces", timeout=5 * 60)
    def get_user_workspaces(self, user_id: str) -> list[WorkspaceMemberDTO]:
        self.check_user_is_active(user_id=user_id)

        return self.workspace_storage.get_active_user_workspaces(
            user_id=user_id
        )
