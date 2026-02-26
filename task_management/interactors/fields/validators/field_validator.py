from typing import Optional

from task_management.exceptions.custom_exceptions import \
    FieldNameAlreadyExists, InvalidOrder, EmptyFieldName, \
    UnsupportedFieldType, FieldNotFound, DeletedFieldException
from task_management.exceptions.enums import FieldType
from task_management.interactors.dtos import UpdateFieldDTO
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidator:

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    def check_field_order(self, template_id: str, order: int):

        if order < 1:
            raise InvalidOrder(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrder(order=order)

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

    def reorder_field_positions(
            self, template_id: str, new_order: int, old_order: int):

        if new_order > old_order:
            self.field_storage.shift_fields_down(
                template_id=template_id,
                old_order=old_order,
                new_order=new_order)
        else:
            self.field_storage.shift_fields_up(
                template_id=template_id,
                new_order=new_order,
                old_order=old_order)

    @staticmethod
    def is_field_properties_not_empty(
            update_field_data: UpdateFieldDTO) -> bool:

        return any([
            update_field_data.field_name is not None,
            update_field_data.config is not None,
            update_field_data.description is not None,
            update_field_data.is_required is not None])
