from task_management.exceptions.custom_exceptions import \
    InvalidOffsetException, \
    InvalidLimitException, InvalidOrderException
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    UpdateTaskDTO, FilterDTO, CreateFieldValueDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.task_field_values_storage_interface import \
    FieldValueStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache


class TaskInteractor(ValidationMixin):
    def __init__(self, task_storage: TaskStorageInterface,
                 list_storage: ListStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 field_storage: FieldStorageInterface,
                 field_value_storage: FieldValueStorageInterface,
                 space_storage: SpaceStorageInterface, ):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.workspace_member_storage = workspace_member_storage
        self.field_storage = field_storage
        self.field_value_storage = field_value_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="tasks")
    def create_task(self, task_data: CreateTaskDTO) -> TaskDTO:
        self.validate_list_is_active(list_id=task_data.list_id,
                                     list_storage=self.list_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=task_data.list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=task_data.created_by,
            workspace_member_storage=self.workspace_member_storage)

        result = self.task_storage.create_task(task_data=task_data)
        self._set_default_field_values_at_task(
            task_id=result.task_id, list_id=task_data.list_id,
            created_by=task_data.created_by)

        return result

    @invalidate_interactor_cache(cache_name="tasks")
    def update_task(self, update_task_data: UpdateTaskDTO,
                    user_id: str) -> TaskDTO:
        list_id = self.get_active_task_list_id(
            task_id=update_task_data.task_id,
            task_storage=self.task_storage)
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.task_storage.update_task(update_task_data=update_task_data)

    @invalidate_interactor_cache(cache_name="tasks")
    def delete_task(self, task_id: str, user_id: str) -> TaskDTO:
        list_id = self.get_active_task_list_id(task_id=task_id,
                                               task_storage=self.task_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.task_storage.remove_task(task_id=task_id)

    @interactor_cache(cache_name="tasks", timeout=5 * 60)
    def get_list_tasks(self, list_id: str) -> list[TaskDTO]:
        self.validate_list_is_active(list_id=list_id,
                                     list_storage=self.list_storage)

        return self.task_storage.get_list_tasks(list_id=list_id)

    def get_task(self, task_id: str) -> TaskDTO:
        self.get_active_task_list_id(task_id=task_id,
                                     task_storage=self.task_storage)

        return self.task_storage.get_task_by_id(task_id=task_id)

    def task_filter(self, task_filter_data: FilterDTO, user_id: str):
        self.validate_list_is_active(list_id=task_filter_data.list_id,
                                     list_storage=self.list_storage)
        self._validate_filter_parameters(filter_data=task_filter_data)

        return self.task_storage.task_filter_data(filter_data=task_filter_data)

    @invalidate_interactor_cache(cache_name="tasks")
    def reorder_task(self, task_id: str, order: int, user_id: str) -> TaskDTO:
        list_id = self.get_active_task_list_id(task_id=task_id,
                                               task_storage=self.task_storage)
        space_id = self.list_storage.get_list_space_id(
            list_id=list_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            workspace_id=workspace_id, user_id=user_id,
            workspace_member_storage=self.workspace_member_storage)
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

    def _set_default_field_values_at_task(self, task_id: str, list_id: str,
                                          created_by: str):
        template_id = self.list_storage.get_template_id_by_list_id(
            list_id=list_id)
        template_fields = self.field_storage.get_fields_for_template(
            template_id=template_id)

        field_values = []
        for field in template_fields:
            default_value = field.config.get('default')

            field_values.append(
                CreateFieldValueDTO(
                    task_id=task_id,
                    field_id=field.field_id,
                    value=default_value,
                    created_by=created_by
                )
            )

        return self.field_value_storage.create_bulk_field_values(
            create_bulk_field_values=field_values)
