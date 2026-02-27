from typing import Optional

from task_management.decorators.caching_decorators import (
    invalidate_interactor_cache,
)
from task_management.exceptions.custom_exceptions import NothingToUpdateList
from task_management.interactors.dtos import ListDTO
from task_management.interactors.lists.validator.list_validator import (
    ListValidator,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
    WorkspaceStorageInterface,
    SpaceStorageInterface,
)
from task_management.mixins import (
    ListValidationMixin,
    SpaceValidationMixin,
    WorkspaceValidationMixin,
    FolderValidationMixin,
)


class UpdateListInteractor:

    def __init__(
            self,
            list_storage: ListStorageInterface,
            folder_storage: FolderStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            space_storage: SpaceStorageInterface,
    ):
        self.list_storage = list_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @property
    def space_mixin(self) -> SpaceValidationMixin:
        return SpaceValidationMixin(space_storage=self.space_storage)

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    @property
    def list_validator(self) -> ListValidator:
        return ListValidator(list_storage=self.list_storage)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def update_list(
            self,
            list_id: str,
            user_id: str,
            name: Optional[str],
            description: Optional[str],
    ) -> ListDTO:
        self._check_update_field_properties(
            list_id=list_id, name=name, description=description
        )
        self.list_mixin.check_list_is_not_deleted(list_id=list_id)
        self._check_user_has_edit_access_for_list(list_id=list_id,
                                                  user_id=user_id)

        return self.list_storage.update_list(
            list_id=list_id, name=name, description=description
        )

    def _check_update_field_properties(
            self, list_id: str, name: Optional[str], description: Optional[str]
    ):

        is_description_provided = description is not None
        is_name_provided = name is not None
        if is_name_provided:
            self.list_validator.check_list_name_not_empty(list_name=name)

        is_update_field_properties_provided = not (
                is_description_provided or is_name_provided
        )
        if is_update_field_properties_provided:
            raise NothingToUpdateList(list_id=list_id)

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):

        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id
        )
