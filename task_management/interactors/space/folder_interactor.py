from typing import Optional

from task_management.exceptions.custom_exceptions import InvalidOrder, \
    EmptyName, UnsupportedVisibilityType, \
    NothingToUpdateFolderException
from task_management.exceptions.enums import Visibility
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UserFolderPermissionDTO, CreateFolderPermissionDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, WorkspaceStorageInterface, SpaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.mixins import FolderValidationMixin, SpaceValidationMixin, \
    WorkspaceValidationMixin


class FolderInteractor(FolderValidationMixin, SpaceValidationMixin,
                       WorkspaceValidationMixin):

    def __init__(self, folder_storage: FolderStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        super().__init__(folder_storage=folder_storage,
                         space_storage=space_storage,
                         workspace_storage=workspace_storage)
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="folders")
    def create_folder(self, create_folder_data: CreateFolderDTO) -> FolderDTO:

        self._check_folder_name_not_empty(name=create_folder_data.name)
        self.check_space_is_active(space_id=create_folder_data.space_id)
        self._validate_user_access_for_space(
            space_id=create_folder_data.space_id,
            user_id=create_folder_data.created_by)

        return self.folder_storage.create_folder(create_folder_data)

    @invalidate_interactor_cache(cache_name="folders")
    def update_folder(self, folder_id: str, user_id: str, name: Optional[str],
                      description: Optional[str]) -> FolderDTO:

        self.check_folder_is_active(folder_id=folder_id)
        space_id = self.folder_storage.get_folder_space_id(
            folder_id=folder_id)
        self._validate_user_access_for_space(space_id=space_id,
                                             user_id=user_id)

        is_name_provided = name is not None
        is_description_provided = description is not None

        field_properties_to_update = {}

        if is_name_provided:
            self._check_folder_name_not_empty(name=name)
            field_properties_to_update['name'] = name

        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateFolderException(folder_id=folder_id)

        return self.folder_storage.update_folder(
            folder_id=folder_id, field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="folders")
    def reorder_folder(self, space_id: str, folder_id: str, user_id: str,
                       order: int) -> FolderDTO:

        self.check_folder_is_active(folder_id=folder_id)
        self.check_space_is_active(space_id=space_id)
        self._validate_user_access_for_space(space_id=space_id,
                                             user_id=user_id)
        self._validate_the_folder_order(space_id=space_id, order=order)

        return self.folder_storage.reorder_folder(folder_id=folder_id,
                                                  new_order=order)

    @invalidate_interactor_cache(cache_name="folders")
    def remove_folder(self, folder_id: str, user_id: str) -> FolderDTO:

        self.check_folder_is_active(folder_id=folder_id)
        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        self._validate_user_access_for_space(space_id=space_id,
                                             user_id=user_id)

        return self.folder_storage.remove_folder(folder_id)

    @invalidate_interactor_cache(cache_name="folders")
    def set_folder_visibility(self, folder_id: str, user_id: str,
                              visibility: Visibility) -> FolderDTO:

        self.check_folder_is_active(folder_id=folder_id)
        self._validate_visibility_type(visibility=visibility.value)
        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        self._validate_user_access_for_space(space_id=space_id,
                                             user_id=user_id)

        if visibility == Visibility.PUBLIC:
            return self.folder_storage.set_folder_public(folder_id=folder_id)

        return self.folder_storage.set_folder_private(folder_id=folder_id)

    @interactor_cache(cache_name="folders", timeout=5 * 60)
    def get_space_folders(self, space_id: str) -> list[FolderDTO]:

        self.check_space_is_active(space_id=space_id)

        return self.folder_storage.get_space_folders(space_ids=[space_id])

    def get_folder_permissions(self, folder_id: str) -> list[
        UserFolderPermissionDTO]:

        self.check_folder_is_active(folder_id=folder_id)

        return self.folder_storage.get_folder_permissions(
            folder_id=folder_id)

    def add_user_for_folder_permission(self,
                                       permission_data: CreateFolderPermissionDTO):

        self.check_folder_is_active(folder_id=permission_data.folder_id)
        space_id = self.folder_storage.get_folder_space_id(
            folder_id=permission_data.folder_id)
        self._validate_user_access_for_space(space_id=space_id,
                                             user_id=permission_data.user_id)

        return self.folder_storage.create_folder_users_permissions(
            users_permission_data=[permission_data])[0]

    # Helping Functions

    def _validate_the_folder_order(self, space_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        lists_count = self.folder_storage.get_space_folder_count(
            space_id=space_id)

        if order > lists_count:
            raise InvalidOrder(order=order)

    @staticmethod
    def _check_folder_name_not_empty(name: str):

        is_name_empty = name is None or not name.strip()

        if is_name_empty:
            raise EmptyName(name=name)

    def _validate_user_access_for_space(self, space_id: str, user_id: str):

        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.check_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)

    @staticmethod
    def _validate_visibility_type(visibility: str):
        existed_visibilities = [each.value for each in Visibility]

        is_visibility_invalid = visibility not in existed_visibilities
        if is_visibility_invalid:
            raise UnsupportedVisibilityType(
                visibility_type=visibility)
