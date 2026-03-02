from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, WorkspaceStorageInterface, SpaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin, FolderValidationMixin


class CreateFolderInteractor:

    def __init__(self, folder_storage: FolderStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage
        self.space_storage = space_storage

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

    @invalidate_interactor_cache(cache_name="folders")
    def create_folder(self, folder_data: CreateFolderDTO) -> FolderDTO:
        self.folder_mixin.check_folder_name_not_empty(
            name=folder_data.name)
        self.space_mixin.check_space_not_deleted(
            space_id=folder_data.space_id)
        self._check_user_has_edit_access_for_space(
            space_id=folder_data.space_id,
            user_id=folder_data.created_by)

        order = self.folder_storage.get_last_folder_order_in_space(
            space_id=folder_data.space_id)

        return self.folder_storage.create_folder(
            create_folder_data=folder_data, order=order + 1)

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)

        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )
