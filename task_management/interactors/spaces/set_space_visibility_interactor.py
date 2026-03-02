from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.custom_exceptions import \
    UnsupportedVisibilityType
from task_management.exceptions.enums import Visibility
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.storage_interfaces import \
    SpaceStorageInterface, WorkspaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin


class SetSpaceVisibilityInteractor:

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
    def set_space_visibility(
            self, space_id: str, user_id: str, visibility: Visibility) \
            -> SpaceDTO:
        self._check_visibility_type(visibility=visibility.value)
        self.space_mixin.check_space_not_deleted(space_id=space_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id
        )
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )

        return self.space_storage.update_space_visibility(
            space_id=space_id, visibility=visibility.value
        )

    @staticmethod
    def _check_visibility_type(visibility: str):
        existed_visibilities = [each.value for each in Visibility]

        is_visibility_invalid = visibility not in existed_visibilities
        if is_visibility_invalid:
            raise UnsupportedVisibilityType(
                visibility_type=visibility)
