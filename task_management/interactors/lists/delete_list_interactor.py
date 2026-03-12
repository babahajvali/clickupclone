from task_management.decorators.caching_decorators import (
    invalidate_interactor_cache,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.mixins import (
    ListValidationMixin,
    WorkspaceValidationMixin,
)


class DeleteListInteractor(ListValidationMixin, WorkspaceValidationMixin):

    def __init__(
            self, list_storage: ListStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            list_storage=list_storage,
            workspace_storage=workspace_storage,
        )
        self.list_storage = list_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def delete_list(self, list_id: str, user_id: str):
        self.check_list_exists(list_id=list_id)

        self._check_user_has_edit_access_for_list(
            list_id=list_id, user_id=user_id
        )

        return self.list_storage.delete_list(list_id=list_id)

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id
        )
        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )
