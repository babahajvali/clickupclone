from task_management.exceptions.custom_exceptions import \
    InvalidOffsetException, \
    InvalidLimitException, InvalidOrderException
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    UpdateTaskDTO, FilterDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, ListStorageInterface, SpaceStorageInterface, \
    WorkspaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.mixins import WorkspaceValidationMixin, \
    ListValidationMixin, TaskValidationMixin


class TaskInteractor(WorkspaceValidationMixin, ListValidationMixin, TaskValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 space_storage: SpaceStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        super().__init__(list_storage=list_storage, task_storage=task_storage,
                         workspace_storage=workspace_storage)
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="tasks")
    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        self.validate_list_is_active(list_id=task_data.list_id)
        space_id = self.list_storage.get_list_space_id(
            list_id=task_data.list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=task_data.created_by)

        result = self.task_storage.create_task(task_data=task_data)

        return result

    @invalidate_interactor_cache(cache_name="tasks")
    def update_task(self, update_task_data: UpdateTaskDTO,
                    user_id: str) -> TaskDTO:
        list_id = self.task_storage.get_task_list_id(
            task_id=update_task_data.task_id)
        self.validate_list_is_active(list_id=list_id)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

        return self.task_storage.update_task(update_task_data=update_task_data)

    @invalidate_interactor_cache(cache_name="tasks")
    def delete_task(self, task_id: str, user_id: str) -> TaskDTO:
        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)

        return self.task_storage.remove_task(task_id=task_id)

    @interactor_cache(cache_name="tasks", timeout=5 * 60)
    def get_list_tasks(self, list_id: str) -> list[TaskDTO]:
        self.validate_list_is_active(list_id=list_id)

        return self.task_storage.get_list_tasks(list_id=list_id)

    def get_task(self, task_id: str) -> TaskDTO:

        self.validate_task_is_active(task_id=task_id)

        return self.task_storage.get_task_by_id(task_id=task_id)

    def task_filter(self, task_filter_data: FilterDTO, user_id: str):

        self.validate_list_is_active(list_id=task_filter_data.list_id)
        self._validate_filter_parameters(filter_data=task_filter_data)

        return self.task_storage.task_filter_data(filter_data=task_filter_data)

    @invalidate_interactor_cache(cache_name="tasks")
    def reorder_task(self, task_id: str, order: int, user_id: str) -> TaskDTO:
        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
        self._validate_the_task_order(list_id=list_id, order=order)

        return self.task_storage.reorder_tasks(task_id=task_id,
                                               new_order=order,
                                               list_id=list_id)

    @staticmethod
    def _validate_filter_parameters(filter_data: FilterDTO):

        if filter_data.offset < 1:
            raise InvalidOffsetException(
                offset=filter_data.offset,
            )

        if filter_data.limit < 1:
            raise InvalidLimitException(
                limit=filter_data.limit)

    def _validate_the_task_order(self, list_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)
        tasks_count = self.task_storage.get_tasks_count(
            list_id=list_id)

        if order > tasks_count:
            raise InvalidOrderException(order=order)
