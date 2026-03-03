from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    BothFolderAndSpaceProvided
from task_management.interactors.dtos import CreateListDTO, ListDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, WorkspaceStorageInterface, \
    SpaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin, FolderValidationMixin, ListValidationMixin


class CreateListInteractor:
    def __init__(
            self, list_storage: ListStorageInterface,
            folder_storage: FolderStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            space_storage: SpaceStorageInterface):
        self.list_storage = list_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def create_list(self, list_data: CreateListDTO) -> ListDTO:

        is_folder_provided = list_data.folder_id is not None
        is_space_provided = list_data.space_id is not None

        is_both_folder_and_space_provided = (
                is_folder_provided and is_space_provided)

        if is_both_folder_and_space_provided:
            raise BothFolderAndSpaceProvided(
                folder_id=list_data.folder_id,
                space_id=list_data.space_id)
        self.list_mixin.check_list_name_not_empty(list_name=list_data.name)

        if is_folder_provided:
            order = self.create_list_in_folder(list_data=list_data)
        else:
            order = self.create_list_in_space(list_data=list_data)

        return self.list_storage.create_list(list_data=list_data, order=order)

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):

        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def create_list_in_folder(self, list_data: CreateListDTO) -> int:

        self.folder_mixin.check_folder_not_deleted(
            folder_id=list_data.folder_id)
        space_id = self.folder_storage.get_folder_space_id(
            folder_id=list_data.folder_id)
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=list_data.created_by
        )
        order = self.list_storage.get_last_list_order_in_folder(
            folder_id=list_data.folder_id)

        return order + 1

    def create_list_in_space(self, list_data: CreateListDTO) -> int:

        self.space_mixin.check_space_not_deleted(
            space_id=list_data.space_id)
        self._check_user_has_edit_access_for_space(
            space_id=list_data.space_id, user_id=list_data.created_by
        )
        order = self.list_storage.get_last_list_order_in_space(
            space_id=list_data.space_id)
        return order + 1
