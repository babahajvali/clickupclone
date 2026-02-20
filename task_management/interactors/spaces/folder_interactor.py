from typing import Optional

from task_management.exceptions.enums import Visibility
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UserFolderPermissionDTO, CreateFolderPermissionDTO
from task_management.interactors.spaces.validators.folder_validator import \
    FolderValidator
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, WorkspaceStorageInterface, SpaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.mixins import FolderValidationMixin, SpaceValidationMixin, \
    WorkspaceValidationMixin


class FolderInteractor:

    def __init__(self, folder_storage: FolderStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage
        self.space_storage = space_storage

    @property
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def folder_validator(self) -> FolderValidator:
        return FolderValidator(folder_storage=self.folder_storage)

    @invalidate_interactor_cache(cache_name="folders")
    def create_folder(self, folder_data: CreateFolderDTO) -> FolderDTO:
        self.folder_validator.check_folder_name_not_empty(
            name=folder_data.name)
        self.space_mixin.check_space_is_active(
            space_id=folder_data.space_id)
        self._check_user_has_edit_access_for_space(
            space_id=folder_data.space_id,
            user_id=folder_data.created_by)

        order = self.folder_storage.get_next_folder_order_in_space(
            space_id=folder_data.space_id)

        return self.folder_storage.create_folder(folder_data, order=order)

    @invalidate_interactor_cache(cache_name="folders")
    def update_folder(
            self, folder_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> FolderDTO:
        self.folder_mixin.check_folder_is_active(folder_id=folder_id)
        field_properties_to_update = (
            self.folder_validator.check_folder_update_field_properties(
                folder_id=folder_id, name=name, description=description))

        space_id = self.folder_storage.get_folder_space_id(
            folder_id=folder_id)
        self._check_user_has_edit_access_for_space(space_id=space_id,
                                                   user_id=user_id)

        return self.folder_storage.update_folder(
            folder_id=folder_id, field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="folders")
    def reorder_folder(self, space_id: str, folder_id: str, user_id: str,
                       order: int) -> FolderDTO:
        self.folder_mixin.check_folder_is_active(folder_id=folder_id)
        self.space_mixin.check_space_is_active(space_id=space_id)
        self._check_user_has_edit_access_for_space(space_id=space_id,
                                                   user_id=user_id)
        self.folder_validator.check_the_folder_order(
            space_id=space_id, order=order)

        return self.folder_storage.reorder_folder(folder_id=folder_id,
                                                  new_order=order)

    @invalidate_interactor_cache(cache_name="folders")
    def delete_folder(self, folder_id: str, user_id: str) -> FolderDTO:
        self.folder_mixin.check_folder_is_active(folder_id=folder_id)
        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=user_id)

        return self.folder_storage.delete_folder(folder_id)

    @invalidate_interactor_cache(cache_name="folders")
    def set_folder_visibility(
            self, folder_id: str, user_id: str, visibility: Visibility) \
            -> FolderDTO:
        self.folder_mixin.check_folder_is_active(folder_id=folder_id)
        self.folder_validator.check_visibility_type(
            visibility=visibility.value)
        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=user_id)

        if visibility == Visibility.PUBLIC:
            return self.folder_storage.set_folder_public(folder_id=folder_id)

        return self.folder_storage.set_folder_private(folder_id=folder_id)

    @interactor_cache(cache_name="folders", timeout=5 * 60)
    def get_active_space_folders(self, space_id: str) -> list[FolderDTO]:
        self.space_mixin.check_space_is_active(space_id=space_id)

        return self.folder_storage.get_active_space_folders(
            space_ids=[space_id])

    def add_user_for_folder_permission(
            self, permission_data: CreateFolderPermissionDTO) \
            -> UserFolderPermissionDTO:
        self.folder_mixin.check_folder_is_active(
            folder_id=permission_data.folder_id)
        space_id = self.folder_storage.get_folder_space_id(
            folder_id=permission_data.folder_id)
        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=permission_data.user_id)

        return self.folder_storage.create_folder_users_permissions(
            users_permission_data=[permission_data])[0]

    # Helping Functions

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)

        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)
