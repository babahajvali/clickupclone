from task_management.exceptions.custom_exceptions import \
    FieldNotFound, DeletedFieldException
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    def check_field_is_active(self, field_id: str):
        field_data = self.get_field_if_exists(
            field_id=field_id)

        is_field_deleted = field_data.is_deleted
        if is_field_deleted:
            raise DeletedFieldException(field_id=field_id)

    # use this method in the check_field_is_active OCP

    def get_field_if_exists(self, field_id: str):
        field_data = self.field_storage.get_field(field_id=field_id)
        is_field_not_exists = not field_data

        if is_field_not_exists:
            raise FieldNotFound(field_id=field_id)

        return field_data
