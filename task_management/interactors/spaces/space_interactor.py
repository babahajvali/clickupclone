from typing import Optional

from task_management.exceptions.enums import Visibility
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    UserSpacePermissionDTO, CreateUserSpacePermissionDTO
from task_management.interactors.spaces.validators.space_validator import \
    SpaceValidator
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class SpaceInteractor:

    def __init__(self, space_storage: SpaceStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
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
    def space_validator(self) -> SpaceValidator:
        return SpaceValidator(space_storage=self.space_storage)

    @invalidate_interactor_cache(cache_name="spaces")
    def create_space(self, space_data: CreateSpaceDTO) -> SpaceDTO:

        self.space_validator.check_space_name_not_empty(name=space_data.name)
        self.workspace_mixin.check_workspace_is_active(
            workspace_id=space_data.workspace_id)
        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=space_data.created_by,
            workspace_id=space_data.workspace_id)

        return self.space_storage.create_space(
            create_space_data=space_data)

    @invalidate_interactor_cache(cache_name="spaces")
    def update_space(
            self, space_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> SpaceDTO:

        self.space_mixin.check_space_is_active(space_id=space_id)
        field_properties_to_update = (
            self.space_validator.check_space_update_field_properties(
            space_id=space_id, name=name, description=description))

        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)

        return self.space_storage.update_space(
            space_id=space_id, field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="spaces")
    def reorder_space(
            self, workspace_id: str, space_id: str, order: int, user_id: str) \
            -> SpaceDTO:

        self.space_mixin.check_space_is_active(space_id=space_id)
        self.workspace_mixin.check_workspace_is_active(
            workspace_id=workspace_id)
        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)
        self.space_validator.check_space_order(
            workspace_id=workspace_id, order=order)

        return self.space_storage.reorder_space(
            workspace_id=workspace_id, space_id=space_id, new_order=order)

    @invalidate_interactor_cache(cache_name="spaces")
    def delete_space(self, space_id: str, deleted_by: str) -> SpaceDTO:

        self.space_mixin.check_space_is_active(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=deleted_by, workspace_id=workspace_id)

        return self.space_storage.delete_space(space_id=space_id)

    @invalidate_interactor_cache(cache_name="spaces")
    def set_space_visibility(
            self, space_id: str, user_id: str, visibility: Visibility) \
            -> SpaceDTO:

        self.space_mixin.check_space_is_active(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id)

        self.space_validator.check_visibility_type(visibility=visibility.value)

        if visibility == Visibility.PUBLIC:
            return self.space_storage.set_space_public(space_id=space_id)

        return self.space_storage.set_space_private(space_id=space_id)

    @interactor_cache(cache_name="spaces", timeout=30 * 60)
    def get_active_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:

        self.workspace_mixin.check_workspace_is_active(
            workspace_id=workspace_id)

        return self.space_storage.get_active_workspace_spaces(
            workspace_id=workspace_id)

    def get_space(self, space_id: str) -> SpaceDTO:

        self.space_mixin.check_space_exists(space_id=space_id)

        return self.space_storage.get_space(space_id=space_id)

    # Permissions Section

    def add_user_for_space_permission(
            self, user_data: CreateUserSpacePermissionDTO) \
            -> UserSpacePermissionDTO:

        self.space_mixin.check_space_is_active(space_id=user_data.space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=user_data.space_id)
        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=user_data.user_id, workspace_id=workspace_id)
        self.space_validator.check_permission(
            permission=user_data.permission_type.value)

        return self.space_storage.create_user_space_permissions(
            permission_data=[user_data])[0]
