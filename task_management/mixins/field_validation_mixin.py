from typing import Optional

from task_management.exceptions.custom_exceptions import \
    FieldNotFound, DeletedFieldException, FieldNameAlreadyExists, \
    EmptyFieldName
from task_management.interactors.dtos import FieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface, **kwargs):
        self.field_storage = field_storage
        super().__init__(**kwargs)

    def check_field_not_deleted(self, field_id: str):
        field_data = self.check_field_exists(
            field_id=field_id)

        is_field_deleted = field_data.is_deleted
        if is_field_deleted:
            raise DeletedFieldException(field_id=field_id)

    def check_field_exists(self, field_id: str) -> FieldDTO:
        field_result = self.field_storage.get_fields(field_ids=[field_id])

        if isinstance(field_result, list):
            field_data = field_result[0] if field_result else None
        else:
            field_data = field_result

        if not field_data:
            raise FieldNotFound(field_id=field_id)

        return field_data

    def check_field_name_not_exist_in_template(
            self, field_name: str, template_id: str, field_id: Optional[str]):

        is_name_exists = self.field_storage.is_field_name_exists(
            field_name=field_name, template_id=template_id,
            excluded_field_id=field_id)

        if is_name_exists:
            raise FieldNameAlreadyExists(field_name=field_name)

    @staticmethod
    def check_field_name_not_empty(field_name: str):

        is_name_empty = not field_name or not field_name.strip()

        if is_name_empty:
            raise EmptyFieldName(field_name=field_name)
