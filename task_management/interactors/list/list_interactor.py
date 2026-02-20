from typing import Optional

from task_management.exceptions.custom_exceptions import InvalidOrderException, \
    NothingToUpdateListException, \
    UnsupportedVisibilityTypeException, UserHaveAlreadyListPermissionException
from task_management.exceptions.enums import Visibility
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    CreateListPermissionDTO, UserListPermissionDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, SpaceStorageInterface, \
    WorkspaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.mixins import ListValidationMixin, \
    SpaceValidationMixin, FolderValidationMixin, WorkspaceValidationMixin


class ListInteractor(ListValidationMixin, SpaceValidationMixin,
                     WorkspaceValidationMixin, FolderValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 folder_storage: FolderStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        super().__init__(list_storage=list_storage,
                         space_storage=space_storage,
                         workspace_storage=workspace_storage,
                         folder_storage=folder_storage)
        self.list_storage = list_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def create_list(self, list_data: CreateListDTO) -> ListDTO:

        self.check_list_name_not_empty(list_name=list_data.name)
        self.validate_space_is_active(space_id=list_data.space_id)
        is_folder_provided = list_data.folder_id is not None
        if is_folder_provided:
            self.validate_folder_is_active(folder_id=list_data.folder_id)

        order = self.get_list_order(folder_id=list_data.folder_id,
                                    space_id=list_data.space_id)

        self.check_user_has_edit_access_for_space(
            space_id=list_data.space_id, user_id=list_data.created_by)

        return self.list_storage.create_list(list_data=list_data, order=order)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def update_list(self, list_id: str, user_id: str, name: Optional[str],
                    description: Optional[str]) -> ListDTO:

        field_properties_to_update = self._check_update_field_properties(
            list_id=list_id, name=name, description=description)

        self.validate_list_is_active(list_id=list_id)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        self.check_user_has_edit_access_for_space(space_id=space_id,
                                                  user_id=user_id)

        return self.list_storage.update_list(
            list_id=list_id, field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="folder_lists")
    def reorder_list_in_folder(self, folder_id: str, list_id: str, order: int,
                               user_id: str) -> ListDTO:

        self.check_list_order_in_folder(folder_id=folder_id, order=order)
        self.validate_list_is_active(list_id=list_id)
        self.validate_folder_is_active(folder_id=folder_id)

        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        self.check_user_has_edit_access_for_space(space_id=space_id,
                                                  user_id=user_id)

        return self.list_storage.reorder_list_in_folder(
            folder_id=folder_id, list_id=list_id, order=order)

    @invalidate_interactor_cache(cache_name="space_lists")
    def reorder_list_in_space(self, list_id: str, space_id: str, order: int,
                              user_id: str) -> ListDTO:
        self.check_list_order_in_space(space_id=space_id, order=order)
        self.validate_list_is_active(list_id=list_id)
        self.validate_space_is_active(space_id=space_id)
        self.check_user_has_edit_access_for_space(space_id=space_id,
                                                  user_id=user_id)

        return self.list_storage.reorder_list_in_space(
            space_id=space_id, list_id=list_id, order=order)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def delete_list(self, list_id: str, user_id: str):

        self.validate_list_is_active(list_id=list_id)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        self.check_user_has_edit_access_for_space(space_id=space_id,
                                                  user_id=user_id)

        return self.list_storage.delete_list(list_id=list_id)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def set_list_visibility(self, list_id: str, visibility: Visibility,
                            user_id: str) -> ListDTO:

        self.check_visibility_type(visibility=visibility.value)

        self.validate_list_is_active(list_id=list_id)
        space_id = self.list_storage.get_list_space_id(list_id=list_id)
        self.check_user_has_edit_access_for_space(space_id=space_id,
                                                  user_id=user_id)

        if visibility == Visibility.PUBLIC:
            return self.list_storage.make_list_public(list_id=list_id)

        return self.list_storage.make_list_private(list_id=list_id)

    def get_active_list(self, list_id: str) -> ListDTO:

        self.validate_list_is_active(list_id=list_id)

        return self.list_storage.get_list(list_id=list_id)

    @interactor_cache(timeout=5 * 60, cache_name="folder_lists")
    def get_active_folder_lists(self, folder_id: str):

        self.validate_folder_is_active(folder_id=folder_id)

        return self.list_storage.get_active_folder_lists(folder_ids=[folder_id])

    @interactor_cache(timeout=30 * 60, cache_name="space_lists")
    def get_active_space_lists(self, space_id: str):

        self.validate_space_is_active(space_id=space_id)

        return self.list_storage.get_active_space_lists(space_ids=[space_id])

    def add_user_in_list_permission(self,
                                    user_permission_data: CreateListPermissionDTO) -> UserListPermissionDTO:
        self.check_user_have_already_list_permission(
            user_id=user_permission_data.user_id,
            list_id=user_permission_data.list_id)
        self.validate_list_is_active(list_id=user_permission_data.list_id)
        space_id = self.list_storage.get_list_space_id(
            list_id=user_permission_data.list_id)
        self.check_user_has_edit_access_for_space(
            space_id=space_id, user_id=user_permission_data.added_by)
        self.check_permission(
            permission=user_permission_data.permission_type.value)

        return self.list_storage.create_list_users_permission(
            user_permissions=[user_permission_data])[0]

    # Helping functions

    def check_list_order_in_folder(self, folder_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)

        lists_count = self.list_storage.get_folder_lists_count(
            folder_id=folder_id)

        if order > lists_count:
            raise InvalidOrderException(order=order)

    def check_list_order_in_space(self, space_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)
        lists_count = self.list_storage.get_space_lists_count(
            space_id=space_id)

        if order > lists_count:
            raise InvalidOrderException(order=order)

    def check_user_has_edit_access_for_space(self, space_id: str, user_id: str):

        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

    @staticmethod
    def check_visibility_type(visibility: str):
        existed_visibilities = Visibility.get_values()
        is_visibility_invalid = visibility not in existed_visibilities

        if is_visibility_invalid:
            raise UnsupportedVisibilityTypeException(
                visibility_type=visibility)

    def _check_update_field_properties(self, list_id: str, name: Optional[str],
                                       description: Optional[str]) -> dict:

        field_properties_to_update = {}

        is_name_provided = name is not None
        if is_name_provided:
            self.check_list_name_not_empty(list_name=name)
            field_properties_to_update['name'] = name

        is_description_provided = description is not None
        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateListException(list_id=list_id)

        return field_properties_to_update
