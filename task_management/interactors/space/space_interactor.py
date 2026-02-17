from typing import Optional

from task_management.exceptions.custom_exceptions import InvalidOrderException, \
    UnexpectedPermissionException, EmptyNameException, \
    NothingToUpdateSpaceException, UnsupportedVisibilityTypeException
from task_management.exceptions.enums import Permissions, Visibility
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    UserSpacePermissionDTO, CreateUserSpacePermissionDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class SpaceInteractor(SpaceValidationMixin, WorkspaceValidationMixin):

    def __init__(self, space_storage: SpaceStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        super().__init__(space_storage=space_storage,
                         workspace_storage=workspace_storage, )
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="spaces")
    def create_space(self, space_data: CreateSpaceDTO) -> SpaceDTO:

        self._check_space_name_not_empty(name=space_data.name)
        self.validate_workspace_is_active(
            workspace_id=space_data.workspace_id)
        self.validate_user_has_access_to_workspace(
            user_id=space_data.created_by,
            workspace_id=space_data.workspace_id)

        return self.space_storage.create_space(
            create_space_data=space_data)

    @invalidate_interactor_cache(cache_name="spaces")
    def update_space(self, space_id: str, user_id: str, name: Optional[str],
                     description: Optional[str]) -> SpaceDTO:

        self.validate_space_is_active(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_workspace_is_active(workspace_id=workspace_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)

        is_name_provided = name is not None
        is_description_provided = description is not None
        fields_to_update = {}

        if is_name_provided:
            self._check_space_name_not_empty(name=name)
            fields_to_update['name'] = name

        if is_description_provided:
            fields_to_update['description'] = description

        if not fields_to_update:
            raise NothingToUpdateSpaceException(space_id=space_id)

        return self.space_storage.update_space(space_id=space_id,
                                               update_fields=fields_to_update)

    @invalidate_interactor_cache(cache_name="spaces")
    def reorder_space(self, workspace_id: str, space_id: str, order: int,
                      user_id: str):

        self.validate_space_is_active(space_id=space_id)
        self.validate_workspace_is_active(workspace_id=workspace_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)
        self._validate_space_order(workspace_id=workspace_id, order=order)

        return self.space_storage.reorder_space(
            workspace_id=workspace_id, space_id=space_id, new_order=order)

    @invalidate_interactor_cache(cache_name="spaces")
    def delete_space(self, space_id: str, deleted_by: str) -> SpaceDTO:

        self.validate_space_is_active(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            user_id=deleted_by, workspace_id=workspace_id)

        return self.space_storage.remove_space(space_id=space_id)

    @invalidate_interactor_cache(cache_name="spaces")
    def set_space_visibility(self, space_id: str, user_id: str,
                             visibility: Visibility):

        self.validate_space_is_active(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)

        self._validate_visibility_type(visibility=visibility.value)

        if visibility == Visibility.PUBLIC:
            return self.space_storage.set_space_public(space_id=space_id)

        return self.space_storage.set_space_private(space_id=space_id)

    @interactor_cache(cache_name="spaces", timeout=30 * 60)
    def get_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:

        self.validate_workspace_is_active(workspace_id=workspace_id)

        return self.space_storage.get_workspace_spaces(
            workspace_id=workspace_id)

    def get_space(self, space_id: str) -> SpaceDTO:

        self.validate_space_is_active(space_id=space_id)

        return self.space_storage.get_space(space_id=space_id)

    # Permissions Section

    def get_space_permissions(self, space_id: str) -> list[
        UserSpacePermissionDTO]:

        self.validate_space_is_active(space_id=space_id)

        return self.space_storage.get_space_permissions(
            space_id=space_id)

    def add_user_for_space_permission(self,
                                      user_data: CreateUserSpacePermissionDTO):
        self.validate_space_is_active(space_id=user_data.space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=user_data.space_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_data.user_id, workspace_id=workspace_id)
        self.validate_permission(permission=user_data.permission_type.value)

        return self.space_storage.create_user_space_permissions(
            permission_data=[user_data])[0]

    def _validate_space_order(self, workspace_id: str, order: int):

        if order < 1:
            raise InvalidOrderException(order=order)
        space_count = self.space_storage.get_workspace_spaces_count(
            workspace_id=workspace_id)

        if order > space_count:
            raise InvalidOrderException(order=order)

    @staticmethod
    def validate_permission(permission: str):

        existed_permissions = Permissions.get_values()

        if permission not in existed_permissions:
            raise UnexpectedPermissionException(permission=permission)

    @staticmethod
    def _check_space_name_not_empty(name: str):

        if not name or not name.strip():
            raise EmptyNameException(name=name)

    @staticmethod
    def _validate_visibility_type(visibility: str):

        existed_visibilities = [each.value for each in Visibility]

        if visibility not in existed_visibilities:
            raise UnsupportedVisibilityTypeException(
                visibility_type=visibility)
