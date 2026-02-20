from task_management.constants.field_constants import FIELD_TYPE_KEYS
from task_management.exceptions.custom_exceptions import \
    DropdownOptionsMissing, InvalidFieldDefaultValue, \
    InvalidFieldValue, InvalidFieldConfig
from task_management.exceptions.enums import FieldConfig, FieldType


class DropdownField:

    @staticmethod
    def check_dropdown_config_data(config: dict):

        allowed_keys = FIELD_TYPE_KEYS[FieldType.DROPDOWN.value][
            FieldConfig.CONFIG_KEYS.value]
        invalid_keys = set(config.keys()) - allowed_keys
        if invalid_keys:
            raise InvalidFieldConfig(
                field_type=FieldType.DROPDOWN.value,
                invalid_keys=list(invalid_keys))


        options = config.get(FieldConfig.OPTIONS.value)

        is_options_empty = not options
        if is_options_empty:
            raise DropdownOptionsMissing(
                field_type=FieldType.DROPDOWN.value)

        default_value = config.get(FieldConfig.DEFAULT.value)
        is_default_value_provided = default_value is not None
        if not is_default_value_provided:
            return

        is_invalid_default = default_value not in options
        if is_invalid_default:
            raise InvalidFieldDefaultValue(
                field_type=FieldType.DROPDOWN.value,
                message="Default value must be one of dropdown options")

    @staticmethod
    def validate_dropdown_field(value: str, config: dict):

        options = config.get(FieldConfig.OPTIONS.value, [])

        if value not in options:
            raise InvalidFieldValue(
                message=f"Invalid option. Option must be one of: {', '.join(options)}")
