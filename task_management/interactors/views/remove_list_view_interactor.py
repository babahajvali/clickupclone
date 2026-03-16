from task_management.interactors.dtos import ListViewDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, ViewStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    ViewValidationMixin


class RemoveListViewInteractor(WorkspaceValidationMixin, ViewValidationMixin):

    def __init__(
            self, list_storage: ListStorageInterface,
            view_storage: ViewStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            workspace_storage=workspace_storage,
            view_storage=view_storage)
        self.list_storage = list_storage
        self.view_storage = view_storage
        self.workspace_storage = workspace_storage

    def remove_view_for_list(
            self, list_view_id: int, user_id: str) -> ListViewDTO:
        self.check_list_view_exist(list_view_id=list_view_id)
        list_view_dto = self.view_storage.get_list_view_by_id(
            list_view_id=list_view_id)
        self._check_user_has_edit_access_to_list(
            user_id=user_id, list_id=list_view_dto.list_id)

        return self.view_storage.remove_list_view(
            list_view_id=list_view_id)

    def _check_user_has_edit_access_to_list(
            self, list_id: str, user_id: str) -> None:
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
