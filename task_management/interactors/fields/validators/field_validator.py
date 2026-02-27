from typing import Optional

from task_management.exceptions.custom_exceptions import \
    FieldNameAlreadyExists, EmptyFieldName, UnsupportedFieldType
from task_management.exceptions.enums import FieldType
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidator:

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    def check_field_name_not_exist_in_template(
            self, field_name: str, template_id: str, field_id: Optional[str]):

        is_exists = self.field_storage.is_field_name_exists(
            field_name=field_name, template_id=template_id,
            exclude_field_id=field_id)

        if is_exists:
            raise FieldNameAlreadyExists(field_name=field_name)

    @staticmethod
    def check_field_name_not_empty(field_name: str):

        is_name_empty = not field_name or not field_name.strip()

        if is_name_empty:
            raise EmptyFieldName(field_name=field_name)

    @staticmethod
    def check_field_type(field_type: str):
        existed_field_types = FieldType.get_values()
        is_invalid_field_type = field_type not in existed_field_types

        if is_invalid_field_type:
            raise UnsupportedFieldType(field_type=field_type)
