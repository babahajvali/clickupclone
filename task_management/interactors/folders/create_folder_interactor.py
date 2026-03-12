from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, WorkspaceStorageInterface, SpaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin, FolderValidationMixin
from task_management.utils.redis_utils import redis_lock


class CreateFolderInteractor(
    FolderValidationMixin,
    SpaceValidationMixin,
    WorkspaceValidationMixin,
):

    def __init__(
            self, folder_storage: FolderStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            space_storage: SpaceStorageInterface):
        super().__init__(
            folder_storage=folder_storage,
            workspace_storage=workspace_storage,
            space_storage=space_storage,
        )
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="folders")
    def create_folder(self, create_folder_dto: CreateFolderDTO) -> FolderDTO:
        self.check_folder_name_not_empty(
            name=create_folder_dto.name)
        self.check_space_not_deleted(
            space_id=create_folder_dto.space_id)
        self._check_user_has_edit_access_for_space(
            space_id=create_folder_dto.space_id,
            user_id=create_folder_dto.created_by)

        with self._get_create_folder_lock(space_id=create_folder_dto.space_id):
            last_folder_order_in_space = (
                self.folder_storage.get_last_folder_order_in_space(
                    space_id=create_folder_dto.space_id
                )
            )

            folder_dto = self.folder_storage.create_folder(
                create_folder_dto=create_folder_dto,
                order=last_folder_order_in_space + 1,
            )
        return folder_dto

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)

        self.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )

    @staticmethod
    def _get_create_folder_lock(space_id: str):
        lock_key = f"lock:create_folder:space:{space_id}"
        return redis_lock(lock_key, timeout=10)
