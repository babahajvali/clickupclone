from task_management.interactors.dtos import ListViewDTO, CreateListViewDTO
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
            self, create_list_view_dto: CreateListViewDTO) -> ListViewDTO:
        self.check_view_type(view_type=create_list_view_dto.view_type.value)
        self.check_list_view_name_not_empty(
            name=create_list_view_dto.view_name)
        self.check_list_not_deleted(list_id=create_list_view_dto.list_id)
        self._check_user_has_edit_access_to_list(
            user_id=create_list_view_dto.created_by,
            list_id=create_list_view_dto.list_id)

        return self.view_storage.create_list_view(
            create_list_view_dto=create_list_view_dto)

    def _check_user_has_edit_access_to_list(
            self, list_id: str, user_id: str) -> None:
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
