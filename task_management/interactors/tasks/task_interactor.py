from typing import Optional

from task_management.exceptions.custom_exceptions import \
    InvalidOffset, InvalidLimit, InvalidOrder, \
    EmptyName, NothingToUpdateTask
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, FilterDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, ListStorageInterface, WorkspaceStorageInterface
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.mixins import WorkspaceValidationMixin, \
    ListValidationMixin, TaskValidationMixin


class TaskInteractor(WorkspaceValidationMixin, ListValidationMixin,
                     TaskValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        super().__init__(workspace_storage=workspace_storage,
                         list_storage=list_storage, task_storage=task_storage)
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @invalidate_interactor_cache(cache_name="tasks")
    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:

        self._check_task_title_not_empty(title=task_data.title)
        self.check_list_is_active(list_id=task_data.list_id)
        self._validate_user_has_access_for_list(list_id=task_data.list_id,
                                                user_id=task_data.created_by)

        result = self.task_storage.create_task(task_data=task_data)

        return result

    @invalidate_interactor_cache(cache_name="tasks")
    def update_task(self, task_id: str, user_id: str, title: Optional[str],
                    description: Optional[str]) -> TaskDTO:

        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        self.check_list_is_active(list_id=list_id)
        self._validate_user_has_access_for_list(list_id=list_id,
                                                user_id=user_id)

        is_title_provided = title is not None
        is_description_provided = description is not None
        field_properties_to_update = {}

        if is_title_provided:
            self._check_task_title_not_empty(title=title)
            field_properties_to_update['title'] = title

        if is_description_provided:
            field_properties_to_update['description'] = description

        if not field_properties_to_update:
            raise NothingToUpdateTask(task_id=task_id)

        return self.task_storage.update_task(
            task_id=task_id, field_properties=field_properties_to_update)

    @invalidate_interactor_cache(cache_name="tasks")
    def delete_task(self, task_id: str, user_id: str) -> TaskDTO:

        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        self._validate_user_has_access_for_list(list_id=list_id,
                                                user_id=user_id)

        return self.task_storage.remove_task(task_id=task_id)

    @interactor_cache(cache_name="tasks", timeout=5 * 60)
    def get_active_tasks_for_list(self, list_id: str) -> list[TaskDTO]:

        self.check_list_is_active(list_id=list_id)

        return self.task_storage.get_active_tasks_for_list(list_id=list_id)

    def get_task(self, task_id: str) -> TaskDTO:

        self.check_task_is_active(task_id=task_id)

        return self.task_storage.get_task_by_id(task_id=task_id)

    def task_filter(self, task_filter_data: FilterDTO):

        self.check_list_is_active(list_id=task_filter_data.list_id)
        self._validate_filter_parameters(filter_data=task_filter_data)

        return self.task_storage.task_filter_data(filter_data=task_filter_data)

    @invalidate_interactor_cache(cache_name="tasks")
    def reorder_task(self, task_id: str, order: int, user_id: str) -> TaskDTO:

        self.check_task_is_active(task_id=task_id)
        list_id = self.task_storage.get_task_list_id(task_id=task_id)
        self._validate_the_task_order(list_id=list_id, order=order)
        self._validate_user_has_access_for_list(list_id=list_id,
                                                user_id=user_id)

        return self.task_storage.reorder_tasks(
            task_id=task_id, new_order=order, list_id=list_id)

    @staticmethod
    def _validate_filter_parameters(filter_data: FilterDTO):

        if filter_data.offset < 1:
            raise InvalidOffset(
                offset=filter_data.offset,
            )

        if filter_data.limit < 1:
            raise InvalidLimit(
                limit=filter_data.limit)

    def _validate_the_task_order(self, list_id: str, order: int):
        if order < 1:
            raise InvalidOrder(order=order)
        tasks_count = self.task_storage.get_tasks_count(
            list_id=list_id)

        if order > tasks_count:
            raise InvalidOrder(order=order)

    @staticmethod
    def _check_task_title_not_empty(title: str):

        is_title_empty = not title or not title.strip()
        if is_title_empty:
            raise EmptyName(name=title)

    def _validate_user_has_access_for_list(self, list_id: str, user_id: str):

        workspace_id = self.list_storage.get_workspace_id_by_list_id(
            list_id=list_id)

        self.check_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id)
