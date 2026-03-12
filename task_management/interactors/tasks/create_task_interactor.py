from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, ListStorageInterface, WorkspaceStorageInterface
from task_management.mixins import ListValidationMixin, \
    WorkspaceValidationMixin, TaskValidationMixin
from task_management.utils.redis_utils import redis_lock


class CreateTaskInteractor(
        ListValidationMixin,
        WorkspaceValidationMixin,
        TaskValidationMixin):

    def __init__(
            self, task_storage: TaskStorageInterface,
            list_storage: ListStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            task_storage=task_storage,
            list_storage=list_storage,
            workspace_storage=workspace_storage,
        )
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="tasks")
    def create_task(self, create_task_dto: CreateTaskDTO) -> TaskDTO:
        self.check_task_title_not_empty(title=create_task_dto.title)
        self.check_list_not_deleted(list_id=create_task_dto.list_id)
        self._check_user_has_edit_access_for_list(
            list_id=create_task_dto.list_id,
            user_id=create_task_dto.created_by,
        )

        lock_key = f"lock:create_task:list:{create_task_dto.list_id}"
        with redis_lock(lock_key, timeout=10):
            last_task_order_in_list = self.task_storage.get_last_task_order_in_list(
                list_id=create_task_dto.list_id,
            )

            task_dto = self.task_storage.create_task(
                task_data=create_task_dto,
                order=last_task_order_in_list + 1,
            )
        return task_dto

    def _check_user_has_edit_access_for_list(self, list_id: str, user_id: str):
        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.check_user_has_edit_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
