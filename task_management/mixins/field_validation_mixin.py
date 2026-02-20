from django.core.exceptions import ObjectDoesNotExist

from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import \
    FieldNameAlreadyExistsException, \
    InvalidFieldDefaultValueException, InvalidFieldConfigException, \
    FieldNotFoundException, InactiveFieldException, InvalidOrderException, \
    MissingFieldConfigException, EmptyNameException, \
    DropdownOptionsMissingException
from task_management.exceptions.enums import FieldType, FieldConfig
from task_management.interactors.storage_interfaces import \
    FieldStorageInterface


class FieldValidationMixin:

    def __init__(self, field_storage: FieldStorageInterface, **kwargs):
        self.field_storage = field_storage
        super().__init__(**kwargs)

    def check_field_is_active(self, field_id: str):
        field_data = self.field_storage.get_active_field_by_id(
            field_id=field_id)

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
    def check_mandatory_config_is_not_empty(config: dict, field_type: str):

        is_empty_config = not config or config == {}
        if is_empty_config:
            raise MissingFieldConfigException(
                field_type=field_type)

    @staticmethod
    def check_field_name_not_empty(field_name: str):
        is_name_empty = not field_name or not field_name.strip()

        if is_name_empty:
            raise EmptyNameException(name=field_name)

    def check_config(self, config: dict, field_type: FieldType):

        mandatory_config_field_types = FieldType.mandatory_config_field_type()

        is_mandatory_config_field_type = (
                field_type.value in mandatory_config_field_types)
        if is_mandatory_config_field_type:
            self.check_mandatory_config_is_not_empty(
                config=config, field_type=field_type.value)

        if config:
            self.check_field_config(field_type=field_type, config=config)

    def check_field_config(self, field_type: FieldType, config: dict):
        self._check_allowed_config_keys(field_type=field_type.value,
                                        config=config)

        validation_handlers = {
            FieldType.DROPDOWN: self.check_dropdown_config_data,
            FieldType.TEXT: self.check_text_config,
            FieldType.NUMBER: self.check_number_config,
        }

        handler = validation_handlers.get(field_type)
        if handler:
            handler(config=config)

    @staticmethod
    def _check_allowed_config_keys(field_type: str, config: dict):
        allowed_keys = FIELD_TYPE_KEYS[field_type][
            FieldConfig.CONFIG_KEYS.value]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise InvalidFieldConfigException(
                field_type=field_type,
                invalid_keys=list(invalid_keys))

    @staticmethod
    def check_dropdown_config_data(config: dict):
        options = config.get(FieldConfig.OPTIONS.value)

        is_options_empty = not options
        if is_options_empty:
            raise DropdownOptionsMissingException(
                field_type=FieldType.DROPDOWN.value)

        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        is_invalid_default = default_value not in options
        if is_invalid_default:
            raise InvalidFieldDefaultValueException(
                field_type=FieldType.DROPDOWN.value,
                message="Default value must be one of dropdown options")

    @staticmethod
    def check_number_config(config: dict):
        min_val = config.get(FieldConfig.MIN.value)
        max_val = config.get(FieldConfig.MAX.value)

        is_min_max_both_provided = min_val is not None and max_val is not None
        if not is_min_max_both_provided:
            return

        is_max_less_than_min = max_val < min_val
        if is_max_less_than_min:
            raise InvalidFieldConfigException(
                field_type=FieldType.NUMBER.value,
                message=f"max {max_val} must be greater than or equal to min {min_val}")

        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        is_below_minimum = min_val is not None and default_value < min_val
        if is_below_minimum:
            raise InvalidFieldDefaultValueException(
                field_type=FieldType.NUMBER.value,
                message=f"Default value {default_value} is less than minimum {min_val}")

        is_above_maximum = max_val is not None and default_value > max_val
        if is_above_maximum:
            raise InvalidFieldDefaultValueException(
                field_type=FieldType.NUMBER.value,
                message=f"Default value {default_value} is greater than maximum {max_val}")

    @staticmethod
    def check_text_config(config: dict):
        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        max_length = config.get(FieldConfig.MAX_LENGTH.value)
        is_exceeds_max_length = max_length is not None and len(
            default_value) > max_length
        if is_exceeds_max_length:
            raise InvalidFieldDefaultValueException(
                field_type=FieldType.TEXT.value,
                message=f"Default value length {len(default_value)} exceeds max_length {max_length}")
