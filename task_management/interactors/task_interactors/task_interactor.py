from task_management.exceptions.custom_exceptions import \
    TasKOrderAlreadyExistedException, InvalidOffsetNumberException, \
    InvalidLimitException
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    UpdateTaskDTO, FilterDTO
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class TaskInteractor(ValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 permission_storage: ListPermissionStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.permission_storage = permission_storage

    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        self.check_list_exists_and_status(list_id=task_data.list_id,
                                          list_storage=self.list_storage)
        self.check_user_has_access_to_list_modification(
            user_id=task_data.created_by, list_id=task_data.list_id,
            permission_storage=self.permission_storage)
        self._validate_task_order(order=task_data.order,
                                  list_id=task_data.list_id)

        return self.task_storage.create_task(task_data=task_data)

    def update_task(self, update_task_data: UpdateTaskDTO) -> TaskDTO:
        self.validate_task_exists(task_id=update_task_data.task_id,
                                  task_storage=self.task_storage)
        self.check_list_exists_and_status(list_id=update_task_data.list_id,
                                          list_storage=self.list_storage)
        self.check_user_has_access_to_list_modification(
            user_id=update_task_data.created_by,
            list_id=update_task_data.list_id,
            permission_storage=self.permission_storage)
        self._validate_task_order(order=update_task_data.order,
                                  list_id=update_task_data.list_id)

        return self.task_storage.update_task(update_task_data=update_task_data)

    def delete_task(self, task_id: str, user_id: str) -> TaskDTO:
        list_id = self.validate_task_exists(task_id=task_id,
                                            task_storage=self.task_storage)
        self.check_user_has_access_to_list_modification(user_id=user_id,
                                                        list_id=list_id,
                                                        permission_storage=self.permission_storage)

        return self.task_storage.remove_task(task_id=task_id)

    def get_list_tasks(self, list_id: str) -> list[TaskDTO]:
        self.check_list_exists_and_status(list_id=list_id,
                                          list_storage=self.list_storage)

        return self.task_storage.get_list_tasks(list_id=list_id)

    def get_task(self, task_id: str) -> TaskDTO:
        self.validate_task_exists(task_id=task_id,
                                  task_storage=self.task_storage)

        return self.task_storage.get_task_by_id(task_id=task_id)

    def task_filter(self, task_filter_data: FilterDTO, user_id: str):
        self.check_user_has_access_to_list_modification(user_id=user_id,
                                                        list_id=task_filter_data.list_id,
                                                        permission_storage=self.permission_storage)
        self.check_list_exists_and_status(list_id=task_filter_data.list_id,
                                          list_storage=self.list_storage)
        self._validate_filter_parameters(filter_data=task_filter_data)

        return self.task_storage.task_filter_data(filter_data=task_filter_data)

    def _validate_task_order(self, order: int, list_id: str):
        is_order_exist = self.task_storage.check_task_order_exist(order=order,
                                                                  list_id=list_id)

        if is_order_exist:
            raise TasKOrderAlreadyExistedException(list_id=list_id)

    @staticmethod
    def _validate_filter_parameters(filter_data: FilterDTO):

        if filter_data.offset < 1:
            raise InvalidOffsetNumberException(
                offset=filter_data.offset,
            )

        if filter_data.limit < 1:
            raise InvalidLimitException(
                limit=filter_data.limit,
            )
