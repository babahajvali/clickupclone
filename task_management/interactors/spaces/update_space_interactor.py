from typing import Optional

from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import NothingToUpdateSpace
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class UpdateSpaceInteractor(SpaceValidationMixin, WorkspaceValidationMixin):
    """
    Update Space Interactor updates space metadata.

    Handle the update space operation.
    This interactor checks the business rules and permission validation
     before updating the space.

    Key Responsibility:
     - Update the space

    Dependencies:
        - SpaceStorageInterface
        - WorkspaceStorageInterface
    """

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            space_storage=space_storage, workspace_storage=workspace_storage)
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="spaces")
    def update_space(
            self, space_id: str, user_id: str, name: Optional[str],
            description: Optional[str]) -> SpaceDTO:
        """Update space metadata for an existing space."""

        self.check_space_not_deleted(space_id=space_id)
        self._check_update_space_properties_not_empty(
            space_id=space_id,
            name=name,
            description=description,
        )
        self._check_user_has_edit_access_to_space(
            space_id=space_id,
            user_id=user_id,
        )

        return self.space_storage.update_space(
            space_id=space_id,
            name=name,
            description=description,
        )

    def _check_update_space_properties_not_empty(
            self, space_id: str, name: Optional[str],
            description: Optional[str]):

        is_description_provided = description is not None
        is_name_provided = name is not None
        has_no_update_space_properties = not (
                is_description_provided or is_name_provided)

        if has_no_update_space_properties:
            raise NothingToUpdateSpace(space_id=space_id)

        if is_name_provided:
            self.check_space_name_not_empty(name=name)

    def _check_user_has_edit_access_to_space(
            self, space_id: str, user_id: str) -> None:
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id
        )

        self.check_user_has_edit_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
        )
