from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    UnsupportedVisibilityType
from task_management.exceptions.enums import VisibilityType
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class SetSpaceVisibilityInteractor(
    SpaceValidationMixin, WorkspaceValidationMixin):
    """
    Set Space Visibility Interactor updates the visibility of a space.

    Handle the set space visibility operation.
    This interactor checks the business rules and permission validation
     before updating visibility.

    Key Responsibility:
     - Update the space visibility

    Dependencies:
        - SpaceStorageInterface
        - WorkspaceStorageInterface
    """

    def __init__(
            self, space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(space_storage=space_storage,
                         workspace_storage=workspace_storage)
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="spaces")
    def set_space_visibility(
            self, space_id: str, user_id: str, visibility: VisibilityType) \
            -> SpaceDTO:
        """Set visibility for a space after validation and access checks."""
        self._check_visibility_type(visibility=visibility.value)
        self.check_space_not_deleted(space_id=space_id)
        self._check_user_has_edit_access_to_space(
            space_id=space_id,
            user_id=user_id,
        )

        return self.space_storage.update_space_visibility(
            space_id=space_id,
            visibility=visibility.value,
        )

    def _check_user_has_edit_access_to_space(
            self, space_id: str, user_id: str) -> None:
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id
        )

        self.check_user_has_edit_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
        )

    @staticmethod
    def _check_visibility_type(visibility: str) -> None:
        existed_visibilities = [each.value for each in VisibilityType]
        is_invalid_visibility_type = visibility not in existed_visibilities

        if is_invalid_visibility_type:
            raise UnsupportedVisibilityType(visibility_type=visibility)
