from task_management.decorators.caching_decorators import interactor_cache
from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, ListStorageInterface
from task_management.mixins import ListValidationMixin


class GetListTasksInteractor:

    def __init__(
            self, task_storage: TaskStorageInterface,
            list_storage: ListStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    @interactor_cache(cache_name="tasks", timeout=5 * 60)
    def get_tasks_for_list(self, list_id: str) -> list[TaskDTO]:
        self.list_mixin.check_list_not_deleted(list_id=list_id)

        return self.task_storage.get_tasks_for_list(list_id=list_id)
