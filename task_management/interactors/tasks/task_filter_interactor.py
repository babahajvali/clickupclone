from task_management.exceptions.custom_exceptions import InvalidOffset, \
    InvalidLimit
from task_management.interactors.dtos import FilterDTO
from task_management.interactors.storage_interfaces import \
    TaskStorageInterface, ListStorageInterface, WorkspaceStorageInterface
from task_management.mixins import ListValidationMixin


class TaskFilterInteractor:
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.workspace_storage = workspace_storage

    @property
    def list_mixin(self) -> ListValidationMixin:
        return ListValidationMixin(list_storage=self.list_storage)

    def task_filter(self, task_filter_data: FilterDTO):
        self._check_filter_parameters(
            filter_data=task_filter_data)
        self.list_mixin.check_list_not_deleted(
            list_id=task_filter_data.list_id)

        return self.task_storage.task_filter_data(filter_data=task_filter_data)

    @staticmethod
    def _check_filter_parameters(filter_data: FilterDTO):

        if filter_data.offset < 1:
            raise InvalidOffset(
                offset=filter_data.offset,
            )

        if filter_data.limit < 1:
            raise InvalidLimit(
                limit=filter_data.limit)
