from task_management.exceptions.custom_exceptions import \
    FieldNotFound, DeletedFieldException
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    def check_field_is_active(self, field_id: str):
        field_data = self.field_storage.get_field_by_id(
            field_id=field_id)

        is_field_not_found = not field_data
        if is_field_not_found:
            raise FieldNotFound(field_id=field_id)

        is_field_deleted = field_data.is_deleted
        if is_field_deleted:
            raise DeletedFieldException(field_id=field_id)

    def check_field_is_exists(self, field_id: str):
        is_field_exists = self.field_storage.is_field_exists(field_id=field_id)
        is_field_not_exists = not is_field_exists

        if is_field_not_exists:
            raise FieldNotFound(field_id=field_id)
