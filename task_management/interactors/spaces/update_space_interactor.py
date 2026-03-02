from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import NothingToUpdateSpace
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class UpdateSpaceInteractor:

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

    @invalidate_interactor_cache(cache_name="spaces")
    def update_space(
            self, space_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> SpaceDTO:
        self._check_space_update_field_properties(
            space_id=space_id, name=name, description=description
        )
        self.space_mixin.check_space_not_deleted(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id
        )
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )

        return self.space_storage.update_space(
            space_id=space_id, name=name, description=description
        )

    def _check_space_update_field_properties(
            self, space_id: str, name: Optional[str],
            description: Optional[str]):

        is_description_provided = description is not None
        is_name_provided = name is not None
        has_no_update_field_properties = not any([
            is_description_provided,
            is_name_provided
        ])

        if has_no_update_field_properties:
            raise NothingToUpdateSpace(space_id=space_id)

        if is_name_provided:
            self.space_mixin.check_space_name_not_empty(name=name)
