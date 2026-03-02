from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    NothingToUpdateFolderException
from task_management.interactors.dtos import FolderDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, WorkspaceStorageInterface, SpaceStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    FolderValidationMixin


class UpdateFolderInteractor:

    def __init__(self, folder_storage: FolderStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage
        self.space_storage = space_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    @invalidate_interactor_cache(cache_name="folders")
    def update_folder(
            self, folder_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> FolderDTO:
        self._check_folder_update_field_properties(
            folder_id=folder_id, name=name, description=description
        )
        self.folder_mixin.check_folder_not_deleted(folder_id=folder_id)
        space_id = self.folder_storage.get_folder_space_id(
            folder_id=folder_id
        )
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=user_id
        )

        return self.folder_storage.update_folder(
            folder_id=folder_id, name=name, description=description)

    def _check_folder_update_field_properties(
            self, folder_id: str, name: Optional[str],
            description: Optional[str]):
        is_name_provided = name is not None
        is_description_provided = description is not None

        has_no_update_field_properties = not (
                is_description_provided or is_name_provided)

        if has_no_update_field_properties:
            raise NothingToUpdateFolderException(folder_id=folder_id)

        if is_name_provided:
            self.folder_mixin.check_folder_name_not_empty(name=name)

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )
