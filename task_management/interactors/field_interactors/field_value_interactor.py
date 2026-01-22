from task_management.interactors.dtos import TaskFieldValueDTO, UpdateFieldValueDTO
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.task_field_values_storage_interface import \
    FieldValueStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class FieldValueInteractor(ValidationMixin):

    def __init__(self, field_value_storage: FieldValueStorageInterface,
                 field_storage: FieldStorageInterface,
                 task_storage: TaskStorageInterface,
                 permission_storage: ListPermissionStorageInterface):
        self.field_value_storage = field_value_storage
        self.field_storage = field_storage
        self.task_storage = task_storage
        self.permission_storage = permission_storage

    def set_task_field_value(self, set_value_data: UpdateFieldValueDTO,
                             user_id: str) -> TaskFieldValueDTO:
        self.validate_field(field_id=set_value_data.field_id,
                            field_storage=self.field_storage)
        list_id = self.get_active_task_list_id(task_id=set_value_data.task_id,
                                               task_storage=self.task_storage)
        self.validate_user_has_access_to_list(user_id=user_id, list_id=list_id,
                                              permission_storage=self.permission_storage)

        return self.field_value_storage.set_task_field_value(field_value_data=set_value_data,)
