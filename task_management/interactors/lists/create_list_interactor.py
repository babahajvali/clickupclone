from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import ListDTO, CreateListDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, WorkspaceStorageInterface, \
    SpaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin, FolderValidationMixin, ListValidationMixin


class CreateListInteractor:
    def __init__(
            self,
            list_storage: ListStorageInterface,
            folder_storage: FolderStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            space_storage: SpaceStorageInterface
    ):
        self.list_storage = list_storage
        self.folder_storage = folder_storage
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
    def folder_mixin(self) -> FolderValidationMixin:
        return FolderValidationMixin(folder_storage=self.folder_storage)

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def create_list(self, list_data: CreateListDTO) -> ListDTO:
        self.list_mixin.check_list_name_not_empty(list_name=list_data.name)

        self._validate_entity_and_check_access(
            entity_type=list_data.entity_type,
            entity_id=list_data.entity_id,
            created_by=list_data.created_by
        )

        order = self.list_storage.get_last_list_order(
            entity_type=list_data.entity_type.value,
            entity_id=list_data.entity_id,
        )

        return self.list_storage.create_list(
            list_data=list_data, order=order + 1)

    def _validate_entity_and_check_access(
            self, entity_type: ListEntityType, entity_id: str,
            created_by: str):
        if entity_type == ListEntityType.FOLDER:
            self.folder_mixin.check_folder_not_deleted(folder_id=entity_id)
            space_id = self.folder_storage.get_folder_space_id(
                folder_id=entity_id)
        else:
            self.space_mixin.check_space_not_deleted(space_id=entity_id)
            space_id = entity_id

        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=created_by)

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
