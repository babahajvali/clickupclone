from task_management.exceptions.custom_exceptions import ListViewNotFound
from task_management.interactors.dtos import ListViewDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, ViewStorageInterface, WorkspaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin


class RemoveListViewInteractor:

    def __init__(
            self, list_storage: ListStorageInterface,
            view_storage: ViewStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.list_storage = list_storage
        self.view_storage = view_storage
        self.workspace_storage = workspace_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    def remove_view_for_list(
            self, view_id: str, list_id: str, user_id: str) -> ListViewDTO:
        self._check_list_view_exist(list_id=list_id, view_id=view_id)
        self._check_user_has_edit_access_to_list(
            user_id=user_id, list_id=list_id)

        return self.view_storage.remove_list_view(
            view_id=view_id, list_id=list_id)

    def _check_list_view_exist(self, list_id: str, view_id: str):
        is_exist = self.view_storage.is_list_view_exist(
            list_id=list_id, view_id=view_id)

        is_list_view_not_found = not is_exist
        if is_list_view_not_found:
            raise ListViewNotFound(view_id=view_id, list_id=list_id)

    def _check_user_has_edit_access_to_list(self, list_id: str, user_id: str):
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
