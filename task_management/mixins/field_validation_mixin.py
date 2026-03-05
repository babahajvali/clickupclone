from task_management.exceptions.custom_exceptions import \
    FieldNotFound, DeletedFieldException
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    def check_field_not_deleted(self, field_id: str):
        field_data = self.check_field_exists(
            field_id=field_id)

        is_field_deleted = field_data.is_deleted
        if is_field_deleted:
            raise DeletedFieldException(field_id=field_id)

    def check_field_exists(self, field_id: str) -> FieldDTO:
        field_data = self.field_storage.get_field(field_id=field_id)

        if not field_data:
            raise FieldNotFound(field_id=field_id)

        return field_data
