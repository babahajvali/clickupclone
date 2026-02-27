from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateListDTO, ListDTO
from task_management.interactors.lists.validator.list_validator import \
    ListValidator
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, WorkspaceStorageInterface, \
    SpaceStorageInterface
from task_management.mixins import ListValidationMixin, SpaceValidationMixin, \
    WorkspaceValidationMixin, FolderValidationMixin


class CreateListInteractor:
    def __init__(self, list_storage: ListStorageInterface,
                 folder_storage: FolderStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.list_storage = list_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

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
    def list_validator(self) -> ListValidator:
        return ListValidator(list_storage=self.list_storage)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def create_list(self, list_data: CreateListDTO) -> ListDTO:

        self.list_validator.check_list_name_not_empty(list_name=list_data.name)
        self._check_user_has_edit_access_for_space(
            space_id=list_data.space_id, user_id=list_data.created_by
        )
        self.space_mixin.check_space_is_not_deleted(
            space_id=list_data.space_id)
        is_folder_provided = list_data.folder_id is not None
        if is_folder_provided:
            self.folder_mixin.check_folder_is_not_deleted(
                folder_id=list_data.folder_id)

        order = self._get_list_order(
            folder_id=list_data.folder_id, space_id=list_data.space_id
        )

        return self.list_storage.create_list(list_data=list_data, order=order)

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):

        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def _get_list_order(self, folder_id: Optional[str], space_id: str) -> int:

        is_folder_provided = folder_id is not None
        if is_folder_provided:
            order = self.list_storage.get_last_list_order_in_folder(
                folder_id=folder_id)
        else:
            order = self.list_storage.get_last_list_order_in_space(
                space_id=space_id)

        return order + 1
