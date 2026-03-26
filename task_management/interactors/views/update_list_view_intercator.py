from typing import Optional

from task_management.interactors.dtos import ListViewDTO
from task_management.interactors.storage_interfaces import \
    ListViewStorageInterface, ListStorageInterface, WorkspaceStorageInterface
from task_management.mixins import ViewValidationMixin, \
    WorkspaceValidationMixin


class UpdateListViewInteractor(ViewValidationMixin, WorkspaceValidationMixin):

    def __init__(self, view_storage: ListViewStorageInterface,
                 list_storage: ListStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            view_storage=view_storage,
            workspace_storage=workspace_storage)
        self.view_storage = view_storage
        self.list_storage = list_storage
        self.workspace_storage = workspace_storage

    def update_list_view(
            self, list_view_id: int, view_name: Optional[str],
            user_id: str) -> ListViewDTO:
        self.check_list_view_exist(
            list_view_id=list_view_id)
        self.check_list_view_name_not_empty(name=view_name)

        list_view_dto = self.view_storage.get_list_view_by_id(
            list_view_id=list_view_id)
        self._check_user_has_edit_access_to_list(
            user_id=user_id, list_id=list_view_dto.list_id)

        return self.view_storage.update_list_view(
            list_view_id=list_view_id, view_name=view_name)

    def _check_user_has_edit_access_to_list(
            self, list_id: str, user_id: str) -> None:
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
