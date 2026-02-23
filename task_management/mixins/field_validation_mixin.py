from task_management.exceptions.custom_exceptions import \
    FieldNotFound, InactiveField
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface, **kwargs):
        self.field_storage = field_storage
        super().__init__(**kwargs)

    def check_field_is_active(self, field_id: str):
        field_data = self.field_storage.get_field_by_id(
            field_id=field_id)

        is_field_not_found = not field_data
        if is_field_not_found:
            raise FieldNotFound(field_id=field_id)

        is_field_deleted = field_data.is_delete
        if is_field_deleted:
            raise InactiveField(field_id=field_id)
