from task_management.decorators.caching_decorators import (
    invalidate_interactor_cache,
)
from task_management.exceptions.custom_exceptions import (
    UnsupportedVisibilityType,
)
from task_management.exceptions.enums import Visibility
from task_management.interactors.dtos import ListDTO
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.mixins import (
    ListValidationMixin,
    WorkspaceValidationMixin,
)


class SetListVisibilityInteractor:

    def __init__(
            self,
            list_storage: ListStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
    ):
        self.list_storage = list_storage
        self.workspace_storage = workspace_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def set_list_visibility(
            self, list_id: str, visibility: Visibility, user_id: str
    ) -> ListDTO:
        self._check_visibility_type(visibility=visibility.value)

        self.list_mixin.check_list_not_deleted(list_id=list_id)
        self._check_user_has_edit_access_for_list(
            list_id=list_id, user_id=user_id)

        return self.list_storage.update_list_visibility(
            list_id=list_id, visibility=visibility.value
        )

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )

    @staticmethod
    def _check_visibility_type(visibility: str):
        existed_visibilities = Visibility.get_values()
        is_visibility_invalid = visibility not in existed_visibilities

        if is_visibility_invalid:
            raise UnsupportedVisibilityType(visibility_type=visibility)
