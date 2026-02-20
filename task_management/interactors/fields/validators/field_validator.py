from task_management.exceptions.custom_exceptions import \
    FieldNameAlreadyExists, InvalidOrder, EmptyName, \
    UnsupportedFieldType, FieldNotFound, InactiveField
from task_management.exceptions.enums import FieldType
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidator:

    def __init__(self, field_storage: FieldStorageInterface):
        self.field_storage = field_storage

    def check_field_is_active(self, field_id: str):
        """Validate that a fields exists and is active."""
        field_data = self.field_storage.get_field_by_id(
            field_id=field_id)

        is_field_not_found = not field_data
        if is_field_not_found:
            raise FieldNotFound(field_id=field_id)

        is_field_inactive = not field_data.is_active
        if is_field_inactive:
            raise InactiveField(field_id=field_id)

    def check_field_name_in_db_except_current_field(
            self, field_id: str, field_name: str, template_id: str):

        is_name_exists = self.field_storage.is_field_name_exists(
            field_name=field_name, template_id=template_id,
            exclude_field_id=field_id)

        if is_name_exists:
            raise FieldNameAlreadyExists(field_name=field_name)

    def check_field_order(self, template_id: str, order: int):

        if order < 1:
            raise InvalidOrder(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrder(order=order)

    def check_field_name_not_exist_in_template(
            self, field_name: str, template_id: str):

        is_exists = self.field_storage.is_field_name_exists(
            field_name=field_name, template_id=template_id,
            exclude_field_id=None)

        if is_exists:
            raise FieldNameAlreadyExists(field_name=field_name)

    @staticmethod
    def check_field_name_not_empty(field_name: str):

        is_name_empty = not field_name or not field_name.strip()

        if is_name_empty:
            raise EmptyName(name=field_name)

    @staticmethod
    def check_field_type(field_type: str):
        field_types = FieldType.get_values()
        is_field_type_invalid = field_type not in field_types

        if is_field_type_invalid:
            raise UnsupportedFieldType(field_type=field_type)
