from task_management.interactors.dtos import ListViewDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, ViewStorageInterface, WorkspaceStorageInterface
from task_management.mixins import ListValidationMixin, \
    WorkspaceValidationMixin, ViewValidationMixin


class CreateListViewInteractor(
    ListValidationMixin,
    WorkspaceValidationMixin,
    ViewValidationMixin):

    def __init__(
            self, list_storage: ListStorageInterface,
            view_storage: ViewStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            list_storage=list_storage,
            view_storage=view_storage,
            workspace_storage=workspace_storage,
        )
        self.list_storage = list_storage
        self.view_storage = view_storage
        self.workspace_storage = workspace_storage

    def create_list_view(
            self, view_id: str, list_id: str, user_id: str) -> ListViewDTO:
        list_view_data = self.view_storage.get_list_view(
            list_id=list_id, view_id=view_id)
        if list_view_data:
            return list_view_data

        self.check_view_exist(view_id=view_id)
        self.check_list_not_deleted(list_id=list_id)
        self._check_user_has_edit_access_to_list(
            user_id=user_id, list_id=list_id)

        return self.view_storage.create_list_view(
            view_id=view_id, list_id=list_id, user_id=user_id)

    def _check_user_has_edit_access_to_list(
            self, list_id: str, user_id: str) -> None:
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
