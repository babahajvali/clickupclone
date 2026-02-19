from django.core.exceptions import ObjectDoesNotExist

from task_management.constants.field_constants import FIELD_TYPE_RULES
from task_management.exceptions.custom_exceptions import \
    UnsupportedFieldTypeException, FieldNameAlreadyExistsException, \
    InvalidFieldDefaultValueException, InvalidFieldConfigException, \
    FieldNotFoundException, InactiveFieldException, InvalidOrderException, \
    MissingFieldConfigException, EmptyNameException
from task_management.exceptions.enums import FieldTypes, FieldConfigs
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface, **kwargs):
        self.field_storage = field_storage
        super().__init__(**kwargs)

    @staticmethod
    def check_field_type(field_type: str):
        field_types = FieldTypes.get_values()
        is_field_type_invalid = field_type not in field_types

        if is_field_type_invalid:
            raise UnsupportedFieldTypeException(field_type=field_type)

    def check_field_name_not_exist_in_template(self, field_name: str,
                                               template_id: str):

        try:
            field_data = self.field_storage.get_field_by_name(
                field_name=field_name, template_id=template_id)
        except ObjectDoesNotExist:
            pass
        else:
            is_field_exists = field_data is not None
            if is_field_exists:
                raise FieldNameAlreadyExistsException(field_name=field_name)

    def check_field_is_active(self, field_id: str):
        field_data = self.field_storage.get_field_by_id(field_id=field_id)

        is_field_not_found = not field_data
        if is_field_not_found:
            raise FieldNotFoundException(field_id=field_id)

        is_field_inactive = not field_data.is_active
        if is_field_inactive:
            raise InactiveFieldException(field_id=field_id)

    def check_field_name_in_db_except_current_field(
            self, field_id: str, field_name: str, template_id: str):

        try:
            field_data = self.field_storage.get_field_by_name(
                field_name=field_name, template_id=template_id)
        except ObjectDoesNotExist:
            pass
        else:
            is_different_field = str(field_data.field_id) != field_id
            if is_different_field:
                raise FieldNameAlreadyExistsException(field_name=field_name)

    def check_field_order(self, template_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)

        fields_count = self.field_storage.template_fields_count(
            template_id=template_id)

        if order > fields_count:
            raise InvalidOrderException(order=order)

    @staticmethod
    def _check_dropdown_config(field_type: FieldTypes, config: dict):
        is_dropdown_field_type = (field_type == FieldTypes.DROPDOWN.value)

        if is_dropdown_field_type and not config:
            raise MissingFieldConfigException(field_type=field_type.value)

    @staticmethod
    def check_field_name_not_empty(field_name: str):
        is_name_empty = not field_name or not field_name.strip()

        if is_name_empty:
            raise EmptyNameException(name=field_name)

    def check_config(self, config: dict, field_type: FieldTypes):

        is_dropdown_field_type = (field_type == FieldTypes.DROPDOWN)
        if is_dropdown_field_type:
            self._check_dropdown_config(field_type=field_type, config=config)

        if config:
            self.check_field_config(field_type=field_type, config=config)

    def check_field_config(self, field_type: FieldTypes, config: dict):

        rules = FIELD_TYPE_RULES[field_type.value]
        allowed_keys = rules[FieldConfigs.CONFIG_KEYS]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise InvalidFieldConfigException(
                field_type=field_type.value,
                invalid_keys=list(invalid_keys)
            )

        is_dropdown_field_type = (field_type == FieldTypes.DROPDOWN)
        if is_dropdown_field_type:
            self.check_dropdown_config_data(field_type=field_type,
                                            config=config)

        is_text_field_type = (field_type == FieldTypes.TEXT)
        if is_text_field_type:
            self.check_text_config(config=config, field_type=field_type)

        is_number_field_type = (field_type == FieldTypes.NUMBER)
        if is_number_field_type:
            self.check_number_config(config=config, field_type=field_type)

    @staticmethod
    def check_dropdown_config_data(config: dict, field_type: FieldTypes):
        options = config.get(FieldConfigs.OPTIONS)
        is_options_empty = not options
        if is_options_empty:
            raise InvalidFieldConfigException(
                field_type=field_type.value,
                message="Dropdown must have non-empty options")

        default_value = config.get(FieldConfigs.DEFAULT)
        is_default_value_provided = default_value is not None
        if is_default_value_provided:
            is_invalid_default = default_value not in options
            if is_invalid_default:
                raise InvalidFieldDefaultValueException(
                    field_type=field_type.value,
                    message="Default value must be one of dropdown options")

    @staticmethod
    def check_number_config(config: dict, field_type: FieldTypes):
        default_value = config.get(FieldConfigs.DEFAULT)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        min_val = config.get(FieldConfigs.MIN)
        max_val = config.get(FieldConfigs.MAX)

        is_below_minimum = min_val is not None and default_value < min_val
        if is_below_minimum:
            raise InvalidFieldDefaultValueException(
                field_type=field_type.value,
                message=f"Default value {default_value} is less than minimum {min_val}")

        is_above_maximum = max_val is not None and default_value > max_val
        if is_above_maximum:
            raise InvalidFieldDefaultValueException(
                field_type=field_type.value,
                message=f"Default value {default_value} is greater than maximum {max_val}")

    @staticmethod
    def check_text_config(config: dict, field_type: FieldTypes):
        default_value = config.get(FieldConfigs.DEFAULT)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        max_length = config.get(FieldConfigs.MAX_LENGTH)
        is_exceeds_max_length = max_length is not None and len(
            default_value) > max_length
        if is_exceeds_max_length:
            raise InvalidFieldDefaultValueException(
                field_type=field_type.value,
                message=f"Default value length {len(default_value)} exceeds max_length {max_length}")
