from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import ListDTO, CreateListDTO
from task_management.interactors.storage_interfaces import \
    ListStorageInterface, FolderStorageInterface, WorkspaceStorageInterface, \
    SpaceStorageInterface
from task_management.mixins import SpaceValidationMixin, \
    WorkspaceValidationMixin, FolderValidationMixin, ListValidationMixin
from task_management.utils.redis_utils import redis_lock


class CreateListInteractor(
    SpaceValidationMixin,
    WorkspaceValidationMixin,
    FolderValidationMixin,
    ListValidationMixin):
    def __init__(
            self,
            list_storage: ListStorageInterface,
            folder_storage: FolderStorageInterface,
            workspace_storage: WorkspaceStorageInterface,
            space_storage: SpaceStorageInterface
    ):
        super().__init__(
            list_storage=list_storage,
            folder_storage=folder_storage,
            workspace_storage=workspace_storage,
            space_storage=space_storage,
        )
        self.list_storage = list_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="space_lists")
    @invalidate_interactor_cache(cache_name="folder_lists")
    def create_list(self, create_list_dto: CreateListDTO) -> ListDTO:
        self.check_list_name_not_empty(list_name=create_list_dto.name)

        self._validate_entity_and_check_access(
            entity_type=create_list_dto.entity_type,
            entity_id=create_list_dto.entity_id,
            created_by=create_list_dto.created_by
        )

        lock_key = (
            f"lock:create_list:{create_list_dto.entity_type.value}:"
            f"{create_list_dto.entity_id}"
        )
        with redis_lock(lock_key, timeout=10):
            last_list_order_in_entity = self.list_storage.get_last_list_order(
                entity_type=create_list_dto.entity_type.value,
                entity_id=create_list_dto.entity_id,
            )

            list_dto = self.list_storage.create_list(
                list_data=create_list_dto, order=last_list_order_in_entity + 1)
        return list_dto

    def _validate_entity_and_check_access(
            self, entity_type: ListEntityType, entity_id: str,
            created_by: str):
        if entity_type == ListEntityType.FOLDER:
            self.check_folder_not_deleted(folder_id=entity_id)
            space_id = self.folder_storage.get_folder_space_id(
                folder_id=entity_id)
        else:
            self.check_space_not_deleted(space_id=entity_id)
            space_id = entity_id

        self._check_user_has_edit_access_for_space(
            space_id=space_id, user_id=created_by)

    def _check_user_has_edit_access_for_space(
            self, space_id: str, user_id: str):
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
